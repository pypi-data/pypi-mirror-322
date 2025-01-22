"""Define a CircuitResponse class and a function to read JSON."""

from dataclasses import dataclass
from typing import Any

from sem_meter_client import from_int, from_list, from_str


@dataclass
class Circuit:
    """Circuit class."""

    id: int
    circuit_alias: str
    number: int
    online: int
    online_on: int
    online_off: int
    type_id: int
    multiplier: str
    type_name: str
    type_image: str
    electric: str

    @staticmethod
    def from_dict(obj: Any) -> "Circuit":
        """Get a Circuit from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        id = from_int(obj.get("id"))  # noqa: A001
        circuit_alias = from_str(obj.get("circuit_alias"))
        number = from_int(obj.get("number"))
        online = from_int(obj.get("online"))
        online_on = from_int(obj.get("online_on"))
        online_off = from_int(obj.get("online_off"))
        type_id = int(from_str(obj.get("type_id")))
        multiplier = from_str(obj.get("multiplier"))
        type_name = from_str(obj.get("typeName"))
        type_image = from_str(obj.get("typeImage"))
        electric = from_str(obj.get("electric"))
        return Circuit(
            id,
            circuit_alias,
            number,
            online,
            online_on,
            online_off,
            type_id,
            multiplier,
            type_name,
            type_image,
            electric,
        )


@dataclass
class CircuitResponse:
    """CircuitResponse class."""

    code: int
    msg: str
    value: list[Circuit]

    @staticmethod
    def from_dict(obj: Any) -> "CircuitResponse":
        """Get a CircuitResponse from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        code = from_int(obj.get("code"))
        msg = from_str(obj.get("msg"))
        value = from_list(Circuit.from_dict, obj.get("value"))
        return CircuitResponse(code, msg, value)
