"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mixpeek.types import BaseModel
from mixpeek.utils import FieldMetadata, PathParamMetadata
from typing_extensions import Annotated, TypedDict


class DeleteAPIKeyV1OrganizationsUsersUserEmailAPIKeysKeyNameDeleteRequestTypedDict(
    TypedDict
):
    user_email: str
    key_name: str


class DeleteAPIKeyV1OrganizationsUsersUserEmailAPIKeysKeyNameDeleteRequest(BaseModel):
    user_email: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]

    key_name: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
