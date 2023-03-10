"""
user repository all the database query strings for user table
"""
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Callable

from sqlalchemy import true
from sqlalchemy.orm import Session

from app.models.user_model import UserModel


@dataclass
class UserRepository:
    """
    class to represent the user repository
    """

    session_factory: Callable[..., AbstractContextManager[Session]]

    def insert_user_db(self, user: dict) -> int:
        """
        creates a new user in the database
        :param user: data to insert into the database previously validated
        :type: dict
        :return: the created user_id
        :rtype: int
        """
        with self.session_factory() as session:
            user_model: UserModel = UserModel()

            user_model.email = user.get("email")
            user_model.first_name = user.get("first_name")
            user_model.last_name = user.get("last_name")
            user_model.hashed_password = user.get("hashed_password")
            user_model.is_admin = user.get("is_admin")
            session.add(user_model)
            session.flush()
            session.commit()
            return user_model.user_id

    def check_user_db(self, email: str) -> UserModel:
        """
        check user by email from the database
        :param email: user email
        :type: str
        :return: the user data
        :rtype: UserModel
        """
        with self.session_factory() as session:
            return session.query(UserModel).filter(UserModel.email == email).first()

    def get_user_db(self, email: str) -> UserModel:
        """
        get active user by email from the database
        :param email: user email
        :type: str
        :return: the user data
        :rtype: UserModel
        """
        with self.session_factory() as session:
            return session.query(UserModel) \
                .filter(UserModel.email == email, UserModel.is_active == true()) \
                .first()

    def update_user_db(self, update_user_db: UserModel) -> None:
        """
        update user data in the database
        :param update_user_db: user data that is being updated
        :type: UserModel
        """
        with self.session_factory() as session:
            session.add(update_user_db)
            session.flush()
            session.commit()
