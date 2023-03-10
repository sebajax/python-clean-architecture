"""
create user service use case definition
"""

import logging
from dataclasses import dataclass

from app.infrastructure.auth.auth import Auth
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserSchema
from app.services.exception_service import ServiceException
from app.services.response_service import ResponseService

# get root logger
logger = logging.getLogger(__name__)


@dataclass
class CreateUserService:
    """
    class to represent the creation of lead use case
    """

    auth: Auth
    user_repository: UserRepository

    async def create_user(
            self,
            user: CreateUserSchema,
    ) -> ResponseService:
        """
        use case resolution for creating a new user
        :param user:
        :type user: CreateUserSchema
        :return: service response message & data
        :rtype: ResponseService
        """
        user_dict = user.dict()

        # check if user email already exists
        check_user = self.user_repository.get_user_db(user.email)
        if check_user is not None:
            raise ServiceException(detail="USER_EXISTS", status_code=400)

        # store hashed password into database using auth class
        user_dict["hashed_password"] = self.auth.get_password_hash(user.password)

        # store the new user into the database to process his leads
        user_id = self.user_repository.insert_user_db(user_dict)
        logger.info("created user %s", user_id)

        return ResponseService(detail="USER_CREATED", data={"user_id": user_id})
