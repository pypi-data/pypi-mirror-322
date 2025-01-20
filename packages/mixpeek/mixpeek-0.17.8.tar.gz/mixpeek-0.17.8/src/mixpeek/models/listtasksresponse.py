"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .db_model_paginationresponse import (
    DbModelPaginationResponse,
    DbModelPaginationResponseTypedDict,
)
from .taskresponse import TaskResponse, TaskResponseTypedDict
from mixpeek.types import BaseModel
from typing import List
from typing_extensions import TypedDict


class ListTasksResponseTypedDict(TypedDict):
    results: List[TaskResponseTypedDict]
    pagination: DbModelPaginationResponseTypedDict


class ListTasksResponse(BaseModel):
    results: List[TaskResponse]

    pagination: DbModelPaginationResponse
