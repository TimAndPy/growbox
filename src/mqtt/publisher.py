"""
MQTT publisher for sensor readings and device states.
Publishes sensor data and device state changes to MQTT topics.
"""

import logging
from datetime import datetime
from typing import Optional

from .client import MQTTClient
from storage.models import SensorReading, DeviceControl, SystemStatus, GrowthCycle

logger = logging.getLogger(__name__)


class MQTTPublisher:
    """Publisher for GrowBox sensor readings and device states."""

    def __init__(self, mqtt_client: MQTTClient):
        """
        Initialize MQTT publisher.

        Args:
            mqtt_client: Configured MQTT client instance
        """
        self.client = mqtt_client

    def publish_sensor_reading(self, reading: SensorReading) -> bool:
        """
        Publish sensor reading to MQTT.

        Args:
            reading: SensorReading instance

        Returns:
            True if published successfully
        """
        topic = self.client.get_topic('sensors', sensor=reading.sensor_type)

        payload = reading.to_dict()

        qos = self.client.config.get('qos_sensor_data', 1)
        return self.client.publish(topic, payload, qos=qos)

    def publish_device_state(self, control: DeviceControl) -> bool:
        """
        Publish device state change to MQTT.

        Args:
            control: DeviceControl instance

        Returns:
            True if published successfully
        """
        topic = self.client.get_topic('device_state', device=control.device_type)

        payload = control.to_dict()

        qos = self.client.config.get('qos_device_commands', 2)
        return self.client.publish(topic, payload, qos=qos, retain=True)

    def publish_system_status(self, status: SystemStatus, growth_cycle: Optional[GrowthCycle] = None) -> bool:
        """
        Publish system status to MQTT.

        Args:
            status: SystemStatus instance
            growth_cycle: Optional current growth cycle

        Returns:
            True if published successfully
        """
        topic = self.client.get_topic('system_status')

        payload = status.to_dict()

        # Add growth cycle info if provided
        if growth_cycle:
            payload['growth_phase'] = growth_cycle.phase
            payload['days_in_phase'] = growth_cycle.days_in_phase
            payload['light_schedule'] = growth_cycle.light_schedule

        return self.client.publish(topic, payload, qos=1, retain=True)

    def publish_heartbeat(self) -> bool:
        """
        Publish heartbeat to indicate system is alive.

        Returns:
            True if published successfully
        """
        topic = self.client.get_topic('system_status')

        payload = {
            'connection_state': 'online',
            'last_mqtt_publish': datetime.utcnow().isoformat(),
            'heartbeat': True
        }

        return self.client.publish(topic, payload, qos=1)
