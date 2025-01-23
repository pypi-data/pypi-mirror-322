from __future__ import annotations

from collections.abc import Collection
from http import HTTPStatus
from typing import Any, ClassVar, Generic, Type, TypeVar, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, SerializeAsAny, create_model

Loc = list[str | int]


class BaseModel(PydanticBaseModel):
    """
    Base model for the diagnostic pydantic models.
    """

    model_config = ConfigDict(extra="forbid")


class GenericError(BaseModel):
    """Generic error model compatible with pydantic diagnostics."""

    loc: Loc = Field(default_factory=list, title="Error location.")
    msg: str = Field(title="Descriptive human readable error message")
    type: str = Field(title="Error type identifier")


class DiagnosticError(GenericError):
    """
    Base class for all diagnostic errors.
    """

    model_config = ConfigDict(extra="allow")

    # This is intentionally protected, as Pydantic does not export protected members to OpenAPI schema,
    # and that is exactly what we want. Status code is not part of the JSON response, but it represents
    # HTTP status code of the error response.
    status_code: ClassVar[int] = HTTPStatus.UNPROCESSABLE_ENTITY

    loc: Loc = Field(default_factory=list, title="Error location")
    msg: str = Field(title="Descriptive human readable error message")
    type: str = Field(title="Error type identifier")


T = TypeVar("T", bound=GenericError)


class DiagnosticResponse(BaseModel, Generic[T]):
    """
    Response returned to user, when any diagnostic error is collected.
    """

    detail: list[SerializeAsAny[T]] = Field(default_factory=list)


def diagnostic_schema(
    types: Collection[Type[DiagnosticError]], include_pydantic_errors: bool = True
) -> dict[int | str, dict[str, Any]]:
    """
    Create a diagnostic response schema for the given error types. Usefull for documenting
    API endpoint diagnostic responses for OpenAPI schema.

    Usage with FastAPI:

    >>> from fastapi import FastAPI
    >>> from gcm_diagnostics.models import diagnostic_schema
    >>> from gcm_diagnostics.errors import EntityNotFound, EntityAlreadyExists
    >>>
    >>> app = FastAPI()
    >>>
    >>>
    >>> @app.get("/", responses=diagnostic_schema([EntityNotFound, EntityAlreadyExists]))
    >>> async def index():
    >>>     pass

    :param types: Collection of diagnostic error types for which the response schema should be generated.
    :param include_pydantic_errors: Include pydantic's default error schema for 422.
    :return: Diagnostic response schema suitable for FastAPI endpoint.
    """

    errors_by_status: dict[int, list[Type[GenericError]]] = {}

    if include_pydantic_errors:
        errors_by_status[HTTPStatus.UNPROCESSABLE_ENTITY] = [GenericError]

    # Group errors by status code.
    for t in types:
        errors_by_status.setdefault(t.status_code, []).append(t)

    # Create schema for each status code.
    return {
        status: {
            "model": create_model(
                f"DiagnosticResponse{status}",
                __doc__=f"Error response for HTTP status {status}.",
                # Union unpacking works for Pydantic, but mypy does not like it.
                __base__=DiagnosticResponse[Union[*types]],  # type: ignore[valid-type]
            )
        }
        for status, types in errors_by_status.items()
    }
