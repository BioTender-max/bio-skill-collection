---
name: turingdb-writing
description: Use when creating or updating data in TuringDB — CREATE nodes/edges, SET properties, and the mandatory change/commit workflow. All writes must go through a change or they will not persist.
---

# TuringDB: Writing Data

All writes (CREATE, SET) require the change workflow. TuringDB uses git-like branching — writes happen inside an isolated change that is then submitted to main.

## The Change Workflow

```python
change = client.new_change()       # create isolated change, returns integer ID
client.checkout(change=change)     # enter the change

# ... run your CREATE / SET queries ...

client.query("CHANGE SUBMIT")      # merge change into main
client.checkout()                  # return to main
```

Never run CREATE or SET outside a change — they will silently not persist.

## Complete End-to-End Example

```python
from turingdb import TuringDB, TuringDBException

client = TuringDB(host="http://localhost:6666")

# Set up graph
try:
    client.create_graph("demo")
except TuringDBException:
    pass
try:
    client.load_graph("demo")
except TuringDBException:
    pass
client.set_graph("demo")

# Write data
change = client.new_change()
client.checkout(change=change)

client.query("CREATE (:Person {name: 'Alice', age: 30})-[:KNOWS]->(:Person {name: 'Bob', age: 25})")
client.query("CREATE (:City {name: 'London'})")
client.query("COMMIT")  # persist so nodes are visible for next query

client.query("""
    MATCH (a:Person {name: 'Alice'}), (c:City {name: 'London'})
    CREATE (a)-[:LIVES_IN]->(c)
""")

client.query("CHANGE SUBMIT")
client.checkout()

# Verify
df = client.query("MATCH (n:Person)-[:LIVES_IN]->(c:City) RETURN n.name, c.name")
print(df)
#   n.name  c.name
# 0  Alice  London
```

## Creating Nodes and Edges

**Single query (preferred):** Create nodes and edges together — no intermediate COMMIT needed:

```python
client.query("CREATE (:Person {name: 'Jane'})-[:KNOWS]->(:Person {name: 'John'})")
client.query("CHANGE SUBMIT")
```

**Separate queries:** If you create nodes first and edges second, you must COMMIT after the nodes before creating edges:

```python
client.query("CREATE (:Person {name: 'Alice'}), (:Person {name: 'Bob'})")
client.query("COMMIT")   # persist nodes so they're visible for the next query
client.query("MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:KNOWS]->(b)")
client.query("CHANGE SUBMIT")
```

## CREATE Syntax

```cypher
CREATE (:Person {name: 'Alice', age: 30})
CREATE (:Person {name: 'Mick'})-[:FRIEND_OF]->(:Person {name: 'John'})

-- Multiple nodes at once:
CREATE (:Person {name: 'Alice'}), (:Person {name: 'Bob'}), (:City {name: 'London'})

-- Connect two existing nodes:
MATCH (n:Person {name: 'Alice'}), (m:Person {name: 'Bob'})
CREATE (n)-[:KNOWS]->(m)

-- Create edge and return properties:
MATCH (n:Person {name: 'Alice'}), (m:Person {name: 'Bob'})
CREATE (n)-[:KNOWS]->(m)
RETURN n.name, m.name
```

Rules:
- Every node and edge requires at least one label
- Pure CREATE has no RETURN clause — only add RETURN when combining with MATCH

## LOAD CSV (Batch CREATE)

Since **v1.29**, `LOAD CSV ... CREATE` reads a CSV file and applies a templated CREATE for each row — useful for bulk ingestion without a Python loop. Like any other CREATE, it must run inside a change.

Two forms:

```cypher
-- Positional: row[i] indexes columns (0-based). Works with headerless CSVs.
LOAD CSV 'mycsv.csv' AS row
CREATE (:NewNode {name: row[0], isFrench: row[2], age: row[3]})

-- Named: treats the first line as a header; columns addressable by name.
LOAD CSV 'mycsv.csv' WITH HEADERS AS row
CREATE (:NewNode {name: row.names, isFrench: row.isFrenches, age: row.ages})
```

Rules:
- **No hard typing** — values arrive as strings. Wrap with `toInteger()` / `toFloat()` if the property needs to be compared or arithmetic'd as a number:
  ```cypher
  LOAD CSV 'patients.csv' WITH HEADERS AS row
  CREATE (:Patient {id: row.id, age: toInteger(row.age)})
  ```
- **File location** — CSVs must sit in the TuringDB data directory (`~/.turing/data` by default), same rule as `LOAD GML` / `LOAD JSONL`.
- **Change workflow required** — wrap the query with `new_change` / `CHANGE SUBMIT` as with any CREATE. Writes run outside a change do not persist.
- **No MERGE / dedup** — each row unconditionally creates a new node. If the same value appears in multiple rows, you get multiple nodes. Pre-dedupe in pandas (`df["col"].drop_duplicates().to_csv(...)`) before calling `LOAD CSV` when you want one-node-per-unique-value.
- **Multi-pattern CREATE per row is supported** — you can create an edge and both endpoints in a single pass:
  ```cypher
  LOAD CSV 'edges.csv' WITH HEADERS AS row
  CREATE (:Person {id: row.src})-[:KNOWS {since: toInteger(row.year)}]->(:Person {id: row.dst})
  ```
  Each row creates fresh nodes on both sides (no MERGE — see the dedup rule above). If `src` or `dst` values repeat across rows, you get duplicate nodes.
- **`LOAD CSV` cannot reference pre-existing nodes** — `LOAD CSV ... MATCH ... CREATE ...` is not supported. To attach new edges or properties to nodes already in the graph, fall back to a Python loop that issues separate `MATCH + CREATE` (or `MATCH + SET`) queries per row. A typical clinical cohort ingest — patients linked to dedup'd Medication / Doctor / Condition nodes — needs this fallback.

```python
# Typical one-shot load
change = client.new_change()
client.checkout(change=change)
client.query("""
    LOAD CSV 'patients.csv' WITH HEADERS AS row
    CREATE (:Patient {id: row.id, name: row.name, age: toInteger(row.age)})
""")
client.query("CHANGE SUBMIT")
client.checkout()
```

## SET Syntax (Update Properties)

SET always follows a MATCH. It creates the property if it doesn't already exist.

```cypher
MATCH (n:Person {name: 'Alice'}) SET n.age = 31

-- Multiple properties at once:
MATCH (n:Person {name: 'Alice'}) SET n.score = n.score * 1.1, n.updated = true

-- Expression-based update:
MATCH (p:Product) SET p.discountPrice = p.price * (1 - 0.15)

-- Update an edge property:
MATCH (n:Person {name: 'Alice'})-[e:KNOWS]->(m) SET e.since = 2020

-- Conditional update:
MATCH (n:Person) WHERE n.age < 18 SET n.isMinor = true

-- Set a vector embedding:
MATCH (n:Person {name: 'Alice'}) SET n.emb = [1.2, 2.0, 0.0, 12.0]
```

## Indexing (CREATE INDEX / DROP INDEX)

Since **v1.29**, per-property indexes accelerate `WHERE` filters and `MATCH` joins. Indexes live inside the versioning system — they are created in a change and become observable after `COMMIT` or `CHANGE SUBMIT`.

### Syntax

```cypher
CREATE INDEX <name> FOR (n) ON n.<propertyname>      -- node property
CREATE INDEX <name> FOR [e] ON e.<propertyname>      -- edge property
DROP INDEX <name>
CALL db.showIndexes()                                   -- list current indexes
```

### Limitations

- **Pattern must be unlabelled.** `FOR (n)` and `FOR [e]` only — you cannot write `FOR (n:Person)` or `FOR [e:KNOWS]`. A single index covers the property across every node (or every edge) that carries it, regardless of label.
- **No `IF EXISTS` on `DROP INDEX`.** Dropping an index that doesn't exist errors — list indexes with `db.showIndexes()` first if unsure what's loaded.

### Workflow

Like any other write, index creation/drop must run inside a change and is only observable once that change is committed or submitted:

```python
change = client.new_change()
client.checkout(change=change)
client.query("CREATE INDEX person_name FOR (n) ON n.name")
client.query("CREATE INDEX knows_since FOR [e] ON e.since")
client.query("CHANGE SUBMIT")
client.checkout()

# Subsequent queries use the index
client.query("MATCH (n) WHERE n.name = 'Alice' RETURN n")
```

Data load and index creation can share the same change — load nodes/edges, create the indexes your queries will hit, submit once.

## Engine Commands for Change Management

These can be issued via `client.query()` or from the CLI:

| Command | Description |
|---------|-------------|
| `CHANGE NEW` | Create a new isolated change |
| `CHANGE SUBMIT` | Merge current change into main |
| `CHANGE DELETE` | Discard current change |
| `CHANGE LIST` | List active uncommitted changes |
| `COMMIT` | Persist intermediate state within a change (needed between separate node/edge creates) |

## Gotchas

- CREATE/SET outside a change do not persist — always use the change workflow
- Creating nodes and edges in separate queries requires `COMMIT` between the two steps so the first set of nodes are visible to the second query
- Pure CREATE has no RETURN clause — only MATCH+CREATE supports RETURN
- Every node and edge must have at least one label — `CREATE (n)` will error; use `CREATE (n:Label)`
- `CHANGE SUBMIT` merges the change into main. After submitting, call `client.checkout()` to return the SDK context to main
- `create_graph()` raises `TuringDBException` if the graph name already exists; `load_graph()` raises if already loaded. Wrap in try/except for idempotent scripts (see `startup.md`)
- `LOAD CSV` values arrive untyped — always wrap numerics with `toInteger()` / `toFloat()` before storing if downstream queries compare them as numbers
- `LOAD CSV` has no MERGE / dedup — each row unconditionally creates new nodes. Pre-dedupe in pandas if you want one-node-per-unique-value
- `LOAD CSV` supports multi-pattern CREATE per row (e.g. `CREATE (:A)-[:R]->(:B)`) but does **not** support `MATCH` — you cannot reference pre-existing nodes in a `LOAD CSV` statement. For that, loop row-by-row in Python with separate `MATCH + CREATE` queries
- `CREATE INDEX` / `DROP INDEX` require the change workflow and are only observable after `COMMIT` / `CHANGE SUBMIT`
- `CREATE INDEX` does not accept a labelled pattern — `FOR (n:Person)` is invalid, use `FOR (n)`. One index covers a property across all nodes/edges that carry it
- `DROP INDEX <name>` errors if the index doesn't exist — no `IF EXISTS`. Call `db.showIndexes()` first when in doubt
