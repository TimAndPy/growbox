"""
Base sensor interface for GrowBox sensors.
Defines contract for all sensor implementations.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from storage.models import SensorReading


class BaseSensor(ABC):
    """Abstract base class for all sensor implementations."""

    def __init__(self, sensor_type: str, unit: str):
        """
        Initialize base sensor.

        Args:
            sensor_type: Type of sensor (temperature, humidity, light, water)
            unit: Measurement unit
        """
        self.sensor_type = sensor_type
        self.unit = unit
        self._last_reading: Optional[SensorReading] = None
        self._last_read_time: Optional[datetime] = None

    @abstractmethod
    def read_raw(self) -> Optional[float]:
        """
        Read raw value from sensor hardware.

        Returns:
            Raw sensor value or None if read fails
        """
        pass

    def read(self) -> SensorReading:
        """
        Read sensor and return structured reading.

        Returns:
            SensorReading object with value and status
        """
        try:
            value = self.read_raw()
            timestamp = datetime.utcnow()

            if value is None:
                status = 'error'
                value = self._last_reading.value if self._last_reading else 0.0
            else:
                status = 'valid'

            reading = SensorReading(
                sensor_type=self.sensor_type,
                value=value,
                unit=self.unit,
                status=status,
                timestamp=timestamp
            )

            self._last_reading = reading
            self._last_read_time = timestamp

            return reading

        except Exception as e:
            # Return error reading with previous value or 0
            return SensorReading(
                sensor_type=self.sensor_type,
                value=self._last_reading.value if self._last_reading else 0.0,
                unit=self.unit,
                status='error',
                timestamp=datetime.utcnow()
            )

    def get_last_reading(self) -> Optional[SensorReading]:
        """Get the last successful reading."""
        return self._last_reading

    def is_stale(self, max_age_seconds: int = 60) -> bool:
        """
        Check if last reading is stale.

        Args:
            max_age_seconds: Maximum age in seconds before reading is stale

        Returns:
            True if reading is older than max_age_seconds
        """
        if not self._last_read_time:
            return True

        age = (datetime.utcnow() - self._last_read_time).total_seconds()
        return age > max_age_seconds

    @abstractmethod
    def cleanup(self):
        """Clean up sensor resources (GPIO, I2C, etc.)."""
        pass
