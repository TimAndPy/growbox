"""
Database interface for GrowBox storage operations.
Provides CRUD methods for all entities with proper error handling.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import json

from .models import SensorReading, DeviceControl, GrowthCycle, TargetParameters, SystemStatus


class DatabaseInterface:
    """Interface for SQLite database operations."""

    def __init__(self, db_path: str = 'data/growbox.db'):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = None

    def connect(self):
        """Establish database connection with WAL mode."""
        if self._connection is None:
            self._connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA journal_mode=WAL")
        return self._connection

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # Sensor Reading Methods

    def insert_sensor_reading(self, reading: SensorReading) -> int:
        """Insert a new sensor reading."""
        conn = self.connect()
        cursor = conn.cursor()

        timestamp = reading.timestamp or datetime.utcnow()

        cursor.execute("""
            INSERT INTO sensor_readings (timestamp, sensor_type, value, unit, status)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, reading.sensor_type, reading.value, reading.unit, reading.status))

        conn.commit()
        return cursor.lastrowid

    def get_latest_sensor_value(self, sensor_type: str) -> Optional[SensorReading]:
        """Get the most recent reading for a sensor."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, sensor_type, value, unit, status
            FROM sensor_readings
            WHERE sensor_type = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (sensor_type,))

        row = cursor.fetchone()
        if row:
            return SensorReading(
                id=row['id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                sensor_type=row['sensor_type'],
                value=row['value'],
                unit=row['unit'],
                status=row['status']
            )
        return None

    def get_sensor_readings_in_range(self, sensor_type: str, start_time: datetime, end_time: datetime) -> List[SensorReading]:
        """Get sensor readings within a time range."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, sensor_type, value, unit, status
            FROM sensor_readings
            WHERE sensor_type = ? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (sensor_type, start_time, end_time))

        readings = []
        for row in cursor.fetchall():
            readings.append(SensorReading(
                id=row['id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                sensor_type=row['sensor_type'],
                value=row['value'],
                unit=row['unit'],
                status=row['status']
            ))
        return readings

    # Device Control Methods

    def insert_device_state(self, control: DeviceControl) -> int:
        """Insert a new device state change."""
        conn = self.connect()
        cursor = conn.cursor()

        timestamp = control.timestamp or datetime.utcnow()

        cursor.execute("""
            INSERT INTO device_states (timestamp, device_type, state, command_source, triggered_by)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, control.device_type, control.state, control.command_source, control.triggered_by))

        conn.commit()
        return cursor.lastrowid

    def get_latest_device_state(self, device_type: str) -> Optional[DeviceControl]:
        """Get the most recent state for a device."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, device_type, state, command_source, triggered_by
            FROM device_states
            WHERE device_type = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (device_type,))

        row = cursor.fetchone()
        if row:
            return DeviceControl(
                id=row['id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                device_type=row['device_type'],
                state=row['state'],
                command_source=row['command_source'],
                triggered_by=row['triggered_by']
            )
        return None

    def get_device_states_in_range(self, device_type: str, start_time: datetime, end_time: datetime) -> List[DeviceControl]:
        """Get device states within a time range."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, timestamp, device_type, state, command_source, triggered_by
            FROM device_states
            WHERE device_type = ? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (device_type, start_time, end_time))

        states = []
        for row in cursor.fetchall():
            states.append(DeviceControl(
                id=row['id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                device_type=row['device_type'],
                state=row['state'],
                command_source=row['command_source'],
                triggered_by=row['triggered_by']
            ))
        return states

    # Growth Cycle Methods

    def get_current_growth_cycle(self) -> Optional[GrowthCycle]:
        """Get the active growth cycle."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, start_date, end_date, phase, light_schedule,
                   target_temp_min, target_temp_max,
                   target_humidity_min, target_humidity_max, active
            FROM growth_cycles
            WHERE active = 1
            LIMIT 1
        """)

        row = cursor.fetchone()
        if row:
            return GrowthCycle(
                id=row['id'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']) if row['end_date'] else None,
                phase=row['phase'],
                light_schedule=row['light_schedule'],
                target_temp_min=row['target_temp_min'],
                target_temp_max=row['target_temp_max'],
                target_humidity_min=row['target_humidity_min'],
                target_humidity_max=row['target_humidity_max'],
                active=bool(row['active'])
            )
        return None

    def insert_growth_cycle(self, cycle: GrowthCycle) -> int:
        """Insert a new growth cycle and deactivate all others."""
        conn = self.connect()
        cursor = conn.cursor()

        # Deactivate all existing cycles
        cursor.execute("UPDATE growth_cycles SET active = 0 WHERE active = 1")

        # Insert new cycle
        cursor.execute("""
            INSERT INTO growth_cycles (start_date, phase, light_schedule,
                                      target_temp_min, target_temp_max,
                                      target_humidity_min, target_humidity_max, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """, (cycle.start_date, cycle.phase, cycle.light_schedule,
              cycle.target_temp_min, cycle.target_temp_max,
              cycle.target_humidity_min, cycle.target_humidity_max))

        conn.commit()
        return cursor.lastrowid

    def update_growth_cycle(self, cycle_id: int, **kwargs) -> bool:
        """Update a growth cycle's attributes."""
        conn = self.connect()
        cursor = conn.cursor()

        allowed_fields = ['end_date', 'phase', 'light_schedule', 'target_temp_min',
                         'target_temp_max', 'target_humidity_min', 'target_humidity_max', 'active']

        updates = []
        values = []
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)

        if not updates:
            return False

        values.append(cycle_id)
        query = f"UPDATE growth_cycles SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0

    # Target Parameters Methods

    def get_target_parameters(self, parameter_name: str) -> Optional[TargetParameters]:
        """Get target parameters for a specific environmental parameter."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, parameter_name, min_value, max_value, hysteresis, warning_threshold, unit
            FROM target_parameters
            WHERE parameter_name = ?
        """, (parameter_name,))

        row = cursor.fetchone()
        if row:
            return TargetParameters(
                id=row['id'],
                parameter_name=row['parameter_name'],
                min_value=row['min_value'],
                max_value=row['max_value'],
                hysteresis=row['hysteresis'],
                warning_threshold=row['warning_threshold'],
                unit=row['unit']
            )
        return None

    def get_all_target_parameters(self) -> List[TargetParameters]:
        """Get all target parameters."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, parameter_name, min_value, max_value, hysteresis, warning_threshold, unit
            FROM target_parameters
        """)

        params = []
        for row in cursor.fetchall():
            params.append(TargetParameters(
                id=row['id'],
                parameter_name=row['parameter_name'],
                min_value=row['min_value'],
                max_value=row['max_value'],
                hysteresis=row['hysteresis'],
                warning_threshold=row['warning_threshold'],
                unit=row['unit']
            ))
        return params

    def update_target_parameters(self, parameter_name: str, **kwargs) -> bool:
        """Update target parameters."""
        conn = self.connect()
        cursor = conn.cursor()

        allowed_fields = ['min_value', 'max_value', 'hysteresis', 'warning_threshold']

        updates = []
        values = []
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)

        if not updates:
            return False

        values.append(parameter_name)
        query = f"UPDATE target_parameters SET {', '.join(updates)} WHERE parameter_name = ?"

        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0

    # System Status Methods

    def get_system_status(self) -> SystemStatus:
        """Get system status (singleton)."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, connection_state, last_mqtt_publish, last_sensor_read,
                   auto_mode_enabled, active_alerts
            FROM system_status
            WHERE id = 1
        """)

        row = cursor.fetchone()
        if row:
            active_alerts = json.loads(row['active_alerts']) if row['active_alerts'] else []

            return SystemStatus(
                id=row['id'],
                connection_state=row['connection_state'],
                last_mqtt_publish=datetime.fromisoformat(row['last_mqtt_publish']) if row['last_mqtt_publish'] else None,
                last_sensor_read=datetime.fromisoformat(row['last_sensor_read']) if row['last_sensor_read'] else None,
                auto_mode_enabled=bool(row['auto_mode_enabled']),
                active_alerts=active_alerts
            )

        # Default if not found
        return SystemStatus(connection_state='offline')

    def update_system_status(self, **kwargs) -> bool:
        """Update system status singleton."""
        conn = self.connect()
        cursor = conn.cursor()

        allowed_fields = ['connection_state', 'last_mqtt_publish', 'last_sensor_read',
                         'auto_mode_enabled', 'active_alerts']

        updates = []
        values = []
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field == 'active_alerts':
                    value = json.dumps(value)
                updates.append(f"{field} = ?")
                values.append(value)

        if not updates:
            return False

        query = f"UPDATE system_status SET {', '.join(updates)} WHERE id = 1"

        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0
