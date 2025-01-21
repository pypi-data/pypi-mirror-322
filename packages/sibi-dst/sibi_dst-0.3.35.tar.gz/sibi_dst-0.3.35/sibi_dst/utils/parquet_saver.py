from pathlib import Path
from typing import Optional

import pyarrow as pa
import fsspec

from sibi_dst.utils import Logger


class ParquetSaver:
    def __init__(self, df_result, parquet_storage_path, logger=None, fs=None):
        """
        Initialize ParquetSaver.
        :param df_result: Dask DataFrame to save.
        :param parquet_storage_path: Base storage path (e.g., "s3://bucket-name/path/").
        :param logger: Logger instance for logging messages.
        :param fs: Pre-initialized fsspec filesystem instance. Defaults to 'file' if None.
        """
        self.df_result = df_result
        self.parquet_storage_path = parquet_storage_path.rstrip("/")
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

        # Default to the local filesystem if `fs` is not provided
        self.fs = fs or fsspec.filesystem("file")

    def save_to_parquet(self, parquet_filename: Optional[str] = None, clear_existing=True):
        """
        Save the DataFrame to Parquet format.
        :param parquet_filename: Filename for the Parquet file.
        :param clear_existing: Whether to clear existing files in the target directory.
        """
        full_path = self._construct_full_path(parquet_filename)

        # Ensure directory exists and clear if necessary
        self._ensure_directory_exists(full_path, clear_existing=clear_existing)

        # Define schema and save DataFrame to Parquet
        schema = self._define_schema()
        self._convert_dtypes(schema)
        self._save_dataframe_to_parquet(full_path, schema)
        # Close the filesystem if the close method exists
        if hasattr(self.fs, 'close') and callable(getattr(self.fs, 'close', None)):
            self.fs.close()

    def _define_schema(self) -> pa.Schema:
        """Define a PyArrow schema dynamically based on df_result column types."""
        pandas_dtype_to_pa = {
            "object": pa.string(),
            "string": pa.string(),
            "Int64": pa.int64(),
            "int64": pa.int64(),
            "float64": pa.float64(),
            "float32": pa.float32(),
            "bool": pa.bool_(),
            "boolean": pa.bool_(),  # pandas nullable boolean
            "datetime64[ns]": pa.timestamp("ns"),
            "timedelta[ns]": pa.duration("ns"),
        }

        dtypes = self.df_result.dtypes

        fields = [
            pa.field(col, pandas_dtype_to_pa.get(str(dtype), pa.string()))
            for col, dtype in dtypes.items()
        ]
        return pa.schema(fields)

    def _convert_dtypes(self, schema: pa.Schema):
        """Convert DataFrame columns to match the specified schema."""
        dtype_mapping = {}
        for field in schema:
            col_name = field.name
            if col_name in self.df_result.columns:
                if pa.types.is_string(field.type):
                    dtype_mapping[col_name] = "string"
                elif pa.types.is_int64(field.type):
                    dtype_mapping[col_name] = "Int64"
                elif pa.types.is_float64(field.type):
                    dtype_mapping[col_name] = "float64"
                elif pa.types.is_float32(field.type):
                    dtype_mapping[col_name] = "float32"
                elif pa.types.is_boolean(field.type):
                    dtype_mapping[col_name] = "boolean"
                elif pa.types.is_timestamp(field.type):
                    dtype_mapping[col_name] = "datetime64[ns]"
                else:
                    dtype_mapping[col_name] = "object"
        self.df_result = self.df_result.astype(dtype_mapping)

    def _construct_full_path(self, parquet_filename: Optional[str]) -> str:
        """Construct and return the full path for the Parquet file."""
        parquet_filename = parquet_filename or "default.parquet"
        return f"{self.parquet_storage_path}/{parquet_filename}"

    def _ensure_directory_exists(self, full_path: str, clear_existing=False):
        """
        Ensure that the directory for the path exists, clearing it if specified.
        :param full_path: Full path for the target file.
        :param clear_existing: Whether to clear existing files/directories.
        """
        directory = "/".join(full_path.split("/")[:-1])

        if self.fs.exists(directory):
            if clear_existing:
                self.logger.info(f"Clearing existing directory: {directory}")
                self.fs.rm(directory, recursive=True)
        else:
            self.logger.info(f"Creating directory: {directory}")
            self.fs.mkdirs(directory, exist_ok=True)

    def _save_dataframe_to_parquet(self, full_path: str, schema: pa.Schema):
        """Save the DataFrame to Parquet using the specified schema."""
        if self.fs.exists(full_path):
            self.logger.info(f"Overwriting existing file: {full_path}")
            self.fs.rm(full_path, recursive=True)

        self.logger.info(f"Saving Parquet file to: {full_path}")
        self.df_result.to_parquet(
            full_path,
            engine="pyarrow",
            schema=schema,
            storage_options=self.fs.storage_options if hasattr(self.fs, "storage_options") else None,
            write_index=False,
        )

