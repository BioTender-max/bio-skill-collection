# Palette selection (categorical / sequential / diverging)

This file explains *how to choose colors*, not just *which colors*.

## 1) Decide palette type

Seaborn’s palette tutorial organizes palettes into three broad classes (choose the class first):

- **Qualitative** (categorical): mostly hue variation
- **Sequential** (numeric): mostly luminance variation
- **Diverging** (numeric with midpoint): two hues with a neutral center

Reference: https://seaborn.pydata.org/tutorial/color_palettes.html

## 2) Categorical palettes: “visually equidistant” matters

LearnUI’s data color picker emphasizes building palettes where colors are *visually equidistant*, which makes categories easier to distinguish and match to keys.

Reference: https://www.learnui.design/tools/data-color-picker.html

### Practical guidance
- Prefer 3–8 categories. Above that, consider small multiples or grouping.
- If you generate a custom palette, pick endpoint hues that are far apart (warm vs cool) so the internal steps remain distinct.
- If using a brand color, adjust saturation/brightness for better harmony; hue does most of the recognition work.

### Seaborn options
- `sns.color_palette("colorblind", n_colors=n)`
- `sns.color_palette("Set2", n_colors=n)` (ColorBrewer)
- `sns.color_palette("husl", n_colors=n)` when you need many distinct hues

## 3) Sequential palettes

Use sequential maps for numeric magnitude. Seaborn includes perceptually uniform sequential colormaps (`rocket`, `mako`, `flare`, `crest`) and you can use matplotlib’s (`viridis`, `magma`, …).

Guideline: if you’re coloring **lines/points**, avoid palettes whose endpoints wash out against the background (especially white/gray).

Reference: https://seaborn.pydata.org/tutorial/color_palettes.html

## 4) Diverging palettes

Use diverging palettes when your data diverges around a meaningful midpoint (e.g., 0, baseline, target). LearnUI’s Divergent Scale generator is designed for this.

Reference: https://www.learnui.design/tools/data-color-picker.html

Guideline: keep the midpoint close to neutral, and be careful that mid-tones don’t collapse into the same muddy color.

## 5) Minimal “inspired” palettes

Below are *example* palettes you can use as starting points. They’re intentionally balanced (mid-saturation, varied hue spacing) and work well on light backgrounds.

Tip: prefer to generate/confirm palettes with LearnUI’s tool for your exact background and number of categories.

```python
# Example categorical palettes (hex)
IBB_SOFT_6 = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]
IBB_BOLD_6 = ["#1D4ED8", "#059669", "#D97706", "#DC2626", "#6D28D9", "#0E7490"]

# Example diverging endpoints (use with a neutral midpoint)
DIVERGE_WARM_COOL = {"low": "#2563EB", "mid": "#E5E7EB", "high": "#DC2626"}
```

## 6) Quick code patterns

```python
import seaborn as sns

# Categorical
palette = sns.color_palette("colorblind", n_colors=6)

# Sequential colormap
cmap = sns.color_palette("crest", as_cmap=True)

# Diverging palette (custom list)
palette = ["#2563EB", "#93C5FD", "#E5E7EB", "#FCA5A5", "#DC2626"]
```

