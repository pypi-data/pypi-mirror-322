import dataclasses
import functools
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union
from urllib.parse import urlparse

import pyarrow

from tecton_core import duckdb_factory
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_types import TimestampType
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.dialect import Dialect
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.schema import Schema
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.offlinestore.delta.metadata__client_pb2 import TectonDeltaMetadata


R = TypeVar("R")
TxnFn = Callable[[], R]

# A single Parquet Row Group (1_000_000 rows by default) is usually 32-128mb
# Our target size for a single Parquet file is 512-1024mb.
# Hence, the limit for number of rows per file:
PARQUET_MAX_ROWS_PER_FILE = 8_000_000


@dataclasses.dataclass
class OfflineStoreParams:
    feature_view_id: str
    feature_view_name: str
    schema: schema_pb2.Schema
    time_spec: TimeSpec
    feature_store_format_version: int
    batch_schedule: Optional[int]

    @staticmethod
    def for_feature_definition(fd: FeatureDefinitionWrapper) -> "OfflineStoreParams":
        return OfflineStoreParams(
            feature_view_id=fd.id,
            feature_view_name=fd.name,
            schema=fd.materialization_schema.to_proto(),
            time_spec=TimeSpec.for_feature_definition(fd),
            feature_store_format_version=fd.get_feature_store_format_version,
            # feature tables do not have schedules
            batch_schedule=fd.get_batch_schedule_for_version if not fd.is_feature_table else None,
        )


class OfflineStoreWriter(ABC):
    def __init__(
        self,
        store_params: OfflineStoreParams,
        table_uri: str,
        join_keys: List[str],
    ):
        self._feature_params = store_params
        self._table_uri = table_uri
        self._join_keys = join_keys
        self._duckdb_conn = duckdb_factory.create_connection()
        self._retry_exceptions = []

    @abstractmethod
    def delete_time_range(self, interval: TimeInterval) -> None:
        """Filters and deletes previously materialized data within the interval.

        :param interval: The feature data time interval to delete
        """

    @abstractmethod
    def write(
        self, table: Union[pyarrow.Table, pyarrow.RecordBatchReader], tags: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """Writes a pyarrow Table to the base_uri.

        Returns a list of URIs for the written file(s).

        This does NOT commit. Call commit() after calling this to commit your changes.
        """

    @abstractmethod
    def delete_keys(self, keys: pyarrow.Table):
        """Deletes keys from offline store."""

    @abstractmethod
    def commit(self, metadata: Optional[TectonDeltaMetadata] = None) -> Optional[int]:
        """commits transaction to offline store."""

    @abstractmethod
    def transaction_exists(self, metadata: TectonDeltaMetadata) -> bool:
        """checks matching transaction metadata, which signals that a previous task attempt already wrote data
        If the task overwrites a previous materialization task interval then we treat it as a new transaction.

        :param metadata: transaction metadata
        :return: whether the same transaction has been executed before
        """

    def transaction(self, metadata: Optional[TectonDeltaMetadata] = None) -> Callable[[TxnFn], TxnFn]:
        """Returns a decorator which wraps a function in a transaction.

        If the function returns successfully, the Delta transaction will be committed automatically. Any exceptions will
        cause an aborted transaction.

        Any Delta conflicts which occur will result in the function being retried in a new transaction.

        :param metadata: Optional metadata to be added to the transaction.
        """

        def decorator(f: TxnFn, max_attempts=5) -> TxnFn:
            @functools.wraps(f)
            def wrapper() -> R:
                for attempt in range(1, max_attempts + 1):
                    r = f()
                    try:
                        self.commit(metadata)
                        return r
                    except self._retry_exceptions:
                        if attempt >= max_attempts:
                            raise
                        print(f"Offline store commit attempt {attempt} failed. Retrying...")
                    finally:
                        print("Offline store write transaction failed. Aborting...")
                        self.abort()

            return wrapper

        return decorator

    @abstractmethod
    def abort(self):
        """
        Abort the transaction by cleaning up any files and state.
        Clean up created parquet files that were not part of a successful commit.
        """

    def _time_limits(self, time_interval: TimeInterval) -> pyarrow.Table:
        """Returns a Table specifying the limits of data affected by a materialization job.

        :param time_interval: The feature time interval
        :returns: A relation with one column for the timestamp key or anchor time, and one with the partition value
            corresponding to the first column. The first row will be the values for feature start time and the second for
            feature end time.
        """
        timestamp_key = self._feature_params.time_spec.timestamp_key
        timestamp_table = pyarrow.table({timestamp_key: [time_interval.start, time_interval.end]})

        if self._feature_params.batch_schedule is None:
            msg = "Batch schedule is required for batch materialization"
            raise Exception(msg)

        tree = AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=AddAnchorTimeNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=ConvertTimestampToUTCNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=StagedTableScanNode(
                        dialect=Dialect.DUCKDB,
                        compute_mode=ComputeMode.RIFT,
                        staged_schema=Schema.from_dict({timestamp_key: TimestampType()}),
                        staging_table_name="timestamp_table",
                    ).as_ref(),
                    timestamp_key=timestamp_key,
                ).as_ref(),
                feature_store_format_version=self._feature_params.feature_store_format_version,
                batch_schedule=self._feature_params.batch_schedule,
                timestamp_field=timestamp_key,
            ).as_ref(),
            time_spec=self._feature_params.time_spec,
        ).as_ref()
        return self._duckdb_conn.sql(tree.to_sql()).arrow()


def path_from_uri(uri):
    parts = urlparse(uri)
    return parts.netloc + parts.path
