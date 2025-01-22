from typing import Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse, Response

media_types = {
    'txt': 'text/plain',
    'csv': 'text/csv',
    'json': 'application/json',
    'xml': 'application/xml',
}


def return_json_response(
        data: Any = None,
        status_code: int = 200,
        return_directly: bool = False,
) -> JSONResponse:
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


def return_direct_file_response(
        data: Any = None,
        status_code: int = 200,
        extension: str = 'txt',
        file_name: str | None = None
):
    return Response(
        status_code=status_code,
        content=data,
        media_type=media_types.get(extension),
        headers={
            "Content-Disposition": f"attachment; filename={file_name}.{extension}"
        } if file_name else None,
    )


def return_file_response(
        data: Any = None,
        status_code: int = 200,
        extension: str = 'txt',
        file_name: str | None = None
):
    return StreamingResponse(
        iter([data.getvalue()]),
        status_code=status_code,
        media_type=media_types.get(extension),
        headers={
            "Content-Disposition": f"attachment; filename={file_name}.{extension}"
        } if file_name else None
    )
