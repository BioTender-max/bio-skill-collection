"""
DGIdb - Drug-Gene Interaction Database
Category: Drug-centric | Type: DB | Subcategory: Drug-Target Interaction (DTI)
Link: https://www.dgidb.org/
Paper: https://doi.org/10.1093/nar/gkac1046

DGIdb curates drug-gene interaction data and gene druggability information
from 40+ databases and literature sources.

API docs: https://dgidb.org/api
GraphQL endpoint: https://dgidb.org/api/graphql
No API key required.
"""

import urllib.request
import json
from typing import Union


GRAPHQL_URL = "https://dgidb.org/api/graphql"


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _run_query(query: str, variables: dict = None) -> dict:
    """Send a GraphQL query and return parsed JSON."""
    payload = {"query": query, "variables": variables or {}}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _detect_type(entity: str) -> str:
    """Auto-detect entity type by naming convention.

    Returns one of: 'gene', 'drug', 'category'.

    Heuristics
    ----------
    - ALL-CAPS and <=15 chars (e.g. EGFR, BRAF, TP53)  -> gene
    - Known druggability category keywords               -> category
    - Otherwise                                          -> drug
    """
    _CATEGORY_KEYWORDS = {
        "clinically actionable", "drug resistance", "druggable genome",
        "tumor suppressor", "transcription factor", "kinase",
        "g protein coupled receptor", "hormone activity",
        "ion channel", "protease", "dna repair",
    }
    low = entity.strip().lower()
    if low in _CATEGORY_KEYWORDS:
        return "category"
    stripped = entity.strip()
    if stripped == stripped.upper() and stripped.isalpha() and len(stripped) <= 15:
        return "gene"
    return "drug"


# ---------------------------------------------------------------------------
# Core query functions
# ---------------------------------------------------------------------------

_GENE_QUERY = """
query GeneInteractions($names: [String!]!) {
  genes(names: $names) {
    nodes {
      name
      longName
      geneCategories { name }
      interactions {
        drug { name conceptId }
        interactionScore
        interactionTypes { type directionality }
        interactionAttributes { name value }
        publications { pmid }
        sources { sourceDbName }
      }
    }
  }
}
"""

_DRUG_QUERY = """
query DrugInteractions($names: [String!]!) {
  drugs(names: $names) {
    nodes {
      name
      conceptId
      drugApprovalRatings { rating source { sourceDbName } }
      drugApplications { appNo }
      interactions {
        gene { name longName }
        interactionScore
        interactionTypes { type directionality }
        interactionAttributes { name value }
        publications { pmid }
        sources { sourceDbName }
      }
    }
  }
}
"""

_CATEGORY_QUERY = """
query DruggableGenes($category: String!, $first: Int!) {
  geneCategories(name: $category) {
    nodes {
      name
      genes(first: $first) {
        nodes { name longName }
      }
    }
  }
}
"""


def _query_gene(names: list, max_interactions: int = 50) -> list:
    """Query gene(s) and return structured results."""
    raw = _run_query(_GENE_QUERY, {"names": names})
    nodes = raw.get("data", {}).get("genes", {}).get("nodes", [])
    results = []
    for n in nodes:
        interactions = []
        for ix in n.get("interactions", [])[:max_interactions]:
            drug = ix.get("drug") or {}
            interactions.append({
                "drug": drug.get("name"),
                "drug_concept_id": drug.get("conceptId"),
                "score": ix.get("interactionScore"),
                "types": [t.get("type") for t in ix.get("interactionTypes", [])],
                "directionality": [t.get("directionality") for t in ix.get("interactionTypes", [])],
                "attributes": {a["name"]: a["value"] for a in ix.get("interactionAttributes", [])},
                "pmids": [p.get("pmid") for p in ix.get("publications", []) if p.get("pmid")],
                "sources": [s.get("sourceDbName") for s in ix.get("sources", [])],
            })
        results.append({
            "query_type": "gene",
            "name": n.get("name"),
            "long_name": n.get("longName"),
            "categories": [c.get("name") for c in n.get("geneCategories", [])],
            "interaction_count": len(n.get("interactions", [])),
            "interactions": interactions,
        })
    return results


def _query_drug(names: list, max_interactions: int = 50) -> list:
    """Query drug(s) and return structured results."""
    raw = _run_query(_DRUG_QUERY, {"names": names})
    nodes = raw.get("data", {}).get("drugs", {}).get("nodes", [])
    results = []
    for n in nodes:
        interactions = []
        for ix in n.get("interactions", [])[:max_interactions]:
            gene = ix.get("gene") or {}
            interactions.append({
                "gene": gene.get("name"),
                "gene_long_name": gene.get("longName"),
                "score": ix.get("interactionScore"),
                "types": [t.get("type") for t in ix.get("interactionTypes", [])],
                "directionality": [t.get("directionality") for t in ix.get("interactionTypes", [])],
                "attributes": {a["name"]: a["value"] for a in ix.get("interactionAttributes", [])},
                "pmids": [p.get("pmid") for p in ix.get("publications", []) if p.get("pmid")],
                "sources": [s.get("sourceDbName") for s in ix.get("sources", [])],
            })
        approvals = [
            f"{a.get('rating', '')} ({a.get('source', {}).get('sourceDbName', '')})"
            for a in n.get("drugApprovalRatings", [])
        ]
        results.append({
            "query_type": "drug",
            "name": n.get("name"),
            "concept_id": n.get("conceptId"),
            "approval_ratings": approvals,
            "interaction_count": len(n.get("interactions", [])),
            "interactions": interactions,
        })
    return results


def _query_category(category: str, limit: int = 50) -> list:
    """Query gene druggability category."""
    raw = _run_query(_CATEGORY_QUERY, {"category": category, "first": limit})
    nodes = raw.get("data", {}).get("geneCategories", {}).get("nodes", [])
    results = []
    for n in nodes:
        genes = [
            {"name": g.get("name"), "long_name": g.get("longName")}
            for g in n.get("genes", {}).get("nodes", [])
        ]
        results.append({
            "query_type": "category",
            "category": n.get("name"),
            "gene_count": len(genes),
            "genes": genes,
        })
    return results


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def search(entity: str, max_interactions: int = 50) -> list:
    """Search DGIdb by a single entity (gene, drug, or category).

    Auto-detects entity type:
      - ALL-CAPS short token (EGFR, BRAF) -> gene query
      - Known category keyword             -> category query
      - Otherwise                          -> drug query

    Returns list of result dicts.
    """
    entity = entity.strip()
    etype = _detect_type(entity)
    if etype == "gene":
        return _query_gene([entity.upper()], max_interactions)
    elif etype == "category":
        return _query_category(entity, max_interactions)
    else:
        return _query_drug([entity], max_interactions)


def search_batch(entities: list, max_interactions: int = 50) -> dict:
    """Search DGIdb for a list of entities. Returns {entity: results}."""
    # Group by type for efficient batching
    genes, drugs, cats = [], [], []
    for e in entities:
        e = e.strip()
        etype = _detect_type(e)
        if etype == "gene":
            genes.append(e.upper())
        elif etype == "category":
            cats.append(e)
        else:
            drugs.append(e)

    out = {}
    if genes:
        results = _query_gene(genes, max_interactions)
        matched = {r["name"]: r for r in results}
        for g in genes:
            out[g] = [matched[g]] if g in matched else []
    if drugs:
        results = _query_drug(drugs, max_interactions)
        matched = {r["name"].lower(): r for r in results}
        for d in drugs:
            key = d.lower()
            out[d] = [matched[key]] if key in matched else []
    for c in cats:
        out[c] = _query_category(c, max_interactions)
    return out


def summarize(results: list, entity: str) -> str:
    """Produce compact LLM-readable summary text."""
    if not results:
        return f"[DGIdb] No results for '{entity}'."
    lines = [f"[DGIdb] Query: {entity}"]
    for r in results:
        qtype = r.get("query_type", "")
        if qtype == "gene":
            lines.append(f"  Gene: {r['name']} ({r.get('long_name', 'N/A')})")
            cats = ", ".join(r.get("categories", [])) or "none"
            lines.append(f"  Categories: {cats}")
            lines.append(f"  Total interactions: {r['interaction_count']}")
            for ix in r.get("interactions", [])[:10]:
                types_str = ",".join(ix["types"]) if ix["types"] else "N/A"
                src = ",".join(ix["sources"][:3]) if ix["sources"] else ""
                lines.append(
                    f"    Drug: {ix['drug']} | Type: {types_str} | "
                    f"Score: {ix.get('score', 'N/A')} | Src: {src}"
                )
            if r["interaction_count"] > 10:
                lines.append(f"    ... and {r['interaction_count'] - 10} more")
        elif qtype == "drug":
            lines.append(f"  Drug: {r['name']} (ID: {r.get('concept_id', 'N/A')})")
            if r.get("approval_ratings"):
                lines.append(f"  Approval: {'; '.join(r['approval_ratings'][:3])}")
            lines.append(f"  Total interactions: {r['interaction_count']}")
            for ix in r.get("interactions", [])[:10]:
                types_str = ",".join(ix["types"]) if ix["types"] else "N/A"
                src = ",".join(ix["sources"][:3]) if ix["sources"] else ""
                lines.append(
                    f"    Gene: {ix['gene']} | Type: {types_str} | "
                    f"Score: {ix.get('score', 'N/A')} | Src: {src}"
                )
            if r["interaction_count"] > 10:
                lines.append(f"    ... and {r['interaction_count'] - 10} more")
        elif qtype == "category":
            lines.append(f"  Category: {r['category']} ({r['gene_count']} genes)")
            for g in r.get("genes", [])[:20]:
                lines.append(f"    {g['name']} - {g.get('long_name', '')}")
            if r["gene_count"] > 20:
                lines.append(f"    ... and {r['gene_count'] - 20} more")
    return "\n".join(lines)


def to_json(results: list) -> list:
    """Return results as JSON-serializable list (passthrough)."""
    return results


# ---------------------------------------------------------------------------
# Runnable examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Single gene query ---
    print("=" * 60)
    print("1) Gene query: EGFR")
    print("=" * 60)
    hits = search("EGFR")
    print(summarize(hits, "EGFR"))

    # --- Single drug query ---
    print("\n" + "=" * 60)
    print("2) Drug query: imatinib")
    print("=" * 60)
    hits = search("imatinib")
    print(summarize(hits, "imatinib"))

    # --- Category query ---
    print("\n" + "=" * 60)
    print("3) Category query: CLINICALLY ACTIONABLE")
    print("=" * 60)
    hits = search("clinically actionable")
    print(summarize(hits, "clinically actionable"))

    # --- Batch query (mixed types) ---
    print("\n" + "=" * 60)
    print("4) Batch query: [BRAF, TP53, erlotinib, sunitinib]")
    print("=" * 60)
    batch = search_batch(["BRAF", "TP53", "erlotinib", "sunitinib"])
    for entity, res in batch.items():
        print(summarize(res, entity))
        print()

    # --- JSON output ---
    print("\n" + "=" * 60)
    print("5) JSON output for VEGFA")
    print("=" * 60)
    hits = search("VEGFA")
    import pprint
    pprint.pprint(to_json(hits)[:1])