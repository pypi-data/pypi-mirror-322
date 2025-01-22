"""Test the User class."""

import json
import unittest

import pytest

from sem_meter_client.user import User, UserResponse

magic_number = "1234567890"
test_token = "test_token"  # noqa: S105


class TestUser(unittest.TestCase):
    """Test the User class."""

    def test_from_dict(self) -> None:
        """Test the from_dict method."""
        user_dict = {
            "id": "1",
            "email": "test@example.com",
            "image": "test.png",
            "nickname": "Test User",
            "address": "Test Address",
            "sex": "Male",
            "telephone": "1234567890",
            "iphone": "1234567890",
            "token": "test_token",
        }
        user = User.from_dict(user_dict)
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.image == "test.png"
        assert user.nickname == "Test User"
        assert user.address == "Test Address"
        assert user.sex == "Male"
        assert user.telephone == magic_number
        assert user.iphone == magic_number
        assert user.token == test_token

    def test_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with invalid type."""
        with pytest.raises(TypeError):
            User.from_dict("invalid")


class TestUserResponse(unittest.TestCase):
    """Test the UserResponse class."""

    def test_from_dict(self) -> None:
        """Test the from_dict method."""
        user_response_dict = {
            "code": 0,
            "msg": "success",
            "value": {
                "id": "1",
                "email": "test@example.com",
                "image": "test.png",
                "nickname": "Test User",
                "address": "Test Address",
                "sex": "Male",
                "telephone": "1234567890",
                "iphone": "1234567890",
                "token": "test_token",
            },
        }
        user_response = UserResponse.from_dict(user_response_dict)
        assert user_response.code == 0
        assert user_response.msg == "success"
        assert user_response.value.id == 1
        assert user_response.value.email == "test@example.com"
        assert user_response.value.image == "test.png"
        assert user_response.value.nickname == "Test User"
        assert user_response.value.address == "Test Address"
        assert user_response.value.sex == "Male"
        assert user_response.value.telephone == magic_number
        assert user_response.value.iphone == magic_number
        assert user_response.value.token == test_token

    def test_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with invalid type."""
        with pytest.raises(TypeError):
            UserResponse.from_dict("invalid")

    def test_read_user_response(self) -> None:
        """Test the read_user_response method."""
        json_text = """
           {
                "code": 0,
                "msg": "success",
                "value": {
                    "id": "1",
                    "email": "test@example.com",
                    "image": "test.png",
                    "nickname": "Test User",
                    "address": "Test Address",
                    "sex": "Male",
                    "telephone": "1234567890",
                    "iphone": "1234567890",
                    "token": "test_token"
                }
            }
        """
        user_response = UserResponse.from_dict(json.loads(json_text))
        assert user_response.value.id == 1
        assert user_response.value.email == "test@example.com"
        assert user_response.value.image == "test.png"
        assert user_response.value.nickname == "Test User"
        assert user_response.value.address == "Test Address"
        assert user_response.value.sex == "Male"
        assert user_response.value.telephone == magic_number
        assert user_response.value.iphone == magic_number
        assert user_response.value.token == test_token
