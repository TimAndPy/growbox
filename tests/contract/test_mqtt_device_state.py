"""
Contract tests for MQTT device state messages.
Validates messages against the JSON schema defined in contracts/mqtt-device-state.json
"""

import pytest
import json
import jsonschema
from pathlib import Path
from datetime import datetime
import uuid


@pytest.fixture
def device_state_schema():
    """Load the device state JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "specs" / "001-i-want-to" / "contracts" / "mqtt-device-state.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def valid_device_state():
    """Create a valid device state message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "device_state",
        "device": "lights",
        "state": "on",
        "command_source": "remote"
    }


@pytest.mark.contract
class TestDeviceStateContract:
    """Test suite for device state MQTT message contract."""

    def test_valid_device_state(self, device_state_schema, valid_device_state):
        """Test that valid device state message passes validation."""
        jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_all_devices_valid(self, device_state_schema, valid_device_state):
        """Test that all device types are valid."""
        devices = ["lights", "ventilation", "pump", "heater", "co2"]
        for device in devices:
            valid_device_state['device'] = device
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_all_states_valid(self, device_state_schema, valid_device_state):
        """Test that all state values are valid."""
        states = ["on", "off", "auto"]
        for state in states:
            valid_device_state['state'] = state
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_all_command_sources_valid(self, device_state_schema, valid_device_state):
        """Test that all command source values are valid."""
        sources = ["local", "remote", "auto", "failsafe"]
        for source in sources:
            valid_device_state['command_source'] = source
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_local_source_valid(self, device_state_schema, valid_device_state):
        """Test that 'local' command source is valid."""
        valid_device_state['command_source'] = 'local'
        jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_auto_source_valid(self, device_state_schema, valid_device_state):
        """Test that 'auto' command source is valid."""
        valid_device_state['command_source'] = 'auto'
        jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_failsafe_source_valid(self, device_state_schema, valid_device_state):
        """Test that 'failsafe' command source is valid."""
        valid_device_state['command_source'] = 'failsafe'
        valid_device_state['state'] = 'off'  # Failsafe always sets to OFF
        jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_missing_device_fails(self, device_state_schema, valid_device_state):
        """Test that missing device field fails validation."""
        del valid_device_state['device']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_missing_state_fails(self, device_state_schema, valid_device_state):
        """Test that missing state field fails validation."""
        del valid_device_state['state']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_missing_command_source_fails(self, device_state_schema, valid_device_state):
        """Test that missing command_source field fails validation."""
        del valid_device_state['command_source']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_invalid_device_fails(self, device_state_schema, valid_device_state):
        """Test that invalid device type fails validation."""
        valid_device_state['device'] = 'invalid_device'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_invalid_state_fails(self, device_state_schema, valid_device_state):
        """Test that invalid state fails validation."""
        valid_device_state['state'] = 'invalid_state'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_invalid_command_source_fails(self, device_state_schema, valid_device_state):
        """Test that invalid command source fails validation."""
        valid_device_state['command_source'] = 'invalid_source'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_additional_properties_fail(self, device_state_schema, valid_device_state):
        """Test that additional properties are not allowed."""
        valid_device_state['extra_field'] = 'should_fail'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)

    def test_wrong_message_type_fails(self, device_state_schema, valid_device_state):
        """Test that wrong message type fails validation."""
        valid_device_state['type'] = 'device_command'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_device_state, schema=device_state_schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
