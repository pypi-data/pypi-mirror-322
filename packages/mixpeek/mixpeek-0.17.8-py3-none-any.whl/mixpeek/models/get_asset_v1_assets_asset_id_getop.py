"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mixpeek.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from mixpeek.utils import (
    FieldMetadata,
    HeaderMetadata,
    PathParamMetadata,
    QueryParamMetadata,
)
import pydantic
from pydantic import model_serializer
from typing import Optional
from typing_extensions import Annotated, NotRequired, TypedDict


class GetAssetV1AssetsAssetIDGetRequestTypedDict(TypedDict):
    asset_id: str
    r"""Unique identifier of the asset"""
    return_url: NotRequired[bool]
    r"""Whether to generate and return presigned S3 URLs for the asset and preview. Set to false to improve performance when URLs aren't needed"""
    x_namespace: NotRequired[Nullable[str]]
    r"""Optional namespace for data isolation. This can be a namespace name or namespace ID. Example: 'netflix_prod' or 'ns_1234567890'. To create a namespace, use the /namespaces endpoint."""


class GetAssetV1AssetsAssetIDGetRequest(BaseModel):
    asset_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""Unique identifier of the asset"""

    return_url: Annotated[
        Optional[bool],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = True
    r"""Whether to generate and return presigned S3 URLs for the asset and preview. Set to false to improve performance when URLs aren't needed"""

    x_namespace: Annotated[
        OptionalNullable[str],
        pydantic.Field(alias="X-Namespace"),
        FieldMetadata(header=HeaderMetadata(style="simple", explode=False)),
    ] = UNSET
    r"""Optional namespace for data isolation. This can be a namespace name or namespace ID. Example: 'netflix_prod' or 'ns_1234567890'. To create a namespace, use the /namespaces endpoint."""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["return_url", "X-Namespace"]
        nullable_fields = ["X-Namespace"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
