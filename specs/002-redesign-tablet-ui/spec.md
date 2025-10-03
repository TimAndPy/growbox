# Feature Specification: Tablet UI Redesign to Match Mockup

**Feature Branch**: `002-redesign-tablet-ui`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "Redesign tablet UI to match mockup: light theme with card-based layout, sensor cards with progress bars showing target ranges, simplified device toggles, growth cycle panel with phase display and light schedule"

## Execution Flow (main)
```
1. Parse user description from Input ✓
   → Feature: UI redesign to match provided mockup
2. Extract key concepts from description ✓
   → Light theme (white background)
   → Card-based layout with clean borders
   → Sensor cards with progress bars
   → Simplified toggle switches
   → Growth cycle info panel
3. Compare current UI (@CurrentUI.png) vs desired UI (@Mockup_ControlPanelUI.png)
   → Current: Dark theme, emoji icons, separate ON/OFF buttons
   → Desired: Light theme, icon badges, toggle switches, progress bars
4. Fill User Scenarios & Testing section ✓
5. Generate Functional Requirements ✓
6. Identify Key UI Components ✓
7. Run Review Checklist
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users see and interact with
- ❌ Avoid HOW to implement CSS/HTML structure
- 👥 Written for UI/UX perspective

---

## User Scenarios & Testing

### Primary User Story
As a grower using the tablet interface, I want a clean, professional control panel that clearly shows sensor readings with visual progress indicators for target ranges, and allows me to control devices with simple toggle switches, so I can quickly assess system status and make adjustments without confusion.

### Acceptance Scenarios

1. **Given** I open the tablet UI, **When** the page loads, **Then** I see a light-themed interface with white/light gray cards on a clean background

2. **Given** I view the sensor cards, **When** looking at temperature/humidity/light/water readings, **Then** each card shows:
   - Sensor icon badge (top)
   - Large numeric value with unit
   - Progress bar showing current value against target range
   - Target range displayed below (e.g., "Target: 22-25°C")

3. **Given** I want to control a device, **When** I look at the System Controls section, **Then** I see:
   - List of devices (Grow Lights, Ventilation, Water Pump, Auto Mode, CO₂ System, Heater)
   - Toggle switches (not separate ON/OFF buttons)
   - Current state clearly visible

4. **Given** I view the Growth Cycle panel, **When** looking at current phase information, **Then** I see:
   - Current phase highlighted (Flowering - Day 28)
   - Light schedule displayed (12h ON / 12h OFF)
   - Days until harvest countdown

5. **Given** I interact with the UI on a tablet, **When** touching any control, **Then** touch targets are large enough (44px minimum) and provide immediate visual feedback

### Edge Cases
- What happens when sensor reading is outside target range? (Progress bar color change)
- How does the UI indicate offline/error status? (Status dot changes, card grays out)
- What if device is in cooldown period? (Toggle disabled with tooltip)

## Requirements

### Functional Requirements

**Visual Design**
- **FR-001**: System MUST display a light theme with white/light gray background instead of dark theme
- **FR-002**: Sensor cards MUST show progress bars indicating current value relative to target range (green when in range)
- **FR-003**: Sensor cards MUST display target ranges below readings (e.g., "Target: 60-70%", "Reservoir: 70%")
- **FR-004**: Device cards MUST use icon badges instead of emoji icons
- **FR-005**: All cards MUST have consistent rounded corners and subtle shadows/borders

**Sensor Display**
- **FR-006**: Temperature card MUST show value in large text (e.g., "23.5°C") with thermometer icon badge
- **FR-007**: Humidity card MUST show percentage with water droplet icon badge
- **FR-008**: Light Level card MUST show reading in μmol (PPFD) with light bulb icon badge
- **FR-009**: Water Level card MUST show liters with water tank icon badge and reservoir percentage
- **FR-010**: Each sensor card MUST include a horizontal progress bar showing current value against min/max target range

**Device Controls**
- **FR-011**: System Controls MUST display as a list with device names and toggle switches (not separate ON/OFF buttons)
- **FR-012**: Device toggles MUST clearly show ON (green) and OFF (gray) states
- **FR-013**: Auto Mode toggle MUST be clearly distinguishable in the device list
- **FR-014**: All device controls MUST be aligned in a single column for tablet layout

**Growth Cycle Panel**
- **FR-015**: Growth Cycle panel MUST display on a light green background to distinguish it from other sections
- **FR-016**: Current Phase MUST be highlighted with phase name and day count (e.g., "Flowering - Day 28")
- **FR-017**: Light Schedule MUST show in format "12h ON / 12h OFF" in a bordered box
- **FR-018**: Days Until Harvest MUST show countdown in a bordered box (e.g., "32 days remaining")

**Layout & Spacing**
- **FR-019**: Header MUST show "GrowBox Control Panel" title on left and connection status (Online/Offline) on right
- **FR-020**: Sensor cards MUST be arranged in a 4-column grid at the top (Temperature, Humidity, Light Level, Water Level)
- **FR-021**: System Controls MUST be positioned on the left side below sensor grid
- **FR-022**: Growth Cycle panel MUST be positioned on the right side below sensor grid
- **FR-023**: All touch targets MUST be minimum 44x44 pixels for tablet usability

**Branding & Polish**
- **FR-024**: Interface MUST display "Squad Apps" branding logo in top-left
- **FR-025**: Footer MUST show "Powered by Squad Apps • Last sync: X min ago"
- **FR-026**: Primary accent color MUST be green (#52C41A or similar) for active states and highlights
- **FR-027**: Connection status indicator MUST be a colored dot (green=online, red=offline) next to "Online/Offline" text

### Key UI Components

- **Header Bar**: Brand logo (left), title (center-left), connection status (right)
- **Sensor Card Grid**: 4 columns, equal width, with icon badge, value, progress bar, target range
- **System Controls Panel**: White card with device list and toggle switches
- **Growth Cycle Panel**: Light green card with phase info, light schedule, harvest countdown
- **Progress Bar**: Visual indicator showing current sensor value against target range
- **Toggle Switch**: Modern iOS-style toggle (green=ON, gray=OFF)
- **Status Indicator**: Colored dot + text for connection state

---

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and visual requirements
- [x] Written for UI/UX stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable (visual comparison to mockup)
- [x] Scope is clearly bounded (UI redesign only, no backend changes)
- [x] Dependencies: Uses existing sensor data and device control logic

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted (light theme, cards, progress bars, toggles)
- [x] Ambiguities marked (none - mockup provides clear visual reference)
- [x] User scenarios defined
- [x] Requirements generated (27 functional requirements)
- [x] UI components identified
- [x] Review checklist passed

---

## Visual Comparison Summary

### Current UI → Desired UI Changes

| Element | Current | Desired |
|---------|---------|---------|
| Theme | Dark (#1a1a1a background) | Light (white/light gray) |
| Sensor Values | Large text only | Large text + progress bar + target range |
| Sensor Icons | Emoji (🌡️💧☀️🚰) | Icon badges (colored, consistent style) |
| Device Controls | Separate ON/OFF buttons | Single toggle switches |
| Layout | 3 sections stacked | 2-column layout (controls left, growth cycle right) |
| Growth Phase | Simple text display | Highlighted panel with detailed info |
| Branding | "GrowBox Control Panel" only | Squad Apps logo + branding footer |
| Connection Status | "Offline" text with dot | "Online" text with green dot (top-right) |

This redesign focuses on improving visual hierarchy, reducing cognitive load, and providing better at-a-glance status understanding through progress bars and cleaner organization.
