# Plot styling rules (pretty + minimal whitespace)

## Goals
- Compact figures with **minimal whitespace**
- Consistent typography and sizing
- A cohesive, **non-default** palette that’s still readable
- Clean axes (no chart junk)

## Matplotlib baseline (recommended)
Put this in an early “Plot styling” cell.

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

# A cohesive, non-default palette (feel free to swap)
PALETTE = [
    "#0B1320",  # deep ink
    "#2C7DA0",  # ocean
    "#5C4D7D",  # dusk purple
    "#F1C453",  # warm sand
    "#E85D75",  # rose
    "#43AA8B",  # mint
]

def set_plot_style() -> None:
    mpl.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "figure.figsize": (8, 4.5),
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=PALETTE),
        # Tight layout defaults
        "figure.constrained_layout.use": True,
    })

set_plot_style()
```

## Whitespace control
- Prefer `constrained_layout=True` (global) or `plt.tight_layout()` (local).
- When saving: `bbox_inches="tight", pad_inches=0.05`.

Example:
```python
fig, ax = plt.subplots(figsize=(7.5, 4.0))
# ... plotting ...
fig.savefig(OUT_DIR / "figure.png", bbox_inches="tight", pad_inches=0.05)
```

## Annotation conventions
- Always label axes (with units if relevant).
- Titles are short; subtitles go in markdown.
- Legends only when needed; place outside if crowded.

## “Pretty plot” checklist
- readable fonts and sizes
- meaningful ticks (not 1000 tick labels)
- consistent palette across plots
- no overlapping labels
- compact margins

## If the notebook uses many plots
Create a helper like:
```python
def finalize(ax, title: str | None = None):
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.25)
    return ax
```
