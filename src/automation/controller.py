"""
Automation controller for environmental control.
Implements threshold-based device control with hysteresis.
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from storage.database import DatabaseInterface
from storage.models import SensorReading, DeviceControl, TargetParameters
from devices.base import BaseDevice

logger = logging.getLogger(__name__)


class AutomationController:
    """Automated environmental control with hysteresis."""

    def __init__(self, database: DatabaseInterface, devices: Dict[str, BaseDevice]):
        """
        Initialize automation controller.

        Args:
            database: Database interface
            devices: Dictionary of device controllers {device_type: controller}
        """
        self.database = database
        self.devices = devices
        self.enabled = False

        # Track device states for hysteresis logic
        self._device_heating_mode: Dict[str, bool] = {}

    def enable(self):
        """Enable automation mode."""
        self.enabled = True
        logger.info("Automation enabled")

        # Update system status
        self.database.update_system_status(auto_mode_enabled=True)

    def disable(self):
        """Disable automation mode."""
        self.enabled = False
        logger.info("Automation disabled")

        # Update system status
        self.database.update_system_status(auto_mode_enabled=False)

    def is_enabled(self) -> bool:
        """Check if automation is enabled."""
        return self.enabled

    def process_sensor_reading(self, reading: SensorReading):
        """
        Process sensor reading and adjust devices if needed.

        Args:
            reading: Latest sensor reading
        """
        if not self.enabled:
            return

        if reading.status != 'valid':
            logger.warning(f"Skipping automation: sensor {reading.sensor_type} status is {reading.status}")
            return

        # Get target parameters for this sensor type
        target = self.database.get_target_parameters(reading.sensor_type)
        if not target:
            logger.debug(f"No target parameters for {reading.sensor_type}")
            return

        # Apply control logic based on sensor type
        if reading.sensor_type == 'temperature':
            self._control_temperature(reading.value, target)
        elif reading.sensor_type == 'humidity':
            self._control_humidity(reading.value, target)
        elif reading.sensor_type == 'water':
            self._control_water_level(reading.value, target)

    def _control_temperature(self, current_temp: float, target: TargetParameters):
        """
        Control heater and ventilation based on temperature.

        Args:
            current_temp: Current temperature reading
            target: Target temperature parameters
        """
        heater = self.devices.get('heater')
        ventilation = self.devices.get('ventilation')

        if not heater or not ventilation:
            return

        # Check if heater is currently active (heating mode)
        heating_mode = self._device_heating_mode.get('heater', False)

        # Temperature too low - activate heater
        if current_temp < target.min_value:
            if heater.get_state() == 'off':
                logger.info(f"Temperature {current_temp}°C below target {target.min_value}°C - activating heater")
                if heater.turn_on():
                    self._log_device_action('heater', 'on', 'auto', f"temp_below_{target.min_value}")
                    self._device_heating_mode['heater'] = True

            # Turn off ventilation if active
            if ventilation.get_state() == 'on':
                ventilation.turn_off()
                self._log_device_action('ventilation', 'off', 'auto', 'heater_active')

        # Temperature in range with hysteresis
        elif target.min_value <= current_temp <= target.max_value:
            # If heater is on and we've passed hysteresis threshold, turn off
            if heating_mode and current_temp >= (target.min_value + target.hysteresis):
                logger.info(f"Temperature {current_temp}°C reached target - deactivating heater")
                heater.turn_off()
                self._log_device_action('heater', 'off', 'auto', f"temp_reached_{target.min_value + target.hysteresis}")
                self._device_heating_mode['heater'] = False

        # Temperature too high - activate ventilation
        elif current_temp > target.max_value:
            if ventilation.get_state() == 'off':
                logger.info(f"Temperature {current_temp}°C above target {target.max_value}°C - activating ventilation")
                if ventilation.turn_on():
                    self._log_device_action('ventilation', 'on', 'auto', f"temp_above_{target.max_value}")

            # Turn off heater if active
            if heater.get_state() == 'on':
                heater.turn_off()
                self._log_device_action('heater', 'off', 'auto', 'temp_too_high')
                self._device_heating_mode['heater'] = False

    def _control_humidity(self, current_humidity: float, target: TargetParameters):
        """
        Control ventilation based on humidity.

        Args:
            current_humidity: Current humidity reading
            target: Target humidity parameters
        """
        ventilation = self.devices.get('ventilation')

        if not ventilation:
            return

        # Humidity too high - activate ventilation
        if current_humidity > target.max_value:
            if ventilation.get_state() == 'off':
                logger.info(f"Humidity {current_humidity}% above target {target.max_value}% - activating ventilation")
                if ventilation.turn_on():
                    self._log_device_action('ventilation', 'on', 'auto', f"humidity_above_{target.max_value}")

        # Humidity in acceptable range - consider turning off ventilation
        elif target.min_value <= current_humidity <= (target.max_value - target.hysteresis):
            if ventilation.get_state() == 'on':
                # Only turn off if not needed for temperature
                temp_reading = self.database.get_latest_sensor_value('temperature')
                temp_target = self.database.get_target_parameters('temperature')

                if temp_reading and temp_target:
                    if temp_reading.value <= temp_target.max_value:
                        logger.info(f"Humidity {current_humidity}% in range - deactivating ventilation")
                        ventilation.turn_off()
                        self._log_device_action('ventilation', 'off', 'auto', 'humidity_in_range')

    def _control_water_level(self, current_level: float, target: TargetParameters):
        """
        Control water pump based on water level.

        Args:
            current_level: Current water level reading
            target: Target water level parameters
        """
        pump = self.devices.get('pump')

        if not pump:
            return

        # Water level too low - activate pump
        if current_level < target.min_value:
            if pump.get_state() == 'off' and pump.get_cooldown_remaining() == 0:
                logger.info(f"Water level {current_level}L below target {target.min_value}L - activating pump")
                if pump.turn_on():
                    self._log_device_action('pump', 'on', 'auto', f"water_below_{target.min_value}")

        # Water level acceptable - turn off pump
        elif current_level >= (target.min_value + target.hysteresis):
            if pump.get_state() == 'on':
                logger.info(f"Water level {current_level}L reached target - deactivating pump")
                pump.turn_off()
                self._log_device_action('pump', 'off', 'auto', f"water_reached_{target.min_value + target.hysteresis}")

    def check_device_max_runtime(self):
        """Check and enforce max runtime limits for all devices."""
        for device_type, device in self.devices.items():
            if device.has_exceeded_max_runtime():
                logger.warning(f"{device_type} exceeded max runtime - forcing OFF")
                device.turn_off()
                self._log_device_action(device_type, 'off', 'auto', 'max_runtime_exceeded')

    def _log_device_action(self, device_type: str, state: str, command_source: str, triggered_by: str):
        """
        Log device action to database.

        Args:
            device_type: Device type
            state: New state (on/off)
            command_source: Command source
            triggered_by: Reason for action
        """
        control = DeviceControl(
            device_type=device_type,
            state=state,
            command_source=command_source,
            triggered_by=triggered_by,
            timestamp=datetime.utcnow()
        )

        try:
            self.database.insert_device_state(control)
        except Exception as e:
            logger.error(f"Failed to log device action: {e}")
