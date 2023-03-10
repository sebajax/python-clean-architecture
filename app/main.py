import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.api.dependencies import Container
from app.core.config import get_settings

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI(title=f"{get_settings().PROJECT_NAME}", version=f"{get_settings().VERSION}")

# wiring container app dependencies
container = Container()
app.container = container

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health_check():
    """api health check"""
    return JSONResponse(content={
        "health": f"API {get_settings().PROJECT_NAME} version {get_settings().VERSION} is healthy"
    })


app.include_router(api_router, prefix=f"{get_settings().API_PREFIX}")
