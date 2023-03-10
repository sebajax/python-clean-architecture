"""
core authentication methods for api
"""
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from app.core.config import get_settings
from app.schemas.user_schema import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES: int = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY: str = get_settings().SECRET_KEY
ALGORITHM: str = get_settings().ALGORITHM

# get root logger
logger = logging.getLogger(__name__)


@dataclass
class Auth:
    """
    class to handle the api authorization methods
    """

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        verifies if the password is correct for the user
        :param plain_password:
        :type plain_password: str
        :param hashed_password:
        :type hashed_password: str
        :return: true if password is correct
        :rtype: bool
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        hash selected user password to store into the database
        :param password:
        :type password: str
        :return: hashed password
        :rtype: str
        """
        return pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, username: str, user_id: int, is_admin: bool) -> str:
        """
        creates the access token and returns with the expiration time
        :param username:
        :type username: str
        :param user_id:
        :type user_id: int
        :param is_admin:
        :type: is_admin: bool
        :return:
        :rtype: str
        """
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {
            "exp": expire,
            "email": str(username),
            "user_id": user_id,
            "is_admin": is_admin
        }

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)) -> UserSchema:
        """
        checks if token is valid and returns user information
        :param token:
        :type token: str
        :return:
        :rtype: UserSchema
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INCORRECT_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            logging.info("token %s", token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if not payload:
                raise credentials_exception

            return UserSchema(**payload)
        except JWTError as jwt_error:
            logging.error(jwt_error)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="jwt error"
            ) from jwt_error

    @classmethod
    async def get_current_user_admin(cls, token: str = Depends(oauth2_scheme)) -> UserSchema:
        """
        checks if token is valid and if user is admin and return admin user info
        :param token:
        :type token: str
        :return:
        :rtype: UserSchema
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INCORRECT_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            logging.info("token %s", token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if not payload:
                raise credentials_exception

            if payload.get("is_admin") is not True:
                raise credentials_exception

            return UserSchema(**payload)
        except JWTError as jwt_error:
            logging.error(jwt_error)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="jwt error"
            ) from jwt_error
