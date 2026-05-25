# Dash Performance Guide (Fast, Scalable Dashboards)

## Performance principles

1) **Move expensive work out of the request loop**
- Cache results
- Pre-aggregate
- Use background callbacks for long tasks

2) **Make UI feel fast**
- Show loading states
- Disable triggering controls while running
- Provide progress for long jobs

3) **Render less**
- Reduce trace count
- Downsample time series
- Use WebGL traces for very large point clouds

## Background callbacks (job queue)

Use background callbacks when:
- a callback can exceed typical web server timeouts (~30s)
- multiple users may trigger expensive work

Backends:
- DiskCache: easiest for local dev
- Celery + Redis: recommended for production

Also consider:
- `running=[(Output(...), True, False)]` to disable controls
- `cancel=[Input(...)]` for cancelation
- progress outputs

## Caching strategies

- Cache at the data layer:
  - Load & filter once per “filter signature”
- Cache at the figure layer:
  - Only if figure building is expensive

Common patterns:
- `flask_caching` for memoization
- DiskCache/Celery for background work

## Large tables

Use `dash-ag-grid` for large datasets.
If a grid looks wrong, it’s often a CSS sizing issue: the grid fills its parent.

## References
- Background callbacks + job queues: https://dash.plotly.com/background-callbacks
- Advanced callbacks (running, prevent_initial_call, etc.): https://dash.plotly.com/advanced-callbacks
- Dash interactive graphing + WebGL mention: https://dash.plotly.com/interactive-graphing
- Dash AG Grid sizing guidance: https://dash.plotly.com/dash-ag-grid/grid-size
