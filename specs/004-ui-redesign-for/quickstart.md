# Quickstart: UI Redesign Visual Validation

**Feature**: 004-ui-redesign-for
**Purpose**: Detailed layout specifications and visual validation checklist for the 1024x600 tablet UI redesign

---

## HTML Layout Specification

### 1. Sensor Cards Grid

**Location**: `src/ui/templates/index.html` (Section around line 26)

**Structure** (NO CHANGES - already optimal):
```html
<section class="section sensors-section">
    <div class="sensors-grid">
        <!-- 4 sensor cards in single horizontal row -->
        <div class="sensor-card" id="temperature">...</div>
        <div class="sensor-card" id="humidity">...</div>
        <div class="sensor-card" id="light">...</div>
        <div class="sensor-card" id="water">...</div>
    </div>
</section>
```

**Requirements**:
- Preserve all existing sensor card HTML structure
- Maintain all IDs and classes (no JavaScript breakage)
- Keep icon badges, value displays, progress bars, and targets

---

### 2. System Controls Panel with Header

**Location**: `src/ui/templates/index.html` (Replace lines 68-135)

**NEW Structure**:
```html
<section class="section system-controls-panel">
    <!-- NEW: Header row with title and phase toggle -->
    <div class="controls-header">
        <h2>System Controls</h2>
        <div class="phase-toggle-container">
            <span class="phase-label-text">Vegetative (18/6)</span>
            <label class="switch">
                <input type="checkbox" id="phaseToggle" onchange="togglePhase()">
                <span class="slider"></span>
            </label>
            <span class="phase-label-text">Flowering (12/12)</span>
        </div>
    </div>

    <!-- EXISTING: Device list (preserve exactly as is) -->
    <div class="device-list">
        <div class="device-item">
            <span class="device-name">Grow Lights</span>
            <label class="switch">
                <input type="checkbox" id="lightsToggle" onchange="toggleDevice('lights')">
                <span class="slider"></span>
            </label>
        </div>
        <div class="device-item">
            <span class="device-name">Ventilation</span>
            <label class="switch">
                <input type="checkbox" id="ventilationToggle" onchange="toggleDevice('ventilation')">
                <span class="slider"></span>
            </label>
        </div>
        <div class="device-item">
            <span class="device-name">Water Pump</span>
            <label class="switch">
                <input type="checkbox" id="pumpToggle" onchange="toggleDevice('pump')">
                <span class="slider"></span>
            </label>
        </div>
        <div class="device-item">
            <span class="device-name">Auto Mode</span>
            <label class="switch">
                <input type="checkbox" id="autoModeToggle" onchange="toggleAutoMode()">
                <span class="slider"></span>
            </label>
        </div>
        <div class="device-item">
            <span class="device-name">CO₂ System</span>
            <label class="switch">
                <input type="checkbox" id="co2Toggle" onchange="toggleDevice('co2')">
                <span class="slider"></span>
            </label>
        </div>
        <div class="device-item">
            <span class="device-name">Heater</span>
            <label class="switch">
                <input type="checkbox" id="heaterToggle" onchange="toggleDevice('heater')">
                <span class="slider"></span>
            </label>
        </div>
    </div>
</section>
```

**Key Changes**:
- Remove `.panels-container` wrapper (no longer 2-column layout)
- Add `.controls-header` div with Flexbox layout
- Move phase toggle from Growth Cycle panel to controls header
- Simplify phase toggle: remove complex `.phase-label` wrapper, use plain text + toggle
- Keep all device toggles exactly as they are
- Preserve all IDs for JavaScript compatibility

**REMOVE ENTIRELY**:
- Growth Cycle panel (`<section class="section growth-panel">...</section>`)
- All growth phase highlight and info elements

---

### 3. Footer

**Location**: `src/ui/templates/index.html` (lines 145-147)

**Structure** (NO CHANGES):
```html
<footer class="footer">
    <div class="footer-branding">Powered by Squad Apps • Last sync: <span id="lastSyncTime">-</span></div>
</footer>
```

**Requirements**:
- Preserve footer exactly as is
- Keep sync timestamp display

---

## CSS Styling Specification

### 1. Sensor Grid Styling

**Location**: `src/ui/static/css/style.css` (around line 267)

**PRESERVE** (already correct):
```css
.sensors-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.sensor-card {
    background-color: var(--white);
    border: 1px solid var(--border-gray);
    border-radius: var(--space-xs);
    padding: var(--space-md);
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s;
}
```

**Verification**: Ensure 4 cards display in single row at 1024px width (no wrapping)

---

### 2. System Controls Panel Styling

**Location**: `src/ui/static/css/style.css`

**REMOVE** (line 145-150):
```css
/* DELETE THIS */
.panels-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-lg);
    margin-top: var(--space-lg);
}
```

**UPDATE** System Controls Panel (line 375-381):
```css
.system-controls-panel {
    background-color: var(--white);
    border: 1px solid var(--border-gray);
    border-radius: var(--space-xs);
    padding: var(--space-lg);
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-top: var(--space-lg); /* ADD: top margin since no longer in grid */
}
```

**ADD** Controls Header Styling:
```css
.controls-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-md);
    border-bottom: 1px solid var(--border-gray);
}

.controls-header h2 {
    margin: 0;
    font-size: var(--heading-size);
    color: var(--text-dark);
    font-weight: 600;
}
```

**UPDATE** Phase Toggle Container (line 222-228):
```css
.phase-toggle-container {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.phase-label-text {
    font-size: var(--label-size);
    color: var(--text-secondary);
    white-space: nowrap;
}
```

**PRESERVE** Device List Styling (already correct):
```css
.device-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.device-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 44px;
    padding: var(--space-xs) 0;
}
```

---

### 3. Growth Cycle CSS Removal

**DELETE ENTIRELY** (lines 152-219 approximately):
```css
/* DELETE ALL OF THESE RULES */
.growth-panel { ... }
.growth-phase-highlight { ... }
.growth-info-box { ... }
.growth-info-box .label { ... }
.growth-info-box .value { ... }
.phase-info { ... }
.phase-info > div { ... }
.phase-info .label { ... }
.phase-info .value { ... }
.phase-controls { ... }
.btn-phase { ... }
```

**KEEP** (but move after controls-header rules):
```css
.phase-toggle-container { ... }
.phase-label-text { ... }
```

---

### 4. Media Query Updates

**Location**: `src/ui/static/css/style.css` (line 526)

**UPDATE** 1024x600 Media Query:
```css
@media (max-width: 1024px) and (max-height: 600px) {
    :root {
        --space-lg: 20px;
        --space-md: 12px;
    }

    .sensor-card {
        padding: 12px;
    }

    .system-controls-panel {
        padding: 16px;
    }

    .controls-header {
        margin-bottom: 12px;
        padding-bottom: 12px;
    }

    /* DELETE: .growth-panel rule */
}
```

**UPDATE** Responsive Breakpoint (line 542):
```css
@media (max-width: 1023px) {
    .sensors-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    /* DELETE: .panels-container rule */
}
```

---

## Visual Validation Checklist

### Pre-Implementation Backup
- [ ] Create backup of `src/ui/templates/index.html` → `index.html.backup`
- [ ] Create backup of `src/ui/static/css/style.css` → `style.css.backup`
- [ ] Screenshot current UI at 1024x600 for comparison

### Layout Verification at 1024x600 Resolution

**Sensor Cards**:
- [ ] All 4 sensor cards visible in single horizontal row
- [ ] Equal width distribution (approx 230px each with 16px gaps)
- [ ] Cards aligned properly with consistent spacing
- [ ] Icons, values, progress bars, and targets all visible
- [ ] No text truncation or overflow

**System Controls Panel**:
- [ ] Card displays full width below sensor cards
- [ ] Header row contains "System Controls" text on left
- [ ] Vegetative/Flowering toggle positioned on right side of header
- [ ] Toggle labels display: "Vegetative (18/6)" and "Flowering (12/12)"
- [ ] Border line separates header from device list
- [ ] All 6 device control rows visible without scrolling

**Growth Cycle Panel**:
- [ ] Growth Cycle panel completely removed (not visible)
- [ ] No empty space or layout gaps where panel was

**Header & Footer**:
- [ ] Header displays Squad Apps logo, "GrowBox Control Panel" title, and Online status
- [ ] Footer displays "Powered by Squad Apps • Last sync: [time]"
- [ ] Header and footer preserved exactly as before

**Viewport Fit**:
- [ ] No horizontal scrolling required
- [ ] No vertical scrolling required
- [ ] All content fits within 1024x600 viewport
- [ ] Adequate spacing between elements (not cramped)

### Functionality Verification

**Device Toggles**:
- [ ] Grow Lights toggle works (on/off)
- [ ] Ventilation toggle works
- [ ] Water Pump toggle works
- [ ] Auto Mode toggle works
- [ ] CO₂ System toggle works
- [ ] Heater toggle works

**Phase Toggle**:
- [ ] Vegetative/Flowering toggle switches correctly
- [ ] Toggle visual state updates (slider moves)
- [ ] Label styling indicates active mode
- [ ] Backend API call triggers correctly (`/api/growth_phase/{phase}`)

**Sensor Updates**:
- [ ] Real-time sensor value updates display correctly
- [ ] Progress bars animate on value changes
- [ ] Color coding works (green/red based on range)
- [ ] Empty progress bars display for missing values ("-")

**WebSocket Connection**:
- [ ] Connection status indicator updates (Online/Offline)
- [ ] Real-time updates continue to work
- [ ] No console errors from missing DOM elements

### Visual Design Consistency

**Colors**:
- [ ] Background remains light gray (#F5F5F5)
- [ ] Cards remain white with gray borders
- [ ] Primary green used for toggles and progress bars
- [ ] Icon badge colors unchanged (red, blue, yellow)

**Typography**:
- [ ] Sensor values: 36px bold
- [ ] Headings: 20px semi-bold
- [ ] Labels: 14px regular
- [ ] Font family unchanged

**Spacing**:
- [ ] Consistent padding in cards (12-16px at 1024x600)
- [ ] Uniform gaps between elements (12-16px)
- [ ] Header and footer spacing preserved

**Icons**:
- [ ] Temperature icon (🌡) preserved
- [ ] Humidity icon (💧) preserved
- [ ] Light icon (☀) preserved
- [ ] Water icon (🚰) preserved

### Code Cleanup Verification

**HTML**:
- [ ] No commented-out Growth Cycle HTML remains
- [ ] No unused IDs or classes left in HTML
- [ ] Proper indentation maintained
- [ ] All closing tags correct

**CSS**:
- [ ] All growth cycle CSS rules removed
- [ ] No orphaned/unused selectors remain
- [ ] CSS file properly organized
- [ ] No duplicate rules

**JavaScript**:
- [ ] No console errors on page load
- [ ] No references to removed elements
- [ ] Event handlers for phase toggle verified working
- [ ] WebSocket handlers updated if needed

---

## Comparison Against Goal Mockup

**Reference**: `UIGoal.png`

**Visual Comparison Checklist**:
- [ ] Sensor cards layout matches goal (4 in horizontal row)
- [ ] System Controls card structure matches goal (single card with header)
- [ ] Phase toggle position matches goal (top-right of controls card)
- [ ] Growth Cycle panel removed as shown in goal
- [ ] Footer retained as shown in goal
- [ ] Overall spacing and proportions similar to goal

**Acceptable Deviations**:
- Icon designs may differ (goal is mockup, we keep current icons)
- Exact font rendering may vary slightly
- Minor spacing differences acceptable if layout intent preserved

---

## Testing Procedure

### Step 1: Visual Inspection
1. Open browser and navigate to `http://localhost:5000`
2. Set browser window to exactly 1024x600 pixels
3. Verify all checklist items above
4. Take screenshot for documentation

### Step 2: Interaction Testing
1. Toggle each device control (6 total)
2. Switch Vegetative/Flowering mode toggle
3. Verify backend API calls in browser DevTools Network tab
4. Confirm sensor values update via WebSocket

### Step 3: Responsive Testing
1. Test at 1024x600 (target resolution)
2. Test at 1023px width (breakpoint verification)
3. Test at 768px width (mobile verification)
4. Confirm no layout breakage at any size

### Step 4: Cross-Browser Testing
1. Test in Chrome/Edge (Chromium)
2. Test in Firefox
3. Test in Safari (if available)
4. Verify consistent rendering

---

## Success Criteria

**MUST PASS**:
- All 4 sensor cards visible in single row at 1024x600
- System Controls displays as single card with header containing toggle
- Growth Cycle panel completely removed
- No scrolling required at 1024x600
- All toggles functional
- No console errors

**SHOULD PASS**:
- Visual design matches goal mockup closely
- Spacing comfortable and not cramped
- Smooth transitions on toggle switches
- WebSocket real-time updates working

**MAY DIFFER**:
- Exact icon styling (current icons preserved)
- Minor font rendering differences
- Subtle spacing variations within reason

---

**Next Steps**: After visual validation passes, run cleanup tasks to remove commented code and verify final quality before merge.
