# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProjectDefaultResponse", "Project"]


class Project(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    name: str

    updated_at: datetime = FieldInfo(alias="updatedAt")

    creator_id: Optional[str] = FieldInfo(alias="creatorId", default=None)

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)

    description: Optional[str] = None

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)

    organization_name: Optional[str] = FieldInfo(alias="organizationName", default=None)


class ProjectDefaultResponse(BaseModel):
    project: Project
