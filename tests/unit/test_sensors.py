"""
Unit tests for sensor modules.
Tests sensor reading logic, error handling, and state management.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.sensors.base import BaseSensor
from src.sensors.temperature import TemperatureSensor
from src.sensors.humidity import HumiditySensor
from src.sensors.light import LightSensor
from src.sensors.water import WaterLevelSensor
from src.storage.models import SensorReading


@pytest.mark.unit
class TestBaseSensor:
    """Test base sensor interface."""

    def test_sensor_initialization(self):
        """Test sensor is initialized with correct type and unit."""
        # Create a concrete implementation for testing
        class TestSensor(BaseSensor):
            def read_raw(self):
                return 25.0
            def cleanup(self):
                pass

        sensor = TestSensor('temperature', 'celsius')
        assert sensor.sensor_type == 'temperature'
        assert sensor.unit == 'celsius'
        assert sensor._last_reading is None

    def test_successful_read_returns_valid_reading(self):
        """Test successful sensor read returns valid reading."""
        class TestSensor(BaseSensor):
            def read_raw(self):
                return 25.0
            def cleanup(self):
                pass

        sensor = TestSensor('temperature', 'celsius')
        reading = sensor.read()

        assert reading.sensor_type == 'temperature'
        assert reading.value == 25.0
        assert reading.unit == 'celsius'
        assert reading.status == 'valid'
        assert reading.timestamp is not None

    def test_failed_read_returns_error_status(self):
        """Test failed sensor read returns error status."""
        class TestSensor(BaseSensor):
            def read_raw(self):
                return None
            def cleanup(self):
                pass

        sensor = TestSensor('temperature', 'celsius')
        reading = sensor.read()

        assert reading.status == 'error'
        assert reading.value == 0.0

    def test_stale_reading_detection(self):
        """Test sensor can detect stale readings."""
        class TestSensor(BaseSensor):
            def read_raw(self):
                return 25.0
            def cleanup(self):
                pass

        sensor = TestSensor('temperature', 'celsius')

        # Fresh reading
        assert sensor.is_stale(max_age_seconds=60) is True  # No reading yet

        # Read sensor
        sensor.read()
        assert sensor.is_stale(max_age_seconds=60) is False

        # Simulate old reading
        sensor._last_read_time = datetime.utcnow() - timedelta(seconds=61)
        assert sensor.is_stale(max_age_seconds=60) is True


@pytest.mark.unit
class TestTemperatureSensor:
    """Test DHT22 temperature sensor."""

    @patch('src.sensors.temperature.Adafruit_DHT')
    def test_temperature_read_success(self, mock_dht):
        """Test successful temperature reading from DHT22."""
        mock_dht.read_retry.return_value = (65.0, 22.5)  # humidity, temperature

        sensor = TemperatureSensor(gpio_pin=4)
        reading = sensor.read()

        assert reading.sensor_type == 'temperature'
        assert reading.value == 22.5
        assert reading.unit == 'celsius'
        assert reading.status == 'valid'

    @patch('src.sensors.temperature.Adafruit_DHT')
    def test_temperature_read_failure(self, mock_dht):
        """Test temperature read failure handling."""
        mock_dht.read_retry.return_value = (None, None)

        sensor = TemperatureSensor(gpio_pin=4)
        reading = sensor.read()

        assert reading.status == 'error'

    def test_temperature_mock_mode(self):
        """Test temperature sensor works in mock mode."""
        sensor = TemperatureSensor(gpio_pin=4)
        reading = sensor.read()

        # Mock mode should return default value
        assert reading.value == 22.5
        assert reading.status == 'valid'


@pytest.mark.unit
class TestHumiditySensor:
    """Test DHT22 humidity sensor."""

    @patch('src.sensors.humidity.Adafruit_DHT')
    def test_humidity_read_success(self, mock_dht):
        """Test successful humidity reading from DHT22."""
        mock_dht.read_retry.return_value = (65.0, 22.5)

        sensor = HumiditySensor(gpio_pin=4)
        reading = sensor.read()

        assert reading.sensor_type == 'humidity'
        assert reading.value == 65.0
        assert reading.unit == 'percent'
        assert reading.status == 'valid'

    def test_humidity_mock_mode(self):
        """Test humidity sensor works in mock mode."""
        sensor = HumiditySensor(gpio_pin=4)
        reading = sensor.read()

        assert reading.value == 65.0
        assert reading.status == 'valid'


@pytest.mark.unit
class TestLightSensor:
    """Test BH1750 light sensor."""

    @patch('src.sensors.light.smbus2.SMBus')
    def test_light_read_success(self, mock_smbus):
        """Test successful light reading from BH1750."""
        mock_bus = MagicMock()
        mock_bus.read_i2c_block_data.return_value = [0x01, 0x2C]  # 300 lux * 1.2
        mock_smbus.return_value = mock_bus

        sensor = LightSensor(i2c_bus=1, i2c_address=0x23)
        sensor.bus = mock_bus

        reading = sensor.read()

        assert reading.sensor_type == 'light'
        assert reading.unit == 'lux'
        assert reading.status == 'valid'

    def test_light_mock_mode(self):
        """Test light sensor works in mock mode."""
        sensor = LightSensor(i2c_bus=1, i2c_address=0x23)
        reading = sensor.read()

        assert reading.value == 15000.0
        assert reading.status == 'valid'


@pytest.mark.unit
class TestWaterLevelSensor:
    """Test HC-SR04 water level sensor."""

    @patch('src.sensors.water.GPIO')
    def test_water_level_calculation(self, mock_gpio):
        """Test water level calculation from distance."""
        sensor = WaterLevelSensor(
            gpio_trigger_pin=23,
            gpio_echo_pin=24,
            tank_height_cm=40.0
        )

        # Mock distance measurement (15cm from sensor to water)
        sensor._measure_distance_cm = Mock(return_value=15.0)

        reading = sensor.read()

        # Water height = 40 - 15 = 25 cm
        # Volume should be calculated based on tank area
        assert reading.sensor_type == 'water'
        assert reading.unit == 'liters'
        assert reading.value > 0
        assert reading.status == 'valid'

    def test_water_level_mock_mode(self):
        """Test water level sensor works in mock mode."""
        sensor = WaterLevelSensor(
            gpio_trigger_pin=23,
            gpio_echo_pin=24
        )

        reading = sensor.read()

        # Mock mode should return calculated value
        assert reading.status == 'valid'
        assert reading.value > 0


@pytest.mark.unit
class TestSensorErrorHandling:
    """Test sensor error handling and recovery."""

    def test_exception_in_read_returns_error(self):
        """Test exception during read returns error status."""
        class FailingSensor(BaseSensor):
            def read_raw(self):
                raise Exception("Sensor hardware failure")
            def cleanup(self):
                pass

        sensor = FailingSensor('test', 'unit')
        reading = sensor.read()

        assert reading.status == 'error'

    def test_last_reading_preserved_on_error(self):
        """Test last valid reading is preserved when error occurs."""
        class TogglingSensor(BaseSensor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.should_fail = False

            def read_raw(self):
                if self.should_fail:
                    return None
                return 25.0

            def cleanup(self):
                pass

        sensor = TogglingSensor('test', 'unit')

        # First read succeeds
        reading1 = sensor.read()
        assert reading1.status == 'valid'
        assert reading1.value == 25.0

        # Second read fails
        sensor.should_fail = True
        reading2 = sensor.read()
        assert reading2.status == 'error'
        assert reading2.value == 25.0  # Should use last valid value


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "unit"])
