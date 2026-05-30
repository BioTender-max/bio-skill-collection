---
id: figure_styling_skills_index
name: Figure Styling Skills Index
description: |
  Aesthetic guidelines for scientific figure production. Each style file
  specifies palettes, typography, layout, and domain-specific sub-styles
  for a given target venue (NeurIPS, Nature, IEEE, etc.) and figure class
  (methodology diagram vs. statistical plot). Used by the Graph Maker
  Team's `illustrator` and `data_plotter` agents.
---

# Figure Styling Skills

Resources for the Graph Maker Team's `illustrator` (diagram) and `data_plotter` (plot) agents. The leader writes `aesthetic_guide: <style_id>` into `style_card.json`; the producing agent then loads the matching style file listed below.

## Available styles

| Style ID | File | Target | Figure class |
|---|---|---|---|
| `neurips_diagram` | [styles/neurips_diagram.md](./styles/neurips_diagram.md) | NeurIPS / top ML venues | Methodology / framework / pipeline diagrams |
| `neurips_plot` | [styles/neurips_plot.md](./styles/neurips_plot.md) | NeurIPS / top ML venues | Statistical plots (bar, line, scatter, heatmap, …) |

## How to use

1. Leader sets `aesthetic_guide: "<style_id>"` in `{workdir}/inputs/style_card.json`.
2. Sub-agent (illustrator / data_plotter) consults this skill index, then reads the style file whose id matches `aesthetic_guide`.
3. Agent applies the guidance alongside `style_card.json`. Priority chain for conflicts:
   **user references > style_card.json > figure_styling/<style_id> > internal defaults**.

If `aesthetic_guide` is `custom` or `null`, sub-agents do not load any file from this skill — they rely purely on `style_card.json` and their internal defaults.

## Custom styles

Users can drop additional `.md` files into `styles/` (e.g. `nature_figure.md`, `ieee_figure.md`, `my_lab_style.md`) following the same section structure as the NeurIPS guides. Set `aesthetic_guide: "<new_style_id>"` in `style_card.json` to activate.
