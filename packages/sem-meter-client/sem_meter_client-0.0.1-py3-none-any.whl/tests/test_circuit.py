"""Test the Circuit class."""

import unittest

import pytest

from sem_meter_client.circuit import Circuit, CircuitResponse


class TestCircuit(unittest.TestCase):
    """Test the Circuit class."""

    def test_circuit_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {
            "id": 1,
            "circuit_alias": "Test Circuit",
            "number": 1,
            "online": 1,
            "online_on": 1,
            "online_off": 0,
            "type_id": "1",
            "multiplier": "1.0",
            "typeName": "Test Type",
            "typeImage": "test.png",
            "electric": "100",
        }
        circuit = Circuit.from_dict(obj)
        assert circuit.id == 1
        assert circuit.circuit_alias == "Test Circuit"
        assert circuit.number == 1
        assert circuit.online == 1
        assert circuit.online_on == 1
        assert circuit.online_off == 0
        assert circuit.type_id == 1
        assert circuit.multiplier == "1.0"
        assert circuit.type_name == "Test Type"
        assert circuit.type_image == "test.png"
        assert circuit.electric == "100"

    def test_circuit_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            Circuit.from_dict(obj)

    def test_circuit_response_from_dict(self) -> None:
        """Test the from_dict method."""
        obj = {
            "code": 0,
            "msg": "success",
            "value": [
                {
                    "id": 1,
                    "circuit_alias": "Test Circuit",
                    "number": 1,
                    "online": 1,
                    "online_on": 1,
                    "online_off": 0,
                    "type_id": "1",
                    "multiplier": "1.0",
                    "typeName": "Test Type",
                    "typeImage": "test.png",
                    "electric": "100",
                }
            ],
        }
        response = CircuitResponse.from_dict(obj)
        assert response.code == 0
        assert response.msg == "success"
        assert response.value[0].id == 1

    def test_circuit_response_from_dict_invalid_type(self) -> None:
        """Test the from_dict method with an invalid type."""
        obj = "invalid"
        with pytest.raises(TypeError):
            CircuitResponse.from_dict(obj)
