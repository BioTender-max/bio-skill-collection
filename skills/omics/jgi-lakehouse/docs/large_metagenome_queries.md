# Large Metagenome Queries: Patterns and Pitfalls

## Overview

Querying NUMG tables across all ~86,800 metagenomes requires a different approach than
standard Lakehouse queries. This document captures lessons learned from a real query:
**retrieve all genes with a Pfam domain hit (PF04896) and their product names**.

Scale of that query:
- 487,390 gene hits across 27,378 metagenomes
- Required joining `gene2pfam` and `gene_product` (both partitioned by `oid`)

---

## Lesson 1: Dremio SQL JOINs on NUMG Tables Fail at Scale

### The error

Any SQL JOIN between two large NUMG tables hits a hard Dremio executor limit:

```
SYSTEM ERROR: UnsupportedOperationException:
Pivoted variable keys length of 156272 bytes can't be more than
the maximum allowed variable block size of 131064 bytes
SqlOperatorImpl HASH_JOIN
```

Dremio's hash join operator accumulates variable-length join keys (VARCHAR `oid` +
VARCHAR `gene_oid`) into fixed-size memory blocks. When one block's worth of keys
exceeds 131 KB, the executor fails.

### What triggers it

- Any `JOIN` between two NUMG tables without a restrictive `oid` filter
- `IN (subquery)` rewrites — Dremio converts these to HASH_JOIN internally, same error
- Affects `gene2pfam ⋈ gene_product`, `gene2pfam ⋈ faa`, `fna ⋈ scaffold_genes`, etc.

### What does NOT trigger it

- Queries on a **single table** (even without an `oid` filter) work fine
- Joins filtered to a **single `oid`** work fine — partition pruning keeps the key set small
- COUNT / aggregation queries on a single table work fine across all partitions

### Workaround

**Do not join NUMG tables in SQL when querying across many metagenomes.**
Fetch each table separately and join in Python (see Lesson 3).

---

## Lesson 2: REST API Pagination Is Too Slow for Large Result Sets

The standard REST client (`rest_client.py`) retrieves results in pages of up to 500 rows
per HTTP request. For a 487K-row result set this means ~975 sequential API calls.

| Result size | REST API pages | Estimated time |
|-------------|---------------|---------------|
| 10,000 rows | 20 calls | ~10s |
| 100,000 rows | 200 calls | ~100s |
| 487,390 rows | 975 calls | ~500s |

**Use Arrow Flight instead** for any result set larger than ~10,000 rows.

---

## Lesson 3: Use Arrow Flight for Bulk Data Retrieval

Arrow Flight streams results as Apache Arrow columnar batches over a persistent gRPC
connection. It is **~20× faster** than REST pagination for large results.

### Setup

```bash
python3 -m venv .venv
.venv/bin/pip install \
  "https://github.com/dremio-hub/arrow-flight-client-examples/releases/download/dremio-flight-python-v1.1.0/dremio_flight-1.1.0-py3-none-any.whl" \
  pandas
```

### Authentication with PAT token (no username needed)

Arrow Flight supports injecting the PAT as a bearer token directly — no username or
password required. This matches the REST API auth pattern.

```python
import os
from dremio.flight.endpoint import DremioFlightEndpoint

def flight_query(sql):
    args = {
        "hostname": "lakehouse-1.jgi.lbl.gov",
        "port":     32010,
        "token":    os.environ["DREMIO_PAT"],   # PAT from ~/.secrets/dremio_pat
        "tls":      False,
        "query":    sql,
    }
    ep = DremioFlightEndpoint(args)
    client = ep.connect()
    return ep.get_reader(client).read_pandas()   # returns a pandas DataFrame
```

### Observed performance

| Step | Rows | Method | Time |
|------|------|--------|------|
| `gene2pfam` WHERE pfam = 'pfam04896' | 487,390 | Arrow Flight | **25s** |
| Same query | 487,390 | REST pagination (estimated) | ~500s |

---

## Lesson 4: The Two-Step Pattern for Cross-Table NUMG Queries

Since SQL JOINs fail and REST is too slow, the recommended pattern for large cross-table
queries is:

1. **Arrow Flight** — fetch table A (the filtering table) in one shot → pandas DataFrame
2. **Parallel batched Arrow Flight** — fetch table B filtered to matching (oid, gene_oid)
   sets in batches → pandas DataFrame
3. **pandas merge** — join in Python
4. **Write output** — CSV or parquet

### Full working example: genes with a Pfam domain + their product names

```python
import os, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from dremio.flight.endpoint import DremioFlightEndpoint
import logging
logging.disable(logging.INFO)

PAT  = os.environ["DREMIO_PAT"]
HOST = "lakehouse-1.jgi.lbl.gov"
PORT = 32010

def flight_query(sql):
    args = {"hostname": HOST, "port": PORT, "token": PAT, "tls": False, "query": sql}
    ep = DremioFlightEndpoint(args)
    return ep.get_reader(ep.connect()).read_pandas()

# ── Step 1: fetch all hits from the filtering table ───────────────────────────
hits_df = flight_query("""
    SELECT oid, gene_oid, evalue, bit_score
    FROM "numg read only".numg.gene2pfam
    WHERE pfam = 'pfam04896'
""")
# 487,390 rows in ~25s

# Build per-oid gene_oid lists for targeted lookup
oid_genes = defaultdict(list)
for oid, gene_oid in zip(hits_df["oid"], hits_df["gene_oid"]):
    oid_genes[oid].append(gene_oid)
oids = sorted(oid_genes)

# ── Step 2: batch-fetch the annotation table in parallel ──────────────────────
BATCH   = 200   # oids per batch
WORKERS = 8     # concurrent Arrow Flight connections

def fetch_product_batch(batch_oids):
    batch_genes = [g for o in batch_oids for g in oid_genes[o]]
    oid_sql  = ", ".join(f"'{o}'" for o in batch_oids)
    gene_sql = ", ".join(f"'{g}'" for g in batch_genes)
    return flight_query(f"""
        SELECT oid, gene_oid, gene_display_name
        FROM "numg read only".numg.gene_product
        WHERE oid IN ({oid_sql}) AND gene_oid IN ({gene_sql})
    """)

batches = [oids[i:i+BATCH] for i in range(0, len(oids), BATCH)]
frames  = []
with ThreadPoolExecutor(max_workers=WORKERS) as pool:
    for df in pool.map(fetch_product_batch, batches):
        frames.append(df)

product_df = pd.concat(frames, ignore_index=True)

# ── Step 3: join and save ─────────────────────────────────────────────────────
result = hits_df.merge(product_df, on=["oid", "gene_oid"], how="left")
result.to_csv("pfam04896_genes.csv", index=False)
```

### Observed performance for the PF04896 query

| Step | Detail | Time |
|------|--------|------|
| Arrow Flight fetch `gene2pfam` | 487,390 rows | 25s |
| 137 batches × 8 threads `gene_product` | 462,363 rows | 657s |
| Python merge + CSV write | 487,439 rows | ~2s |
| **Total** | | **~11 min** |

---

## Batch size and parallelism tuning

| Parameter | Value used | Notes |
|-----------|-----------|-------|
| `BATCH` (oids per query) | 200 | Larger batches → fewer queries but longer IN clauses |
| `WORKERS` | 8 | More workers → higher Dremio server load; 8 is a safe default |

**Bottleneck:** each gene_product batch query must scan the matching `oid` partitions.
With 27K metagenomes split into 137 batches of 200, the per-query cost dominates.
Increasing WORKERS helps up to the point where the Dremio cluster becomes the limit.

If the number of affected metagenomes is small (< 500 oids), a single batched query
without threading is sufficient.

---

## Decision Guide

```
Need to query one NUMG table only?
  → REST client (rest_client.query_all) is fine for < ~10K rows
  → Arrow Flight for anything larger

Need to join two NUMG tables?
  → Filter to a SINGLE oid?  SQL JOIN works fine.
  → Across many oids?        Use the two-step Python pattern above.
                             Never use SQL JOIN across full NUMG tables.

Result set > 10K rows?
  → Use Arrow Flight (flight_query above), not REST pagination.
```

---

## Pitfalls Summary

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| SQL JOIN on two NUMG tables without oid filter | `HASH_JOIN` block size error, query fails | Fetch tables separately, join in Python |
| `IN (subquery)` rewrite | Same HASH_JOIN error — Dremio converts it internally | Same fix |
| REST API for large results | ~500s for 487K rows | Use Arrow Flight |
| No `oid` filter on a single table | Full scan of all ~86K partitions, slow but works | Add `oid =` filter when querying one metagenome |
| Pfam IDs in wrong case | `pfam = 'PF04896'` returns 0 rows | Use lowercase: `pfam = 'pfam04896'` |
| Joining NUMG tables on `gene_oid` only | Wrong results (gene_oid not globally unique) | Always join on both `oid AND gene_oid` |

---

## Related Documentation

- [numg_metagenome_sequences.md](numg_metagenome_sequences.md) — NUMG table schemas and column reference
- [arrow-flight-python.md](arrow-flight-python.md) — Arrow Flight setup and connection details
- [data-catalog.md](data-catalog.md) — Overview of all Lakehouse sources
