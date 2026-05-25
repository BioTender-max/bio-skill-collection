# Beautiful Data Viz Checklist

Use this as a final QA pass before you declare a chart “done”.

## 1) Integrity (never tell a lie)

- Encodings match semantics (ordered data → ordered axis; categories → discrete encodings).
- Axes scales are appropriate (avoid deceptive truncation unless explicitly justified and clearly labeled).
- Uncertainty is represented when it matters (CI bands, error bars, quantiles).
- Aggregations are explicit (mean vs median; rolling window; binning).

## 2) Readability (works at the size it will be seen)

- Tick labels are readable at the target embed size (no overlaps, no micro-font).
- Labels include **units** and use consistent numeric formatting (%, $, thousands separators).
- Long category names are wrapped, abbreviated, or switched to a horizontal layout (barh / dot plot).

## 3) Visual hierarchy (the viewer sees what matters first)

- One primary element (data marks) gets the most contrast.
- Secondary elements (grid, spines, annotations) are quieter.
- Titles and annotations explain the “so what” without duplicating axis labels.

## 4) Layout and whitespace (tight but not cramped)

- Use `constrained_layout=True` or `fig.tight_layout()`; avoid accidental huge margins.
- Legends don’t create a dead column/row of whitespace.
- If labels/legend must be outside the axes, resize the figure to compensate (don’t just shrink the data area).
- Export with `bbox_inches="tight"` and small `pad_inches`.

## 5) Color and accessibility

- Palette type matches data (qualitative / sequential / diverging).
- Do not encode meaning using color alone when shape/position could do it better.
- Palette is distinguishable under common color-vision deficiencies and in grayscale (when practical).
- Limit categorical palette length; if > 8–10 categories, consider grouping, small multiples, or annotation.

## 6) Finishing touches

- Remove chart junk (gratuitous borders, heavy grids, 3D, shadows).
- Prefer direct labels for a small number of series; otherwise use a clean legend.
- Use consistent styling across figures in a deck/paper (same palette + typography + line widths).

