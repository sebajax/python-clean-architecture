"""
routing api for users
"""

import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies import Container
from app.schemas.user_schema import CreateUserSchema
from app.services.create_user_service import CreateUserService
from app.services.exception_service import ServiceException
from app.services.response_service import ResponseService

# get root logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=ResponseService)
@inject
async def create_user(
        user: CreateUserSchema,
        # admin: UserSchema = Depends(Provide[Container.auth_provider.provided.get_current_user_admin]),
        create_user_service: CreateUserService = Depends(Provide[Container.create_user_service_provider])
) -> ResponseService:
    """
    api insert a new user
    :param user:
    :param admin:
    :param create_user_service:
    :return:
    """
    try:
        logger.info("to %s", user.email)
        # logger.info("admin creating user %s", admin.email)

        response = await create_user_service.create_user(
            user=user
        )
        return response

    except ServiceException as service_exception:
        logger.warning(service_exception)
        raise HTTPException(
            status_code=service_exception.status_code,
            detail=service_exception.detail
        ) from service_exception
    except Exception as error:
        logger.error("ERROR ENTRE ACA")
        print(error)
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        ) from error
