"""
Growth phase scheduler for light schedule management.
Handles light timing based on growth phase (vegetative/flowering).
"""

import logging
from datetime import datetime, time as dt_time
from typing import Optional

from storage.database import DatabaseInterface
from storage.models import GrowthCycle, DeviceControl
from devices.base import BaseDevice

logger = logging.getLogger(__name__)


class GrowthPhaseScheduler:
    """Scheduler for growth phase light timing."""

    def __init__(self, database: DatabaseInterface, lights: BaseDevice):
        """
        Initialize growth phase scheduler.

        Args:
            database: Database interface
            lights: Lights device controller
        """
        self.database = database
        self.lights = lights
        self._current_phase: Optional[str] = None
        self._light_on_hour: int = 6
        self._light_on_hours: int = 18

    def load_current_phase(self):
        """Load current growth phase from database."""
        cycle = self.database.get_current_growth_cycle()

        if cycle:
            self._current_phase = cycle.phase
            self._update_light_schedule(cycle)
            logger.info(f"Loaded growth phase: {cycle.phase} ({cycle.light_schedule})")
        else:
            logger.warning("No active growth cycle found")

    def _update_light_schedule(self, cycle: GrowthCycle):
        """
        Update light schedule based on growth cycle.

        Args:
            cycle: Current growth cycle
        """
        if cycle.phase == 'vegetative':
            self._light_on_hours = 18
        elif cycle.phase == 'flowering':
            self._light_on_hours = 12
        else:
            logger.warning(f"Unknown growth phase: {cycle.phase}")

        logger.info(f"Light schedule: {self._light_on_hours} hours ON, {24 - self._light_on_hours} hours OFF")

    def switch_phase(self, new_phase: str, start_date: datetime = None) -> bool:
        """
        Switch to a new growth phase.

        Args:
            new_phase: New phase (vegetative or flowering)
            start_date: Start date for new phase (default: now)

        Returns:
            True if phase switch successful
        """
        if new_phase not in ['vegetative', 'flowering']:
            logger.error(f"Invalid phase: {new_phase}")
            return False

        start_date = start_date or datetime.utcnow()

        # Get default targets from config
        if new_phase == 'vegetative':
            light_schedule = '18/6'
            light_hours = 18
        else:
            light_schedule = '12/12'
            light_hours = 12

        # Create new growth cycle
        new_cycle = GrowthCycle(
            phase=new_phase,
            start_date=start_date,
            light_schedule=light_schedule,
            target_temp_min=22.0,
            target_temp_max=25.0,
            target_humidity_min=60.0,
            target_humidity_max=70.0,
            active=True
        )

        try:
            self.database.insert_growth_cycle(new_cycle)
            self._current_phase = new_phase
            self._light_on_hours = light_hours

            logger.info(f"Switched to {new_phase} phase with {light_schedule} light schedule")
            return True

        except Exception as e:
            logger.error(f"Failed to switch growth phase: {e}")
            return False

    def check_light_schedule(self):
        """Check and enforce light schedule based on current time and phase."""
        if not self._current_phase:
            logger.debug("No active growth phase - skipping light schedule check")
            return

        current_hour = datetime.now().hour

        # Calculate when lights should be on
        light_off_hour = (self._light_on_hour + self._light_on_hours) % 24

        # Determine if lights should be on
        if self._light_on_hour < light_off_hour:
            # Normal case: e.g., ON from 6:00 to 24:00 (18 hours)
            should_be_on = self._light_on_hour <= current_hour < light_off_hour
        else:
            # Wraparound case: e.g., ON from 18:00 to 6:00 (12 hours)
            should_be_on = current_hour >= self._light_on_hour or current_hour < light_off_hour

        # Apply schedule
        current_state = self.lights.get_state()

        if should_be_on and current_state == 'off':
            logger.info(f"Light schedule: turning ON (hour {current_hour})")
            if self.lights.turn_on():
                self._log_light_action('on', 'schedule')

        elif not should_be_on and current_state == 'on':
            logger.info(f"Light schedule: turning OFF (hour {current_hour})")
            if self.lights.turn_off():
                self._log_light_action('off', 'schedule')

    def set_light_on_time(self, hour: int):
        """
        Set the hour when lights should turn on.

        Args:
            hour: Hour (0-23) when lights should turn on
        """
        if not 0 <= hour <= 23:
            logger.error(f"Invalid hour: {hour}")
            return

        self._light_on_hour = hour
        logger.info(f"Light on time set to {hour}:00")

    def get_current_phase(self) -> Optional[str]:
        """Get current growth phase."""
        return self._current_phase

    def _log_light_action(self, state: str, triggered_by: str):
        """
        Log light schedule action to database.

        Args:
            state: Light state (on/off)
            triggered_by: Reason for action
        """
        control = DeviceControl(
            device_type='lights',
            state=state,
            command_source='auto',
            triggered_by=triggered_by,
            timestamp=datetime.utcnow()
        )

        try:
            self.database.insert_device_state(control)
        except Exception as e:
            logger.error(f"Failed to log light action: {e}")
