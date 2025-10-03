"""
MQTT subscriber for device commands.
Handles incoming MQTT commands and routes them to device controllers.
"""

import logging
from typing import Dict, Callable

from .client import MQTTClient

logger = logging.getLogger(__name__)


class MQTTSubscriber:
    """Subscriber for device commands from MQTT."""

    def __init__(self, mqtt_client: MQTTClient):
        """
        Initialize MQTT subscriber.

        Args:
            mqtt_client: Configured MQTT client instance
        """
        self.client = mqtt_client
        self._device_handlers: Dict[str, Callable] = {}

    def register_device_handler(self, device_type: str, handler: Callable[[str, str], None]):
        """
        Register handler for device commands.

        Args:
            device_type: Device type (lights, ventilation, pump, heater, co2)
            handler: Callback function (device_type, command) -> None
        """
        self._device_handlers[device_type] = handler

        # Subscribe to command topic
        topic = self.client.get_topic('device_command', device=device_type)
        self.client.subscribe(topic, self._handle_device_command)

        logger.info(f"Registered handler for device: {device_type}")

    def _handle_device_command(self, topic: str, payload: dict):
        """
        Handle incoming device command.

        Args:
            topic: MQTT topic
            payload: Command payload
        """
        try:
            device_type = payload.get('device_type')
            command = payload.get('command')

            if not device_type or not command:
                logger.error(f"Invalid command payload: {payload}")
                return

            if device_type not in self._device_handlers:
                logger.error(f"No handler registered for device: {device_type}")
                return

            logger.info(f"Received command for {device_type}: {command}")
            self._device_handlers[device_type](device_type, command)

        except Exception as e:
            logger.error(f"Error handling device command: {e}")

    def subscribe_to_all_devices(self):
        """Subscribe to commands for all registered devices."""
        for device_type in self._device_handlers.keys():
            topic = self.client.get_topic('device_command', device=device_type)
            self.client.subscribe(topic, self._handle_device_command)
            logger.info(f"Subscribed to commands for: {device_type}")

    def unregister_device_handler(self, device_type: str):
        """
        Unregister handler for device.

        Args:
            device_type: Device type to unregister
        """
        if device_type in self._device_handlers:
            del self._device_handlers[device_type]

            topic = self.client.get_topic('device_command', device=device_type)
            self.client.unsubscribe(topic)

            logger.info(f"Unregistered handler for device: {device_type}")
