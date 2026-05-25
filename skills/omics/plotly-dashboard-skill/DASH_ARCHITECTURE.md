# Dash Architecture Guide (Maintainable Apps)

## Recommended project structure

Single-page (small apps):
```
my_app/
  app.py
  assets/
    styles.css
  utils/
    data.py
    figures.py
  README.md
```

Multi-page (recommended for growth):
```
my_app/
  app.py
  pages/
    overview.py
    drilldown.py
  components/
    header.py
    filters.py
    cards.py
  callbacks/
    overview_callbacks.py
    drilldown_callbacks.py
  utils/
    data.py
    transforms.py
    figures.py
  assets/
    styles.css
  README.md
  data_dictionary.md
```

## Multi-page apps (Dash Pages)

Use Dash Pages for URL routing and structure.

Pattern:
- `app = Dash(__name__, use_pages=True)`
- Create `pages/` modules and register each page.

## Callback rules (readability + maintainability)

1) Separate layout from callbacks
- Layout modules should mostly define components
- Callback modules define interactivity

2) Keep callbacks “about one thing”
- Avoid callbacks that both transform data and build many outputs.
- Extract transforms into `utils/transforms.py`.

3) Prefer `dcc.Store` for shared intermediate results
Store expensive pre-aggregations once, then feed multiple charts.

4) Avoid callback spaghetti
- Don’t chain callbacks unless needed.
- Prefer one “data callback” → many “render callbacks” (fan-out pattern).

## Advanced callback tools you should use

- `PreventUpdate`: stop updating outputs until inputs are valid
- `dash.no_update`: update only some outputs
- `prevent_initial_call=True`: avoid unnecessary initial work
- `ctx.triggered_id`: handle multi-input callbacks cleanly
- `running=[(...)]`: disable buttons/inputs while callback runs

## References
- Dash Pages (multi-page apps): https://dash.plotly.com/urls
- Dash advanced callbacks: https://dash.plotly.com/advanced-callbacks
- Dash callback organization best practices: https://dash-resources.com/dash-callbacks-best-practices-with-examples/ (updated 2025)
- Common Dash app architecture patterns: https://deepwiki.com/plotly/dash-sample-apps/9-best-practices-and-common-patterns
