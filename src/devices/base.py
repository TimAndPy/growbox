"""
Base device controller for GrowBox devices.
Defines contract for all device implementations.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Literal
import logging

logger = logging.getLogger(__name__)


class BaseDevice(ABC):
    """Abstract base class for all device controllers."""

    def __init__(self, device_type: str, max_runtime_seconds: Optional[int] = None,
                 cooldown_seconds: Optional[int] = None):
        """
        Initialize base device controller.

        Args:
            device_type: Type of device (lights, ventilation, pump, heater, co2)
            max_runtime_seconds: Maximum continuous runtime (None = unlimited)
            cooldown_seconds: Required cooldown period between activations
        """
        self.device_type = device_type
        self.max_runtime_seconds = max_runtime_seconds
        self.cooldown_seconds = cooldown_seconds

        self._current_state: Literal['on', 'off'] = 'off'
        self._last_state_change: Optional[datetime] = None
        self._last_turn_off: Optional[datetime] = None

    @abstractmethod
    def turn_on_hardware(self) -> bool:
        """
        Turn on the physical device.

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def turn_off_hardware(self) -> bool:
        """
        Turn off the physical device.

        Returns:
            True if successful, False otherwise
        """
        pass

    def turn_on(self) -> bool:
        """
        Turn on device with safety checks.

        Returns:
            True if device turned on successfully
        """
        if self._current_state == 'on':
            logger.debug(f"{self.device_type} already on")
            return True

        if not self._can_turn_on():
            logger.warning(f"{self.device_type} cannot turn on: cooldown active")
            return False

        if self.turn_on_hardware():
            self._current_state = 'on'
            self._last_state_change = datetime.utcnow()
            logger.info(f"{self.device_type} turned ON")
            return True

        logger.error(f"Failed to turn on {self.device_type}")
        return False

    def turn_off(self) -> bool:
        """
        Turn off device.

        Returns:
            True if device turned off successfully
        """
        if self._current_state == 'off':
            logger.debug(f"{self.device_type} already off")
            return True

        if self.turn_off_hardware():
            self._current_state = 'off'
            self._last_state_change = datetime.utcnow()
            self._last_turn_off = datetime.utcnow()
            logger.info(f"{self.device_type} turned OFF")
            return True

        logger.error(f"Failed to turn off {self.device_type}")
        return False

    def get_state(self) -> Literal['on', 'off']:
        """Get current device state."""
        return self._current_state

    def _can_turn_on(self) -> bool:
        """
        Check if device can be turned on (cooldown check).

        Returns:
            True if device can be turned on
        """
        if self.cooldown_seconds is None:
            return True

        if self._last_turn_off is None:
            return True

        elapsed = (datetime.utcnow() - self._last_turn_off).total_seconds()
        return elapsed >= self.cooldown_seconds

    def get_cooldown_remaining(self) -> float:
        """
        Get remaining cooldown time in seconds.

        Returns:
            Seconds remaining in cooldown, or 0 if no cooldown
        """
        if self.cooldown_seconds is None or self._last_turn_off is None:
            return 0.0

        elapsed = (datetime.utcnow() - self._last_turn_off).total_seconds()
        remaining = self.cooldown_seconds - elapsed

        return max(0.0, remaining)

    def has_exceeded_max_runtime(self) -> bool:
        """
        Check if device has exceeded maximum runtime.

        Returns:
            True if device should be turned off due to max runtime
        """
        if self.max_runtime_seconds is None:
            return False

        if self._current_state != 'on' or self._last_state_change is None:
            return False

        runtime = (datetime.utcnow() - self._last_state_change).total_seconds()
        return runtime >= self.max_runtime_seconds

    def get_runtime_seconds(self) -> float:
        """
        Get current runtime in seconds (if device is on).

        Returns:
            Runtime in seconds, or 0 if device is off
        """
        if self._current_state != 'on' or self._last_state_change is None:
            return 0.0

        return (datetime.utcnow() - self._last_state_change).total_seconds()

    @abstractmethod
    def cleanup(self):
        """Clean up device resources (GPIO, etc.)."""
        pass
