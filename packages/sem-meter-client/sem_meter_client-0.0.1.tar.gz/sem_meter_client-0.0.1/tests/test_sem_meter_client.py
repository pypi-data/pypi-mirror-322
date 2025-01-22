"""Test the SEMMeterClient class."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from sem_meter_client.circuit import CircuitResponse
from sem_meter_client.equipment import (
    EquipmentResponse,
)
from sem_meter_client.sem_meter_client import SEMMeterClient


class TestSEMMeterClient(unittest.IsolatedAsyncioTestCase):
    """Test the SEMMeterClient class."""

    @patch("aiohttp.ClientSession.post")
    async def test_login(self, mock_post: MagicMock) -> None:
        """Test the login method."""
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(
            return_value='{"code":200,"msg":"succeed","value":{"id":"8294","email":"test@example.com","image":"","nickname":"User1732160580","address":"","sex":"0","telephone":"","iphone":"","token":"test_token"}}'
        )
        mock_post.return_value.__aenter__.return_value = mock_response

        client = SEMMeterClient()
        user_response = await client.login("test@example.com", "password", "GMT")
        user = user_response.value
        mock_post.assert_called_once()
        assert user.id == 8294  # noqa: PLR2004
        assert user.token == "test_token"  # noqa: S105

    @patch("aiohttp.ClientSession.post")
    async def test_get_equipment_list(self, mock_post: MagicMock) -> None:
        """Test the get_equipment_list method."""
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(
            return_value='{"code": 0, "msg": "success", "value": []}'
        )
        mock_post.return_value.__aenter__.return_value = mock_response

        client = SEMMeterClient()
        client.current_token = "test_token"  # noqa: S105
        equipment = await client.get_equipment_list()

        mock_post.assert_called_once()
        self.assertIsInstance(equipment, EquipmentResponse)

    @patch("aiohttp.ClientSession.post")
    async def test_get_circuit_list(self, mock_post: MagicMock) -> None:
        """Test the get_circuit_list method."""
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(
            return_value='{"code": 0, "msg": "success", "value": []}'
        )
        mock_post.return_value.__aenter__.return_value = mock_response

        client = SEMMeterClient()
        client.current_token = "test_token"  # noqa: S105
        circuits = await client.get_circuit_list(1)

        mock_post.assert_called_once()
        self.assertIsInstance(circuits, CircuitResponse)
