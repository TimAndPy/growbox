"""
Unit tests for database storage operations.
Tests CRUD operations, indexes, and data integrity.
"""

import pytest
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from src.storage.database import DatabaseInterface
from src.storage.models import (
    SensorReading,
    DeviceControl,
    GrowthCycle,
    TargetParameters,
    SystemStatus
)


@pytest.mark.unit
class TestDatabaseInterface:
    """Test database interface basic operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"

        # Initialize schema
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        # Create interface
        db = DatabaseInterface(str(db_path))
        db.connect()

        yield db

        db.close()

    def test_database_connection(self, test_db):
        """Test database connects successfully."""
        assert test_db._connection is not None

    def test_wal_mode_enabled(self, test_db):
        """Test WAL mode is enabled for concurrent access."""
        cursor = test_db._connection.cursor()
        cursor.execute("PRAGMA journal_mode")
        result = cursor.fetchone()

        assert result[0].upper() == 'WAL'


@pytest.mark.unit
class TestSensorReadingOperations:
    """Test sensor reading CRUD operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_insert_sensor_reading(self, test_db):
        """Test inserting sensor reading."""
        reading = SensorReading(
            sensor_type='temperature',
            value=23.5,
            unit='celsius',
            status='valid',
            timestamp=datetime.utcnow()
        )

        reading_id = test_db.insert_sensor_reading(reading)
        assert reading_id > 0

    def test_get_latest_sensor_value(self, test_db):
        """Test retrieving latest sensor value."""
        # Insert multiple readings
        for i in range(3):
            reading = SensorReading(
                sensor_type='temperature',
                value=20.0 + i,
                unit='celsius',
                status='valid',
                timestamp=datetime.utcnow()
            )
            test_db.insert_sensor_reading(reading)

        # Get latest
        latest = test_db.get_latest_sensor_value('temperature')

        assert latest is not None
        assert latest.value == 22.0
        assert latest.sensor_type == 'temperature'

    def test_get_sensor_readings_in_range(self, test_db):
        """Test retrieving sensor readings within time range."""
        now = datetime.utcnow()

        # Insert readings with different timestamps
        for i in range(5):
            reading = SensorReading(
                sensor_type='humidity',
                value=60.0 + i,
                unit='percent',
                status='valid',
                timestamp=now - timedelta(minutes=5-i)
            )
            test_db.insert_sensor_reading(reading)

        # Query range
        start_time = now - timedelta(minutes=3)
        end_time = now

        readings = test_db.get_sensor_readings_in_range('humidity', start_time, end_time)

        assert len(readings) == 3
        assert all(r.sensor_type == 'humidity' for r in readings)


@pytest.mark.unit
class TestDeviceControlOperations:
    """Test device control CRUD operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_insert_device_state(self, test_db):
        """Test inserting device state change."""
        control = DeviceControl(
            device_type='lights',
            state='on',
            command_source='local',
            triggered_by='tablet_ui',
            timestamp=datetime.utcnow()
        )

        control_id = test_db.insert_device_state(control)
        assert control_id > 0

    def test_get_latest_device_state(self, test_db):
        """Test retrieving latest device state."""
        # Insert multiple states
        for state in ['on', 'off', 'on']:
            control = DeviceControl(
                device_type='pump',
                state=state,
                command_source='auto',
                triggered_by='water_level_low',
                timestamp=datetime.utcnow()
            )
            test_db.insert_device_state(control)

        # Get latest
        latest = test_db.get_latest_device_state('pump')

        assert latest is not None
        assert latest.state == 'on'
        assert latest.device_type == 'pump'


@pytest.mark.unit
class TestGrowthCycleOperations:
    """Test growth cycle CRUD operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_get_current_growth_cycle(self, test_db):
        """Test retrieving current active growth cycle."""
        cycle = test_db.get_current_growth_cycle()

        # Should have default vegetative cycle from init
        assert cycle is not None
        assert cycle.phase == 'vegetative'
        assert cycle.active is True

    def test_insert_growth_cycle_deactivates_others(self, test_db):
        """Test inserting new cycle deactivates previous cycles."""
        # Create new flowering cycle
        new_cycle = GrowthCycle(
            phase='flowering',
            start_date=datetime.utcnow(),
            light_schedule='12/12',
            target_temp_min=22.0,
            target_temp_max=25.0,
            target_humidity_min=60.0,
            target_humidity_max=70.0,
            active=True
        )

        cycle_id = test_db.insert_growth_cycle(new_cycle)
        assert cycle_id > 0

        # Get current - should be flowering
        current = test_db.get_current_growth_cycle()
        assert current.phase == 'flowering'

        # Old cycle should be inactive
        cursor = test_db._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM growth_cycles WHERE active = 1")
        count = cursor.fetchone()[0]
        assert count == 1

    def test_update_growth_cycle(self, test_db):
        """Test updating growth cycle attributes."""
        current = test_db.get_current_growth_cycle()

        # Update cycle
        success = test_db.update_growth_cycle(
            current.id,
            target_temp_min=23.0,
            target_temp_max=26.0
        )

        assert success is True

        # Verify update
        updated = test_db.get_current_growth_cycle()
        assert updated.target_temp_min == 23.0
        assert updated.target_temp_max == 26.0


@pytest.mark.unit
class TestTargetParametersOperations:
    """Test target parameters CRUD operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_get_target_parameters(self, test_db):
        """Test retrieving target parameters."""
        temp_params = test_db.get_target_parameters('temperature')

        assert temp_params is not None
        assert temp_params.parameter_name == 'temperature'
        assert temp_params.min_value is not None
        assert temp_params.max_value is not None

    def test_get_all_target_parameters(self, test_db):
        """Test retrieving all target parameters."""
        all_params = test_db.get_all_target_parameters()

        assert len(all_params) == 3  # temperature, humidity, water_level
        assert all(isinstance(p, TargetParameters) for p in all_params)

    def test_update_target_parameters(self, test_db):
        """Test updating target parameters."""
        success = test_db.update_target_parameters(
            'temperature',
            min_value=20.0,
            max_value=26.0
        )

        assert success is True

        # Verify update
        updated = test_db.get_target_parameters('temperature')
        assert updated.min_value == 20.0
        assert updated.max_value == 26.0


@pytest.mark.unit
class TestSystemStatusOperations:
    """Test system status singleton operations."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_get_system_status(self, test_db):
        """Test retrieving system status."""
        status = test_db.get_system_status()

        assert status is not None
        assert status.id == 1
        assert status.connection_state in ['online', 'offline']

    def test_update_system_status(self, test_db):
        """Test updating system status."""
        now = datetime.utcnow()

        success = test_db.update_system_status(
            connection_state='online',
            last_mqtt_publish=now,
            auto_mode_enabled=True
        )

        assert success is True

        # Verify update
        status = test_db.get_system_status()
        assert status.connection_state == 'online'
        assert status.auto_mode_enabled is True

    def test_system_status_is_singleton(self, test_db):
        """Test that system status is singleton (only one row)."""
        cursor = test_db._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM system_status")
        count = cursor.fetchone()[0]

        assert count == 1


@pytest.mark.unit
class TestDatabaseIndexes:
    """Test database indexes for performance."""

    @pytest.fixture
    def test_db(self, tmp_path):
        """Create temporary test database."""
        db_path = tmp_path / "test.db"
        from src.storage.init_db import initialize_database
        initialize_database(db_path)

        db = DatabaseInterface(str(db_path))
        db.connect()
        yield db
        db.close()

    def test_sensor_readings_indexes_exist(self, test_db):
        """Test sensor_readings table has proper indexes."""
        cursor = test_db._connection.cursor()

        # Check for timestamp index
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_sensor_timestamp'
        """)
        assert cursor.fetchone() is not None

        # Check for composite index
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_sensor_type_timestamp'
        """)
        assert cursor.fetchone() is not None

    def test_device_states_indexes_exist(self, test_db):
        """Test device_states table has proper indexes."""
        cursor = test_db._connection.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_device_timestamp'
        """)
        assert cursor.fetchone() is not None

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_device_type_timestamp'
        """)
        assert cursor.fetchone() is not None


@pytest.mark.unit
class TestDataModelConversions:
    """Test data model to_dict and from_dict conversions."""

    def test_sensor_reading_to_dict(self):
        """Test sensor reading converts to dictionary."""
        reading = SensorReading(
            sensor_type='temperature',
            value=23.5,
            unit='celsius',
            status='valid',
            timestamp=datetime.utcnow()
        )

        data = reading.to_dict()

        assert data['sensor_type'] == 'temperature'
        assert data['value'] == 23.5
        assert data['unit'] == 'celsius'
        assert data['status'] == 'valid'

    def test_sensor_reading_from_dict(self):
        """Test sensor reading creates from dictionary."""
        data = {
            'sensor_type': 'humidity',
            'value': 65.0,
            'unit': 'percent',
            'status': 'valid',
            'timestamp': datetime.utcnow().isoformat()
        }

        reading = SensorReading.from_dict(data)

        assert reading.sensor_type == 'humidity'
        assert reading.value == 65.0

    def test_growth_cycle_days_in_phase(self):
        """Test growth cycle calculates days in phase correctly."""
        start_date = datetime.utcnow() - timedelta(days=10)

        cycle = GrowthCycle(
            phase='vegetative',
            start_date=start_date,
            light_schedule='18/6',
            target_temp_min=22.0,
            target_temp_max=25.0,
            target_humidity_min=60.0,
            target_humidity_max=70.0
        )

        assert cycle.days_in_phase == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "unit"])
