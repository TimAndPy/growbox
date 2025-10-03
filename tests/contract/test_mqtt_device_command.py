"""
Contract tests for MQTT device command messages.
Validates messages against the JSON schema defined in contracts/mqtt-device-command.json
"""

import pytest
import json
import jsonschema
from pathlib import Path
from datetime import datetime
import uuid


@pytest.fixture
def device_command_schema():
    """Load the device command JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "specs" / "001-i-want-to" / "contracts" / "mqtt-device-command.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def valid_lights_command():
    """Create a valid lights control command."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "device_command",
        "device": "lights",
        "command": "on",
        "source": "remote",
        "triggered_by": "user_mendix_123"
    }


@pytest.mark.contract
class TestDeviceCommandContract:
    """Test suite for device command MQTT message contract."""

    def test_lights_on_command_valid(self, device_command_schema, valid_lights_command):
        """Test that valid lights ON command passes validation."""
        jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_all_devices_valid(self, device_command_schema, valid_lights_command):
        """Test that all device types are valid."""
        devices = ["lights", "ventilation", "pump", "heater", "co2"]
        for device in devices:
            valid_lights_command['device'] = device
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_all_commands_valid(self, device_command_schema, valid_lights_command):
        """Test that all command types are valid."""
        commands = ["on", "off", "auto"]
        for command in commands:
            valid_lights_command['command'] = command
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_local_source_valid(self, device_command_schema, valid_lights_command):
        """Test that 'local' source is valid."""
        valid_lights_command['source'] = 'local'
        jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_remote_source_valid(self, device_command_schema, valid_lights_command):
        """Test that 'remote' source is valid."""
        valid_lights_command['source'] = 'remote'
        jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_triggered_by_optional(self, device_command_schema, valid_lights_command):
        """Test that triggered_by field is optional."""
        del valid_lights_command['triggered_by']
        jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_missing_device_fails(self, device_command_schema, valid_lights_command):
        """Test that missing device field fails validation."""
        del valid_lights_command['device']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_missing_command_fails(self, device_command_schema, valid_lights_command):
        """Test that missing command field fails validation."""
        del valid_lights_command['command']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_invalid_device_fails(self, device_command_schema, valid_lights_command):
        """Test that invalid device type fails validation."""
        valid_lights_command['device'] = 'invalid_device'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_invalid_command_fails(self, device_command_schema, valid_lights_command):
        """Test that invalid command fails validation."""
        valid_lights_command['command'] = 'invalid_command'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_invalid_source_fails(self, device_command_schema, valid_lights_command):
        """Test that invalid source fails validation."""
        valid_lights_command['source'] = 'invalid_source'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)

    def test_additional_properties_fail(self, device_command_schema, valid_lights_command):
        """Test that additional properties are not allowed."""
        valid_lights_command['extra_field'] = 'should_fail'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_lights_command, schema=device_command_schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
