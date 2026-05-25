# Color Palettes for Dash + Plotly

This file gives **ready-to-use palettes** and rules for using them in dashboards.

## 1) Pick the right palette type

- **Categorical / Multi-hue**: categories (regions, products)
- **Sequential (single-hue)**: magnitude (low → high)
- **Diverging (two-hue)**: negative → neutral → positive

The Learn UI Design tools are great for generating *visually equidistant* palettes and scales.

## 2) Ready-to-use categorical palettes

### A) “Flat UI Classic” (high contrast, vibrant)
Source: ColorsWall “Flat UI Colors Codes”

```python
FLAT_UI_CLASSIC = [
    "#1abc9c",  # Turquoise
    "#2ecc71",  # Emerald
    "#3498db",  # Peter River
    "#9b59b6",  # Amethyst
    "#34495e",  # Wet Asphalt
    "#16a085",  # Green Sea
    "#27ae60",  # Nephritis
    "#2980b9",  # Belize Hole
    "#8e44ad",  # Wisteria
    "#2c3e50",  # Midnight Blue
    "#f1c40f",  # Sunflower
    "#e67e22",  # Carrot
    "#e74c3c",  # Alizarin
    "#95a5a6",  # Concrete
    "#7f8c8d",  # Asbestos
]
```

### B) “LearnUI Design” (muted, modern)
Source: Color-Hex palette “Learnui Design”

```python
LEARNUI_DESIGN = [
    "#003f5c",
    "#7a5195",
    "#ef5675",
    "#ffa600",
    "#aaaaaa",
]
```

### C) Plotly built-ins
Plotly Express includes qualitative palettes (e.g., `px.colors.qualitative.*`).
If you don’t want to ship custom hex codes, prefer built-ins.

## 3) How to apply palettes in Plotly

Use `colorway` (global per figure / template):

```python
import plotly.graph_objects as go

fig.update_layout(colorway=FLAT_UI_CLASSIC)
```

Or set via template (recommended; see FIGURE_STYLE.md).

## 4) Palette usage rules (to keep dashboards readable)

- Aim for **6–8 distinct** categorical colors per view.
- If you have > 8 categories, switch to:
  - top-N + “Other”, or
  - small multiples, or
  - a table
- Don’t use saturated colors for backgrounds; keep backgrounds neutral.
- Keep semantic color meaning consistent (e.g., red = negative).

## References
- Learn UI Design Data Viz Color Picker: https://www.learnui.design/tools/data-color-picker.html
- Learn UI Design article on palette types: https://www.learnui.design/blog/picking-colors-for-your-data-visualizations.html
- Flat UI hex codes list: https://colorswall.com/colors/flat-ui/
- “Learnui Design” palette values: https://www.color-hex.com/color-palette/103612
