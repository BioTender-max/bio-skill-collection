# Dashboard UI Style Guide (Dash + Plotly)

This file focuses on **readability, hierarchy, and consistency** — the things that make dashboards feel “designed”.

## Layout rules

### Prefer a predictable structure
Use one of these, consistently:
- Header → Filters → Content grid → Footer
- Left rail filters → Content grid
- Overview page → Drilldown page(s)

### Use an 8px spacing system
Pick a spacing scale and stick to it:
- 4, 8, 12, 16, 24, 32, 48

**Common pattern**
- Page padding: 24
- Card padding: 16
- Card gap: 16
- Section spacing: 24–32

### Use “cards” for grouping
Each card should have:
- A short title
- Optional subtitle (“last 30 days”, “vs previous period”)
- One primary chart or KPI
- Optional footnote (data caveat, source)

## Typography rules

### Choose one font family
Use one font for everything:
- UI components
- Headings
- Charts

A safe default:
- `Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif`

### Clear hierarchy
Recommended sizes (web):
- H1 page title: 24–28
- Section title: 16–18 (bold)
- Body: 13–14
- Small labels / helper text: 12

### Use sentence case
Avoid ALL CAPS except tiny labels.

## Color rules

### Don’t overuse color
- Use neutrals for structure (background, borders, text)
- Use color only when it encodes meaning or guides attention

### Reserve semantic colors
If you can, reserve:
- Green = good / increase
- Red = bad / decrease
- Gray = neutral / no data

### Make colors distinguishable
For categorical charts:
- Prefer palettes that are *visually equidistant*
- Avoid multiple near-identical hues (e.g., 4 blues)

See [PALETTES.md](PALETTES.md).

## Chart readability rules

### Default to “plotly_white” style (or equivalent)
- White plot background
- Light y-grid lines
- No heavy borders

### Reduce visual noise
- Remove chart junk: unnecessary gridlines, thick axis lines, redundant legends
- Prefer horizontal legend at top (space-efficient)

### Tooltips must include units
A tooltip that only shows “1234” is not acceptable.
Always include:
- Metric name
- Value with units
- Time period / category label

### Keep axes honest and readable
- Label the axis *or* embed the unit in the title (don’t do both inconsistently)
- Format large numbers (K/M/B)
- Use date tick formatting (e.g., “Jan 2026”)

## Interaction rules

### Filters should be obvious and grouped
- Group filters by type (time, geography, product)
- Provide sensible defaults
- Put “Advanced” filters behind a collapsible panel

### Cross-filtering: only if it’s predictable
If clicking a chart filters others, add:
- Visual feedback (selection highlight)
- “Clear selection” action
- Microcopy hint (“Click bars to filter”)

## Accessibility & inclusivity

- Don’t encode meaning by color alone (use labels, shapes, ordering).
- Ensure sufficient contrast for text.
- Avoid red/green as the only distinguishing pair.

## References
- Dash dashboard design principles: https://dash-resources.com/a-guide-to-beautiful-dashboards-basic-design-principles/ (2025)
- Learn UI Design color guidance + equidistant palettes: https://www.learnui.design/tools/data-color-picker.html
- Learn UI Design article (palette types): https://www.learnui.design/blog/picking-colors-for-your-data-visualizations.html
