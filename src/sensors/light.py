"""
Light sensor implementation using BH1750.
Reads light intensity via I2C bus.
"""

from typing import Optional
import logging

from .base import BaseSensor

logger = logging.getLogger(__name__)

try:
    import smbus2
    SMBUS_AVAILABLE = True
except ImportError:
    SMBUS_AVAILABLE = False
    logger.warning("smbus2 library not available. Using mock sensor.")


class LightSensor(BaseSensor):
    """Light sensor using BH1750."""

    # BH1750 constants
    POWER_DOWN = 0x00
    POWER_ON = 0x01
    RESET = 0x07
    CONTINUOUS_HIGH_RES_MODE = 0x10

    def __init__(self, i2c_bus: int = 1, i2c_address: int = 0x23):
        """
        Initialize BH1750 light sensor.

        Args:
            i2c_bus: I2C bus number (default 1 for Jetson Nano)
            i2c_address: I2C address of BH1750 (default 0x23)
        """
        super().__init__(sensor_type='light', unit='lux')
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.bus = None

        if SMBUS_AVAILABLE:
            try:
                self.bus = smbus2.SMBus(i2c_bus)
                self._initialize_sensor()
            except Exception as e:
                logger.error(f"Failed to initialize BH1750: {e}")
                self.bus = None

    def _initialize_sensor(self):
        """Initialize BH1750 sensor."""
        if self.bus:
            self.bus.write_byte(self.i2c_address, self.POWER_ON)
            self.bus.write_byte(self.i2c_address, self.CONTINUOUS_HIGH_RES_MODE)

    def read_raw(self) -> Optional[float]:
        """
        Read light intensity from BH1750.

        Returns:
            Light intensity in lux or None if read fails
        """
        if not SMBUS_AVAILABLE or not self.bus:
            logger.debug("Mock light read (smbus2 not available)")
            return 15000.0

        try:
            data = self.bus.read_i2c_block_data(self.i2c_address, self.CONTINUOUS_HIGH_RES_MODE, 2)
            lux = ((data[0] << 8) | data[1]) / 1.2

            logger.debug(f"Light read: {lux} lux")
            return round(lux, 1)

        except Exception as e:
            logger.error(f"Error reading light sensor: {e}")
            return None

    def cleanup(self):
        """Clean up I2C bus resources."""
        if self.bus:
            try:
                self.bus.write_byte(self.i2c_address, self.POWER_DOWN)
                self.bus.close()
            except Exception as e:
                logger.error(f"Error cleaning up light sensor: {e}")
