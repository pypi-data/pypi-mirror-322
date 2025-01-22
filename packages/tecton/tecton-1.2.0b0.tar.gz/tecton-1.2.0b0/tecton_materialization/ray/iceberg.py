import dataclasses
import uuid
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pyarrow
from duckdb.typing import INTEGER
from pyarrow._dataset import WrittenFile
from pyarrow.filesystem import FileSystem
from pyiceberg.exceptions import CommitFailedException
from pyiceberg.expressions import And
from pyiceberg.expressions import BooleanExpression
from pyiceberg.expressions import GreaterThanOrEqual
from pyiceberg.expressions import LessThan
from pyiceberg.manifest import DataFile
from pyiceberg.partitioning import PartitionField
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.table import TableProperties
from pyiceberg.table import _parquet_files_to_data_files
from pyiceberg.transforms import IdentityTransform
from pyiceberg.typedef import EMPTY_DICT

from tecton_core.arrow import PARQUET_WRITE_OPTIONS
from tecton_core.iceberg_catalog import MetadataCatalog
from tecton_core.iceberg_catalog import bucket_transform
from tecton_core.offline_store import patch_timestamps_in_arrow_schema
from tecton_core.query_consts import anchor_time
from tecton_core.schema import Schema
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.offline_store_writer import PARQUET_MAX_ROWS_PER_FILE
from tecton_materialization.ray.offline_store_writer import OfflineStoreParams
from tecton_materialization.ray.offline_store_writer import OfflineStoreWriter
from tecton_materialization.ray.offline_store_writer import path_from_uri
from tecton_proto.common import data_type__client_pb2 as data_type_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.offlinestore.delta.metadata__client_pb2 import TectonDeltaMetadata


PHYSICAL_PARTITION_NAME = "bucket"
# TODO: make this configurable but also immutable once the table is created.
# TODO: Support partition evolution
BUCKET_NUM = 1000
ENTITY_PARTITION_NAME = "entity_bucket"


@dataclasses.dataclass
class IcebergWriter(OfflineStoreWriter):
    def __init__(
        self,
        store_params: OfflineStoreParams,
        table_uri: str,
        join_keys: List[str],
        filesystem: Optional[FileSystem] = None,
    ):
        super().__init__(store_params, table_uri, join_keys)
        self._add_uris: List[str] = []
        self._deletes: List[DataFile] = []
        if filesystem:
            self._filesystem = filesystem
        else:
            self._filesystem, _ = pyarrow.fs.FileSystem.from_uri(self._table_uri)
        self._catalog = MetadataCatalog(name="object_store_catalog", properties={})
        bucket_transformer_name = f"bucket_transform_{uuid.uuid4().hex[:10]}"
        self._duckdb_conn.create_function(bucket_transformer_name, bucket_transform(BUCKET_NUM), return_type=INTEGER)
        self._bucket_expression = f"{bucket_transformer_name}({self.join_keys_expression(self._join_keys)})"
        self._retry_exceptions = [CommitFailedException]

    def delete_time_range(self, interval: TimeInterval) -> None:
        """Filters and deletes previously materialized data within the interval.

        :param interval: The feature data time interval to delete
        """
        print(f"Clearing prior data in range {interval.start} - {interval.end}")

        time_spec = self._feature_params.time_spec

        def table_filter(input_table: pyarrow.dataset.Dataset) -> pyarrow.Table:
            time_limit_table = self._time_limits(interval)
            # Add timezone to timestamps
            input_table = input_table.cast(patch_timestamps_in_arrow_schema(input_table.schema))
            # Not using pypika because it lacks support for ANTI JOIN
            return self._duckdb_conn.sql(
                f"""
                WITH flattened_limits AS(
                    SELECT MIN("{time_spec.time_column}") AS start, MAX("{time_spec.time_column}") AS end
                    FROM time_limit_table
                )
                SELECT * FROM input_table
                LEFT JOIN flattened_limits
                ON input_table."{time_spec.time_column}" >= flattened_limits.start
                AND input_table."{time_spec.time_column}" < flattened_limits.end
                WHERE flattened_limits.start IS NULL
            """
            ).arrow()

        if time_spec.time_column == anchor_time():
            start_time = convert_timestamp_for_version(
                interval.start, self._feature_params.feature_store_format_version
            )
            end_time = convert_timestamp_for_version(interval.end, self._feature_params.feature_store_format_version)
            predicate = And(
                GreaterThanOrEqual(time_spec.time_column, start_time), LessThan(time_spec.time_column, end_time)
            )
        else:
            start_time_str = interval.start.strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = interval.end.strftime("%Y-%m-%d %H:%M:%S")
            predicate = And(
                GreaterThanOrEqual(time_spec.time_column, start_time_str), LessThan(time_spec.time_column, end_time_str)
            )
        self._filter_files_for_deletion(predicate, table_filter)

    def _filter_files_for_deletion(
        self,
        predicate: BooleanExpression,
        filter_table: Callable[[pyarrow.dataset.Dataset], pyarrow.Table],
        force_overwrite: bool = False,
        **write_kwargs,
    ):
        tbl = self._catalog.load_table(self._table_uri)
        plan_files = tbl.scan(
            row_filter=predicate,
        ).plan_files()
        deletes = []
        for plan_file in plan_files:
            input_table = pyarrow.dataset.dataset(
                source=plan_file.file.file_path,
                filesystem=self._filesystem,
            ).to_table()
            output_table = filter_table(input_table)
            if input_table.num_rows != output_table.num_rows or force_overwrite:
                deletes.append(plan_file.file)
                if output_table.num_rows:
                    self.write(output_table, **write_kwargs)
        self._deletes.extend(deletes)

    def write(
        self, input_table: Union[pyarrow.Table, pyarrow.RecordBatchReader], tags: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """Writes a pyarrow Table to the base_uri.

        Returns a list of URIs for the written file(s).

        This does NOT commit. Call commit() after calling this to commit your changes.
        """
        query = f"""
            SELECT
                *,
                {self._bucket_expression} AS {ENTITY_PARTITION_NAME},
                {ENTITY_PARTITION_NAME} AS {PHYSICAL_PARTITION_NAME}
            FROM input_table
            ORDER BY {self._feature_params.time_spec.time_column};
        """
        bucketed_table = self._duckdb_conn.sql(query).arrow()

        adds = []
        failed = False

        def visit_file(f: WrittenFile):
            try:
                path = f.path
                adds.append(path)
            except Exception as e:
                # Pyarrow logs and swallows exceptions from this function, so we need some other way of knowing there
                # was a failure
                nonlocal failed
                failed = True
                raise e

        # TODO: consider using duckdb to write the parquet files directly
        pyarrow.dataset.write_dataset(
            data=bucketed_table,
            filesystem=self._filesystem,
            base_dir=self._table_uri,
            format=pyarrow.dataset.ParquetFileFormat(),
            file_options=PARQUET_WRITE_OPTIONS,
            basename_template=f"{uuid.uuid4()}-part-{{i}}.parquet",
            partitioning=pyarrow.dataset.partitioning(
                pyarrow.schema([(PHYSICAL_PARTITION_NAME, pyarrow.int32())]),
                flavor="hive",
            ),
            file_visitor=visit_file,
            existing_data_behavior="overwrite_or_ignore",
            max_partitions=365 * 100,
            max_rows_per_file=PARQUET_MAX_ROWS_PER_FILE,
            use_threads=True,
        )

        if failed:
            msg = "file visitor failed during write"
            raise Exception(msg)

        self._add_uris.extend(adds)
        return adds

    def delete_keys(self, keys: pyarrow.Table):
        """Deletes keys from offline store."""
        raise NotImplementedError

    def commit(self, metadata: Optional[TectonDeltaMetadata] = None) -> Optional[int]:
        """commits files to the offline store."""
        if not self._add_uris and not self._deletes:
            # nothing to commit
            return
        try:
            if len(self._add_uris) != len(set(self._add_uris)):
                msg = "`_add_uris` file paths must be unique"
                raise ValueError(msg)

            if len(self._deletes) != len(set(self._deletes)):
                msg = "`_deletes` file paths must be unique"
                raise ValueError(msg)

            if not self._catalog.table_exists(self._table_uri):
                feature_schema_proto = self._feature_params.schema
                partition_column = schema_pb2.Column(
                    name=ENTITY_PARTITION_NAME,
                    offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_INT32),
                )
                feature_schema_proto.columns.append(partition_column)

                tecton_schema = Schema(feature_schema_proto)
                pa_schema = tecton_schema_to_arrow_schema(tecton_schema)
                # TODO: have the bucket transformer also defined in the spec.
                #  requires us to rewrite pyiceberg `parquet_files_to_data_files` since it's a non-linear transformation.
                partition_spec = PartitionSpec(
                    PartitionField(
                        source_id=-1,
                        field_id=-1,
                        transform=IdentityTransform(),
                        name=ENTITY_PARTITION_NAME,
                    )
                )
                tbl = self._catalog.create_table(
                    self._table_uri, pa_schema, self._table_uri, partition_spec=partition_spec
                )
            else:
                tbl = self._catalog.load_table(self._table_uri)

            with tbl.transaction() as tx:
                snapshot_properties = (
                    {"featureStartTime": metadata.feature_start_time.seconds} if metadata else EMPTY_DICT
                )
                if tx.table_metadata.name_mapping() is None:
                    tx.set_properties(
                        **{
                            TableProperties.DEFAULT_NAME_MAPPING: tx.table_metadata.schema().name_mapping.model_dump_json()
                        }
                    )
                with tx.update_snapshot(snapshot_properties=snapshot_properties).overwrite() as update_snapshot:
                    add_data_files = _parquet_files_to_data_files(
                        table_metadata=tbl.metadata, file_paths=self._add_uris, io=tbl.io
                    )
                    for add_data_file in add_data_files:
                        update_snapshot.append_data_file(add_data_file)
                    for delete_data_file in self._deletes:
                        update_snapshot.delete_data_file(delete_data_file)
        except self._retry_exceptions:
            # Commit should be retried together with new write.
            self.abort()
            raise
        finally:
            self._reset_state()

    def transaction_exists(self, metadata: TectonDeltaMetadata) -> bool:
        """checks matching transaction metadata, which signals that a previous task attempt already wrote data
        If the task overwrites a previous materialization task interval then we treat it as a new transaction.

        :param metadata: transaction metadata
        :return: whether the same transaction has been executed before
        """
        if not self._catalog.table_exists(self._table_uri):
            return False

        tbl = self._catalog.load_table(self._table_uri)
        for snapshot in tbl.metadata.snapshots:
            if snapshot.summary["featureStartTime"] == metadata.feature_start_time.seconds:
                return True
        return False

    def abort(self):
        """
        Abort the transaction by cleaning up any files and state.
        Clean up created parquet files that were not part of a successful commit.
        """
        for add_file in self._add_uris:
            self._filesystem.delete_file(path_from_uri(add_file))
        self._reset_state()

    def _reset_state(self):
        self._add_uris = []
        self._deletes = []

    @staticmethod
    def join_keys_expression(join_keys: List[str]):
        # TODO: make the partition scheme more explicit so that the customer can define which key(s) to bucket.
        return join_keys[0]
