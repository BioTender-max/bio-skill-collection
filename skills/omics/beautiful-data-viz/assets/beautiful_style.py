"""Beautiful plotting defaults for matplotlib / seaborn.

Goal:
- Publication-quality plots with readable labels, minimal whitespace, and sensible defaults.
- Works in Jupyter notebooks.
- Matplotlib-first; uses seaborn if available for easier theming.

References:
- Seaborn aesthetics + palettes: https://seaborn.pydata.org/
- LearnUI palette guidance: https://www.learnui.design/tools/data-color-picker.html
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


@dataclass(frozen=True)
class VizConfig:
    medium: str = "notebook"      # notebook | paper | slides
    background: str = "light"     # light | dark
    font_scale: float = 1.0
    dpi: int = 150


def _maybe_set_retina() -> None:
    """Make notebook output crisper if running inside IPython."""
    try:
        from IPython import get_ipython  # type: ignore
        ip = get_ipython()
        if ip is not None:
            ip.run_line_magic("config", "InlineBackend.figure_format = 'retina'")
    except Exception:
        pass


def set_beautiful_style(*, medium: str = "notebook", background: str = "light", font_scale: float = 1.0, dpi: int = 150) -> VizConfig:
    """Set global plotting defaults.

    Parameters
    ----------
    medium:
        notebook | paper | slides
    background:
        light | dark
    font_scale:
        Additional scale factor applied to font sizes.
    dpi:
        Figure DPI for notebook rendering.
    """
    _maybe_set_retina()

    # Base size ladder (points)
    base = {
        "paper":   {"title": 11, "label": 9,  "tick": 8,  "legend": 8},
        "notebook":{"title": 13, "label": 11, "tick": 10, "legend": 10},
        "slides":  {"title": 18, "label": 14, "tick": 12, "legend": 12},
    }.get(medium, {"title": 13, "label": 11, "tick": 10, "legend": 10})

    title = base["title"] * font_scale
    label = base["label"] * font_scale
    tick = base["tick"] * font_scale
    legend = base["legend"] * font_scale

    is_dark = background.lower() == "dark"

    # Neutral ink colors (avoid pure black/white)
    fg = "#F3F4F6" if is_dark else "#111827"
    grid = "#374151" if is_dark else "#E5E7EB"
    face = "#111827" if is_dark else "#FFFFFF"

    rc = {
        # Figure / save
        "figure.dpi": dpi,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "figure.facecolor": face,
        "axes.facecolor": face,

        # Typography
        "font.family": "DejaVu Sans",
        "text.color": fg,
        "axes.labelcolor": fg,
        "axes.titlecolor": fg,
        "axes.titlesize": title,
        "axes.labelsize": label,
        "xtick.color": fg,
        "ytick.color": fg,
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,

        # Lines / markers
        "lines.linewidth": 2.0,
        "lines.markersize": 6,

        # Axes / spines
        "axes.edgecolor": grid,
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": grid,
        "grid.linewidth": 0.8,
        "grid.alpha": 0.6 if is_dark else 1.0,

        # Ticks
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,

        # Legend
        "legend.frameon": False,
        "legend.fontsize": legend,
        "legend.title_fontsize": legend,
    }

    mpl.rcParams.update(rc)

    # If seaborn is available, use it for coherent themes/palettes.
    try:
        import seaborn as sns  # type: ignore
        sns.set_theme(style="whitegrid", context=medium)
        sns.set_context(medium, font_scale=font_scale)
        sns.set_palette("colorblind")
    except Exception:
        pass

    return VizConfig(medium=medium, background=background, font_scale=font_scale, dpi=dpi)


def despine(ax: Axes) -> Axes:
    """Remove top/right spines and soften left/bottom."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_alpha(0.8)
    ax.spines["bottom"].set_alpha(0.8)
    return ax


def minimize_whitespace(ax: Axes, *, x: float = 0.02, y: float = 0.05) -> Axes:
    """Reduce default margins while keeping slight breathing room."""
    ax.margins(x=x, y=y)
    return ax


def finalize_axes(
    ax: Axes,
    *,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    tight: bool = True,
) -> Axes:
    """Apply final presentation tweaks."""
    despine(ax)
    minimize_whitespace(ax)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if title:
        ax.set_title(title, loc="left", pad=10, weight="semibold")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, ha="left", va="bottom")

    # Prefer y-grid only for most charts
    ax.xaxis.grid(False)

    if tight:
        fig = ax.figure
        if isinstance(fig, Figure):
            try:
                fig.tight_layout()
            except Exception:
                pass

    return ax

