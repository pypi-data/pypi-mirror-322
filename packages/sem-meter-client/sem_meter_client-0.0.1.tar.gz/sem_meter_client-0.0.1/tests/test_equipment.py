"""Test the equipment module."""

import unittest

import pytest

from sem_meter_client.equipment import (
    Equipment,
    EquipmentResponse,
    Family,
    Notification,
)


class TestFamily:
    """Test the Family class."""

    def test_family_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {
            "id": 1,
            "facility_id": 1,
            "home_name": "Test Home",
            "address": "Test Address",
            "price": "1.0",
            "billingtime": 1,
            "etc": "1",
            "utc": "1",
            "time_name": "Test Time",
            "facility_alias": "Test Alias",
        }
        family = Family.from_dict(obj)
        assert family.id == 1
        assert family.facility_id == 1
        assert family.home_name == "Test Home"

    def test_family_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            Family.from_dict(obj)


class TestNotification(unittest.TestCase):
    """Test the Notification class."""

    def test_notification_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {"online_on": 1, "online_off": 0}
        notification = Notification.from_dict(obj)
        assert notification.online_on == 1
        assert notification.online_off == 0

    def test_notification_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            Notification.from_dict(obj)


class TestEquipment(unittest.TestCase):
    """Test the Equipment class."""

    def test_equipment_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {
            "facility_id": 1,
            "facility_number": "1",
            "facility_alias": "Test Alias",
            "online_on": 1,
            "online_off": 0,
            "versions": "1.0",
            "online": "1",
            "family": {
                "id": 1,
                "facility_id": 1,
                "home_name": "Test Home",
                "address": "Test Address",
                "price": "1.0",
                "billingtime": 1,
                "etc": "1",
                "utc": "1",
                "time_name": "Test Time",
                "facility_alias": "Test Alias",
            },
            "notification": {"online_on": 1, "online_off": 0},
            "home_name": "Test Home",
            "pitch": 1,
        }
        equipment = Equipment.from_dict(obj)
        assert equipment.facility_id == 1
        assert equipment.facility_number == "1"
        assert equipment.facility_alias == "Test Alias"
        assert equipment.online_on == 1
        assert equipment.online_off == 0
        assert equipment.versions == "1.0"
        assert equipment.online == 1
        assert equipment.family.id == 1
        assert equipment.notification.online_on == 1
        assert equipment.home_name == "Test Home"
        assert equipment.pitch == 1

    def test_equipment_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            Equipment.from_dict(obj)


class TestEquipmentResponse(unittest.TestCase):
    """Test the EquipmentResponse class."""

    def test_equipment_response_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {
            "code": 0,
            "msg": "success",
            "value": [
                {
                    "facility_id": 1,
                    "facility_number": "1",
                    "facility_alias": "Test Alias",
                    "online_on": 1,
                    "online_off": 0,
                    "versions": "1.0",
                    "online": "1",
                    "family": {
                        "id": 1,
                        "facility_id": 1,
                        "home_name": "Test Home",
                        "address": "Test Address",
                        "price": "1.0",
                        "billingtime": 1,
                        "etc": "1",
                        "utc": "1",
                        "time_name": "Test Time",
                        "facility_alias": "Test Alias",
                    },
                    "notification": {"online_on": 1, "online_off": 0},
                    "home_name": "Test Home",
                    "pitch": 1,
                }
            ],
        }
        response = EquipmentResponse.from_dict(obj)
        assert response.code == 0
        assert response.msg == "success"
        assert len(response.value) == 1

    def test_equipment_response_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            EquipmentResponse.from_dict(obj)
