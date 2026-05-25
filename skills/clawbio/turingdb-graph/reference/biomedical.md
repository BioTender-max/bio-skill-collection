---
name: turingdb-biomedical
description: Use when modelling biomedical data in TuringDB — patient cohorts, pathway/reaction graphs, antibody–protein–publication networks, drug–target relationships, and GraphRAG over biomedical literature. Covers schema patterns, tabular-to-graph ingestion, common biomedical query patterns, and vector search for retrieval.
---

# TuringDB: Biomedical Reference

Short reference for the recurring patterns when using TuringDB for biomedical and clinical data. Assumes you already have a running server and a loaded graph — see `startup.md`. For generic Cypher syntax see `querying.md` / `writing.md`.

## When to reach for this file

- Patient cohort / clinical graphs — patients, conditions, medications, providers, encounters
- Biological pathway / reaction graphs — Reactome, BIKG, entity-reaction networks
- Antibody / reagent / publication citation graphs
- Drug–target–indication / target-discovery knowledge graphs
- GraphRAG or semantic search over biomedical literature

---

## 1. Ingestion Patterns

Three documented load paths — pick based on your input format. All writes go through the change/commit workflow in `writing.md`. For large batch ingestion from a CSV, `LOAD CSV … CREATE` (`writing.md` § LOAD CSV) is usually faster than the row-by-row pattern in §1b.

### 1a. Inline CREATE (small seeds, test fixtures, tiny ontologies)

Direct Cypher inside a change. Best for hand-crafted seed data or tests.

```python
change = client.new_change()
client.checkout(change=change)
client.query("""
    CREATE (:Drug {name: 'Imatinib', atc: 'L01XE01'})-[:TARGETS]->
           (:Protein {name: 'BCR-ABL', uniprot: 'A9UF07'})
""")
client.query("CHANGE SUBMIT")
client.checkout()
```

### 1b. Row-by-row CREATE from a DataFrame (clinical CSVs, denormalised tables)

When the input is a single tabular file where each row links one primary entity to several secondary ones (patient → doctor, medication, hospital, …). Model it as: one primary node per row, secondary nodes deduped by value, one edge per secondary column. Do the work in Python against a single change, then submit.

This pattern is **required**, not just preferred, when secondary nodes need to be dedup'd: `LOAD CSV` has no MERGE, and `LOAD CSV + MATCH` is not supported (see `writing.md` § LOAD CSV), so you cannot attach new rows' edges to pre-existing shared nodes inside a single `LOAD CSV` statement.

```python
import pandas as pd

df = pd.read_csv("clinical_export.csv")

change = client.new_change()
client.checkout(change=change)

# 1. Create dedup'd secondary nodes first (one per unique value)
for col, label, edge in [
    ("Medical Condition", "MedicalCondition",  "HAS"),
    ("Medication",        "Medication",        "TOOK_MEDICATION"),
    ("Doctor",            "Doctor",            "IS_TREATED_BY"),
    ("Hospital",          "Hospital",          "IS_TREATED_IN"),
]:
    for val in df[col].dropna().unique():
        safe = val.replace("'", "\\'")
        client.query(f"CREATE (:{label} {{name: '{safe}'}})")

client.query("COMMIT")   # persist secondaries before edges reference them

# 2. Create the primary node + edges, one row at a time
for _, row in df.iterrows():
    pid = row["Patient ID"]
    client.query(f"""
        CREATE (:Patient {{id: '{pid}', name: '{row["Name"]}', age: {int(row["Age"])}}})
    """)
    client.query("COMMIT")

    client.query(f"""
        MATCH (p:Patient {{id: '{pid}'}}),
              (c:MedicalCondition {{name: '{row["Medical Condition"]}'}}),
              (m:Medication {{name: '{row["Medication"]}'}}),
              (d:Doctor {{name: '{row["Doctor"]}'}}),
              (h:Hospital {{name: '{row["Hospital"]}'}})
        CREATE (p)-[:HAS]->(c),
               (p)-[:TOOK_MEDICATION]->(m),
               (p)-[:IS_TREATED_BY]->(d),
               (p)-[:IS_TREATED_IN]->(h)
    """)

client.query("CHANGE SUBMIT")
client.checkout()
```

Note the `COMMIT` between the node-creation step and the edge-creation step — see `writing.md` § "Creating Nodes and Edges". Always escape user-supplied strings (apostrophes, quotes) before interpolating into Cypher.

### 1c. `LOAD GML` / `LOAD JSONL` for pre-built networks (Reactome, BIKG, exported KGs)

For networks that already exist as a file (Reactome entity-pairwise exports, ontology dumps, Neo4j APOC exports), use the engine-side loaders documented in `introspection.md`:

```python
# GML — collapses everything into label GMLNode / edge type GMLEdge,
# and all properties become strings. Simple but untyped.
client.query("LOAD GML 'entities_pairwise.gml' AS reactome")

# JSONL — preserves typed labels and properties. Compatible with
# Neo4j APOC JSON export (useTypes:true). Preferred for rich KGs.
client.query("LOAD JSONL 'bikg_export.jsonl' AS bikg")

client.load_graph("reactome")
client.set_graph("reactome")
```

Files must sit in the TuringDB data directory (`~/.turing/data` by default). See `introspection.md` § "Data Import" for format details.

---

## 2. Canonical Biomedical Schemas

Each schema is one `CALL db.labels()` away after ingestion — these are the shapes that recur.

### 2a. Patient Cohort (healthcare/clinical)

```
(Patient) -[:IS]->             (Gender)
(Patient) -[:IS]->             (BloodType)
(Patient) -[:HAS]->            (MedicalCondition)
(Patient) -[:IS_TREATED_BY]->  (Doctor)
(Patient) -[:IS_TREATED_IN]->  (Hospital  {room_number})
(Patient) -[:IS_CLIENT_OF]->   (InsuranceProvider)
(Patient) -[:TOOK_MEDICATION]->(Medication)
(Patient) -[:HAS_RESULT]->     (TestResult)
```

Patient-level properties: `age`, `dateOfAdmission`, `dischargeDate`, `billingAmount`.

### 2b. Pathway / Reaction (Reactome-style)

```
(EntityWithAccessionedSequence {referenceType})
(Complex)
(Reaction)
(BlackBoxEvent)
(PositiveGeneExpressionRegulation)
(Process)
```

Edges are typically untyped in GML imports. Node properties: `displayName`, `schemaClass`, `category`, `id`. Use `schemaClass` as the label during ingestion.

### 2c. Antibody–Protein–Publication (reagent/citation)

```
(Antibody {code, company, clonality, clone, conjugate}) -->(Protein)
(Antibody) -->(Host {Rabbit, Mouse, ...})
(Publication {pubmedid, published_year, country, cited_by_count, institution}) -->(Protein)
(Journal   {journal_impact}) -->(Protein)
(Protein   {gene_name, ncbi_gene_id, modification, modification_site}) -->(Species)
```

Generalises cleanly to drug–target–indication by renaming: `Antibody → Drug`, `Protein → Target`, `Publication → Trial`, `Host → Organism`.

### 2d. Drug–Target–Indication (discovery KG) — *example shape only*

Not pulled from a worked example — this is one way you *could* model a discovery KG, shown as a starting point. Real drug-discovery graphs vary a lot (cf. OpenTargets, BIKG, DrugBank, Hetionet); inspect the source you're ingesting before committing to a schema.

```
(Drug)      -[:TARGETS]->     (Target:Protein)
(Drug)      -[:INDICATED_FOR]-> (Indication:Disease)
(Target)    -[:PART_OF]->     (Pathway)
(Drug)      -[:INTERACTS_WITH]-> (Drug)       -- DDI
(Drug)      -[:ADVERSE_EVENT]->  (AdverseEvent)
(Trial)     -[:EVALUATES]->   (Drug)
(Trial)     -[:ENROLLS]->     (Cohort)        -- links back to patient graph
```

---

## 3. Common Biomedical Queries

### 3a. Always start with schema introspection

Every bio notebook runs these three before writing a single query. Do the same on any unfamiliar graph.

```python
labels     = client.query("CALL db.labels()")
edge_types = client.query("CALL db.edgeTypes()")
props      = client.query("CALL db.propertyTypes()")
```

Count per label:

```python
for label in labels["label"]:
    n = client.query(f"MATCH (n:{label}) RETURN count(n)").iloc[0, 0]
    print(f"{label}: {n}")
```

### 3b. Cohort filters

```cypher
-- Patients with a specific condition
MATCH (p:Patient)-[:HAS]->(c:MedicalCondition)
WHERE c.displayName = 'Cancer'
RETURN p.displayName, p.Age

-- Demographic slice
MATCH (p:Patient)-[:IS]->(bt:BloodType)
WHERE bt.displayName = 'A+' AND p.Age > 60
RETURN p.displayName, p.Age

-- Elderly + pediatric edges of the distribution
MATCH (p:Patient) WHERE p.Age < 18 OR p.Age > 65
RETURN p.displayName, p.Age
```

Backtick properties with spaces from raw CSV columns: `` n.`Billing Amount` ``, `` n.`Date of Admission` ``.

### 3c. Comedication / comorbidity (co-occurrence on a shared neighbour)

Classic biomedical question: which two entities are linked through the same third entity?

```cypher
-- Patients on two medications simultaneously
MATCH (p:Patient)-[:TOOK_MEDICATION]->(m1:Medication),
      (p)-[:TOOK_MEDICATION]->(m2:Medication)
WHERE m1.displayName = 'Aspirin' AND m2.displayName = 'Warfarin'
RETURN p.displayName

-- Comorbidity pairs (conditions co-occurring in patients)
MATCH (p:Patient)-[:HAS]->(c1:MedicalCondition),
      (p)-[:HAS]->(c2:MedicalCondition)
WHERE c1.displayName < c2.displayName
RETURN c1.displayName, c2.displayName, count(p) AS patients
ORDER BY patients DESC
```

### 3d. Co-citation / co-use (antibody, drug, reagent)

Same shape, different domain. From the CiteAb notebook:

```cypher
-- Antibodies that co-target the same protein
MATCH (ab1:Antibody)-->(prot:Protein), (ab2:Antibody)-->(prot:Protein)
WHERE ab1.displayName <> ab2.displayName
RETURN ab1.displayName, ab2.displayName, prot.displayName, prot.gene_name
```

Generalises to drug–drug co-targeting, gene co-mention in publications, etc.

### 3e. Bridge queries (three-entity join)

```cypher
-- Antibodies cited in publications, with target protein as bridge
MATCH (ab:Antibody)-->(prot:Protein)<--(pub:Publication)
RETURN ab.displayName, ab.company,
       prot.gene_name, prot.ncbi_gene_id,
       pub.pubmedid, pub.published_year

-- Add a fourth entity (journal) for impact filtering
MATCH (pub:Publication)-->(prot:Protein)<--(j:Journal)
WHERE j.journal_impact > 10
RETURN pub.displayName, prot.displayName, j.displayName, j.journal_impact
```

### 3f. Multi-hop pathway / reaction traversal

For Reactome / pathway data, iterate hop counts to find the shortest causal chain between two entity classes:

```python
for hops in range(1, 15):
    pattern = "-[]->".join([f"(n{i})" for i in range(hops + 1)])
    q = f"""
        MATCH {pattern}
        WHERE n0:EntityWithAccessionedSequence AND n{hops}:BlackBoxEvent
        RETURN {", ".join(f"n{i}.displayName" for i in range(hops + 1))}
    """
    df = client.query(q)
    if not df.empty:
        print(f"Found path in {hops} hops")
        break
```

For a single weighted shortest path between named entities, use `shortestPath()` — see `algorithms.md`.

### 3g. Publication / literature filters

```cypher
-- Recent publications
MATCH (pub:Publication) WHERE pub.published_year >= 2020
RETURN pub.displayName, pub.pubmedid, pub.cited_by_count

-- Exact year (property stored as string) — use toInteger
MATCH (pub:Publication)
WHERE pub.published_year = toInteger('2020') AND pub.pubmedid > 0
RETURN pub.displayName, pub.pubmedid

-- Normalised impact score
MATCH (pub:Publication) WHERE pub.cited_by_count > 0
RETURN pub.displayName, pub.cited_by_count,
       pub.cited_by_count / toFloat('1000') AS impact_score
```

### 3h. Cohort snapshots via changes and commits

For a biomedically meaningful subset — a specific patient cohort, a pathway slice, a literature window — lean on TuringDB's git-like versioning rather than extracting to a new graph. A change is an isolated workspace, a commit is a named snapshot.

```python
# Run your cohort-defining MATCH, inspect results
df = client.query("""
    MATCH (p:Patient)-[:TOOK_MEDICATION]->(m:Medication {name: 'Paracetamol'})
    RETURN p.id, p.name, p.age
""")

# Open a new change — any writes now (e.g. tagging cohort members) stay isolated
change = client.new_change()
client.checkout(change=change)
client.query("""
    MATCH (p:Patient)-[:TOOK_MEDICATION]->(:Medication {name: 'Paracetamol'})
    SET p.cohortTag = 'paracetamol_2024_q1'
""")
client.query("CHANGE SUBMIT")
client.checkout()

# The commit is now in db.history() and any past cohort state can be revisited:
hist = client.query("CALL db.history()")
client.set_commit(str(hist.iloc[1, 0]))   # strip (HEAD) suffix on current row
# ...queries now see the pre-tagging state...
client.checkout()   # back to HEAD
```

If you genuinely need a standalone graph (to load into a separate TuringDB context, share with a collaborator, or feed into another pipeline), export the rows via `MATCH … RETURN` and re-CREATE them in a new graph using the change workflow from §1a / §1b.

---

## 4. What to index for biomedical workloads

`CREATE INDEX` / `DROP INDEX` syntax and workflow live in `writing.md` § Indexing. This section is the bio-specific guidance on *which* properties are worth indexing.

Candidates that usually pay back their cost:

- **Identifier properties used as query entry points** — `id` on Patient, `pubmedid` on Publication, `uniprot` / `ncbi_gene_id` on Protein, `atc` / `drugbank_id` on Drug. Anything you'd use in a `WHERE n.<id> = '...'` lookup or to seed a multi-hop traversal.
- **High-selectivity names used as join keys** — `gene_name` in antibody–publication bridges (§3e), `displayName` on Medication / MedicalCondition when those are the join anchor in cohort queries.
- **Filter-heavy numerics** — `published_year`, `cited_by_count`, patient `age` — indexing pays back when combined with range filters (`>=`, `<`, `<>`).

Skip:

- Properties you rarely filter on (free-text `summary`, `abstract`, `description`).
- Very low-cardinality properties (boolean flags, `Gender`, `BloodType` as a property) — a full scan is already cheap and the index overhead isn't worth it.
- Vector / embedding properties — use `CREATE VECTOR INDEX` instead (see `algorithms.md` § Vector Search).

Remember the current TuringDB limitation: `CREATE INDEX … FOR (n) ON n.<prop>` is unlabelled. One index covers the property across every node that carries it — in practice fine for identifier properties (`pubmedid`, `uniprot`, etc.) which don't overlap between entity types.

---

## 5. GraphRAG: Schema-grounded NL→Cypher

Pattern used across the three bio notebooks: fetch live schema, inject into the LLM system prompt, let the model generate Cypher against the *actual* graph, catch and retry on `TuringDBException`.

```python
labels     = client.query("CALL db.labels()")
edge_types = client.query("CALL db.edgeTypes()")
props      = client.query("CALL db.propertyTypes()")

sample_q = "MATCH (n) RETURN " + \
           ", ".join(f"n.`{p}`" for p in props["propertyType"]) + " LIMIT 3"
samples = client.query(sample_q)

schema_context = f"""Node labels: {labels}
Relationship types: {edge_types}
Property names and types: {props}
Sample nodes: {samples}"""

system_prompt = TURINGDB_CYPHER_SYSTEM_PROMPT.replace("{schema_context}", schema_context)
cypher = natural_language_to_cypher(user_question, system_prompt, provider="Anthropic")

try:
    df = client.query(cypher)
except TuringDBException as e:
    # feed the error back to the LLM for self-correction
    ...
```

The system prompt must pin the model to **TuringDB's Cypher subset** — no UNWIND, no `$parameters`, no `IN [...]` on strings. See `querying.md` § "Not Supported".

---

## 6. Vector Search for Biomedical Literature

Full GraphRAG pattern: semantic retrieval by embedding similarity, then chain into graph traversal. Covered in depth in `algorithms.md` § Vector Search — this section is the biomedical spin.

### 6a. Build the index from graph nodes

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # 384 dims

# Pull the nodes you want to index, with their internal TuringDB IDs
docs = client.query("MATCH (p:Publication) RETURN n, n.title, n.abstract")
texts = (docs["n.title"] + ". " + docs["n.abstract"]).tolist()
embs  = model.encode(texts, batch_size=64)

# Write the CSV — first column is the TuringDB internal node ID (from "n")
import csv
with open(f"{DATA_DIR}/pub_embeddings.csv", "w") as f:
    w = csv.writer(f)
    for node_id, vec in zip(docs["n"].astype(int), embs):
        w.writerow([int(node_id), *vec.tolist()])

client.query("CREATE VECTOR INDEX pub_idx WITH DIMENSION 384 METRIC COSINE")
client.query("LOAD VECTOR FROM 'pub_embeddings.csv' IN pub_idx")
```

### 6b. Semantic search → graph join

```python
def semantic_search(question, k=5):
    qvec = model.encode([question])[0]
    vec_str = "[" + ", ".join(f"{v:.6f}" for v in qvec) + "]"
    return client.query(f"""
        VECTOR SEARCH IN pub_idx FOR {k} {vec_str} YIELD ids
        MATCH (p:Publication)-->(prot:Protein)
        WHERE p = ids
        RETURN p.title, p.pubmedid, prot.gene_name
    """)
```

### 6c. Hybrid retrieval — graph filter scopes, vector ranks

Classic pattern for narrow biomedical queries: first constrain by graph structure (e.g. "publications about BRCA1"), then rank the scoped set by semantic similarity.

```python
# Step 1: scope by graph pattern
scope = client.query("""
    MATCH (p:Publication)-->(prot:Protein)
    WHERE prot.gene_name = 'BRCA1'
    RETURN p
""")
scope_ids = set(int(x) for x in scope["p"].tolist())

# Step 2: rank that scope by semantic similarity (Python-side)
qvec = model.encode([question])[0]
mask = docs["n"].astype(int).isin(scope_ids)
scope_embs = embs[docs.index[mask].tolist()]
sims = (scope_embs / np.linalg.norm(scope_embs, axis=1, keepdims=True)) @ \
       (qvec / np.linalg.norm(qvec))
ranked = np.argsort(sims)[::-1][:k]
```

### 6d. Embeddings as node properties

Alternative to a vector index — store embeddings directly on nodes for small sets where you don't need kNN. Covered in `algorithms.md`:

```python
change = client.new_change()
client.checkout(change=change)
client.query("MATCH (p:Publication {pubmedid: 12345}) SET p.emb = [0.12, 0.45, ...]")
client.query("CHANGE SUBMIT")
client.checkout()
```

This stores the vector as a property but does *not* add it to a vector index — use `LOAD VECTOR FROM` for indexed search.

---

## 7. Bio-specific Gotchas

- **Backtick column names with spaces.** Clinical CSVs routinely have columns like `"Billing Amount"`, `"Date of Admission"`. Use backticks in Cypher: `` n.`Billing Amount` ``. Or rename columns before ingestion.
- **Property types after raw CSV ingestion.** Numerics often land as strings — wrap with `toInteger('2020')` / `toFloat('1.1')` in WHERE and RETURN as shown in §3g.
- **Escape interpolated strings.** Apostrophes in names (`O'Brien`, drug names with quotes) break Cypher if you string-concatenate them. Escape `'` → `\\'` before interpolation.
- **`LOAD GML` loses types.** Every node becomes `GMLNode`, every edge `GMLEdge`, every property a string. For typed biomedical data, prefer JSONL or row-by-row CREATE.
- **Vector index IDs must match node IDs.** The first column of the embeddings CSV is what `VECTOR SEARCH` yields — to join back to graph nodes, that column must be the TuringDB internal node ID (query `MATCH (n:Label) RETURN n` to get it).
- **String `IN` lists aren't supported.** To filter on a list of gene names or patient IDs, build an `OR` chain (see `querying.md` § "Injecting Seed Nodes").
- **`labels(n)` in RETURN only, never in WHERE.** Use a direct label constraint `(n:Protein)` instead.
- **Large patient × condition Cartesian products.** `MATCH (p:Patient), (c:MedicalCondition)` on a real cohort is easily billions of rows. Always add a join variable or WHERE constraint.
- **Cohort refreshes: prefer versioning to mutation.** Instead of overwriting a cohort in place, open a new change, tag or re-create the cohort's members, and submit — old snapshots stay queryable via `CALL db.history()` and `client.set_commit()`.
