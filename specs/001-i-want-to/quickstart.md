# Quickstart Manual Testing: GrowBox IoT Control System

**Purpose**: Step-by-step manual validation of all functional requirements
**Date**: 2025-10-03
**Prerequisites**: Fully implemented system, hardware connected, MQTT broker running

---

## Test Environment Setup

**Hardware**:
- NVIDIA Jetson Nano 2GB with sensors connected
  - DHT22 on GPIO pin X (temperature/humidity)
  - BH1750 on I2C bus 1 (light sensor)
  - HC-SR04 on GPIO pins Y/Z (water level)
- Relay board for devices on GPIO pins (see config/devices.json)
- Tablet browser pointed to http://jetson-nano-ip:5000
- Mendix mobile app configured with MQTT broker URL

**Software**:
- MQTT broker (Mosquitto) running and accessible
- GrowBox Python application running (`python src/main.py`)
- Test MQTT client (mosquitto_pub/sub or MQTT Explorer)

---

## Test Suite

### Test 1: Sensor Reading Display (FR-001 through FR-005)

**Objective**: Verify all sensors are read every 5 seconds and displayed correctly

**Steps**:
1. Open tablet browser to control panel
2. Observe sensor cards (Temperature, Humidity, Light Level, Water Level)
3. Wait for 5-second update cycle
4. Verify each card shows:
   - Current numeric value
   - Correct unit (°C, %, μmol, L)
   - Progress bar indicating status
5. Use MQTT client to subscribe to `growbox/001/sensors/#`
6. Confirm MQTT messages published every 5 seconds

**Expected Results**:
- ✅ Temperature card updates every 5 seconds with °C value
- ✅ Humidity card updates every 5 seconds with % value
- ✅ Light level card updates every 5 seconds with μmol value
- ✅ Water level card updates every 5 seconds with liters and % capacity
- ✅ MQTT messages match JSON schema (contracts/mqtt-sensor-data.json)
- ✅ No sensor errors or stale data warnings

**Validation**: FR-001, FR-002, FR-003, FR-004, FR-005 ✓

---

### Test 2: Manual Device Control - Local Tablet (FR-006 through FR-012)

**Objective**: Verify tablet toggles activate devices with <2-second response

**Steps**:
1. In System Controls panel, toggle "Grow Lights" switch to ON
2. Observe physical relay/device activation
3. Check MQTT client for device state message
4. Verify toggle switch UI updates
5. Repeat for all devices:
   - Ventilation
   - Water Pump
   - Heater
   - CO₂ System
6. Toggle each device OFF and verify deactivation

**Expected Results**:
- ✅ Physical devices activate within 2 seconds of toggle
- ✅ Toggle switch UI reflects current state
- ✅ MQTT publishes device state message to `growbox/001/devices/{device}/state`
- ✅ All 5 devices respond correctly (lights, ventilation, pump, heater, co2)
- ✅ State changes logged to SQLite `device_states` table

**Validation**: FR-006, FR-007, FR-008, FR-009, FR-010, FR-012 ✓

---

### Test 3: Manual Device Control - Remote Mendix App (FR-012, FR-027, FR-030)

**Objective**: Verify Mendix app control commands activate devices

**Steps**:
1. Open Mendix mobile app
2. Publish MQTT command to `growbox/001/devices/lights/command`:
   ```json
   {
     "schema_version": "1.0",
     "message_id": "test-uuid-123",
     "timestamp": "2025-10-03T20:00:00Z",
     "box_id": "001",
     "type": "device_command",
     "device": "lights",
     "command": "on",
     "source": "remote"
   }
   ```
3. Observe physical light activation
4. Check tablet UI for updated toggle state
5. Repeat for remaining devices

**Expected Results**:
- ✅ Jetson Nano receives MQTT command and activates device
- ✅ Tablet UI updates to reflect new state (synchronized)
- ✅ Physical device activates within 2 seconds
- ✅ MQTT state message published confirming change

**Validation**: FR-012, FR-027, FR-030 ✓

---

### Test 4: Auto Mode Activation (FR-011, FR-023 through FR-026)

**Objective**: Verify automated control based on target parameters

**Steps**:
1. Set target temperature range to 22-25°C via UI or config
2. Enable "Auto Mode" toggle in System Controls
3. Simulate low temperature (e.g., place ice pack near sensor OR temporarily adjust target to be above current temp)
4. Wait for sensor reading update (5 seconds)
5. Verify heater automatically turns ON
6. Simulate high temperature (remove ice pack OR adjust target below current)
7. Verify heater turns OFF, ventilation turns ON
8. Check hysteresis behavior (no rapid on/off cycling)

**Expected Results**:
- ✅ Auto mode toggle enables automation
- ✅ Heater activates when temp < (target_min - hysteresis)
- ✅ Ventilation activates when temp > (target_max + hysteresis)
- ✅ Devices deactivate when target range reached
- ✅ No rapid cycling (hysteresis respected)
- ✅ Manual toggle overrides auto mode for that device

**Validation**: FR-011, FR-023, FR-024, FR-025, FR-026 ✓

---

### Test 5: Growth Phase Management (FR-013 through FR-019)

**Objective**: Verify phase selection and light schedule automation

**Steps**:
1. In Growth Cycle panel, verify current phase displayed (e.g., "Vegetative - Day 12")
2. Verify light schedule shows "18h ON / 6h OFF" for vegetative
3. Click "Switch to Flowering" button
4. Confirm phase changes to "Flowering - Day 1"
5. Verify light schedule updates to "12h ON / 12h OFF"
6. Check that lights respect new schedule (may need to wait for schedule trigger time)
7. Verify "Days Until Harvest" field is NOT editable (observational approach)

**Expected Results**:
- ✅ Current phase and day count displayed
- ✅ Light schedule matches phase (18/6 for veg, 12/12 for flower)
- ✅ Phase switch button works (manual selection)
- ✅ Day counter resets to 1 on phase change
- ✅ Lights follow automated schedule based on phase
- ✅ No harvest date input required (FR-019)

**Validation**: FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019 ✓

---

### Test 6: Target Parameter Adjustment (FR-020 through FR-026)

**Objective**: Verify users can adjust targets with guided warnings

**Steps**:
1. Click "Edit" on Temperature target range
2. Attempt to set min=10°C, max=50°C (extreme values)
3. Verify warning message appears (outside recommended range)
4. Confirm system allows override (set anyway)
5. Set reasonable values (min=22°C, max=25°C)
6. Verify no warning for reasonable values
7. Repeat for humidity and water level targets
8. Enable auto mode and confirm new targets are used

**Expected Results**:
- ✅ Target ranges are editable
- ✅ Warning shown for extreme values (loose boundaries)
- ✅ User can override warning
- ✅ Reasonable values accepted without warning
- ✅ Different targets supported per growth phase
- ✅ Auto mode uses updated targets immediately

**Validation**: FR-020, FR-021, FR-022, FR-023, FR-024, FR-025, FR-026 ✓

---

### Test 7: Communication Loss Safety (FR-041)

**Objective**: Verify all devices turn OFF on MQTT connection loss

**Steps**:
1. Ensure some devices are ON (lights, heater)
2. Stop MQTT broker OR disconnect network cable from Jetson Nano
3. Wait 30 seconds (watchdog timeout)
4. Observe all devices (lights, ventilation, pump, heater, co2)
5. Check device state logs in SQLite

**Expected Results**:
- ✅ All devices turn OFF within 30 seconds of connection loss
- ✅ Tablet UI shows "Offline" indicator
- ✅ Mendix app shows "Offline" status
- ✅ Device states logged with `command_source = 'failsafe'`
- ✅ Auto mode disabled

**Validation**: FR-041 ✓

**Reconnection Test**:
1. Restore MQTT broker connection
2. Verify "Online" indicator appears
3. Devices remain OFF (safe state, wait for user command)

---

### Test 8: Historical Data Storage (FR-037 through FR-039)

**Objective**: Verify full-season data retention and access

**Steps**:
1. Let system run for at least 1 hour (collecting sensor readings)
2. Open SQLite database: `sqlite3 <path>/growbox.db`
3. Query sensor readings:
   ```sql
   SELECT COUNT(*) FROM sensor_readings WHERE sensor_type = 'temperature';
   -- Expected: ~720 readings (1 hour / 5 seconds = 720)
   ```
4. Query device state history:
   ```sql
   SELECT * FROM device_states ORDER BY timestamp DESC LIMIT 10;
   ```
5. Verify historical data access via UI (if graphing implemented) or SQL
6. Confirm data persists after system reboot

**Expected Results**:
- ✅ All sensor readings stored with timestamps
- ✅ All device state changes logged
- ✅ Data accessible for trend analysis
- ✅ Data persists across reboots
- ✅ No automatic deletion (full season retained)

**Validation**: FR-037, FR-038, FR-039 ✓

---

### Test 9: UI Consistency Verification (Constitutional Principle III)

**Objective**: Verify tablet UI matches mockup design system

**Steps**:
1. Open mockup image (Mockup_ControlPanelUI.png)
2. Compare tablet UI side-by-side with mockup
3. Verify:
   - Sensor card layout (4-column grid)
   - Color scheme (greens, grays, white backgrounds)
   - Typography (font sizes, weights)
   - Spacing and padding consistency
   - Toggle switch appearance
   - Online indicator position (top right)
4. Test touch targets (minimum 44px)
5. Verify visual feedback on button press

**Expected Results**:
- ✅ UI visually matches mockup
- ✅ Design tokens (colors, spacing) consistent
- ✅ Touch targets adequately sized
- ✅ Interaction patterns uniform
- ✅ Responsive layout (if tested on different screen sizes)

**Validation**: FR-033, FR-034, FR-035, FR-036 + Constitutional Principle III ✓

---

### Test 10: MQTT Message Schema Compliance

**Objective**: Verify all MQTT messages match contract definitions

**Steps**:
1. Use MQTT client to subscribe to `growbox/001/#` (all topics)
2. Capture samples of each message type:
   - Sensor readings
   - Device commands (publish test command)
   - Device state updates
   - System status
3. Validate each message against JSON schemas:
   - contracts/mqtt-sensor-data.json
   - contracts/mqtt-device-command.json
   - contracts/mqtt-device-state.json
   - contracts/mqtt-system-status.json
4. Use JSON schema validator (e.g., ajv-cli, online validator)

**Expected Results**:
- ✅ All sensor messages validate against mqtt-sensor-data.json
- ✅ All device commands validate against mqtt-device-command.json
- ✅ All device states validate against mqtt-device-state.json
- ✅ All system status messages validate against mqtt-system-status.json
- ✅ QoS levels correct (sensors QoS 1, commands QoS 2, states QoS 1)
- ✅ Retained flags correct (sensors/states retained, commands not retained)

**Validation**: FR-027, FR-028, FR-029, FR-030, FR-031 ✓

---

## Pass/Fail Criteria

**PASS**: All tests above complete with ✅ expected results
**FAIL**: Any test shows ❌ or missing functionality

**Sign-off**:
- [ ] All 10 tests passed
- [ ] No critical bugs discovered
- [ ] UI consistency verified against mockup
- [ ] MQTT contracts validated
- [ ] Communication loss safety confirmed

**Tester**: ________________
**Date**: ________________
**Notes**: ________________

---

## Additional Edge Case Testing (Optional)

These edge cases were identified in spec but may require custom test setups:

1. **Auto mode vs manual override conflict**: Enable auto mode, manually toggle device, verify auto mode disabled for that device
2. **Low water reservoir behavior**: Drain water below threshold, check for alert (if implemented)
3. **Power loss and restoration**: Power cycle Jetson Nano, verify graceful restart and state recovery
4. **Sensor error handling**: Disconnect sensor, verify "error" status displayed and logged
5. **Concurrent MQTT clients**: Connect multiple Mendix app instances, verify all receive updates

---

## Automated Test Execution (Future)

This quickstart is for manual execution. For automated testing:
- Contract tests: See `tests/contract/` directory
- Integration tests: See `tests/integration/` directory
- Run: `pytest tests/`

Manual testing validates the complete user experience; automated tests validate code correctness.
