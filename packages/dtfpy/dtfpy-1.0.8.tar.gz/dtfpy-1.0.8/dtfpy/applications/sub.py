from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..middlewares import runtime, http_exception, validation_exception
from ..routes.router import Router


@dataclass
class SubApp:
    application_title: str
    version: str = '*'
    redoc_url: str = '/'
    docs_url: str = '/swagger'
    middlewares: list | None = None
    routers: list[Router] | None = None
    gzip_compression: int | None = None
    session_middleware_settings: dict | None = None

    def create(self) -> FastAPI:
        self.applicable_middlewares = [
            runtime.Runtime()
        ]

        if isinstance(self.middlewares, list):
            self.applicable_middlewares.extend(self.middlewares)

        if self.session_middleware_settings is None:
            self.session_middleware_settings = {}

        if self.routers is None:
            self.routers = []

        fapp = FastAPI(
            title=self.application_title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1}
        )

        if self.gzip_compression is not None:
            fapp.add_middleware(GZipMiddleware, minimum_size=self.gzip_compression)

        if self.applicable_middlewares:
            from starlette.middleware.base import BaseHTTPMiddleware
            for middleware in self.applicable_middlewares:
                fapp.add_middleware(BaseHTTPMiddleware, dispatch=middleware)

        if self.session_middleware_settings:
            from starlette.middleware.sessions import SessionMiddleware
            fapp.add_middleware(
                SessionMiddleware,
                secret_key=self.session_middleware_settings.get('secret_key'),
                session_cookie=self.session_middleware_settings.get('session_cookie'),
                https_only=self.session_middleware_settings.get('https_only'),
                same_site=self.session_middleware_settings.get('same_site'),
            )

        @fapp.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request, exc):
            return await http_exception.http_exception_handler(request, exc)

        @fapp.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return await validation_exception.validation_exception_handler(request, exc)

        for router in self.routers:
            fapp.include_router(router=router)

        return fapp
