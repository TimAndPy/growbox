"""
Heater controller using GPIO relay with cooldown.
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


class HeaterController(BaseDevice):
    """Controller for heater via relay with cooldown period."""

    def __init__(self, gpio_pin: int, active_high: bool = True, cooldown_seconds: int = 60):
        """
        Initialize heater controller.

        Args:
            gpio_pin: GPIO pin connected to relay
            active_high: True if relay is active high (default)
            cooldown_seconds: Cooldown period between activations (default 60s)
        """
        super().__init__(
            device_type='heater',
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
                logger.error(f"Failed to initialize heater GPIO: {e}")

    def turn_on_hardware(self) -> bool:
        """Turn on heater relay."""
        if not GPIO_AVAILABLE:
            logger.debug("Mock heater turned ON")
            return True

        try:
            state = GPIO.HIGH if self.active_high else GPIO.LOW
            GPIO.output(self.gpio_pin, state)
            return True
        except Exception as e:
            logger.error(f"Error turning on heater: {e}")
            return False

    def turn_off_hardware(self) -> bool:
        """Turn off heater relay."""
        if not GPIO_AVAILABLE:
            logger.debug("Mock heater turned OFF")
            return True

        try:
            state = GPIO.LOW if self.active_high else GPIO.HIGH
            GPIO.output(self.gpio_pin, state)
            return True
        except Exception as e:
            logger.error(f"Error turning off heater: {e}")
            return False

    def cleanup(self):
        """Clean up GPIO resources."""
        if GPIO_AVAILABLE:
            try:
                self.turn_off_hardware()
                GPIO.cleanup(self.gpio_pin)
            except Exception as e:
                logger.error(f"Error cleaning up heater: {e}")
