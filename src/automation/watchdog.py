"""
Communication watchdog for failsafe operation.
Monitors MQTT connectivity and triggers failsafe if connection lost.
"""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Callable

from devices.base import BaseDevice

logger = logging.getLogger(__name__)


class CommunicationWatchdog:
    """Watchdog that monitors MQTT connectivity and triggers failsafe."""

    def __init__(self, devices: Dict[str, BaseDevice], timeout_seconds: int = 30):
        """
        Initialize communication watchdog.

        Args:
            devices: Dictionary of device controllers
            timeout_seconds: Timeout before triggering failsafe (default 30s)
        """
        self.devices = devices
        self.timeout_seconds = timeout_seconds

        self._running = False
        self._thread: threading.Thread = None
        self._last_heartbeat: datetime = datetime.utcnow()
        self._failsafe_triggered = False

        self._on_failsafe_callback: Callable = None

    def start(self):
        """Start watchdog monitoring thread."""
        if self._running:
            logger.warning("Watchdog already running")
            return

        self._running = True
        self._failsafe_triggered = False
        self.reset()

        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

        logger.info(f"Watchdog started with {self.timeout_seconds}s timeout")

    def stop(self):
        """Stop watchdog monitoring."""
        self._running = False

        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

        logger.info("Watchdog stopped")

    def reset(self):
        """Reset watchdog timer (call on successful MQTT activity)."""
        self._last_heartbeat = datetime.utcnow()
        logger.debug("Watchdog timer reset")

    def set_failsafe_callback(self, callback: Callable):
        """
        Set callback function to execute on failsafe trigger.

        Args:
            callback: Function to call when failsafe triggers
        """
        self._on_failsafe_callback = callback

    def _monitor_loop(self):
        """Main monitoring loop (runs in separate thread)."""
        while self._running:
            elapsed = (datetime.utcnow() - self._last_heartbeat).total_seconds()

            if elapsed >= self.timeout_seconds and not self._failsafe_triggered:
                logger.critical(f"Communication lost for {elapsed:.1f}s - TRIGGERING FAILSAFE")
                self._trigger_failsafe()

            time.sleep(1.0)

    def _trigger_failsafe(self):
        """Execute failsafe procedure: turn OFF all devices."""
        self._failsafe_triggered = True

        logger.critical("FAILSAFE ACTIVATED - Turning OFF all devices")

        # Turn off all devices
        for device_type, device in self.devices.items():
            try:
                if device.get_state() == 'on':
                    device.turn_off()
                    logger.info(f"Failsafe: {device_type} turned OFF")
            except Exception as e:
                logger.error(f"Failsafe: Failed to turn off {device_type}: {e}")

        # Execute callback if registered
        if self._on_failsafe_callback:
            try:
                self._on_failsafe_callback()
            except Exception as e:
                logger.error(f"Failsafe callback error: {e}")

    def is_failsafe_active(self) -> bool:
        """Check if failsafe has been triggered."""
        return self._failsafe_triggered

    def clear_failsafe(self):
        """Clear failsafe state (after connection restored)."""
        if self._failsafe_triggered:
            logger.info("Clearing failsafe state")
            self._failsafe_triggered = False
            self.reset()
