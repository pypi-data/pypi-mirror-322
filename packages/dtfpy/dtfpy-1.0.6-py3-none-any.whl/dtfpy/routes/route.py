from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Callable, List, Optional, Type, Any, Dict
from pydantic import BaseModel
from .response import (
    return_direct_file_response,
    return_json_response,
    return_file_response,
)


class ResponseType(Enum):
    JSON = "json"
    DIRECT_FILE = "direct_file"
    FILE = "file"
    CUSTOM = "custom"


def is_async_callable(func: Callable) -> bool:
    return callable(func) and hasattr(func, "__await__")


@dataclass
class Route:
    path: str
    method: str
    handler: Callable
    response_type: ResponseType = ResponseType.JSON
    response_model: Optional[Type[BaseModel]] = None
    status_code: int = 200
    dependencies: List[Any] = field(default_factory=list)
    wrapper_kwargs: Dict[str, Any] = field(default_factory=dict)
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    response_description: str = ""
    responses: Optional[Dict[int, Dict[str, Any]]] = None
    deprecated: bool = False
    operation_id: Optional[str] = None
    include_in_schema: bool = True
    response_class: Optional[Type[Any]] = None
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    response_model_by_alias: bool = True

    def wrapped_handler(self) -> Callable:
        is_async = is_async_callable(self.handler)

        def wrap_function(wrapped_func: Callable) -> Callable:
            if self.response_type == ResponseType.JSON:
                @wraps(wrapped_func)
                async def async_wrapper(*args, **kwargs):
                    result = await wrapped_func(*args, **kwargs)
                    return return_json_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                @wraps(wrapped_func)
                def sync_wrapper(*args, **kwargs):
                    result = wrapped_func(*args, **kwargs)
                    return return_json_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                return async_wrapper if is_async else sync_wrapper

            elif self.response_type == ResponseType.DIRECT_FILE:
                @wraps(wrapped_func)
                async def async_wrapper(*args, **kwargs):
                    result = await wrapped_func(*args, **kwargs)
                    return return_direct_file_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                @wraps(wrapped_func)
                def sync_wrapper(*args, **kwargs):
                    result = wrapped_func(*args, **kwargs)
                    return return_direct_file_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                return async_wrapper if is_async else sync_wrapper

            elif self.response_type == ResponseType.FILE:
                @wraps(wrapped_func)
                async def async_wrapper(*args, **kwargs):
                    result = await wrapped_func(*args, **kwargs)
                    return return_file_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                @wraps(wrapped_func)
                def sync_wrapper(*args, **kwargs):
                    result = wrapped_func(*args, **kwargs)
                    return return_file_response(data=result, status_code=self.status_code, **self.wrapper_kwargs)

                return async_wrapper if is_async else sync_wrapper

            elif self.response_type == ResponseType.CUSTOM:
                @wraps(wrapped_func)
                async def async_wrapper(*args, **kwargs):
                    return await wrapped_func(*args, **kwargs)

                @wraps(wrapped_func)
                def sync_wrapper(*args, **kwargs):
                    return wrapped_func(*args, **kwargs)

                return async_wrapper if is_async else sync_wrapper

            else:
                raise ValueError(f"Unsupported response type: {self.response_type}")

        return wrap_function(self.handler)
