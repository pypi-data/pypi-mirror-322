"""Define a User class and a function to read JSON."""

from dataclasses import dataclass
from typing import Any

from sem_meter_client import from_int, from_str, from_str_none


@dataclass
class User:
    """User class."""

    id: int
    email: str
    image: str | None
    nickname: str
    address: str | None
    sex: str | None
    telephone: str | None
    iphone: str | None
    token: str

    @staticmethod
    def from_dict(obj: Any) -> "User":
        """Get a User from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        id = int(from_str(obj.get("id")))  # noqa: A001
        email = from_str(obj.get("email"))
        image = from_str_none(obj.get("image"))
        nickname = from_str(obj.get("nickname"))
        address = from_str_none(obj.get("address"))
        sex = from_str_none(obj.get("sex"))
        telephone = from_str_none(obj.get("telephone"))
        iphone = from_str_none(obj.get("iphone"))
        token = from_str(obj.get("token"))
        return User(id, email, image, nickname, address, sex, telephone, iphone, token)


@dataclass
class UserResponse:
    """UserResponse class."""

    code: int
    msg: str
    value: User

    @staticmethod
    def from_dict(obj: Any) -> "UserResponse":
        """Get a UserResponse from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        code = from_int(obj.get("code"))
        msg = from_str(obj.get("msg"))
        value = User.from_dict(obj.get("value"))
        return UserResponse(code, msg, value)
