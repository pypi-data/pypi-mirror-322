from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


def run_fastapi(
    application_title: str,
    main_application_path: str,
    applications: list[tuple],
    startups: list[callable],
    shutdowns: list[callable],
    version: str = '*',
    redoc_url: str | None = None,
    docs_url: str | None = None,
    allow_credentials: bool = True,
    allow_methods: list[str] | None = None,
    allow_headers: list[str] | None = None,
    allow_origins: list[str] | None = None,
) -> FastAPI:
    if allow_methods is None:
        allow_methods = ['*']

    if allow_headers is None:
        allow_headers = ['*']

    if allow_origins is None:
        allow_origins = [
            'https://admin.dealertower.com',
            'https://dashboard.datgate.com',
            'http://localhost:3000',
        ]

    app = FastAPI(
        title=application_title,
        version=version,
        redoc_url=redoc_url,
        docs_url=docs_url,
        swagger_ui_parameters={'defaultModelsExpandDepth': -1}
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        allow_origins=allow_origins,
    )

    for path, application in applications:
        app.mount(path, application)

    @app.on_event('startup')
    async def startup():
        for startup_application in startups:
            startup_application()

    @app.on_event('shutdown')
    async def shutdown_event():
        for shutdown_application in shutdowns:
            shutdown_application()

    @app.get('/', status_code=302)
    async def redirect():
        return RedirectResponse(main_application_path)

    return app
