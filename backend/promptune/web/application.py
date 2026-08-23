from fastapi import FastAPI

from promptune.log import configure_logging
from promptune.web.api.router import api_router
from promptune.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="promptune",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
