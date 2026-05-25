---
name: turingdb-startup
description: Use when TuringDB needs to be started before querying — finds the binary in the project's virtual environment, starts the server if not already running, connects with the SDK, and loads a graph ready for exploration.
---

# TuringDB: Startup & Connection

## Step 1 — Ensure turingdb is installed

Check whether the package is available, and install it if not:

```bash
uv add turingdb
```

If the project doesn't use uv, fall back to:

```bash
pip install turingdb
```

## Step 2 — Check if the server is already running

Try connecting first. If it succeeds, skip to Step 4.

```python
from turingdb import TuringDB

try:
    client = TuringDB(host="http://localhost:6666")
    client.list_loaded_graphs()
    print("Server already running")
    # skip to Step 4
except Exception:
    print("Server not running, starting it...")
    # continue to Step 3
```

Note: `host` is the full URL (`http://localhost:6666`), not a hostname with a separate `port` argument.

## Step 3 — Find and start the binary

The binary has `start` and `stop` subcommands (`start` is the default if omitted). **Flags use a single dash**: `-turing-dir`, `-demon`, `-load`, `-p`, `-i`.

Useful flags:
- `-turing-dir <path>` — root data directory (contains `graphs/`, `data/`, etc.)
- `-demon` — run as background daemon
- `-load <graph>` — load a graph at startup (saves a separate `load_graph()` call)
- `-p <port>` — override default port 6666
- `-in-memory` — don't persist writes to disk
- `-ui` — launch the browser visualizer proxy on port 8080

Try each invocation in order, stopping at the first one that works:

```bash
# Option 1: uv project (recommended — uv resolves the venv automatically)
uv run turingdb start -turing-dir <path> -demon

# Option 2: uv-managed venv at standard location
.venv/bin/turingdb start -turing-dir <path> -demon

# Option 3: standard Python venv
venv/bin/turingdb start -turing-dir <path> -demon

# Option 4: activated venv or global install
turingdb start -turing-dir <path> -demon
```

To load a graph at the same time as starting the server:
```bash
uv run turingdb start -turing-dir <path> -load <graph_name> -demon
```

After starting, verify the server is up:

```python
from turingdb import TuringDB

client = TuringDB(host="http://localhost:6666")
client.list_loaded_graphs()  # raises if not ready
print("Server started successfully")
```

If the server fails to start, re-run Step 1 to confirm installation succeeded.

## Step 4 — List and load a graph

```python
available = client.list_available_graphs()  # all graphs on disk
print("Available graphs:", available)       # → ['mygraph', 'default']

loaded = client.list_loaded_graphs()        # graphs currently in memory
print("Already loaded:", loaded)            # → ['default']
```

If the graph you want is not already loaded, load it and set it as the current context:

```python
client.load_graph("my_graph")   # loads into memory — raises TuringDBException if already loaded
client.set_graph("my_graph")    # set SDK context — required before querying
```

If no graphs exist yet, create one and set it as the current context:

```python
client.create_graph("my_graph")  # raises TuringDBException if name already taken
client.set_graph("my_graph")
```

**Idempotent helper pattern** (safe to call repeatedly):

```python
from turingdb import TuringDB, TuringDBException

client = TuringDB(host="http://localhost:6666")
try:
    client.create_graph("my_graph")
except TuringDBException:
    pass  # already exists
try:
    client.load_graph("my_graph")
except TuringDBException:
    pass  # already loaded
client.set_graph("my_graph")
```

## Step 5 — Explore the graph

Once connected and a graph is loaded, read `introspection.md` (in this same directory) to map the shape of the data:

```python
df_labels     = client.query("CALL db.labels()")
df_edge_types = client.query("CALL db.edgeTypes()")
df_props      = client.query("CALL db.propertyTypes()")
```

Print these results before writing any queries — they tell you what node labels, edge types, and properties exist.

## Stopping the server

You **must** pass the same `-turing-dir` used at startup — otherwise `stop` looks at the default `~/.turing` and reports no instance found.

```bash
# If started with -turing-dir:
uv run turingdb stop -turing-dir <path>

# Default data directory (~/.turing):
uv run turingdb stop
```
