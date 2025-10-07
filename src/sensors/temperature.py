"""
Temperature sensor implementation using DHT11/DHT22.
Reads temperature from Jetson-specific C_DHT library.
"""

from typing import Optional
import logging

from .base import BaseSensor

logger = logging.getLogger(__name__)

try:
    import C_DHT
    DHT_AVAILABLE = True
except ImportError:
    DHT_AVAILABLE = False
    logger.warning("C_DHT library not available. Using mock sensor.")


class TemperatureSensor(BaseSensor):
    """Temperature sensor using DHT11."""

    def __init__(self, gpio_pin: int):
        """
        Initialize DHT11 temperature sensor using Jetson C_DHT library.

        Args:
            gpio_pin: GPIO pin number (must match PIN0 definition in C_DHT.c)
        """
        super().__init__(sensor_type='temperature', unit='celsius')
        self.gpio_pin = gpio_pin
        # C_DHT library uses hardcoded pins - PIN0 is set to Nano pin 12
        # We use sensor index 0 which corresponds to PIN0
        self.sensor_index = 0

    def read_raw(self) -> Optional[float]:
        """
        Read temperature from DHT11 sensor using C_DHT library.

        Returns:
            Temperature in Celsius or None if read fails
        """
        if not DHT_AVAILABLE:
            logger.debug("Mock temperature read (C_DHT not available)")
            return 22.5

        try:
            # C_DHT.readSensorDHT11 returns (temperature, humidity) tuple
            result = C_DHT.readSensorDHT11(self.sensor_index)

            if result and len(result) >= 2:
                temperature = result[0]
                if temperature is not None and temperature != 0.0:
                    logger.debug(f"Temperature read: {temperature}°C")
                    return round(temperature, 1)
                else:
                    logger.debug("DHT11 read returned 0 or None")
                    return None
            else:
                logger.error("Failed to read from DHT11 sensor")
                return None

        except Exception as e:
            logger.error(f"Error reading temperature from DHT11: {e}")
            return None

    def cleanup(self):
        """Clean up DHT11 resources."""
        # C_DHT library doesn't require explicit cleanup
        pass
