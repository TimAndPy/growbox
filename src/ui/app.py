"""
Flask web application for GrowBox tablet UI.
Provides real-time monitoring and control interface.
"""

import logging
import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security configuration
app.config['SECRET_KEY'] = os.environ.get('GROWBOX_SECRET_KEY', 'growbox_secret_key_change_in_production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB max request size

# CORS configuration for local network access
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Global references (set by main app)
_database = None
_devices = None
_automation = None
_scheduler = None


def init_app(database, devices, automation, scheduler):
    """
    Initialize Flask app with GrowBox components.

    Args:
        database: DatabaseInterface instance
        devices: Dictionary of device controllers
        automation: AutomationController instance
        scheduler: GrowthPhaseScheduler instance
    """
    global _database, _devices, _automation, _scheduler
    _database = database
    _devices = devices
    _automation = automation
    _scheduler = scheduler

    logger.info("Flask app initialized")


# Web Routes

@app.route('/')
def index():
    """Render main control panel."""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get current system status."""
    try:
        status = _database.get_system_status()
        cycle = _database.get_current_growth_cycle()

        response = {
            'connection_state': status.connection_state,
            'auto_mode_enabled': status.auto_mode_enabled,
            'active_alerts': status.active_alerts,
            'growth_phase': cycle.phase if cycle else None,
            'days_in_phase': cycle.days_in_phase if cycle else 0,
            'light_schedule': cycle.light_schedule if cycle else None
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors')
def get_sensors():
    """Get latest sensor readings."""
    try:
        sensors = {}

        for sensor_type in ['temperature', 'humidity', 'light', 'water']:
            reading = _database.get_latest_sensor_value(sensor_type)
            if reading:
                sensors[sensor_type] = {
                    'value': reading.value,
                    'unit': reading.unit,
                    'status': reading.status,
                    'timestamp': reading.timestamp.isoformat()
                }

        return jsonify(sensors)

    except Exception as e:
        logger.error(f"Error getting sensors: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices')
def get_devices():
    """Get current device states."""
    try:
        devices = {}

        for device_type in ['lights', 'ventilation', 'pump', 'heater', 'co2']:
            if device_type in _devices:
                device = _devices[device_type]
                devices[device_type] = {
                    'state': device.get_state(),
                    'runtime_seconds': device.get_runtime_seconds(),
                    'cooldown_remaining': device.get_cooldown_remaining()
                }

        return jsonify(devices)

    except Exception as e:
        logger.error(f"Error getting devices: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/device/<device_type>/<command>', methods=['POST'])
def control_device(device_type, command):
    """
    Control a device (turn on/off).

    Args:
        device_type: Device name (lights, ventilation, pump, heater, co2)
        command: Command (on/off)
    """
    try:
        if device_type not in _devices:
            return jsonify({'error': f'Unknown device: {device_type}'}), 400

        if command not in ['on', 'off']:
            return jsonify({'error': f'Invalid command: {command}'}), 400

        device = _devices[device_type]

        if command == 'on':
            success = device.turn_on()
        else:
            success = device.turn_off()

        if success:
            # Log to database
            from storage.models import DeviceControl
            from datetime import datetime

            control = DeviceControl(
                device_type=device_type,
                state=command,
                command_source='local',
                triggered_by='tablet_ui',
                timestamp=datetime.utcnow()
            )
            _database.insert_device_state(control)

            # Emit update via WebSocket
            socketio.emit('device_update', {
                'device_type': device_type,
                'state': command
            })

            return jsonify({'success': True, 'state': command})
        else:
            return jsonify({'error': 'Failed to control device'}), 500

    except Exception as e:
        logger.error(f"Error controlling device: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/auto_mode/<action>', methods=['POST'])
def set_auto_mode(action):
    """
    Enable or disable automation mode.

    Args:
        action: Action (enable/disable)
    """
    try:
        if action == 'enable':
            _automation.enable()
            return jsonify({'success': True, 'auto_mode_enabled': True})
        elif action == 'disable':
            _automation.disable()
            return jsonify({'success': True, 'auto_mode_enabled': False})
        else:
            return jsonify({'error': f'Invalid action: {action}'}), 400

    except Exception as e:
        logger.error(f"Error setting auto mode: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/growth_phase/<phase>', methods=['POST'])
def set_growth_phase(phase):
    """
    Switch growth phase.

    Args:
        phase: New phase (vegetative/flowering)
    """
    try:
        if phase not in ['vegetative', 'flowering']:
            return jsonify({'error': f'Invalid phase: {phase}'}), 400

        success = _scheduler.switch_phase(phase)

        if success:
            # Emit update via WebSocket
            socketio.emit('phase_update', {'phase': phase})
            return jsonify({'success': True, 'phase': phase})
        else:
            return jsonify({'error': 'Failed to switch phase'}), 500

    except Exception as e:
        logger.error(f"Error switching phase: {e}")
        return jsonify({'error': str(e)}), 500


# WebSocket Events

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    logger.info("Client connected via WebSocket")
    emit('connected', {'message': 'Connected to GrowBox'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    logger.info("Client disconnected from WebSocket")


def broadcast_sensor_update(sensor_type, reading):
    """
    Broadcast sensor update to all connected clients.

    Args:
        sensor_type: Sensor type
        reading: SensorReading instance
    """
    socketio.emit('sensor_update', {
        'sensor_type': sensor_type,
        'value': reading.value,
        'unit': reading.unit,
        'status': reading.status,
        'timestamp': reading.timestamp.isoformat()
    })


def broadcast_device_update(device_type, state):
    """
    Broadcast device state update to all connected clients.

    Args:
        device_type: Device type
        state: New state (on/off)
    """
    socketio.emit('device_update', {
        'device_type': device_type,
        'state': state
    })


def run_app(host='0.0.0.0', port=5000):
    """
    Run Flask app.

    Args:
        host: Host address (default 0.0.0.0 for all interfaces)
        port: Port number (default 5000)
    """
    logger.info(f"Starting Flask app on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=False)
