from pydantic import BaseModel, TypeAdapter
from typing import Any, cast
import inspect

def is_dict(value: Any) -> bool:
    return isinstance(value, dict)

def is_list(value: Any) -> bool:
    return isinstance(value, list)

def has_more_than_n_keys(value: Any, n: int) -> bool:
    return len(value.keys()) > n


def to_strict_json_schema(model: type[BaseModel] | TypeAdapter[Any]) -> dict[str, Any]:
    if inspect.isclass(model) and issubclass(model, BaseModel):
        schema = model.model_json_schema()
    elif isinstance(model, TypeAdapter):
        schema = model.json_schema()
    else:
        raise TypeError(f"Unsupported model type - {model}")
    return schema


def type_to_response_format_param(response_format_input: type):

    if isinstance(response_format_input, dict):
        return response_format

    # type checkers don't narrow the negation of a `TypeGuard` as it isn't
    # a safe default behaviour but we know that at this point the `response_format`
    # can only be a `type`
    response_format = cast(type, response_format_input)

    json_schema_type: type[BaseModel] | TypeAdapter[Any] | None = None

    if issubclass(response_format, BaseModel):
        name = response_format.__name__
        json_schema_type = response_format

    elif hasattr(response_format, "__pydantic_config__"):
        name = response_format.__name__
        json_schema_type = TypeAdapter(response_format)
    else:
        raise TypeError(f"Unsupported response_format type - {response_format}")

    return {
        "schema": to_strict_json_schema(json_schema_type),
        "name": name,
    }
