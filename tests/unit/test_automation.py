"""
Unit tests for automation controller logic.
Tests hysteresis calculations, threshold comparisons, and cooldown periods.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta

from src.automation.controller import AutomationController
from src.automation.watchdog import CommunicationWatchdog
from src.automation.scheduler import GrowthPhaseScheduler
from src.storage.models import (
    SensorReading,
    TargetParameters,
    GrowthCycle,
    DeviceControl
)


@pytest.mark.unit
class TestAutomationController:
    """Test automation controller logic."""

    @pytest.fixture
    def mock_database(self):
        """Create mock database."""
        db = MagicMock()
        db.get_target_parameters = Mock()
        db.insert_device_state = Mock()
        db.update_system_status = Mock()
        return db

    @pytest.fixture
    def mock_devices(self):
        """Create mock devices."""
        devices = {}
        for device_type in ['lights', 'ventilation', 'pump', 'heater', 'co2']:
            device = MagicMock()
            device.get_state = Mock(return_value='off')
            device.turn_on = Mock(return_value=True)
            device.turn_off = Mock(return_value=True)
            device.get_cooldown_remaining = Mock(return_value=0.0)
            devices[device_type] = device
        return devices

    @pytest.fixture
    def controller(self, mock_database, mock_devices):
        """Create automation controller."""
        return AutomationController(mock_database, mock_devices)

    def test_automation_disabled_by_default(self, controller):
        """Test automation is disabled by default."""
        assert controller.is_enabled() is False

    def test_enable_automation(self, controller):
        """Test enabling automation."""
        controller.enable()
        assert controller.is_enabled() is True

    def test_disable_automation(self, controller):
        """Test disabling automation."""
        controller.enable()
        controller.disable()
        assert controller.is_enabled() is False

    def test_disabled_automation_ignores_readings(self, controller, mock_devices):
        """Test disabled automation does not process readings."""
        reading = SensorReading(
            sensor_type='temperature',
            value=15.0,
            unit='celsius',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        # No device should have been controlled
        mock_devices['heater'].turn_on.assert_not_called()

    def test_invalid_sensor_status_ignored(self, controller, mock_database):
        """Test readings with error status are ignored."""
        controller.enable()

        reading = SensorReading(
            sensor_type='temperature',
            value=15.0,
            unit='celsius',
            status='error'
        )

        controller.process_sensor_reading(reading)

        # Should not query target parameters
        mock_database.get_target_parameters.assert_not_called()


@pytest.mark.unit
class TestTemperatureControl:
    """Test temperature-based automation."""

    @pytest.fixture
    def controller_with_targets(self):
        """Create controller with temperature targets."""
        db = MagicMock()

        # Mock target parameters
        temp_target = TargetParameters(
            parameter_name='temperature',
            min_value=22.0,
            max_value=25.0,
            hysteresis=0.5,
            warning_threshold=1.0,
            unit='celsius'
        )
        db.get_target_parameters = Mock(return_value=temp_target)
        db.insert_device_state = Mock()

        # Mock devices
        devices = {
            'heater': MagicMock(get_state=Mock(return_value='off'),
                               turn_on=Mock(return_value=True),
                               turn_off=Mock(return_value=True)),
            'ventilation': MagicMock(get_state=Mock(return_value='off'),
                                    turn_on=Mock(return_value=True),
                                    turn_off=Mock(return_value=True))
        }

        controller = AutomationController(db, devices)
        controller.enable()

        return controller, db, devices

    def test_low_temperature_activates_heater(self, controller_with_targets):
        """Test heater activates when temperature is below minimum."""
        controller, db, devices = controller_with_targets

        reading = SensorReading(
            sensor_type='temperature',
            value=20.0,
            unit='celsius',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        # Heater should be turned on
        devices['heater'].turn_on.assert_called_once()

    def test_high_temperature_activates_ventilation(self, controller_with_targets):
        """Test ventilation activates when temperature is above maximum."""
        controller, db, devices = controller_with_targets

        reading = SensorReading(
            sensor_type='temperature',
            value=26.0,
            unit='celsius',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        # Ventilation should be turned on
        devices['ventilation'].turn_on.assert_called_once()

    def test_temperature_hysteresis_prevents_rapid_cycling(self, controller_with_targets):
        """Test hysteresis prevents rapid on/off cycling."""
        controller, db, devices = controller_with_targets

        # Simulate heater is on and heating
        devices['heater'].get_state = Mock(return_value='on')
        controller._device_heating_mode['heater'] = True

        # Temperature just reached minimum (22.0)
        reading = SensorReading(
            sensor_type='temperature',
            value=22.0,
            unit='celsius',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        # Heater should NOT turn off yet (hysteresis = 0.5)
        devices['heater'].turn_off.assert_not_called()

        # Temperature reaches minimum + hysteresis (22.5)
        reading2 = SensorReading(
            sensor_type='temperature',
            value=22.5,
            unit='celsius',
            status='valid'
        )

        controller.process_sensor_reading(reading2)

        # NOW heater should turn off
        devices['heater'].turn_off.assert_called_once()


@pytest.mark.unit
class TestHumidityControl:
    """Test humidity-based automation."""

    @pytest.fixture
    def controller_with_targets(self):
        """Create controller with humidity targets."""
        db = MagicMock()

        humidity_target = TargetParameters(
            parameter_name='humidity',
            min_value=60.0,
            max_value=70.0,
            hysteresis=3.0,
            warning_threshold=5.0,
            unit='percent'
        )
        db.get_target_parameters = Mock(return_value=humidity_target)
        db.insert_device_state = Mock()
        db.get_latest_sensor_value = Mock(return_value=None)

        devices = {
            'ventilation': MagicMock(get_state=Mock(return_value='off'),
                                    turn_on=Mock(return_value=True),
                                    turn_off=Mock(return_value=True))
        }

        controller = AutomationController(db, devices)
        controller.enable()

        return controller, db, devices

    def test_high_humidity_activates_ventilation(self, controller_with_targets):
        """Test ventilation activates when humidity is too high."""
        controller, db, devices = controller_with_targets

        reading = SensorReading(
            sensor_type='humidity',
            value=75.0,
            unit='percent',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        devices['ventilation'].turn_on.assert_called_once()


@pytest.mark.unit
class TestWaterLevelControl:
    """Test water level-based automation."""

    @pytest.fixture
    def controller_with_targets(self):
        """Create controller with water level targets."""
        db = MagicMock()

        water_target = TargetParameters(
            parameter_name='water',
            min_value=30.0,
            max_value=100.0,
            hysteresis=2.0,
            warning_threshold=5.0,
            unit='liters'
        )
        db.get_target_parameters = Mock(return_value=water_target)
        db.insert_device_state = Mock()

        devices = {
            'pump': MagicMock(get_state=Mock(return_value='off'),
                             turn_on=Mock(return_value=True),
                             turn_off=Mock(return_value=True),
                             get_cooldown_remaining=Mock(return_value=0.0))
        }

        controller = AutomationController(db, devices)
        controller.enable()

        return controller, db, devices

    def test_low_water_level_activates_pump(self, controller_with_targets):
        """Test pump activates when water level is below minimum."""
        controller, db, devices = controller_with_targets

        reading = SensorReading(
            sensor_type='water',
            value=25.0,
            unit='liters',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        devices['pump'].turn_on.assert_called_once()

    def test_pump_cooldown_prevents_activation(self, controller_with_targets):
        """Test pump respects cooldown period."""
        controller, db, devices = controller_with_targets

        # Pump is in cooldown
        devices['pump'].get_cooldown_remaining = Mock(return_value=30.0)

        reading = SensorReading(
            sensor_type='water',
            value=25.0,
            unit='liters',
            status='valid'
        )

        controller.process_sensor_reading(reading)

        # Pump should NOT turn on during cooldown
        devices['pump'].turn_on.assert_not_called()


@pytest.mark.unit
class TestCommunicationWatchdog:
    """Test communication watchdog failsafe."""

    @pytest.fixture
    def mock_devices(self):
        """Create mock devices."""
        devices = {}
        for device_type in ['lights', 'ventilation', 'pump', 'heater', 'co2']:
            device = MagicMock()
            device.get_state = Mock(return_value='on')
            device.turn_off = Mock(return_value=True)
            devices[device_type] = device
        return devices

    def test_watchdog_initialization(self, mock_devices):
        """Test watchdog initializes with correct timeout."""
        watchdog = CommunicationWatchdog(mock_devices, timeout_seconds=30)

        assert watchdog.timeout_seconds == 30
        assert watchdog._failsafe_triggered is False

    def test_watchdog_reset(self, mock_devices):
        """Test watchdog timer can be reset."""
        watchdog = CommunicationWatchdog(mock_devices, timeout_seconds=30)

        initial_time = watchdog._last_heartbeat
        watchdog.reset()
        reset_time = watchdog._last_heartbeat

        assert reset_time > initial_time

    def test_failsafe_not_active_initially(self, mock_devices):
        """Test failsafe is not active initially."""
        watchdog = CommunicationWatchdog(mock_devices, timeout_seconds=30)

        assert watchdog.is_failsafe_active() is False

    def test_clear_failsafe(self, mock_devices):
        """Test failsafe can be cleared."""
        watchdog = CommunicationWatchdog(mock_devices, timeout_seconds=30)

        watchdog._failsafe_triggered = True
        watchdog.clear_failsafe()

        assert watchdog.is_failsafe_active() is False


@pytest.mark.unit
class TestGrowthPhaseScheduler:
    """Test growth phase scheduler."""

    @pytest.fixture
    def mock_database(self):
        """Create mock database."""
        db = MagicMock()

        cycle = GrowthCycle(
            phase='vegetative',
            start_date=datetime.utcnow(),
            light_schedule='18/6',
            target_temp_min=22.0,
            target_temp_max=25.0,
            target_humidity_min=60.0,
            target_humidity_max=70.0,
            active=True
        )
        db.get_current_growth_cycle = Mock(return_value=cycle)
        db.insert_growth_cycle = Mock()

        return db

    @pytest.fixture
    def mock_lights(self):
        """Create mock lights controller."""
        lights = MagicMock()
        lights.get_state = Mock(return_value='off')
        lights.turn_on = Mock(return_value=True)
        lights.turn_off = Mock(return_value=True)
        return lights

    def test_scheduler_loads_current_phase(self, mock_database, mock_lights):
        """Test scheduler loads current growth phase."""
        scheduler = GrowthPhaseScheduler(mock_database, mock_lights)
        scheduler.load_current_phase()

        assert scheduler._current_phase == 'vegetative'
        assert scheduler._light_on_hours == 18

    def test_switch_to_flowering_phase(self, mock_database, mock_lights):
        """Test switching to flowering phase."""
        scheduler = GrowthPhaseScheduler(mock_database, mock_lights)

        success = scheduler.switch_phase('flowering')

        assert success is True
        mock_database.insert_growth_cycle.assert_called_once()

    def test_invalid_phase_rejected(self, mock_database, mock_lights):
        """Test invalid phase is rejected."""
        scheduler = GrowthPhaseScheduler(mock_database, mock_lights)

        success = scheduler.switch_phase('invalid_phase')

        assert success is False

    def test_vegetative_light_schedule(self, mock_database, mock_lights):
        """Test vegetative phase uses 18/6 light schedule."""
        scheduler = GrowthPhaseScheduler(mock_database, mock_lights)
        scheduler.load_current_phase()

        assert scheduler._light_on_hours == 18

    def test_flowering_light_schedule(self, mock_database, mock_lights):
        """Test flowering phase uses 12/12 light schedule."""
        # Mock flowering cycle
        cycle = GrowthCycle(
            phase='flowering',
            start_date=datetime.utcnow(),
            light_schedule='12/12',
            target_temp_min=22.0,
            target_temp_max=25.0,
            target_humidity_min=60.0,
            target_humidity_max=70.0,
            active=True
        )
        mock_database.get_current_growth_cycle = Mock(return_value=cycle)

        scheduler = GrowthPhaseScheduler(mock_database, mock_lights)
        scheduler.load_current_phase()

        assert scheduler._light_on_hours == 12


@pytest.mark.unit
class TestMaxRuntimeEnforcement:
    """Test device max runtime enforcement."""

    def test_check_device_max_runtime(self):
        """Test automation checks and enforces max runtime."""
        db = MagicMock()
        db.insert_device_state = Mock()

        # Create device that has exceeded max runtime
        device = MagicMock()
        device.has_exceeded_max_runtime = Mock(return_value=True)
        device.turn_off = Mock(return_value=True)

        devices = {'pump': device}

        controller = AutomationController(db, devices)
        controller.check_device_max_runtime()

        # Device should be turned off
        device.turn_off.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "unit"])
