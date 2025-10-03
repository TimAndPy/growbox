/**
 * GrowBox Control Panel JavaScript
 * Handles WebSocket communication and UI updates
 */

// Global socket connection
let socket;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initWebSocket();
    loadInitialData();
    startPeriodicUpdates();
});

/**
 * Initialize WebSocket connection
 */
function initWebSocket() {
    socket = io();

    socket.on('connect', function() {
        console.log('WebSocket connected');
        updateConnectionStatus(true);
    });

    socket.on('disconnect', function() {
        console.log('WebSocket disconnected');
        updateConnectionStatus(false);
    });

    socket.on('sensor_update', function(data) {
        updateSensor(data.sensor_type, data.value, data.unit, data.status);
    });

    socket.on('device_update', function(data) {
        updateDeviceState(data.device_type, data.state);
    });

    socket.on('phase_update', function(data) {
        loadStatus();
    });
}

/**
 * Update connection status indicator
 */
function updateConnectionStatus(isConnected) {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');

    if (isConnected) {
        statusDot.classList.add('online');
        statusText.textContent = 'Online';
    } else {
        statusDot.classList.remove('online');
        statusText.textContent = 'Offline';
    }
}

/**
 * Load initial data from API
 */
function loadInitialData() {
    loadStatus();
    loadSensors();
    loadDevices();
}

/**
 * Start periodic data refresh
 */
function startPeriodicUpdates() {
    // Refresh sensors every 5 seconds
    setInterval(loadSensors, 5000);

    // Refresh devices every 2 seconds
    setInterval(loadDevices, 2000);

    // Refresh status every 10 seconds
    setInterval(loadStatus, 10000);
}

/**
 * Load system status
 */
function loadStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // Update growth phase highlight
            const phase = data.growth_phase ? capitalizeFirst(data.growth_phase) : 'Unknown';
            const daysInPhase = data.days_in_phase || 0;
            document.getElementById('phaseHighlight').textContent = `${phase} - Day ${daysInPhase}`;

            // Update phase toggle checked state
            const phaseToggle = document.getElementById('phaseToggle');
            if (phaseToggle) {
                phaseToggle.checked = (data.growth_phase === 'flowering');
            }

            document.getElementById('autoModeToggle').checked = data.auto_mode_enabled;

            updateAlerts(data.active_alerts || []);

            // Update last sync time
            const now = new Date();
            document.getElementById('lastSyncTime').textContent = now.toLocaleTimeString();
        })
        .catch(error => console.error('Error loading status:', error));
}

/**
 * Load sensor readings
 */
function loadSensors() {
    fetch('/api/sensors')
        .then(response => response.json())
        .then(data => {
            for (const [sensorType, reading] of Object.entries(data)) {
                updateSensor(sensorType, reading.value, reading.unit, reading.status);
            }
        })
        .catch(error => console.error('Error loading sensors:', error));
}

/**
 * Load device states
 */
function loadDevices() {
    fetch('/api/devices')
        .then(response => response.json())
        .then(data => {
            for (const [deviceType, device] of Object.entries(data)) {
                updateDeviceState(deviceType, device.state);
            }
        })
        .catch(error => console.error('Error loading devices:', error));
}

/**
 * Target ranges for sensors
 */
const SENSOR_TARGETS = {
    'temperature': { min: 22, max: 25, unit: '°C' },
    'humidity': { min: 60, max: 70, unit: '%' },
    'light': { min: 400, max: 600, unit: ' μmol' },
    'water': { min: 30, max: 100, unit: ' L' }
};

/**
 * Update progress bar
 */
function updateProgressBar(sensorType, value) {
    const target = SENSOR_TARGETS[sensorType];
    if (!target) return;

    const progressBarId = sensorType + 'ProgressBar';
    const progressBar = document.getElementById(progressBarId);

    if (progressBar) {
        // Calculate percentage within range
        const range = target.max - target.min;
        let percentage = ((value - target.min) / range) * 100;

        // Clamp between 0 and 100
        percentage = Math.max(0, Math.min(100, percentage));

        progressBar.style.width = percentage + '%';

        // Add out-of-range class if needed
        if (value < target.min || value > target.max) {
            progressBar.classList.add('out-of-range');
        } else {
            progressBar.classList.remove('out-of-range');
        }
    }
}

/**
 * Update sensor display
 */
function updateSensor(sensorType, value, unit, status) {
    const valueId = sensorType + 'Value';
    const statusId = sensorType + 'Status';

    const valueElement = document.getElementById(valueId);
    const statusElement = document.getElementById(statusId);

    if (valueElement) {
        valueElement.textContent = `${value.toFixed(1)} ${unit}`;
    }

    if (statusElement) {
        statusElement.textContent = capitalizeFirst(status);
        statusElement.className = 'sensor-status ' + status;
    }

    // Update progress bar
    updateProgressBar(sensorType, value);
}

/**
 * Update device state display
 */
function updateDeviceState(deviceType, state) {
    const toggleId = deviceType + 'Toggle';
    const toggleElement = document.getElementById(toggleId);

    if (toggleElement) {
        toggleElement.checked = (state === 'on');
    }
}

/**
 * Update alerts display
 */
function updateAlerts(alerts) {
    const alertsSection = document.getElementById('alertsSection');
    const alertsList = document.getElementById('alertsList');

    if (alerts.length > 0) {
        alertsSection.style.display = 'block';
        alertsList.innerHTML = '';

        alerts.forEach(alert => {
            const alertItem = document.createElement('div');
            alertItem.className = 'alert-item';
            alertItem.textContent = alert.replace(/_/g, ' ').toUpperCase();
            alertsList.appendChild(alertItem);
        });
    } else {
        alertsSection.style.display = 'none';
    }
}

/**
 * Control device (turn on/off)
 */
function controlDevice(deviceType, command) {
    fetch(`/api/device/${deviceType}/${command}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateDeviceState(deviceType, data.state);
        } else {
            console.error('Device control failed:', data.error);
            alert('Failed to control device: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error controlling device:', error);
        alert('Error controlling device');
    });
}

/**
 * Toggle device via checkbox
 */
function toggleDevice(deviceType) {
    const toggleElement = document.getElementById(deviceType + 'Toggle');
    const command = toggleElement.checked ? 'on' : 'off';
    controlDevice(deviceType, command);
}

/**
 * Toggle automation mode
 */
function toggleAutoMode() {
    const isEnabled = document.getElementById('autoModeToggle').checked;
    const action = isEnabled ? 'enable' : 'disable';

    fetch(`/api/auto_mode/${action}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Auto mode ' + action + 'd');
        } else {
            console.error('Failed to toggle auto mode:', data.error);
            document.getElementById('autoModeToggle').checked = !isEnabled;
            alert('Failed to toggle automation mode');
        }
    })
    .catch(error => {
        console.error('Error toggling auto mode:', error);
        document.getElementById('autoModeToggle').checked = !isEnabled;
        alert('Error toggling automation mode');
    });
}

/**
 * Toggle growth phase via checkbox
 */
function togglePhase() {
    const toggle = document.getElementById('phaseToggle');
    const phase = toggle.checked ? 'flowering' : 'vegetative';
    switchPhase(phase);
}

/**
 * Switch growth phase
 */
function switchPhase(phase) {
    if (!confirm(`Switch to ${capitalizeFirst(phase)} phase?`)) {
        return;
    }

    fetch(`/api/growth_phase/${phase}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadStatus();
            alert(`Switched to ${capitalizeFirst(phase)} phase`);
        } else {
            console.error('Failed to switch phase:', data.error);
            alert('Failed to switch growth phase');
        }
    })
    .catch(error => {
        console.error('Error switching phase:', error);
        alert('Error switching growth phase');
    });
}

/**
 * Utility: Capitalize first letter
 */
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
