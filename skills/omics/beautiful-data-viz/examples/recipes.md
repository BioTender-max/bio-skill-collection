# Plot recipes (copy/paste friendly)

These are *patterns* — adjust to the specific dataset and story.

---

## Line chart (time series) with direct labeling

```python
import matplotlib.pyplot as plt
import pandas as pd
from assets.beautiful_style import set_beautiful_style, finalize_axes

set_beautiful_style(medium="notebook", background="light")

fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)

# df has columns: date, value, series
for name, g in df.groupby("series"):
    ax.plot(g["date"], g["value"], label=name)

# Direct-label last point (reduces legend + whitespace)
for name, g in df.groupby("series"):
    g = g.sort_values("date")
    ax.text(g["date"].iloc[-1], g["value"].iloc[-1], f"  {name}", va="center")

finalize_axes(
    ax,
    title="Metric over time",
    subtitle="Direct labels; subtle grid; tight layout.",
    xlabel=None,
    ylabel="Value (units)",
)
plt.show()
```

---

## Ranked dot plot (clean alternative to bars)

```python
import matplotlib.pyplot as plt
from assets.beautiful_style import set_beautiful_style, finalize_axes

set_beautiful_style(medium="notebook", background="light")

# df has columns: category, value
df_sorted = df.sort_values("value")

fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
ax.hlines(y=df_sorted["category"], xmin=0, xmax=df_sorted["value"], alpha=0.3)
ax.plot(df_sorted["value"], df_sorted["category"], marker="o", linestyle="")

finalize_axes(
    ax,
    title="Ranking",
    subtitle="Dot plot reduces ink and keeps labels readable.",
    xlabel="Value",
    ylabel=None,
)
plt.show()
```

---

## Heatmap (numeric matrix) with perceptually uniform colormap

```python
import seaborn as sns
import matplotlib.pyplot as plt
from assets.beautiful_style import set_beautiful_style, finalize_axes

set_beautiful_style(medium="notebook", background="light")

fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
sns.heatmap(matrix, cmap="crest", ax=ax, cbar_kws={"shrink": 0.8})

finalize_axes(ax, title="Heatmap", subtitle="Use perceptually uniform sequential colormaps.")
plt.show()
```

