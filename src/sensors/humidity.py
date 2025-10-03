"""
Humidity sensor implementation using DHT22.
Reads humidity from Adafruit DHT sensor library.
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


class HumiditySensor(BaseSensor):
    """Humidity sensor using DHT22."""

    def __init__(self, gpio_pin: int):
        """
        Initialize DHT22 humidity sensor.

        Args:
            gpio_pin: GPIO pin number where DHT22 is connected
        """
        super().__init__(sensor_type='humidity', unit='percent')
        self.gpio_pin = gpio_pin
        self.sensor = Adafruit_DHT.DHT22 if DHT_AVAILABLE else None

    def read_raw(self) -> Optional[float]:
        """
        Read humidity from DHT22 sensor.

        Returns:
            Relative humidity percentage or None if read fails
        """
        if not DHT_AVAILABLE:
            logger.debug("Mock humidity read (DHT not available)")
            return 65.0

        try:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio_pin)

            if humidity is not None:
                logger.debug(f"Humidity read: {humidity}%")
                return round(humidity, 1)
            else:
                logger.error("Failed to read humidity from DHT22")
                return None

        except Exception as e:
            logger.error(f"Error reading humidity: {e}")
            return None

    def cleanup(self):
        """Clean up DHT22 resources."""
        # DHT22 doesn't require explicit cleanup
        pass
