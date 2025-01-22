from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from .middlewares import runtime, http_exception, validation_exception
from starlette.exceptions import HTTPException as StarletteHTTPException
from .utilities.logging import configure_dt_logging


def create_app(
        application_title: str,
        version: str = '*',
        redoc_url: str = '/',
        docs_url: str = '/swagger',
        env_path: str | None = None,
        override_env: bool = True,
        middlewares: list | None = None,
        routes: list[dict] | None = None,
        gzip_compression: int | None = None,
        session_middleware_settings: dict | None = None,
        settings=None,
) -> FastAPI:

    if env_path:
        load_dotenv(dotenv_path=env_path, override=override_env)

    configure_dt_logging()

    applicable_middlewares = []

    if settings:
        applicable_middlewares.append(runtime.Runtime(
            settings=settings,
        ))

    if isinstance(middlewares, list):
        applicable_middlewares.extend(middlewares)

    if session_middleware_settings is None:
        session_middleware_settings = {}

    if routes is None:
        routes = []

    app = FastAPI(
        title=application_title,
        version=version,
        redoc_url=redoc_url,
        docs_url=docs_url,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )

    if gzip_compression is not None:
        app.add_middleware(GZipMiddleware, minimum_size=gzip_compression)

    if applicable_middlewares:
        from starlette.middleware.base import BaseHTTPMiddleware
        for middleware in applicable_middlewares:
            app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)

    if session_middleware_settings:
        from starlette.middleware.sessions import SessionMiddleware
        app.add_middleware(
            SessionMiddleware,
            secret_key=session_middleware_settings.get('secret_key'),
            session_cookie=session_middleware_settings.get('session_cookie'),
            https_only=session_middleware_settings.get('https_only'),
            same_site=session_middleware_settings.get('same_site'),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return await http_exception.http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return await validation_exception.validation_exception_handler(request, exc)

    for route in routes:
        app.include_router(
            router=route.get('router'),
            tags=route.get('tags'),
            prefix=route.get('prefix', ''),
            dependencies=route.get('dependencies', []),
            deprecated=route.get('deprecated', False),
            include_in_schema=route.get('include_in_schema', True),
        )

    return app
