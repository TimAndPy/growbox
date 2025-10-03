"""
Contract tests for MQTT sensor data messages.
Validates messages against the JSON schema defined in contracts/mqtt-sensor-data.json
"""

import pytest
import json
import jsonschema
from pathlib import Path
from datetime import datetime
import uuid


@pytest.fixture
def sensor_data_schema():
    """Load the sensor data JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "specs" / "001-i-want-to" / "contracts" / "mqtt-sensor-data.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def valid_temperature_message():
    """Create a valid temperature sensor message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "sensor_reading",
        "sensor": "temperature",
        "value": 23.5,
        "unit": "celsius",
        "status": "valid"
    }


@pytest.fixture
def valid_humidity_message():
    """Create a valid humidity sensor message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "sensor_reading",
        "sensor": "humidity",
        "value": 68.0,
        "unit": "percent",
        "status": "valid"
    }


@pytest.fixture
def valid_light_message():
    """Create a valid light sensor message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "sensor_reading",
        "sensor": "light",
        "value": 850.0,
        "unit": "ppfd",
        "status": "valid"
    }


@pytest.fixture
def valid_water_message():
    """Create a valid water level sensor message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "sensor_reading",
        "sensor": "water",
        "value": 42.0,
        "unit": "liters",
        "status": "valid"
    }


@pytest.mark.contract
class TestSensorDataContract:
    """Test suite for sensor data MQTT message contract."""

    def test_temperature_message_valid(self, sensor_data_schema, valid_temperature_message):
        """Test that valid temperature message passes schema validation."""
        # Should not raise an exception
        jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_humidity_message_valid(self, sensor_data_schema, valid_humidity_message):
        """Test that valid humidity message passes schema validation."""
        jsonschema.validate(instance=valid_humidity_message, schema=sensor_data_schema)

    def test_light_message_valid(self, sensor_data_schema, valid_light_message):
        """Test that valid light message passes schema validation."""
        jsonschema.validate(instance=valid_light_message, schema=sensor_data_schema)

    def test_water_message_valid(self, sensor_data_schema, valid_water_message):
        """Test that valid water message passes schema validation."""
        jsonschema.validate(instance=valid_water_message, schema=sensor_data_schema)

    def test_missing_required_field_fails(self, sensor_data_schema, valid_temperature_message):
        """Test that message without required field fails validation."""
        del valid_temperature_message['sensor']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_invalid_sensor_type_fails(self, sensor_data_schema, valid_temperature_message):
        """Test that invalid sensor type fails validation."""
        valid_temperature_message['sensor'] = 'invalid_sensor'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_invalid_status_fails(self, sensor_data_schema, valid_temperature_message):
        """Test that invalid status value fails validation."""
        valid_temperature_message['status'] = 'invalid_status'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_wrong_schema_version_fails(self, sensor_data_schema, valid_temperature_message):
        """Test that wrong schema version fails validation."""
        valid_temperature_message['schema_version'] = '2.0'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_additional_properties_fail(self, sensor_data_schema, valid_temperature_message):
        """Test that additional properties are not allowed."""
        valid_temperature_message['extra_field'] = 'should_fail'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_non_string_message_id_fails(self, sensor_data_schema, valid_temperature_message):
        """Test that non-string message_id fails validation."""
        valid_temperature_message['message_id'] = 12345
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_error_status_valid(self, sensor_data_schema, valid_temperature_message):
        """Test that 'error' status is valid."""
        valid_temperature_message['status'] = 'error'
        jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)

    def test_stale_status_valid(self, sensor_data_schema, valid_temperature_message):
        """Test that 'stale' status is valid."""
        valid_temperature_message['status'] = 'stale'
        jsonschema.validate(instance=valid_temperature_message, schema=sensor_data_schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
