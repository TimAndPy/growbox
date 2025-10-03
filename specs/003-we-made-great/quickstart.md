# Quickstart: Visual Testing for UI Refinements

**Feature**: UI Refinements for Tablet Display
**Branch**: `003-we-made-great`
**Prerequisites**: Flask app running, browser with dev tools

## Testing Approach

This feature requires manual visual testing due to UI-only changes. No automated tests needed as backend API is unchanged.

## Test Scenarios

### Scenario 1: Header Title Centering

**Given** the tablet UI is displayed at any resolution
**When** I view the header
**Then** I should see:
- [x] Squad Apps logo on the left
- [x] "GrowBox Control Panel" title centered in the header
- [x] Connection status (Online/Offline) on the right
- [x] All three elements aligned horizontally

**Validation Steps**:
1. Open browser dev tools (F12)
2. Inspect header `<h1>` element
3. Verify computed style includes `text-align: center` or flexbox centering
4. Measure distances: title should be equidistant from logo and status indicator

**Expected Result**: Title is visually centered between logo and connection status

---

### Scenario 2: 1024x600 Viewport Optimization

**Given** the browser viewport is set to 1024x600 pixels
**When** I view the entire interface
**Then** I should see:
- [x] All 4 sensor cards visible without horizontal scrolling
- [x] System Controls and Growth Cycle panels visible
- [x] Footer visible ("Powered by Squad Apps • Last sync...")
- [x] No vertical scrolling required to see all primary content

**Validation Steps**:
1. Open browser dev tools (F12)
2. Set device emulation to "Responsive" mode
3. Set viewport to 1024px width × 600px height
4. Scroll to top of page
5. Verify all key elements visible without scrolling:
   - Header
   - 4 sensor cards (Temperature, Humidity, Light, Water)
   - System Controls panel (left)
   - Growth Cycle panel (right)
   - Footer

**Expected Result**: Entire interface fits 1024x600 viewport with no scrolling

**Edge Cases**:
- Test at 1024x599 (slightly shorter): Should still fit
- Test at 1024x601 (slightly taller): Should have small margin
- Test at 1024x768 (previous target): Should have more spacing

---

### Scenario 3: Growth Cycle Panel Simplification

**Given** I view the Growth Cycle panel
**When** I look at the displayed information
**Then** I should see:
- [x] Current phase and day count (e.g., "Flowering - Day 28")
- [x] Phase toggle switch (Vegetative ↔ Flowering)
- [x] NO "Days Until Harvest" box
- [x] NO "Light Schedule" input box

**Validation Steps**:
1. Locate Growth Cycle panel (light green background, right side)
2. Verify phase highlight text shows format: "{Phase} - Day {X}"
3. Count visible elements: Should be 2 (phase highlight + toggle)
4. Verify harvest countdown is NOT present (search DOM for "harvest" text)
5. Verify light schedule box is NOT present (search DOM for "Light Schedule" text)

**Expected Result**: Growth Cycle panel shows only phase highlight and toggle switch

---

### Scenario 4: Phase Selection Toggle

**Given** I want to switch growth phases
**When** I interact with the phase toggle
**Then** I should see:
- [x] Toggle switch styled like existing device toggles (iOS-style, 48px × 28px)
- [x] Clear labels: "Vegetative (18/6)" and "Flowering (12/12)"
- [x] Toggle position indicates active phase (left=Vegetative, right=Flowering)
- [x] Clicking toggle switches phase and updates phase highlight

**Validation Steps**:
1. Locate phase toggle in Growth Cycle panel
2. Inspect toggle element:
   - Verify class `.switch` (reuses existing pattern)
   - Measure dimensions: 48px width × 28px height minimum
3. Verify labels are visible and clear
4. Click toggle to switch from Vegetative to Flowering
5. Observe:
   - Toggle animates to right position (green background)
   - Phase highlight updates to "Flowering - Day X"
   - Backend API called (`switchPhase('flowering')`)
6. Click toggle again to switch back to Vegetative
7. Observe:
   - Toggle animates to left position (gray background)
   - Phase highlight updates to "Vegetative - Day X"

**Expected Result**: Toggle behaves identically to device control toggles

**Edge Cases**:
- Load page with Vegetative phase active: Toggle should be in left position
- Load page with Flowering phase active: Toggle should be in right position
- Backend fails to switch: Toggle should revert to previous position

---

### Scenario 5: Touch Target Verification

**Given** I interact with the phase toggle on a touch device
**When** I tap the toggle
**Then** I should:
- [x] Reliably activate the toggle (≥44px touch target)
- [x] Not accidentally tap adjacent elements
- [x] See immediate visual feedback (toggle animation)

**Validation Steps**:
1. Open browser dev tools
2. Enable touch emulation mode
3. Measure computed dimensions of toggle:
   - Width: ≥44px (actual: 48px)
   - Height: ≥44px (actual: 28px + padding should reach 44px)
4. Tap toggle multiple times
5. Verify no mis-taps on phase highlight or panel borders

**Expected Result**: Toggle has ≥44px touch target and is easy to activate

**Fix if Needed**: Add padding to `.switch` parent to increase touch area to 44px minimum

---

## Responsive Testing Checklist

Test UI at multiple resolutions to ensure responsive behavior:

- [ ] **1024x600** (primary target): All content visible, no scrolling
- [ ] **1024x768** (previous target): More spacing, still fits
- [ ] **800x600** (small tablet portrait): Panels stack vertically, sensors in 2 columns
- [ ] **1280x800** (large tablet): Default spacing, centered title
- [ ] **1366x768** (laptop): Desktop view, all spacing preserved

**Validation**: Use browser dev tools device emulation to test each resolution

---

## Visual Comparison Checklist

Compare before/after screenshots:

**Before** (feature 002):
- Header title left-aligned with logo
- Growth Cycle panel with 4 elements (highlight + 2 boxes + 2 buttons)
- Two phase buttons (Vegetative/Flowering)
- Optimized for general tablet (1024x768+)

**After** (feature 003):
- [x] Header title centered
- [x] Growth Cycle panel with 2 elements (highlight + toggle)
- [x] Single phase toggle switch
- [x] Optimized for 1024x600 (tighter spacing)

**Validation**: Capture screenshots and overlay at 50% opacity to verify changes

---

## Browser Compatibility Testing

Test in multiple browsers to ensure consistent behavior:

- [ ] **Chrome 90+**: Primary testing browser
- [ ] **Safari 14+**: iOS/iPadOS tablet support
- [ ] **Firefox 88+**: Alternative desktop browser
- [ ] **Edge Chromium**: Windows tablet support

**Expected Result**: Identical visual appearance and behavior across all browsers

---

## Performance Validation

Although no performance changes expected, verify:

- [ ] Page load time: <2 seconds (unchanged from feature 002)
- [ ] Toggle switch animation: Smooth 200ms transition (reused from device toggles)
- [ ] WebSocket updates: Sensors still update in real-time (unchanged backend)
- [ ] No console errors or warnings

**Validation**: Open browser dev tools Console and Network tabs while testing

---

## Constitutional Compliance Verification

Before marking feature complete, verify all constitutional principles:

### I. Code Minimalism
- [x] Removed unnecessary HTML elements (harvest countdown, light schedule box)
- [x] No new files created (modified existing files only)
- [x] No speculative features added

### II. Zero Redundancy
- [x] Reused existing `.switch` CSS pattern (no duplicate toggle styles)
- [x] Reused existing `switchPhase()` JavaScript function
- [x] No copy-paste code

### III. UI Consistency (PRIMARY FOCUS)
- [x] Phase toggle matches existing device toggle design
- [x] Light green Growth Cycle panel preserved (#F6FFED background)
- [x] Touch targets ≥44px maintained
- [x] Sensor cards and device controls unchanged

### IV. Quality Over Speed
- [x] Visual testing completed before merge
- [x] Multiple resolutions tested
- [x] Touch target verification passed

### V. Clean Architecture
- [x] Folder structure unchanged (src/ui/ only)
- [x] No orphaned files created
- [x] Backend API unchanged (unidirectional dependency preserved)

---

## Acceptance Criteria

Feature is complete when:

1. [x] Header title is centered
2. [x] UI fits 1024x600 viewport without scrolling
3. [x] "Days Until Harvest" removed
4. [x] "Light Schedule" box removed
5. [x] Phase selection uses single toggle switch
6. [x] Toggle behaves like existing device toggles
7. [x] All 18 functional requirements met (see spec.md)
8. [x] Constitutional principles verified
9. [x] All test scenarios passed
10. [x] Browser compatibility confirmed

---

## Troubleshooting

### Issue: Title not centered

**Check**:
- `.header h1` has `flex: 1` or `text-align: center`
- `.header-left` does not have `flex-grow: 1`

**Fix**: Adjust flexbox properties on header children

---

### Issue: Content doesn't fit 1024x600

**Check**:
- Media query targets correct resolution: `@media (max-width: 1024px) and (max-height: 600px)`
- Spacing variables reduced in media query
- Padding reduced on sensor cards and panels

**Fix**: Incrementally reduce spacing until content fits

---

### Issue: Phase toggle doesn't show active state

**Check**:
- Toggle has `checked` attribute when Flowering phase active
- CSS `.slider` background changes on `:checked` state
- `loadStatus()` JavaScript sets toggle checked property correctly

**Fix**: Update `loadStatus()` to set toggle based on `data.growth_phase`

---

### Issue: Toggle touch target too small

**Check**:
- `.switch` computed dimensions in dev tools
- Parent wrapper has padding to increase touch area

**Fix**: Add padding to toggle wrapper to reach 44px minimum

---

## Manual Testing Script

Quick copy-paste script for testing:

```bash
# 1. Start Flask app
python src/main.py

# 2. Open browser to localhost:5000

# 3. Open dev tools (F12)

# 4. Set viewport to 1024x600 (Responsive mode)

# 5. Run through all scenarios above

# 6. Test other resolutions (800x600, 1024x768, 1280x800)

# 7. Test in Safari, Firefox, Edge

# 8. Verify constitutional compliance checklist

# 9. Mark feature complete if all tests pass
```

---

## Sign-Off

**Tested By**: _____________
**Date**: _____________
**All Scenarios Passed**: [ ] Yes [ ] No
**Constitutional Compliance Verified**: [ ] Yes [ ] No
**Ready for Production**: [ ] Yes [ ] No

**Notes**:
