"""
Unit tests for device controller modules.
Tests device control logic, state management, and safety features.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.devices.base import BaseDevice
from src.devices.lights import LightsController
from src.devices.ventilation import VentilationController
from src.devices.pump import PumpController
from src.devices.heater import HeaterController
from src.devices.co2 import CO2Controller


@pytest.mark.unit
class TestBaseDevice:
    """Test base device controller."""

    def test_device_initialization(self):
        """Test device initializes with correct type and default state."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test', max_runtime_seconds=300, cooldown_seconds=60)

        assert device.device_type == 'test'
        assert device.get_state() == 'off'
        assert device.max_runtime_seconds == 300
        assert device.cooldown_seconds == 60

    def test_successful_turn_on(self):
        """Test device can be turned on successfully."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test')
        assert device.turn_on() is True
        assert device.get_state() == 'on'

    def test_successful_turn_off(self):
        """Test device can be turned off successfully."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test')
        device.turn_on()
        assert device.turn_off() is True
        assert device.get_state() == 'off'

    def test_cooldown_prevents_immediate_restart(self):
        """Test cooldown period prevents device from turning on immediately."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test', cooldown_seconds=60)

        # Turn on and off
        device.turn_on()
        device.turn_off()

        # Try to turn on again immediately - should fail
        assert device.turn_on() is False
        assert device.get_state() == 'off'

    def test_cooldown_remaining_calculation(self):
        """Test cooldown remaining time is calculated correctly."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test', cooldown_seconds=60)

        # No cooldown initially
        assert device.get_cooldown_remaining() == 0.0

        # Turn on and off
        device.turn_on()
        device.turn_off()

        # Should have cooldown remaining
        remaining = device.get_cooldown_remaining()
        assert 0 < remaining <= 60

    def test_max_runtime_detection(self):
        """Test device detects when max runtime is exceeded."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test', max_runtime_seconds=10)
        device.turn_on()

        # Simulate time passing
        device._last_state_change = datetime.utcnow() - timedelta(seconds=11)

        assert device.has_exceeded_max_runtime() is True

    def test_runtime_calculation(self):
        """Test device runtime is calculated correctly."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test')

        # Device off - runtime should be 0
        assert device.get_runtime_seconds() == 0.0

        # Turn on device
        device.turn_on()
        assert device.get_runtime_seconds() >= 0.0


@pytest.mark.unit
class TestLightsController:
    """Test lights controller."""

    @patch('src.devices.lights.GPIO')
    def test_lights_turn_on(self, mock_gpio):
        """Test lights can be turned on."""
        controller = LightsController(gpio_pin=17, active_high=True)

        assert controller.turn_on() is True
        assert controller.get_state() == 'on'
        mock_gpio.output.assert_called()

    @patch('src.devices.lights.GPIO')
    def test_lights_turn_off(self, mock_gpio):
        """Test lights can be turned off."""
        controller = LightsController(gpio_pin=17, active_high=True)
        controller.turn_on()

        assert controller.turn_off() is True
        assert controller.get_state() == 'off'

    def test_lights_mock_mode(self):
        """Test lights controller works in mock mode."""
        controller = LightsController(gpio_pin=17, active_high=True)

        assert controller.turn_on() is True
        assert controller.turn_off() is True


@pytest.mark.unit
class TestVentilationController:
    """Test ventilation controller."""

    @patch('src.devices.ventilation.GPIO')
    def test_ventilation_control(self, mock_gpio):
        """Test ventilation can be controlled."""
        controller = VentilationController(gpio_pin=27, active_high=True)

        assert controller.turn_on() is True
        assert controller.get_state() == 'on'
        assert controller.turn_off() is True
        assert controller.get_state() == 'off'


@pytest.mark.unit
class TestPumpController:
    """Test water pump controller with safety limits."""

    @patch('src.devices.pump.GPIO')
    def test_pump_has_max_runtime(self, mock_gpio):
        """Test pump has maximum runtime limit."""
        controller = PumpController(
            gpio_pin=22,
            max_runtime_seconds=300,
            cooldown_seconds=60
        )

        assert controller.max_runtime_seconds == 300
        assert controller.cooldown_seconds == 60

    @patch('src.devices.pump.GPIO')
    def test_pump_cooldown_enforced(self, mock_gpio):
        """Test pump cooldown is enforced."""
        controller = PumpController(
            gpio_pin=22,
            max_runtime_seconds=300,
            cooldown_seconds=60
        )

        # Run and stop pump
        controller.turn_on()
        controller.turn_off()

        # Try to restart immediately
        assert controller.turn_on() is False

    def test_pump_mock_mode(self):
        """Test pump works in mock mode."""
        controller = PumpController(gpio_pin=22)

        assert controller.turn_on() is True
        assert controller.turn_off() is True


@pytest.mark.unit
class TestHeaterController:
    """Test heater controller with cooldown."""

    @patch('src.devices.heater.GPIO')
    def test_heater_has_cooldown(self, mock_gpio):
        """Test heater has cooldown period."""
        controller = HeaterController(
            gpio_pin=10,
            cooldown_seconds=60
        )

        assert controller.cooldown_seconds == 60

    def test_heater_mock_mode(self):
        """Test heater works in mock mode."""
        controller = HeaterController(gpio_pin=10)

        assert controller.turn_on() is True
        assert controller.turn_off() is True


@pytest.mark.unit
class TestCO2Controller:
    """Test CO2 dispenser controller with safety limits."""

    @patch('src.devices.co2.GPIO')
    def test_co2_has_safety_limits(self, mock_gpio):
        """Test CO2 controller has max runtime and cooldown."""
        controller = CO2Controller(
            gpio_pin=9,
            max_runtime_seconds=180,
            cooldown_seconds=300
        )

        assert controller.max_runtime_seconds == 180
        assert controller.cooldown_seconds == 300

    def test_co2_mock_mode(self):
        """Test CO2 controller works in mock mode."""
        controller = CO2Controller(gpio_pin=9)

        assert controller.turn_on() is True
        assert controller.turn_off() is True


@pytest.mark.unit
class TestDeviceCleanup:
    """Test device cleanup on shutdown."""

    def test_cleanup_turns_off_device(self):
        """Test cleanup ensures device is turned off."""
        class TestDevice(BaseDevice):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cleaned = False

            def turn_on_hardware(self):
                return True

            def turn_off_hardware(self):
                return True

            def cleanup(self):
                self.cleaned = True

        device = TestDevice('test')
        device.turn_on()
        device.cleanup()

        assert device.cleaned is True

    @patch('src.devices.lights.GPIO')
    def test_lights_cleanup_releases_gpio(self, mock_gpio):
        """Test lights cleanup releases GPIO resources."""
        controller = LightsController(gpio_pin=17)
        controller.turn_on()
        controller.cleanup()

        # Should have called cleanup
        assert controller.get_state() == 'off'


@pytest.mark.unit
class TestDeviceStateTransitions:
    """Test device state transitions and edge cases."""

    def test_turn_on_when_already_on(self):
        """Test turning on device that is already on."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test')
        device.turn_on()

        # Turn on again
        assert device.turn_on() is True
        assert device.get_state() == 'on'

    def test_turn_off_when_already_off(self):
        """Test turning off device that is already off."""
        class TestDevice(BaseDevice):
            def turn_on_hardware(self):
                return True
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = TestDevice('test')

        # Turn off when already off
        assert device.turn_off() is True
        assert device.get_state() == 'off'

    def test_hardware_failure_handling(self):
        """Test device handles hardware failures gracefully."""
        class FailingDevice(BaseDevice):
            def turn_on_hardware(self):
                return False  # Simulate hardware failure
            def turn_off_hardware(self):
                return True
            def cleanup(self):
                pass

        device = FailingDevice('test')

        # Attempt to turn on should fail
        assert device.turn_on() is False
        assert device.get_state() == 'off'


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "unit"])
