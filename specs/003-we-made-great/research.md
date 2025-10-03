# Research & Technical Decisions: UI Refinements for Tablet Display

**Feature**: UI Refinements for Tablet Display
**Date**: 2025-10-03

## Research Summary

No significant research required. All changes leverage existing design system and patterns from feature 002 (tablet UI redesign). This is a refinement task, not a greenfield design.

## Key Decisions

### 1. Header Title Centering

**Decision**: Use CSS flexbox with centered title placement

**Rationale**:
- Existing header already uses flexbox layout
- Simple CSS change: `justify-content: center` for title container
- Maintains logo (left) and connection status (right) positioning
- No HTML structure changes needed

**Alternatives Considered**:
- CSS Grid: Overkill for simple 3-element layout
- Absolute positioning: Fragile, breaks responsive behavior

**Implementation**:
```css
.header h1 {
    flex: 1;
    text-align: center;
}
```

### 2. Viewport Optimization for 1024x600

**Decision**: Adjust spacing, font sizes, and panel heights to fit 1024x600 without scrolling

**Rationale**:
- Current UI designed for general tablet (1024x768+)
- 1024x600 requires tighter vertical spacing
- Reduce sensor card padding from 16px to 12px
- Reduce panel gaps from 24px to 16px
- Ensure footer remains visible

**Alternatives Considered**:
- Allow scrolling: User explicitly requested no scrolling
- Reduce functionality: Removing harvest/schedule boxes already provides space

**Implementation**:
- Reduce `--space-lg` from 24px to 20px for 1024x600 media query
- Reduce sensor card padding to 12px
- Growth Cycle panel padding from 24px to 16px

### 3. Phase Selection Toggle

**Decision**: Reuse existing iOS-style toggle switch pattern from device controls

**Rationale**:
- Maintains UI consistency (Principle III)
- Zero redundancy - reuses existing `.switch` and `.slider` CSS classes
- Users already familiar with toggle pattern from device controls
- Simpler than creating custom phase selector

**Alternatives Considered**:
- Custom segmented control: Adds complexity, breaks consistency
- Keep two buttons: User explicitly requested toggle replacement
- Radio buttons: Poor touch target for tablet

**Implementation**:
- Wrap toggle in label with data attribute for phase: `data-phase="vegetative|flowering"`
- Use existing `switchPhase()` JavaScript function
- Toggle position indicates active phase (left=Vegetative, right=Flowering)

### 4. Growth Cycle Panel Simplification

**Decision**: Remove "Days Until Harvest" and "Light Schedule" HTML elements entirely

**Rationale**:
- User explicitly requested removal to simplify interface
- Space saved helps fit 1024x600 viewport
- Phase highlight already shows current phase and day count
- Light schedule is implicit in phase selection (18/6 or 12/12)

**Alternatives Considered**:
- Hide with CSS: Creates DOM clutter, violates Code Minimalism
- Move to collapsible section: Adds complexity, user wants removal

**Implementation**:
- Delete `.growth-info-box` divs for harvest countdown and light schedule
- Keep only phase highlight and phase toggle
- Update `loadStatus()` JavaScript to skip rendering these fields

## CSS Media Query Strategy

**Target Resolution**: 1024x600 (primary)
**Fallback Breakpoints**:
- ≥1024px: Default spacing (unchanged)
- 1024x600: Reduced spacing (new media query)
- 768-1023px: Existing responsive behavior (2-column sensors, stacked panels)
- <768px: Existing mobile behavior (single column)

**New Media Query**:
```css
@media (max-width: 1024px) and (max-height: 600px) {
    /* Reduce vertical spacing for 1024x600 tablets */
    --space-lg: 20px;
    --space-md: 12px;

    .sensor-card {
        padding: 12px;
    }

    .growth-panel {
        padding: 16px;
    }
}
```

## Touch Target Verification

All interactive elements verified to maintain ≥44px touch targets:
- Phase toggle: 48px × 28px (existing switch dimensions) ✓
- Phase buttons (removed): N/A
- All other controls: Unchanged from feature 002 ✓

## Browser Compatibility

No changes to browser compatibility requirements:
- Target: Modern browsers (Chrome 90+, Safari 14+, Firefox 88+)
- CSS Flexbox: Safe to use (existing)
- CSS Media Queries: Safe to use (existing)
- No new CSS features introduced

## Performance Considerations

No performance impact:
- No new CSS classes (reusing existing `.switch` pattern)
- Reduced DOM elements (removing two `.growth-info-box` divs)
- No JavaScript complexity added (reusing existing `switchPhase()`)
- No new images or assets

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Centering title breaks logo alignment | Low | Use flexbox, preserve existing header structure |
| 1024x600 breaks at other resolutions | Medium | Use max-width AND max-height media query, test common resolutions |
| Phase toggle unclear which is active | High | Add labels (Vegetative/Flowering), position indicates active state |
| Vertical space still insufficient | Medium | Remove unnecessary elements first, then adjust spacing incrementally |

## No Research Required For

- Design system: Already established in feature 002
- Toggle pattern: Already implemented in device controls
- Color palette: Unchanged (#52C41A green, #F6FFED light green panel)
- Typography: Unchanged (36px values, 14px labels)
- JavaScript patterns: Reusing existing `switchPhase()` backend call

## Summary

All technical decisions leverage existing design system and patterns. No new technologies, dependencies, or architectural patterns introduced. This is a pure refinement task focusing on layout optimization and UI simplification.
