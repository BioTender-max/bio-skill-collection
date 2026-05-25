---
name: turingdb-algorithms
description: Use when running graph algorithms in TuringDB — shortest path (Dijkstra) and vector/embedding similarity search.
---

# TuringDB: Algorithms

## Shortest Path

Uses Dijkstra's algorithm to find the shortest route between nodes, weighted by an edge property.

```cypher
MATCH (a:Station {name: 'Ashchurch'}), (b:Station {name: 'Worcestershire Parkway'})
shortestPath(a, b, distance, dist, path)
RETURN dist, path
```

```python
df = client.query("""
    MATCH (a:Station {name: 'Ashchurch'}), (b:Station {name: 'Worcestershire Parkway'})
    shortestPath(a, b, distance, dist, path)
    RETURN dist, path
""")
print(df)
#    dist          path
# 0  11.29  [0, 1, 6]
```

Signature: `shortestPath(source, target, edge_weight_property, dist_var, path_var)`

- `edge_weight_property` — the edge property to use as the weight (bare identifier, no quotes)
- `dist_var` — output variable for the total distance
- `path_var` — output variable for the path (list of internal node/edge IDs)

**Multiple sources/targets:** Pass multiple nodes as source or target — the algorithm returns the best result across all combinations:

```cypher
MATCH (a:Station), (b:Station {name: 'London Euston'})
WHERE a.name = 'Birmingham' OR a.name = 'Manchester'
shortestPath(a, b, distance, dist, path)
RETURN dist, path
```

**Return either or both outputs:**

```cypher
RETURN dist          -- distance only
RETURN path          -- path only
RETURN dist, path    -- both
```

**Gotcha:** Variables used as source or target are consumed by `shortestPath` and **cannot appear in RETURN**. To return properties of the endpoints, add an extra variable in the same MATCH clause:

```cypher
-- Wrong: a and b cannot appear in RETURN
MATCH (a:Station {name: 'A'}), (b:Station {name: 'B'})
shortestPath(a, b, distance, dist, path)
RETURN a.name, dist   -- ERROR

-- Correct: add a third variable in the same MATCH for data you want to return
MATCH (a:Station {name: 'A'}), (b:Station {name: 'B'}), (start:Station {name: 'A'})
shortestPath(a, b, distance, dist, path)
RETURN start.name, dist, path
```

---

## Vector Search

TuringDB has built-in k-nearest-neighbor search over high-dimensional embeddings.

Vector indexes live at the TuringDB root level, **independent of graphs and versioning**. A single vector index can serve searches across multiple graphs. Each vector is associated with a numerical ID that you use to join search results back to graph nodes.

### Create index (one-time, outside a change)

```cypher
CREATE VECTOR INDEX my_index WITH DIMENSION 128 METRIC COSINE
```

Metric options: `COSINE`, `EUCLID`

### Load embeddings from file

The CSV format is `id,v1,v2,...,vn` — one row per vector, no header. The ID is a numerical identifier you'll use to join results back to graph nodes. Place files in the `data` subdirectory of the TuringDB directory (`~/.turing/data` by default):

```
0,1.2,2.0,0.0,0.5
1,0.8,1.5,0.3,0.2
2,1.0,1.8,0.1,0.4
```

```cypher
LOAD VECTOR FROM "embeddings.csv" IN my_index
```

### Store embeddings as node properties

Separately from the vector index, you can store embeddings directly on nodes via the normal write workflow. This is useful for keeping the raw vectors alongside graph data:

```python
change = client.new_change()
client.checkout(change=change)
client.query("MATCH (n:Person {name: 'Alice'}) SET n.emb = [1.2, 2.0, 0.0, 0.5]")
client.query("CHANGE SUBMIT")
client.checkout()
```

Note: `SET n.emb = [...]` stores the embedding as a node property — it does **not** add it to a vector index. Use `LOAD VECTOR FROM` to populate the index for search.

### Search

`VECTOR SEARCH` finds the k nearest neighbors and yields their numerical IDs. Chain with `MATCH` to join back to graph nodes:

```cypher
-- Find 5 nearest neighbors, returns their IDs:
VECTOR SEARCH IN my_index FOR 5 [1.2, 0.5, 3.0, ...] YIELD ids
RETURN ids

-- Chain results into a graph query (n.id must match the IDs loaded into the index):
VECTOR SEARCH IN my_index FOR 5 [1.2, 0.5, 3.0, ...] YIELD ids
MATCH (n:Document) WHERE n.id = ids
RETURN n.title, n.summary

-- Traverse from matched nodes:
VECTOR SEARCH IN my_index FOR 5 [1.2, 0.5, 3.0, ...] YIELD ids
MATCH (n:Person)-[:AUTHORED]->(p:Publication)
WHERE n.id = ids
RETURN n.name, p.title
```

The `ids` variable from `YIELD` works like a variable from `CALL ... YIELD` — any subsequent `MATCH` can reference it.

### Complete Python example

```python
# Create index
client.query("CREATE VECTOR INDEX doc_index WITH DIMENSION 384 METRIC COSINE")

# Load pre-computed embeddings (file at ~/.turing/data/doc_vectors.csv)
client.query('LOAD VECTOR FROM "doc_vectors.csv" IN doc_index')

# Search and join to graph
df = client.query("""
    VECTOR SEARCH IN doc_index FOR 10 [0.12, 0.45, 0.78, ...] YIELD ids
    MATCH (d:Document) WHERE d.id = ids
    RETURN d.title, d.summary
""")
print(df)
#       d.title         d.summary
# 0  Graph DBs  An overview of ...
# 1   Vectors   Embedding search ...

# Inspect and clean up
client.query("SHOW VECTOR INDEXES")
client.query("DELETE VECTOR INDEX doc_index")
```

### Index management

```cypher
SHOW VECTOR INDEXES
DELETE VECTOR INDEX my_index
```
