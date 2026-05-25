# Examples (Dash + Plotly)

These are patterns you can copy into real apps.

## 1) Minimal “good-looking” app skeleton (single page)

```python
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = px.data.gapminder().query("year==2007")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def make_fig(continent: str):
    dff = df if continent == "All" else df[df["continent"] == continent]
    fig = px.scatter(
        dff, x="gdpPercap", y="lifeExp", size="pop", color="continent",
        hover_name="country", log_x=True, size_max=40, template="plotly_white"
    )
    fig.update_layout(margin=dict(l=40, r=20, t=50, b=40), hovermode="closest")
    return fig

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H2("Gapminder Overview"), md=8),
                dbc.Col(
                    dcc.Dropdown(
                        id="continent",
                        options=[{"label": "All", "value": "All"}]
                        + [{"label": c, "value": c} for c in sorted(df["continent"].unique())],
                        value="All",
                        clearable=False,
                    ),
                    md=4,
                ),
            ],
            align="center",
            className="my-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Life Expectancy vs GDP"),
                            dbc.CardBody(
                                dcc.Graph(id="fig", config={"displayModeBar": False, "responsive": True})
                            ),
                        ]
                    ),
                    md=12,
                ),
            ],
            className="g-3",
        ),
        html.Div("Data source: plotly.express gapminder dataset", className="text-muted mt-3"),
    ],
    fluid=True,
)

@callback(Output("fig", "figure"), Input("continent", "value"))
def update_fig(continent):
    return make_fig(continent)

if __name__ == "__main__":
    app.run_server(debug=True)
```

## 2) Pattern: “data callback” → “render callbacks”
Use this when multiple charts use the same filtered data:
- One callback filters/aggregates and stores results in `dcc.Store`
- Other callbacks build charts from stored data

## References
- Dash Bootstrap Components layout docs: https://www.dash-bootstrap-components.com/docs/components/layout/
- Plotly theming/templates: https://plotly.com/python/templates/
