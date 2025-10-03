"""
Contract tests for MQTT system status messages.
Validates messages against the JSON schema defined in contracts/mqtt-system-status.json
"""

import pytest
import json
import jsonschema
from pathlib import Path
from datetime import datetime
import uuid


@pytest.fixture
def system_status_schema():
    """Load the system status JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "specs" / "001-i-want-to" / "contracts" / "mqtt-system-status.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def valid_system_status():
    """Create a valid system status message."""
    return {
        "schema_version": "1.0",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "box_id": "001",
        "type": "system_status",
        "connection_state": "online",
        "auto_mode_enabled": True,
        "active_alerts": ["water_level_low"],
        "uptime_seconds": 86400,
        "current_phase": "flowering",
        "days_in_phase": 28
    }


@pytest.mark.contract
class TestSystemStatusContract:
    """Test suite for system status MQTT message contract."""

    def test_valid_system_status(self, system_status_schema, valid_system_status):
        """Test that valid system status message passes validation."""
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_online_connection_state(self, system_status_schema, valid_system_status):
        """Test that 'online' connection state is valid."""
        valid_system_status['connection_state'] = 'online'
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_offline_connection_state(self, system_status_schema, valid_system_status):
        """Test that 'offline' connection state is valid."""
        valid_system_status['connection_state'] = 'offline'
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_auto_mode_enabled_true(self, system_status_schema, valid_system_status):
        """Test that auto_mode_enabled=true is valid."""
        valid_system_status['auto_mode_enabled'] = True
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_auto_mode_enabled_false(self, system_status_schema, valid_system_status):
        """Test that auto_mode_enabled=false is valid."""
        valid_system_status['auto_mode_enabled'] = False
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_empty_alerts_array(self, system_status_schema, valid_system_status):
        """Test that empty alerts array is valid."""
        valid_system_status['active_alerts'] = []
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_multiple_alerts(self, system_status_schema, valid_system_status):
        """Test that multiple alerts are valid."""
        valid_system_status['active_alerts'] = ["water_level_low", "temperature_high", "sensor_error"]
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_vegetative_phase(self, system_status_schema, valid_system_status):
        """Test that 'vegetative' phase is valid."""
        valid_system_status['current_phase'] = 'vegetative'
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_flowering_phase(self, system_status_schema, valid_system_status):
        """Test that 'flowering' phase is valid."""
        valid_system_status['current_phase'] = 'flowering'
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_zero_uptime(self, system_status_schema, valid_system_status):
        """Test that zero uptime is valid."""
        valid_system_status['uptime_seconds'] = 0
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_zero_days_in_phase(self, system_status_schema, valid_system_status):
        """Test that zero days in phase is valid."""
        valid_system_status['days_in_phase'] = 0
        jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_optional_fields_can_be_omitted(self, system_status_schema, valid_system_status):
        """Test that optional fields (active_alerts, uptime, current_phase, days_in_phase) can be omitted."""
        minimal_status = {
            "schema_version": "1.0",
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "box_id": "001",
            "type": "system_status",
            "connection_state": "online",
            "auto_mode_enabled": False
        }
        jsonschema.validate(instance=minimal_status, schema=system_status_schema)

    def test_missing_connection_state_fails(self, system_status_schema, valid_system_status):
        """Test that missing connection_state fails validation."""
        del valid_system_status['connection_state']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_missing_auto_mode_enabled_fails(self, system_status_schema, valid_system_status):
        """Test that missing auto_mode_enabled fails validation."""
        del valid_system_status['auto_mode_enabled']
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_invalid_connection_state_fails(self, system_status_schema, valid_system_status):
        """Test that invalid connection state fails validation."""
        valid_system_status['connection_state'] = 'invalid_state'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_invalid_phase_fails(self, system_status_schema, valid_system_status):
        """Test that invalid phase fails validation."""
        valid_system_status['current_phase'] = 'invalid_phase'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_negative_uptime_fails(self, system_status_schema, valid_system_status):
        """Test that negative uptime fails validation."""
        valid_system_status['uptime_seconds'] = -100
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_negative_days_in_phase_fails(self, system_status_schema, valid_system_status):
        """Test that negative days in phase fails validation."""
        valid_system_status['days_in_phase'] = -5
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_non_boolean_auto_mode_fails(self, system_status_schema, valid_system_status):
        """Test that non-boolean auto_mode_enabled fails validation."""
        valid_system_status['auto_mode_enabled'] = "true"  # String instead of boolean
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)

    def test_additional_properties_fail(self, system_status_schema, valid_system_status):
        """Test that additional properties are not allowed."""
        valid_system_status['extra_field'] = 'should_fail'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=valid_system_status, schema=system_status_schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
