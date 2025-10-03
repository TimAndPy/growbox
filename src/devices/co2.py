"""
CO2 dispenser controller using GPIO relay with safety limits.
"""

import logging
from .base import BaseDevice

logger = logging.getLogger(__name__)

try:
    import Jetson.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    logger.warning("Jetson.GPIO not available. Using mock device.")


class CO2Controller(BaseDevice):
    """Controller for CO2 dispenser via relay with max runtime and cooldown."""

    def __init__(self, gpio_pin: int, active_high: bool = True,
                 max_runtime_seconds: int = 180, cooldown_seconds: int = 300):
        """
        Initialize CO2 controller.

        Args:
            gpio_pin: GPIO pin connected to relay
            active_high: True if relay is active high (default)
            max_runtime_seconds: Maximum continuous runtime (default 180s = 3min)
            cooldown_seconds: Cooldown period between runs (default 300s = 5min)
        """
        super().__init__(
            device_type='co2',
            max_runtime_seconds=max_runtime_seconds,
            cooldown_seconds=cooldown_seconds
        )
        self.gpio_pin = gpio_pin
        self.active_high = active_high

        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gpio_pin, GPIO.OUT)
                self.turn_off_hardware()
            except Exception as e:
                logger.error(f"Failed to initialize CO2 GPIO: {e}")

    def turn_on_hardware(self) -> bool:
        """Turn on CO2 relay."""
        if not GPIO_AVAILABLE:
            logger.debug("Mock CO2 turned ON")
            return True

        try:
            state = GPIO.HIGH if self.active_high else GPIO.LOW
            GPIO.output(self.gpio_pin, state)
            return True
        except Exception as e:
            logger.error(f"Error turning on CO2: {e}")
            return False

    def turn_off_hardware(self) -> bool:
        """Turn off CO2 relay."""
        if not GPIO_AVAILABLE:
            logger.debug("Mock CO2 turned OFF")
            return True

        try:
            state = GPIO.LOW if self.active_high else GPIO.HIGH
            GPIO.output(self.gpio_pin, state)
            return True
        except Exception as e:
            logger.error(f"Error turning off CO2: {e}")
            return False

    def cleanup(self):
        """Clean up GPIO resources."""
        if GPIO_AVAILABLE:
            try:
                self.turn_off_hardware()
                GPIO.cleanup(self.gpio_pin)
            except Exception as e:
                logger.error(f"Error cleaning up CO2: {e}")
