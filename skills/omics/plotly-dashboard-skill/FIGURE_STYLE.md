# Plotly Figure Style Guide (Templates + Helpers)

Goal: **Every chart looks like it belongs in the same product.**

This is achieved by:
1) A global Plotly **template**
2) A few helper functions to apply formatting consistently

## 1) Recommended template defaults

Start from `plotly_white` and override:
- font family/size
- `colorway`
- margins
- legend
- hover label
- grid styling

### Example: create and register a template

```python
import plotly.io as pio
import plotly.graph_objects as go

DASH_COLORWAY = [
    "#3498db",  # blue
    "#2ecc71",  # green
    "#e67e22",  # orange
    "#9b59b6",  # purple
    "#e74c3c",  # red
    "#1abc9c",  # teal
]

dash_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif", size=13),
        title=dict(font=dict(size=16)),
        colorway=DASH_COLORWAY,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=48, r=20, t=56, b=44),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            title_text="",
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            ticks="outside",
            ticklen=4,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)",
            zeroline=False,
            ticks="outside",
            ticklen=4,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
        ),
    )
)

pio.templates["dash_ui"] = dash_template
pio.templates.default = "dash_ui"
```

## 2) Helper functions (high leverage)

### A) Standard number formatting
Use `tickformat` and `hovertemplate`:
- Percent: `.1%`
- Thousands separators: `,.0f`
- Currency (simple): `$,.0f`

Example:

```python
def format_currency(fig, axis="y"):
    fig.update_layout({f"{axis}axis": dict(tickprefix="$", separatethousands=True)})
    return fig
```

### B) Consistent titles and subtitles
Use:
- `fig.update_layout(title="Title", subtitle="...")` is not native everywhere.
Instead, consider a small annotation for subtitles:

```python
def add_subtitle(fig, subtitle: str):
    fig.add_annotation(
        text=subtitle,
        xref="paper",
        yref="paper",
        x=0,
        y=1.08,
        showarrow=False,
        align="left",
        font=dict(size=12, color="rgba(0,0,0,0.6)"),
    )
    return fig
```

### C) Preserve zoom / UI state during updates
If a graph updates often (e.g., filter changes), set `uirevision`:
```python
fig.update_layout(uirevision="keep")
```

## 3) Dash `dcc.Graph` configuration

Recommended defaults:
- Responsive resizing
- Minimal modebar (or hidden)
- Scroll zoom off unless required

```python
dcc.Graph(
    id="sales-trend",
    figure=fig,
    config={
        "displayModeBar": False,
        "scrollZoom": False,
        "responsive": True,
    },
)
```

## References
- Plotly templates & theming: https://plotly.com/python/templates/
- Dash Graph component docs (configuration, Plotly.js relationship): https://dash.plotly.com/dash-core-components/graph
