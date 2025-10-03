"""
Temperature sensor implementation using DHT22.
Reads temperature from Adafruit DHT sensor library.
"""

from typing import Optional
import logging

from .base import BaseSensor

logger = logging.getLogger(__name__)

try:
    import Adafruit_DHT
    DHT_AVAILABLE = True
except ImportError:
    DHT_AVAILABLE = False
    logger.warning("Adafruit_DHT library not available. Using mock sensor.")


class TemperatureSensor(BaseSensor):
    """Temperature sensor using DHT22."""

    def __init__(self, gpio_pin: int):
        """
        Initialize DHT22 temperature sensor.

        Args:
            gpio_pin: GPIO pin number where DHT22 is connected
        """
        super().__init__(sensor_type='temperature', unit='celsius')
        self.gpio_pin = gpio_pin
        self.sensor = Adafruit_DHT.DHT22 if DHT_AVAILABLE else None

    def read_raw(self) -> Optional[float]:
        """
        Read temperature from DHT22 sensor.

        Returns:
            Temperature in Celsius or None if read fails
        """
        if not DHT_AVAILABLE:
            logger.debug("Mock temperature read (DHT not available)")
            return 22.5

        try:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio_pin)

            if temperature is not None:
                logger.debug(f"Temperature read: {temperature}°C")
                return round(temperature, 1)
            else:
                logger.error("Failed to read temperature from DHT22")
                return None

        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return None

    def cleanup(self):
        """Clean up DHT22 resources."""
        # DHT22 doesn't require explicit cleanup
        pass
