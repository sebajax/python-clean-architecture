from fastapi import FastAPI
from .api import routes

def create_app():
    app = FastAPI(
        title="Python code structure for developing using clean architecture",
        version="1.0.0",
    )

    app.include_router(routes.health.router)

    return app