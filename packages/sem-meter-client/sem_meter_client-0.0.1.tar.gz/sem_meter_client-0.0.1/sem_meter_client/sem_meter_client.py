"""Client for the SEM Meter API."""

import json

import aiohttp

from .circuit import CircuitResponse
from .equipment import EquipmentResponse
from .user import UserResponse


class SEMMeterClient:
    """Client for the SEM Meter API."""

    _base_url = "https://sem-meter.tumblevd.com/index"
    _fcm_token = "cn0IPHVGS3qrJdp5SRHqGy:APA91bFrEGN3Mca9oB9FLhDzrKbCqZ-rzts4oAqVYcEtFkYh6O9vLMg63juL6cI7y7VqT00B5O93NmqRBSbYi5eMLXCRVUx-Bzu8C65Z-rRQQ2kLa2JNpdE"  # noqa: E501, S105

    current_token: str | None = None

    async def login(self, username: str, password: str, timezone: str) -> UserResponse:
        """Login to the SEM Meter API."""
        url = f"{self._base_url}/Login/login"
        data = {
            "identificationCode": "1",
            "password": password,
            "phone_type": 0,
            "login_type": 1,
            "fcmToken": self._fcm_token,
            "email": username,
            "gmt": timezone,
        }
        async with (
            aiohttp.ClientSession() as session,
            session.post(url, data=data) as response,
        ):
            response_text = await response.text()
            user_dict = json.loads(response_text)
            return UserResponse.from_dict(user_dict)

    async def get_equipment_list(self) -> EquipmentResponse:
        """Get the equipment list."""
        data = {"token": self.current_token}
        url = f"{self._base_url}/Equipment/EquipmentsList"
        async with (
            aiohttp.ClientSession() as session,
            session.post(url, data=data) as response,
        ):
            response_text = await response.text()
            equipment_dict = json.loads(response_text)
            return EquipmentResponse.from_dict(equipment_dict)

    async def get_circuit_list(self, facility_id: int) -> CircuitResponse:
        """Get the circuit list."""
        data = {"token": self.current_token, "facility_id": facility_id}
        url = f"{self._base_url}/circuit/list"
        async with (
            aiohttp.ClientSession() as session,
            session.post(url, data=data) as response,
        ):
            response_text = await response.text()
            circuit_dict = json.loads(response_text)
            return CircuitResponse.from_dict(circuit_dict)
