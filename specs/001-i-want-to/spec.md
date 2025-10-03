# Feature Specification: GrowBox IoT Control System

**Feature Branch**: `001-i-want-to`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "I want to setup my growbox with an IoT device. I have a nvidia jetson nano 2gb developer kit connected to a tablet on which I want to display a control panel. The side pins of the nvidia jetson nano 2gb developer kit can be used to read from sensors or to activate lights, pumps etc. I want to be able to subscribe the nvidia jetson nano 2gb developer kit to a websocket (MQTT) via which I can read and control the device from my Mendix app (which also allows me to subscribe to a websocket (MQTT)."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

---

## Clarifications

### Session 2025-10-03
- Q: What should happen to device states (lights, pump, heater, etc.) when the system loses connection to the MQTT broker or tablet? → A: Safe default - all devices turn OFF immediately upon connection loss
- Q: Should the system store historical sensor data (temperature, humidity, light, water level readings over time)? → A: Long-term archive - keep full growing season history for analysis
- Q: How frequently should sensor readings be updated and transmitted? → A: Standard (5 seconds) - good balance of responsiveness and efficiency
- Q: Can users adjust target environmental ranges (temperature, humidity, water level), and if so, with what constraints? → A: Guided adjustment - user adjusts within recommended ranges with warnings for unsafe values (boundaries should be loose to avoid excessive warnings; varies by plant type and growth stage)
- Q: How should users configure and change growth phases (vegetative, flowering) and light schedules? → A: Manual phase selection only - user manually switches between growth/flower phases when they observe flowering starts; each phase has preset light hours (no duration prefill or templates); phase determines light schedule automatically

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a GrowBox operator, I want to monitor and control my indoor garden remotely through a mobile application, so that I can maintain optimal growing conditions (temperature, humidity, light, water) without being physically present at the GrowBox.

The system displays real-time sensor data (temperature, humidity, light level, water level) on both a local tablet interface and a remote mobile app. Operators can view current environmental conditions, manually toggle system controls (grow lights, ventilation, water pump, heater, CO₂ system), enable automated control modes, and track the growth cycle progress including flowering phase and harvest countdown.

### Acceptance Scenarios
1. **Given** the GrowBox is powered on and connected, **When** I open the mobile app, **Then** I see current readings for temperature, humidity, light level, and water level with data refreshed every 5 seconds
2. **Given** I'm viewing the control panel, **When** I toggle the "Grow Lights" switch to ON, **Then** the physical lights activate within 2 seconds and the status updates on all connected displays
3. **Given** the system is in Auto Mode, **When** temperature falls below the target range, **Then** the heater activates automatically without manual intervention
4. **Given** the GrowBox is offline, **When** I attempt to view data in the mobile app, **Then** I see a clear "Offline" indicator and the last known values with timestamp
5. **Given** I'm monitoring the growth cycle and observe flowering has started, **When** I manually switch from Vegetative to Flowering phase, **Then** the system automatically adjusts the light schedule and begins tracking days in flowering phase
6. **Given** sensor data is being collected, **When** values exceed safe thresholds, **Then** [NEEDS CLARIFICATION: Should system send alerts/notifications? What are the alert thresholds?]

### Edge Cases
- What happens when the tablet loses connection to the IoT device? → All devices turn OFF immediately for safety
- How does the system handle conflicting commands (auto mode vs manual override)?
- What happens when water reservoir is critically low?
- How does system behave during power loss and restoration?
- What happens if MQTT broker becomes unavailable? → All devices turn OFF immediately for safety
- How are sensor reading errors or invalid data handled?

## Requirements *(mandatory)*

### Functional Requirements

**Sensor Monitoring**:
- **FR-001**: System MUST continuously read temperature from connected sensor and display current value
- **FR-002**: System MUST continuously read humidity from connected sensor and display current percentage
- **FR-003**: System MUST continuously read light level from connected sensor and display in PPFD (micromoles)
- **FR-004**: System MUST continuously measure water level and display in liters with reservoir capacity percentage
- **FR-005**: System MUST update all sensor readings every 5 seconds and transmit to all connected interfaces

**Device Control**:
- **FR-006**: Users MUST be able to manually toggle grow lights on/off
- **FR-007**: Users MUST be able to manually toggle ventilation system on/off
- **FR-008**: Users MUST be able to manually toggle water pump on/off
- **FR-009**: Users MUST be able to manually toggle heater on/off
- **FR-010**: Users MUST be able to manually toggle CO₂ system on/off
- **FR-011**: System MUST enable/disable Auto Mode which automatically controls all devices based on target parameters
- **FR-012**: System MUST reflect control state changes on all connected interfaces within 2 seconds

**Growth Cycle Management**:
- **FR-013**: System MUST display current growth phase (e.g., "Flowering - Day 28")
- **FR-014**: System MUST display configured light schedule (e.g., "12h ON / 12h OFF")
- **FR-015**: System MUST display days remaining until harvest
- **FR-016**: Users MUST be able to manually select between growth phases (Vegetative/Flowering) based on visual observation
- **FR-017**: System MUST automatically set appropriate light schedule when phase is selected (phase determines light hours)
- **FR-018**: System MUST track days in current phase automatically from phase selection date
- **FR-019**: System MUST NOT require users to input phase durations or harvest dates (observational approach only)

**Target Parameter Management**:
- **FR-020**: System MUST display target ranges for temperature (shown: 22-25°C)
- **FR-021**: System MUST display target ranges for humidity (shown: 60-70%)
- **FR-022**: System MUST display reservoir capacity target (shown: 70%)
- **FR-023**: Users MUST be able to adjust target ranges for temperature, humidity, and water level within recommended safe limits
- **FR-024**: System MUST provide warnings when users attempt to set values outside recommended ranges, but allow override
- **FR-025**: System MUST support different target ranges based on plant type and growth stage (vegetative vs flowering)
- **FR-026**: System MUST use loose warning boundaries to prevent excessive alerts during normal operation

**Remote Communication**:
- **FR-027**: IoT device MUST publish sensor data to message broker for remote access
- **FR-028**: IoT device MUST subscribe to control commands from message broker
- **FR-029**: Mobile app MUST subscribe to sensor data updates from message broker
- **FR-030**: Mobile app MUST publish control commands to message broker
- **FR-031**: System MUST indicate connection status (Online/Offline) on all interfaces
- **FR-032**: System MUST handle message delivery failures gracefully with [NEEDS CLARIFICATION: retry logic? queuing? user notification?]

**Local Display**:
- **FR-033**: Tablet MUST display identical control panel as shown in mockup (sensor readings, system controls, growth cycle info)
- **FR-034**: Tablet interface MUST update in real-time when sensor values change
- **FR-035**: Tablet interface MUST respond to touch input for toggling controls
- **FR-036**: Tablet display MUST remain synchronized with mobile app state

**Data Management**:
- **FR-037**: System MUST store all sensor readings (temperature, humidity, light level, water level) with timestamps for the entire growing season
- **FR-038**: System MUST provide access to historical data for trend analysis, graphing, and season retrospectives
- **FR-039**: System MUST retain historical data until explicitly deleted by user or until growing season is marked complete and archived

**Safety & Reliability**:
- **FR-040**: System MUST [NEEDS CLARIFICATION: What safety behaviors are required - auto-shutoff if sensors fail? Maximum run times for pumps/heaters?]
- **FR-041**: System MUST turn OFF all devices (lights, pump, heater, ventilation, CO₂) immediately upon detecting communication loss with MQTT broker or tablet
- **FR-042**: System MUST [NEEDS CLARIFICATION: Are there user authentication/authorization requirements for the mobile app?]

### Key Entities *(include if feature involves data)*

- **SensorReading**: Represents a single environmental measurement including sensor type (temperature/humidity/light/water), current value, unit of measurement, timestamp, and status (valid/error)

- **DeviceControl**: Represents a controllable system component including device type (lights/ventilation/pump/heater/CO₂), current state (on/off/auto), last command timestamp, and command source (local/remote/auto)

- **GrowthCycle**: Represents the plant growth timeline including current phase name, phase start date, phase duration, light schedule configuration, target environmental parameters, and harvest date

- **SystemStatus**: Represents overall system health including connection state (online/offline), last communication timestamp, active alerts, and auto mode status

- **TargetParameters**: Represents desired environmental ranges including min/max temperature, min/max humidity, target water level, and associated tolerance values

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous (where specified)
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed (blocked by NEEDS CLARIFICATION items)

---
