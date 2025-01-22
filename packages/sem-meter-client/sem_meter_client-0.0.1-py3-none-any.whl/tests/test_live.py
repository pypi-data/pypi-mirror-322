"""Run a test against the live api."""

import os

import pytest

from sem_meter_client.sem_meter_client import SEMMeterClient


@pytest.mark.skip(reason="Live testing disabled.")
async def test_async() -> None:
    """Test the async login."""
    client = SEMMeterClient()
    username = os.environ["SEM_USERNAME"]
    password = os.environ["SEM_PASSWORD"]
    user = await client.login(username.strip(), password.strip(), "CST")
    client.current_token = user.token
    assert user.token is not None

    equipment = await client.get_equipment_list()
    assert equipment is not None
    assert len(equipment.value) > 0

    assert equipment.value[0].facility_id is not None
    circuits = await client.get_circuit_list(equipment.value[0].facility_id)
    assert circuits is not None
    assert len(circuits.value) > 0
