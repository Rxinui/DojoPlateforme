"""Responses model for FastAPI app.

@author Rxinui
@date 2022-02-02
@see https://fastapi.tiangolo.com/
"""
from typing import Any
from pydantic import BaseModel


class BasicResponse(BaseModel):
    """
    API response model

    msg: message to describe a response
    items: data to submit with the response
    """

    msg: str = ...
    items: dict = {}


class BasicError(BaseModel):
    """
    API error response model

    msg: message to describe a response
    """

    msg: str = ...
    code: str = ...
    details: Any
