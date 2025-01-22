from dataclasses import dataclass
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from ..utilities.logging import configure_dt_logging


@dataclass
class MainApp:
    application_title: str
    applications: list[tuple[str, FastAPI]]
    startups: list[callable]
    shutdowns: list[callable]
    version: str = '*'
    redirection_path: str = None
    redoc_url: str | None = None
    docs_url: str | None = None
    allow_credentials: bool = False
    allow_methods: list[str] | None = None
    allow_headers: list[str] | None = None
    allow_origins: list[str] | None = None
    env_path: str | None = None
    override_env: bool = True

    def create(self) -> FastAPI:
        if self.env_path:
            load_dotenv(dotenv_path=self.env_path, override=self.override_env)

        configure_dt_logging()

        if self.allow_methods is None:
            self.allow_methods = ['*']

        if self.allow_headers is None:
            self.allow_headers = ['*']

        if self.allow_origins is None:
            self.allow_origins = ['*']

        if self.redirection_path is None and self.applications:
            self.redirection_path = self.applications[0][0]

        fapp = FastAPI(
            title=self.application_title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={'defaultModelsExpandDepth': -1}
        )

        fapp.add_middleware(
            CORSMiddleware,
            allow_credentials=self.allow_credentials,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
            allow_origins=self.allow_origins,
        )

        for path, application in self.applications:
            fapp.mount(path, application)

        @fapp.on_event('startup')
        async def startup():
            for startup_application in self.startups:
                startup_application()

        @fapp.on_event('shutdown')
        async def shutdown_event():
            for shutdown_application in self.shutdowns:
                shutdown_application()

        if self.redirection_path:
            @fapp.get('/', status_code=302)
            async def redirect():
                return RedirectResponse(self.redirection_path)

        return fapp
