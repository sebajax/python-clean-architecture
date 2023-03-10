"""
pydantic schemas definition for user
"""
from pydantic import Field, EmailStr, BaseModel, Required


class UserSchema(BaseModel):
    """properties to return userdata with a valid token"""
    email: EmailStr = Field(default=Required)
    user_id: int = Field(default=Required)
    is_admin: bool = Field(default=Required)


class CreateUserSchema(BaseModel):
    """properties to receive on user creation"""
    email: EmailStr = Field(default=Required)
    first_name: str = Field(default=Required, min_length=1)
    last_name: str = Field(default=Required, min_length=1)
    password: str = Field(default=Required, min_length=1)
    is_admin: bool | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@mail.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "secret",
                "is_admin": False
            }
        }


class ResetPasswordSchema(BaseModel):
    """properties to reset a user password with a new one only accessed by admins"""
    email: EmailStr = Field(default=Required)
    password: str = Field(default=Required, min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@mail.com",
                "password": "secret",
            }
        }
