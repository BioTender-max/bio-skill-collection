---
name: turingdb-introspection
description: Use when exploring an unfamiliar TuringDB graph, inspecting schema, navigating version history, or time-travelling to past commits.
---

# TuringDB: Introspection & Versioning

## Exploring an Unfamiliar Graph

Before writing queries against a graph you don't know, use these procedures to understand its shape:

```cypher
CALL db.labels()           -- all node labels
CALL db.edgeTypes()        -- all edge types
CALL db.propertyTypes()    -- all property keys and their data types
CALL db.history()          -- full commit history
```

```python
df = client.query("CALL db.labels()")
print(df)
#    id     label
# 0   0    Person
# 1   1      City
# 2   2  Interest

df = client.query("CALL db.edgeTypes()")
print(df)
#    id edgeType
# 0   0    KNOWS
# 1   1 LIVES_IN

df = client.query("CALL db.propertyTypes()")
print(df)
#    id propertyType valueType
# 0   0         name    String
# 1   1          age     Int64
# 2   2        score    Double
# 3   3         flag      Bool
# 4   4          emb Embedding
```

## Graph and Change Management

```cypher
LIST GRAPH              -- list all available graphs
CALL db.history()       -- show commit history
CHANGE LIST             -- list active uncommitted changes
```

```python
client.list_available_graphs()  # → list[str]
client.list_loaded_graphs()     # → list[str]
```

## Versioning / Time Travel

TuringDB stores an immutable commit history. You can query any past state without affecting the current graph.

```python
# View commit history
history = client.query("CALL db.history()")
print(history)
#              commit  numNodes  numEdges
# 0  a1b2c3d4(HEAD)       150       320
# 1  e5f6a7b8              120       280
# 2  c9d0e1f2              100       250

# The current HEAD commit has a (HEAD) suffix — strip it for programmatic use
commit_hash = str(history.iloc[1, 0])  # "e5f6a7b8" — a past commit

# Query a specific past commit
client.set_commit(commit_hash)
df = client.query("MATCH (n:Person) RETURN n.name")  # sees graph at that point in time

# Return to current HEAD
client.checkout()   # defaults to main, HEAD

# Switch to a specific change (without checking out)
client.set_change(change_id)

# Switch graph context
client.set_graph("other_graph")
```

**Gotcha:** You cannot create a new change while viewing a past commit. Always `client.checkout()` to return to HEAD first.

Via Cypher (REST API only — CLI and SDK handle this automatically):
```cypher
LOAD COMMIT 'abc123'
```

## Data Import

Import external files into a new graph. Files must be placed in the `data` subdirectory (`~/.turing/data` by default):

```cypher
-- GML files (all nodes get label GMLNode, all edges get type GMLEdge, properties become strings):
LOAD GML 'network.gml' AS my_graph

-- JSONL files (compatible with Neo4j APOC JSON export using useTypes:true):
LOAD JSONL 'export.jsonl' AS my_graph
```

```python
client.query("LOAD JSONL 'export.jsonl' AS imported_graph")
client.load_graph("imported_graph")
client.set_graph("imported_graph")
```

## Full SDK Method Reference

```python
# Graph management
client.list_available_graphs() → list[str]
client.list_loaded_graphs() → list[str]
client.create_graph(graph_name: str)
client.load_graph(graph_name: str, raise_if_loaded: bool = True)

# Query execution
client.query(query: str) → pandas.DataFrame

# Change workflow
client.new_change() → int                     # returns integer change ID
client.checkout(change: int | str = "main", commit: str = "HEAD")

# Version navigation
client.set_commit(commit: str)
client.set_change(change: int | str)
client.set_graph(graph_name: str)
```

All SDK errors raise `TuringDBException`.
