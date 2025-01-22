"""Define a Equipment class and a function to read JSON."""

from dataclasses import dataclass
from typing import Any

from sem_meter_client import from_int, from_list, from_str


@dataclass
class Family:
    """Family class."""

    id: int
    facility_id: int
    home_name: str
    address: str
    price: str
    billingtime: int
    etc: int
    utc: int
    time_name: str
    facility_alias: str

    @staticmethod
    def from_dict(obj: Any) -> "Family":
        """Get a Family from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        id = from_int(obj.get("id"))  # noqa: A001
        facility_id = from_int(obj.get("facility_id"))
        home_name = from_str(obj.get("home_name"))
        address = from_str(obj.get("address"))
        price = from_str(obj.get("price"))
        billingtime = from_int(obj.get("billingtime"))
        etc = int(from_str(obj.get("etc")))
        utc = int(from_str(obj.get("utc")))
        time_name = from_str(obj.get("time_name"))
        facility_alias = from_str(obj.get("facility_alias"))
        return Family(
            id,
            facility_id,
            home_name,
            address,
            price,
            billingtime,
            etc,
            utc,
            time_name,
            facility_alias,
        )


@dataclass
class Notification:
    """Notification class."""

    online_on: int
    online_off: int

    @staticmethod
    def from_dict(obj: Any) -> "Notification":
        """Get a Notification from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        online_on = from_int(obj.get("online_on"))
        online_off = from_int(obj.get("online_off"))
        return Notification(online_on, online_off)


@dataclass
class Equipment:
    """Equipment class."""

    facility_id: int
    facility_number: str
    facility_alias: str
    online_on: int
    online_off: int
    versions: str
    online: int
    family: Family
    notification: Notification
    home_name: str
    pitch: int

    @staticmethod
    def from_dict(obj: Any) -> "Equipment":
        """Get a Value from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        facility_id = from_int(obj.get("facility_id"))
        facility_number = from_str(obj.get("facility_number"))
        facility_alias = from_str(obj.get("facility_alias"))
        online_on = from_int(obj.get("online_on"))
        online_off = from_int(obj.get("online_off"))
        versions = from_str(obj.get("versions"))
        online = int(from_str(obj.get("online")))
        family = Family.from_dict(obj.get("family"))
        notification = Notification.from_dict(obj.get("notification"))
        home_name = from_str(obj.get("home_name"))
        pitch = from_int(obj.get("pitch"))
        return Equipment(
            facility_id,
            facility_number,
            facility_alias,
            online_on,
            online_off,
            versions,
            online,
            family,
            notification,
            home_name,
            pitch,
        )


@dataclass
class EquipmentResponse:
    """EquipmentResponse class."""

    code: int
    msg: str
    value: list[Equipment]

    @staticmethod
    def from_dict(obj: Any) -> "EquipmentResponse":
        """Get a EquipmentResponse from a dict."""
        if not isinstance(obj, dict):
            msg = f"Expected dict, got {type(obj)}"
            raise TypeError(msg)
        code = from_int(obj.get("code"))
        msg = from_str(obj.get("msg"))
        value = from_list(Equipment.from_dict, obj.get("value"))
        return EquipmentResponse(code, msg, value)
