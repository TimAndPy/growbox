"""
Water level sensor implementation using HC-SR04 ultrasonic sensor.
Measures distance to water surface and converts to volume.
"""

from typing import Optional
import time
import logging

from .base import BaseSensor

logger = logging.getLogger(__name__)

try:
    import Jetson.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    logger.warning("Jetson.GPIO not available. Using mock sensor.")


class WaterLevelSensor(BaseSensor):
    """Water level sensor using HC-SR04 ultrasonic sensor."""

    def __init__(self, gpio_trigger_pin: int, gpio_echo_pin: int, tank_height_cm: float = 40.0):
        """
        Initialize HC-SR04 water level sensor.

        Args:
            gpio_trigger_pin: GPIO pin for trigger signal
            gpio_echo_pin: GPIO pin for echo signal
            tank_height_cm: Total tank height in centimeters
        """
        super().__init__(sensor_type='water', unit='liters')
        self.gpio_trigger_pin = gpio_trigger_pin
        self.gpio_echo_pin = gpio_echo_pin
        self.tank_height_cm = tank_height_cm

        # Assuming a cylindrical tank: 30cm diameter, calculate liters from height
        self.tank_diameter_cm = 30.0
        self.tank_area_cm2 = 3.14159 * (self.tank_diameter_cm / 2) ** 2

        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gpio_trigger_pin, GPIO.OUT)
                GPIO.setup(self.gpio_echo_pin, GPIO.IN)
                GPIO.output(self.gpio_trigger_pin, GPIO.LOW)
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed to initialize HC-SR04: {e}")

    def _measure_distance_cm(self) -> Optional[float]:
        """
        Measure distance to water surface in centimeters.

        Returns:
            Distance in cm or None if measurement fails
        """
        if not GPIO_AVAILABLE:
            return 15.0  # Mock distance

        try:
            # Send trigger pulse
            GPIO.output(self.gpio_trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.gpio_trigger_pin, GPIO.LOW)

            # Wait for echo
            timeout = time.time() + 0.1
            while GPIO.input(self.gpio_echo_pin) == GPIO.LOW:
                pulse_start = time.time()
                if time.time() > timeout:
                    return None

            timeout = time.time() + 0.1
            while GPIO.input(self.gpio_echo_pin) == GPIO.HIGH:
                pulse_end = time.time()
                if time.time() > timeout:
                    return None

            pulse_duration = pulse_end - pulse_start
            distance_cm = (pulse_duration * 34300) / 2

            return distance_cm

        except Exception as e:
            logger.error(f"Error measuring distance: {e}")
            return None

    def read_raw(self) -> Optional[float]:
        """
        Read water level and convert to liters.

        Returns:
            Water volume in liters or None if read fails
        """
        distance_cm = self._measure_distance_cm()

        if distance_cm is None:
            logger.error("Failed to measure water distance")
            return None

        # Calculate water height from distance to surface
        water_height_cm = self.tank_height_cm - distance_cm

        # Ensure valid range
        if water_height_cm < 0:
            water_height_cm = 0
        elif water_height_cm > self.tank_height_cm:
            water_height_cm = self.tank_height_cm

        # Convert to liters (1 liter = 1000 cm³)
        volume_liters = (self.tank_area_cm2 * water_height_cm) / 1000.0

        logger.debug(f"Water level: {volume_liters:.1f} liters (height: {water_height_cm:.1f} cm)")
        return round(volume_liters, 1)

    def cleanup(self):
        """Clean up GPIO resources."""
        if GPIO_AVAILABLE:
            try:
                GPIO.cleanup([self.gpio_trigger_pin, self.gpio_echo_pin])
            except Exception as e:
                logger.error(f"Error cleaning up water sensor: {e}")
