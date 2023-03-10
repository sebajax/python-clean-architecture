"""
create lead service unit tests
"""
from unittest.mock import Mock

import pytest

from app.schemas.user_schema import CreateUserSchema
from app.services.admins.create_user_service import CreateUserService
from app.services.exception_service import ServiceException


# pylint: disable=redefined-outer-name
# ^^^ this

@pytest.fixture()
def user() -> CreateUserSchema:
    """
    function to generate the user pytest fixture
    """
    return CreateUserSchema(
        email="test@test.com",
        first_name="test_first",
        last_name="test_last",
        identity_number="1-9",
        client_name="test_client",
        password="test",
        is_admin=False
    )


def test_create_user_success(user: CreateUserSchema) -> None:
    """
    function to test CreateUserService.create_user -> success
    """
    # create mock UserRepository
    mock_user_repository = Mock()
    mock_created_user_id = 1
    mock_user_repository.get_user_db.return_value = None
    mock_user_repository.insert_user_db.return_value = mock_created_user_id
    # create mock Auth
    mock_auth = Mock()
    mock_hashed_password = "hashed_password"
    mock_auth.get_password_hash.return_value = mock_hashed_password

    # call create user use case method
    response = CreateUserService.create_user(
        user=user,
        auth=mock_auth,
        user_repository=mock_user_repository
    )

    # create data to check assert call
    user_dict = user.dict()
    user_dict["hashed_password"] = mock_hashed_password

    # check test
    mock_user_repository.get_user_db.assert_called_once_with(user.email)
    mock_auth.get_password_hash.assert_called_once_with(user.password)
    mock_user_repository.insert_user_db.assert_called_once_with(user_dict)
    assert response.detail == "USER_CREATED"
    assert response.data.get("user_id") == mock_created_user_id


def test_create_user_fail_user_exists(user: CreateUserSchema) -> None:
    """
    function to test CreateUserService.create_user -> fail user already exists in the database
    """
    with pytest.raises(ServiceException) as service_exception:
        # create mock UserRepository
        mock_user_repository = Mock()
        mock_user_repository.get_user_db.return_value = Mock(user_id=1, email="test@test.com")
        # create mock Auth
        mock_auth = Mock()

        # call create user use case method
        CreateUserService.create_user(
            user=user,
            auth=mock_auth,
            user_repository=mock_user_repository
        )

        # check test
        mock_user_repository.get_user_db.assert_called_once_with(user.email)
        mock_auth.get_password_hash.assert_not_called()
        mock_user_repository.insert_user_db.assert_not_called()
        assert service_exception.value.detail == "USER_EXISTS"
        assert service_exception.value.status_code == 400
