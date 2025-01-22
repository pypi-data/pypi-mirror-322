from fastapi import Request
from ..utilities.exception import RequestException
from ..utilities.settings import get_settings


def simple_api_key(request: Request):
    auth_token = request.headers.get('Authorization')
    if auth_token is None or auth_token != get_settings('api_key'):
        raise RequestException(
            controller='dtfpy.middlewares.authentication.simple_api_key',
            message='Wrong credential.',
            status_code=403,
        )
