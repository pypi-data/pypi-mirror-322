"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mixpeek.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from pydantic import model_serializer
from typing_extensions import NotRequired, TypedDict


class QuerySettingsTypedDict(TypedDict):
    limit: NotRequired[Nullable[int]]
    r"""Optional limit for number of results per vector index, this is overriden by ?page_size=int if a single query is provided."""
    min_score: NotRequired[Nullable[float]]
    r"""Optional score threshold for filtering results"""
    modality: NotRequired[Nullable[str]]
    r"""Optional modality override for the query, this is only used for multimodal embeddings"""


class QuerySettings(BaseModel):
    limit: OptionalNullable[int] = UNSET
    r"""Optional limit for number of results per vector index, this is overriden by ?page_size=int if a single query is provided."""

    min_score: OptionalNullable[float] = UNSET
    r"""Optional score threshold for filtering results"""

    modality: OptionalNullable[str] = UNSET
    r"""Optional modality override for the query, this is only used for multimodal embeddings"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["limit", "min_score", "modality"]
        nullable_fields = ["limit", "min_score", "modality"]
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
