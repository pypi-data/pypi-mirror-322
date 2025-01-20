"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .collectionresult import CollectionResult, CollectionResultTypedDict
from .db_model_paginationresponse import (
    DbModelPaginationResponse,
    DbModelPaginationResponseTypedDict,
)
from mixpeek.types import BaseModel
from typing import List
from typing_extensions import TypedDict


class ListCollectionsResponseTypedDict(TypedDict):
    results: List[CollectionResultTypedDict]
    pagination: DbModelPaginationResponseTypedDict


class ListCollectionsResponse(BaseModel):
    results: List[CollectionResult]

    pagination: DbModelPaginationResponse
