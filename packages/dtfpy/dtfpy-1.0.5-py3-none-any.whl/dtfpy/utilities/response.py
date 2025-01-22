from typing import Any, Callable, Generator
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse, Response

media_types = {
    'txt': 'text/plain',
    'csv': 'text/csv',
    'json': 'application/json',
    'xml': 'application/xml',
}


def return_json_response(data: Any = None, status_code: int = 200, return_directly: bool = False) -> JSONResponse:
    if not return_directly:
        if status_code < 300:
            return JSONResponse(
                status_code=status_code,
                content={
                    'success': True,
                    'data': jsonable_encoder(data)
                }
            )
        else:
            return JSONResponse(
                status_code=status_code,
                content={
                    'success': False,
                    'message': data
                }
            )
    else:
        return JSONResponse(
            status_code=status_code,
            content=data
        )


def return_direct_file_response(data: Any = None, status_code: int = 200, extension: str = 'txt',
                                file_name: str | None = None):
    return Response(
        status_code=status_code,
        content=data,
        media_type=media_types.get(extension),
        headers={
            "Content-Disposition": f"attachment; filename={file_name}.{extension}"
        } if file_name else None,
    )


def return_file_response(data: Any = None, status_code: int = 200, extension: str = 'txt',
                         file_name: str | None = None):
    return StreamingResponse(
        iter([data.getvalue()]),
        status_code=status_code,
        media_type=media_types.get(extension),
        headers={
            "Content-Disposition": f"attachment; filename={file_name}.{extension}"
        } if file_name else None
    )


def stream_json_array(filename: str, add_signs: bool, generator_func: Callable[..., Generator], *args, **kwargs) -> StreamingResponse:
    """
    Stream data as a JSON array from any generator function.

    This function ensures that the streamed data is correctly formatted as a JSON array,
    by adding the opening `[`, separating elements with `,`, and adding the closing `]`.

    Parameters:
    - generator_func: The generator function that yields JSON-formatted strings.
    - *args, **kwargs: Additional arguments to pass to the generator function.

    Returns:
    - StreamingResponse: Response to stream JSON array data.
    """

    def json_array_generator():
        # Yield the start of the JSON array
        if add_signs:
            yield "[\n"

        first_item = True
        for item in generator_func(*args, **kwargs):
            if add_signs:
                if not first_item:
                    # Yield a comma before each subsequent item
                    yield ",\n"
                else:
                    first_item = False

            # Yield the JSON-formatted item (it should already be a JSON-formatted string)
            yield item

        if add_signs:
            # Yield the end of the JSON array
            yield "]\n"

    headers = {"Content-Disposition": f"attachment; filename={filename}.json"}
    return StreamingResponse(json_array_generator(), media_type="application/json", headers=headers)
