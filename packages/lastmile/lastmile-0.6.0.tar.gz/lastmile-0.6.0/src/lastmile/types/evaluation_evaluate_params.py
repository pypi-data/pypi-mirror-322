# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EvaluationEvaluateParams", "Metadata", "MetadataValue", "Metric", "CommonMetadata"]


class EvaluationEvaluateParams(TypedDict, total=False):
    ground_truth: Required[Annotated[List[str], PropertyInfo(alias="groundTruth")]]

    input: Required[List[str]]

    labels: Required[List[str]]

    metadata: Required[Iterable[Metadata]]

    metric: Required[Metric]

    output: Required[List[str]]

    common_metadata: Annotated[CommonMetadata, PropertyInfo(alias="commonMetadata")]
    """
    Common metadata relevant to the application configuration from which all request
    inputs were derived. E.g. 'llm_model', 'chunk_size'
    """

    project_id: Annotated[str, PropertyInfo(alias="projectId")]
    """The project where evaluation inference logs will be stored"""


class MetadataValue(TypedDict, total=False):
    fields: Required[Dict[str, Dict[str, object]]]


class Metadata(TypedDict, total=False):
    value: MetadataValue


class Metric(TypedDict, total=False):
    id: str

    deployment_status: Annotated[
        Literal[
            "MODEL_DEPLOYMENT_STATUS_UNSPECIFIED",
            "MODEL_DEPLOYMENT_STATUS_PENDING",
            "MODEL_DEPLOYMENT_STATUS_ONLINE",
            "MODEL_DEPLOYMENT_STATUS_OFFLINE",
            "MODEL_DEPLOYMENT_STATUS_PAUSED",
        ],
        PropertyInfo(alias="deploymentStatus"),
    ]

    description: str

    name: str


class CommonMetadata(TypedDict, total=False):
    fields: Required[Dict[str, Dict[str, object]]]
