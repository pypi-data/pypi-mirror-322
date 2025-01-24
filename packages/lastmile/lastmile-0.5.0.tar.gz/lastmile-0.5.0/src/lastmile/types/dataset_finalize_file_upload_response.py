# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DatasetFinalizeFileUploadResponse", "DatasetFile", "DatasetFileColumn"]


class DatasetFileColumn(BaseModel):
    id: str
    """The ID of the dataset file."""

    created_at: datetime = FieldInfo(alias="createdAt")

    index: int
    """Index of the column within the dataset file."""

    literal_name: str = FieldInfo(alias="literalName")
    """The literal name for the column."""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    dtype: Optional[
        Literal[
            "DATASET_COLUMN_D_TYPE_UNSPECIFIED",
            "DATASET_COLUMN_D_TYPE_INT32",
            "DATASET_COLUMN_D_TYPE_INT64",
            "DATASET_COLUMN_D_TYPE_FLOAT32",
            "DATASET_COLUMN_D_TYPE_FLOAT64",
            "DATASET_COLUMN_D_TYPE_STRING",
            "DATASET_COLUMN_D_TYPE_BYTES",
            "DATASET_COLUMN_D_TYPE_ANY",
            "DATASET_COLUMN_D_TYPE_LIST_OF_STRINGS",
        ]
    ] = None
    """Datatypes for a column in a dataset file.

    We likely don't need everything here, but it's good to be explicit, for example
    to avoid unknowingly coercing int64 values into int32. Encoding for text is
    UTF_8 unless indicated otherwise.
    """


class DatasetFile(BaseModel):
    id: str
    """The ID of the dataset file."""

    columns: List[DatasetFileColumn]

    content_md5_hash: str = FieldInfo(alias="contentMd5Hash")

    created_at: datetime = FieldInfo(alias="createdAt")

    dataset_id: str = FieldInfo(alias="datasetId")
    """The ID of the corresponding dataset."""

    file_size_bytes: int = FieldInfo(alias="fileSizeBytes")

    num_cols: int = FieldInfo(alias="numCols")

    num_rows: int = FieldInfo(alias="numRows")

    updated_at: datetime = FieldInfo(alias="updatedAt")


class DatasetFinalizeFileUploadResponse(BaseModel):
    dataset_file: Optional[DatasetFile] = FieldInfo(alias="datasetFile", default=None)
    """Information about the dataset file if the upload was successful"""
