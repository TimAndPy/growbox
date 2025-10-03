# Research: UI Redesign for 1024x600 Tablet Display

**Feature**: 004-ui-redesign-for
**Date**: 2025-10-03
**Purpose**: Document current UI structure analysis and design decisions for the 1024x600 tablet UI redesign

---

## Current UI Implementation Analysis

### HTML Structure Inventory

**Current Layout** (`src/ui/templates/index.html`):

1. **Header** (lines 13-22):
   - `.header` container
   - `.header-left` with logo and h1
   - `.connection-status` with status indicator

2. **Sensors Section** (lines 26-65):
   - `.sensors-section` containing `.sensors-grid`
   - 4 sensor cards: temperature, humidity, light, water
   - Each card structure:
     - `.sensor-icon-badge` with modifier class (temp-icon, humidity-icon, etc.)
     - `.sensor-name`
     - `.sensor-value` with ID (tempValue, humidityValue, etc.)
     - `.progress-bar-container` > `.progress-bar-fill` with ID
     - `.sensor-target` with ID

3. **Two-Column Panels** (lines 68-135):
   - `.panels-container` (CSS Grid with 2 columns)
   - **Left**: `.system-controls-panel`
     - h2 "System Controls"
     - `.device-list` with 6 `.device-item` elements
     - Each device has name + `.switch` toggle
   - **Right**: `.growth-panel`
     - h2 "Growth Cycle"
     - `.growth-phase-highlight` with ID `phaseHighlight`
     - `.phase-toggle-container` with vegetative/flowering toggle

4. **Footer** (lines 145-147):
   - `.footer` with `.footer-branding` and sync time

### CSS Classes & IDs Used

**Layout Classes**:
- `.container` - main wrapper
- `.sensors-grid` - 4-column grid for sensors
- `.panels-container` - 2-column grid for controls/growth
- `.system-controls-panel` - left panel
- `.growth-panel` - right panel (TO BE REMOVED)

**Component Classes**:
- `.sensor-card`, `.sensor-icon-badge`, `.sensor-name`, `.sensor-value`, `.sensor-target`
- `.progress-bar-container`, `.progress-bar-fill`
- `.device-list`, `.device-item`, `.device-name`
- `.switch`, `.slider`
- `.phase-toggle-container`, `.phase-label`, `.phase-toggle-labels`

**Growth Cycle Classes (TO BE REMOVED)**:
- `.growth-panel`
- `.growth-phase-highlight`
- `.growth-info-box`
- `.phase-info`
- `.phase-controls`
- `.btn-phase`

**JavaScript Element IDs**:
- Sensors: `#temperature`, `#humidity`, `#light`, `#water`
- Sensor values: `#tempValue`, `#humidityValue`, `#lightValue`, `#waterValue`
- Progress bars: `#tempProgressBar`, `#humidityProgressBar`, `#lightProgressBar`, `#waterProgressBar`
- Device toggles: `#lightsToggle`, `#ventilationToggle`, `#pumpToggle`, `#autoModeToggle`, `#co2Toggle`, `#heaterToggle`
- Phase toggle: `#phaseToggle`
- Connection status: `#connectionStatus`, `#statusDot`, `#statusText`
- Sync time: `#lastSyncTime`

### Current Viewport Media Queries

From `style.css`:

1. **Line 526-539**: `@media (max-width: 1024px) and (max-height: 600px)`
   - Reduces spacing for 1024x600 viewport
   - Current adjustments: `--space-lg: 20px`, `--space-md: 12px`
   - Reduces sensor card padding to 12px
   - Reduces growth panel padding to 16px

2. **Line 542-550**: `@media (max-width: 1023px)`
   - Converts sensors to 2-column grid
   - Stacks panels vertically

3. **Line 552-578**: `@media (max-width: 768px)`
   - Mobile responsive: single column for everything

---

## CSS Layout Technique Decision

**Decision**: Use CSS Grid for sensor cards horizontal layout

**Rationale**:
- CSS Grid provides precise control over equal-width columns
- Current implementation already uses Grid (`grid-template-columns: repeat(4, 1fr)`)
- Grid handles responsive behavior cleanly with media queries
- No need to switch to Flexbox - Grid is optimal for this use case

**Implementation**:
```css
.sensors-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
}
```

**Alternatives Considered**:
- Flexbox with `flex: 1`: Would work but requires more spacing management
- Fixed widths: Rejected - not responsive to viewport changes
- Table layout: Rejected - obsolete and inflexible

---

## Visual Design System Documentation

### Color Palette (Preserved)
```css
--primary-green: #52C41A
--light-gray: #F5F5F5
--white: #FFFFFF
--border-gray: #D9D9D9
--text-dark: #262626
--text-secondary: #8C8C8C
--success-green: #52C41A
--growth-panel-bg: #F6FFED (will be unused after removal)
--growth-panel-border: #B7EB8F (will be unused after removal)
--danger-color: #FF4D4F
--warning-color: #FAAD14
```

### Typography Scale (Preserved)
```css
--value-size: 36px (sensor values)
--label-size: 14px (labels, targets)
--heading-size: 20px (section headings)
--body-size: 14px (body text, device names)
```

### Spacing System (Preserved)
```css
--space-xs: 8px
--space-sm: 12px
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
```

### Component Styling (Preserved)
- Card shadow: `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`
- Border radius: `var(--space-xs)` (8px)
- Card border: `1px solid var(--border-gray)`
- Progress bar height: `8px`
- Toggle switch dimensions: `48px × 28px`

---

## Layout Changes Required

### 1. Sensor Grid
**Current**: 4-column grid (already correct for 1024x600)
**Change**: None required - preserve existing
**Verification**: Ensure single row at 1024x600 (no wrapping)

### 2. System Controls Panel Restructure
**Current**: Two separate panels side-by-side in `.panels-container`
**New**: Single System Controls card with integrated header

**HTML Structure Change**:
```html
<!-- OLD: Two-column layout -->
<div class="panels-container">
  <section class="section system-controls-panel">
    <h2>System Controls</h2>
    ...
  </section>
  <section class="section growth-panel">
    <h2>Growth Cycle</h2>
    ...
  </section>
</div>

<!-- NEW: Single card with header -->
<section class="section system-controls-panel">
  <div class="controls-header">
    <h2>System Controls</h2>
    <div class="phase-toggle-container">
      <!-- Move Vegetative/Flowering toggle here -->
    </div>
  </div>
  <div class="device-list">
    <!-- Existing device toggles -->
  </div>
</section>
```

**CSS Changes Required**:
- Remove `.panels-container` grid layout
- Add `.controls-header` with Flexbox (space-between)
- Position toggle in header right side
- Adjust card width to fit 1024x600 (full width or centered)

### 3. Growth Cycle Panel Removal
**Remove Entirely**:
- `.growth-panel` section (lines 118-134 in HTML)
- All CSS rules for growth cycle classes
- Phase toggle will move to System Controls header

---

## JavaScript Selector Mapping

### Selectors Requiring Review

**Phase Toggle**:
- Current: `#phaseToggle` inside `.growth-panel`
- New: `#phaseToggle` inside `.system-controls-panel .controls-header`
- **Action**: Verify `togglePhase()` function in main.js still works after DOM move

**Device Toggles**:
- IDs unchanged: `#lightsToggle`, `#ventilationToggle`, `#pumpToggle`, `#autoModeToggle`, `#co2Toggle`, `#heaterToggle`
- **Action**: No changes needed

**Sensor Elements**:
- All IDs unchanged
- **Action**: No changes needed

**Potential Issues**:
- Check if any CSS selectors use descendant relationships (e.g., `.growth-panel .phase-toggle`)
- Verify WebSocket update handlers don't rely on growth panel existence

---

## 1024x600 Viewport Optimization

### Spacing Adjustments

**Current Media Query** (line 526):
```css
@media (max-width: 1024px) and (max-height: 600px) {
  --space-lg: 20px;
  --space-md: 12px;
  .sensor-card { padding: 12px; }
  .growth-panel { padding: 16px; }
}
```

**Updated Strategy**:
- Keep reduced spacing values (--space-lg: 20px, --space-md: 12px)
- Remove `.growth-panel` padding rule (panel no longer exists)
- Add `.system-controls-panel` padding optimization if needed
- Verify header/footer heights don't cause overflow

### Height Budget Calculation

**Available Height at 1024x600**:
- Total: 600px
- Header: ~60px (estimated)
- Footer: ~40px (estimated)
- Margins/spacing: ~40px
- **Content area**: ~460px

**Content Breakdown**:
- Sensor cards: ~150px (icon + value + progress + target)
- System Controls card: ~250px (header + 6 device rows)
- Remaining buffer: ~60px

**Verification Needed**: Test actual heights at 1024x600 to ensure no scrolling

---

## CSS Classes to Remove

**Growth Cycle Related** (from style.css):
- `.growth-panel` (lines 153-159)
- `.growth-phase-highlight` (lines 161-166)
- `.growth-info-box` (lines 168-174)
- `.growth-info-box .label` (lines 176-180)
- `.growth-info-box .value` (lines 182-186)
- `.phase-info` (lines 188-192)
- `.phase-info > div` (lines 194-198)
- `.phase-info .label` (lines 200-203)
- `.phase-info .value` (lines 205-209)
- `.phase-controls` (lines 211-214)
- `.btn-phase` (lines 217-219)

**Phase Toggle Classes** (KEEP but may need repositioning):
- `.phase-toggle-container` (lines 222-228) - KEEP, move to controls header
- `.phase-label` (lines 230-235) - KEEP
- `.phase-toggle-labels` (lines 242-246) - KEEP

---

## Summary of Decisions

1. **Layout Technique**: Continue using CSS Grid for sensors, add Flexbox for controls header
2. **Design System**: Preserve all existing color variables, typography, and spacing
3. **HTML Changes**:
   - Remove Growth Cycle panel entirely
   - Consolidate System Controls into single full-width card
   - Move Vegetative/Flowering toggle to controls header
4. **CSS Changes**:
   - Remove all growth cycle styling (~150 lines)
   - Add controls header styling (Flexbox layout)
   - Update 1024x600 media query (remove growth panel references)
5. **JavaScript**: Minimal changes - verify phase toggle event handlers still work after DOM move

---

**Next Phase**: Phase 1 will produce detailed HTML/CSS specifications in quickstart.md for implementation
