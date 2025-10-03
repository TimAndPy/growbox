"""
Data models for GrowBox entities.
Provides clean, minimal data structures for sensor readings, device states,
growth cycles, target parameters, and system status.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class SensorReading:
    """Represents a single sensor measurement."""

    sensor_type: Literal['temperature', 'humidity', 'light', 'water']
    value: float
    unit: str
    status: Literal['valid', 'error', 'stale'] = 'valid'
    timestamp: Optional[datetime] = None
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for MQTT publishing."""
        return {
            'sensor_type': self.sensor_type,
            'value': self.value,
            'unit': self.unit,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SensorReading':
        """Create instance from dictionary."""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            sensor_type=data['sensor_type'],
            value=data['value'],
            unit=data['unit'],
            status=data.get('status', 'valid'),
            timestamp=timestamp,
            id=data.get('id')
        )


@dataclass
class DeviceControl:
    """Represents a device state change or command."""

    device_type: Literal['lights', 'ventilation', 'pump', 'heater', 'co2']
    state: Literal['on', 'off']
    command_source: Literal['local', 'remote', 'auto', 'failsafe']
    triggered_by: Optional[str] = None
    timestamp: Optional[datetime] = None
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for MQTT publishing."""
        return {
            'device_type': self.device_type,
            'state': self.state,
            'command_source': self.command_source,
            'triggered_by': self.triggered_by,
            'timestamp': self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DeviceControl':
        """Create instance from dictionary."""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            device_type=data['device_type'],
            state=data['state'],
            command_source=data['command_source'],
            triggered_by=data.get('triggered_by'),
            timestamp=timestamp,
            id=data.get('id')
        )


@dataclass
class GrowthCycle:
    """Represents a growth phase cycle."""

    phase: Literal['vegetative', 'flowering']
    start_date: datetime
    light_schedule: str
    target_temp_min: float
    target_temp_max: float
    target_humidity_min: float
    target_humidity_max: float
    active: bool = True
    end_date: Optional[datetime] = None
    id: Optional[int] = None

    @property
    def days_in_phase(self) -> int:
        """Calculate days since start of this phase."""
        if self.start_date:
            delta = datetime.now() - self.start_date
            return delta.days
        return 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'phase': self.phase,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, datetime) else self.start_date,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'light_schedule': self.light_schedule,
            'target_temp_min': self.target_temp_min,
            'target_temp_max': self.target_temp_max,
            'target_humidity_min': self.target_humidity_min,
            'target_humidity_max': self.target_humidity_max,
            'active': self.active,
            'days_in_phase': self.days_in_phase
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GrowthCycle':
        """Create instance from dictionary."""
        start_date = data['start_date']
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)

        end_date = data.get('end_date')
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)

        return cls(
            phase=data['phase'],
            start_date=start_date,
            light_schedule=data['light_schedule'],
            target_temp_min=data['target_temp_min'],
            target_temp_max=data['target_temp_max'],
            target_humidity_min=data['target_humidity_min'],
            target_humidity_max=data['target_humidity_max'],
            active=data.get('active', True),
            end_date=end_date,
            id=data.get('id')
        )


@dataclass
class TargetParameters:
    """Represents target environmental parameters."""

    parameter_name: str
    min_value: float
    max_value: float
    hysteresis: float
    warning_threshold: float
    unit: str
    id: Optional[int] = None

    def is_below_target(self, current_value: float) -> bool:
        """Check if value is below minimum target."""
        return current_value < self.min_value

    def is_above_target(self, current_value: float) -> bool:
        """Check if value is above maximum target."""
        return current_value > self.max_value

    def is_in_range(self, current_value: float) -> bool:
        """Check if value is within acceptable range."""
        return self.min_value <= current_value <= self.max_value

    def should_deactivate(self, current_value: float, was_heating: bool) -> bool:
        """Determine if device should deactivate based on hysteresis."""
        if was_heating:
            return current_value >= (self.min_value + self.hysteresis)
        else:
            return current_value <= (self.max_value - self.hysteresis)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'parameter_name': self.parameter_name,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'hysteresis': self.hysteresis,
            'warning_threshold': self.warning_threshold,
            'unit': self.unit
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TargetParameters':
        """Create instance from dictionary."""
        return cls(
            parameter_name=data['parameter_name'],
            min_value=data['min_value'],
            max_value=data['max_value'],
            hysteresis=data['hysteresis'],
            warning_threshold=data['warning_threshold'],
            unit=data['unit'],
            id=data.get('id')
        )


@dataclass
class SystemStatus:
    """Represents system-wide status (singleton)."""

    connection_state: Literal['online', 'offline']
    last_mqtt_publish: Optional[datetime] = None
    last_sensor_read: Optional[datetime] = None
    auto_mode_enabled: bool = False
    active_alerts: list = None
    id: int = 1

    def __post_init__(self):
        """Initialize mutable default."""
        if self.active_alerts is None:
            self.active_alerts = []

    def add_alert(self, alert: str):
        """Add an alert to active alerts."""
        if alert not in self.active_alerts:
            self.active_alerts.append(alert)

    def clear_alert(self, alert: str):
        """Remove an alert from active alerts."""
        if alert in self.active_alerts:
            self.active_alerts.remove(alert)

    def clear_all_alerts(self):
        """Clear all active alerts."""
        self.active_alerts = []

    def to_dict(self) -> dict:
        """Convert to dictionary for MQTT publishing."""
        return {
            'connection_state': self.connection_state,
            'last_mqtt_publish': self.last_mqtt_publish.isoformat() if self.last_mqtt_publish else None,
            'last_sensor_read': self.last_sensor_read.isoformat() if self.last_sensor_read else None,
            'auto_mode_enabled': self.auto_mode_enabled,
            'active_alerts': self.active_alerts
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SystemStatus':
        """Create instance from dictionary."""
        last_mqtt_publish = data.get('last_mqtt_publish')
        if isinstance(last_mqtt_publish, str):
            last_mqtt_publish = datetime.fromisoformat(last_mqtt_publish)

        last_sensor_read = data.get('last_sensor_read')
        if isinstance(last_sensor_read, str):
            last_sensor_read = datetime.fromisoformat(last_sensor_read)

        return cls(
            connection_state=data['connection_state'],
            last_mqtt_publish=last_mqtt_publish,
            last_sensor_read=last_sensor_read,
            auto_mode_enabled=data.get('auto_mode_enabled', False),
            active_alerts=data.get('active_alerts', []),
            id=data.get('id', 1)
        )
