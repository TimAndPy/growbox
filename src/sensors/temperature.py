"""
Temperature sensor implementation using DHT22.
Reads temperature from Adafruit DHT sensor library.
"""

from typing import Optional
import logging

from .base import BaseSensor

logger = logging.getLogger(__name__)

try:
    import adafruit_dht
    import board
    DHT_AVAILABLE = True
except ImportError:
    DHT_AVAILABLE = False
    logger.warning("adafruit_dht library not available. Using mock sensor.")


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
        if DHT_AVAILABLE:
            # Map GPIO pin number to board pin
            pin_map = {4: board.D4, 17: board.D17, 18: board.D18, 27: board.D27}
            board_pin = pin_map.get(gpio_pin, board.D4)
            self.sensor = adafruit_dht.DHT22(board_pin, use_pulseio=False)
        else:
            self.sensor = None

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
            temperature = self.sensor.temperature

            if temperature is not None:
                logger.debug(f"Temperature read: {temperature}°C")
                return round(temperature, 1)
            else:
                logger.error("Failed to read temperature from DHT22")
                return None

        except RuntimeError as e:
            # DHT sensors often fail to read, retry on next cycle
            logger.debug(f"DHT read error (will retry): {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return None

    def cleanup(self):
        """Clean up DHT22 resources."""
        if self.sensor:
            self.sensor.exit()
        pass
