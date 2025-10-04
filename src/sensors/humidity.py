"""
Humidity sensor implementation using DHT22.
Reads humidity from Adafruit DHT sensor library.
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
        if DHT_AVAILABLE:
            # Map GPIO pin number to board pin
            pin_map = {4: board.D4, 17: board.D17, 18: board.D18, 27: board.D27}
            board_pin = pin_map.get(gpio_pin, board.D4)
            self.sensor = adafruit_dht.DHT22(board_pin, use_pulseio=False)
        else:
            self.sensor = None

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
            humidity = self.sensor.humidity

            if humidity is not None:
                logger.debug(f"Humidity read: {humidity}%")
                return round(humidity, 1)
            else:
                logger.error("Failed to read humidity from DHT22")
                return None

        except RuntimeError as e:
            # DHT sensors often fail to read, retry on next cycle
            logger.debug(f"DHT read error (will retry): {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading humidity: {e}")
            return None

    def cleanup(self):
        """Clean up DHT22 resources."""
        if self.sensor:
            self.sensor.exit()
        pass
