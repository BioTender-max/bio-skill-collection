"""
CPIC - Clinical Pharmacogenomics Implementation Consortium
Category: Drug-centric | Type: DB | Subcategory: Drug Knowledgebase
Link: https://cpicpgx.org/
Paper: https://pubmed.ncbi.nlm.nih.gov/33479744/
API docs: https://cpicpgx.org/cpic-data/
No API key required. PostgREST-based API.

API schema (verified):
  /v1/drug        — drugid, name, drugbankid, atcid, flowchart, guidelineid ...
  /v1/guideline   — name, url, version ...
  /v1/pair        — genesymbol, drugid, cpiclevel, clinpgxlevel, pgxtesting, citations ...
  /v1/recommendation — drugid, phenotypes, implications, drugrecommendation, classification ...
Note: pair and recommendation use 'drugid' (e.g. 'RxNorm:32968'), NOT drug name.
      Must resolve name → drugid via /v1/drug first.
"""

import urllib.request
import urllib.parse
import json
from typing import Union

BASE_URL = "https://api.cpicpgx.org/v1"


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _get_json(url: str):
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.loads(resp.read())


def _resolve_drug(name: str) -> list[dict]:
    """Look up drug table by name (case-insensitive fuzzy). Returns list of drug rows."""
    encoded = urllib.parse.quote(f"*{name}*")
    return _get_json(f"{BASE_URL}/drug?name=ilike.{encoded}")


def _resolve_drugid(name: str) -> str | None:
    """Resolve a drug name to its drugid (e.g. 'RxNorm:32968'). None if not found."""
    hits = _resolve_drug(name)
    return hits[0]["drugid"] if hits else None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_drug_info(drug_name: str) -> list[dict]:
    """Get drug metadata from CPIC drug table by name (fuzzy match)."""
    return _resolve_drug(drug_name)


def get_guidelines(drug_name: str = None) -> list[dict]:
    """
    Get CPIC guidelines. If drug_name given, filter by that drug.
    Uses two strategies: (1) name substring match, (2) guidelineid from drug table.
    This handles cases like simvastatin whose guideline is named 'Statins'.
    """
    all_gl = _get_json(f"{BASE_URL}/guideline")
    if not drug_name:
        return all_gl

    q = drug_name.lower()
    # Strategy 1: name substring match
    matched = [g for g in all_gl if q in str(g.get("name", "")).lower()]

    # Strategy 2: resolve guidelineid via drug table
    drug_rows = _resolve_drug(drug_name)
    gl_ids = {d["guidelineid"] for d in drug_rows if d.get("guidelineid")}
    if gl_ids:
        id_matched = [g for g in all_gl if g.get("id") in gl_ids]
        # Merge without duplicates
        seen = {id(g) for g in matched}
        for g in id_matched:
            if id(g) not in seen:
                matched.append(g)
    return matched


def get_gene_drug_pairs(drug_name: str = None, gene: str = None) -> list[dict]:
    """
    Get gene-drug pairs. Filter by drug name and/or gene symbol.
    Drug name is resolved to drugid via the drug table.
    """
    filters = []
    if drug_name:
        drugid = _resolve_drugid(drug_name)
        if not drugid:
            return []
        filters.append(f"drugid=eq.{urllib.parse.quote(drugid)}")
    if gene:
        filters.append(f"genesymbol=eq.{urllib.parse.quote(gene.upper())}")

    qs = "&".join(filters) if filters else ""
    url = f"{BASE_URL}/pair?{qs}" if qs else f"{BASE_URL}/pair"
    return _get_json(url)


def get_recommendations(drug_name: str) -> list[dict]:
    """Get CPIC dosing recommendations for a drug (resolved by name → drugid)."""
    drugid = _resolve_drugid(drug_name)
    if not drugid:
        return []
    return _get_json(f"{BASE_URL}/recommendation?drugid=eq.{urllib.parse.quote(drugid)}")


def query(entities: Union[str, list[str]], fields: str = "all") -> list[dict]:
    """
    Unified query interface. Accepts one or more drug names (or gene symbols).

    Parameters
    ----------
    entities : str or list[str]
        Drug name(s) or gene symbol(s) to query.
    fields : str
        'all'             — drug info + guidelines + gene-drug pairs + recommendations.
        'guidelines'      — guidelines only.
        'pairs'           — gene-drug pairs only.
        'recommendations' — dosing recommendations only.

    Returns
    -------
    list[dict] — one dict per entity with query results.
    """
    if isinstance(entities, str):
        entities = [entities]

    results = []
    for entity in entities:
        entity = entity.strip()
        if not entity:
            continue

        record = {"query": entity}
        try:
            # Heuristic: gene symbols are short, uppercase, start with letter
            is_gene = entity.isupper() and entity[0].isalpha() and len(entity) <= 12

            if fields in ("all",):
                drug_rows = get_drug_info(entity)
                record["drug_info"] = [
                    {"drugid": d.get("drugid"), "name": d.get("name"),
                     "drugbankid": d.get("drugbankid"), "atcid": d.get("atcid"),
                     "flowchart": d.get("flowchart")}
                    for d in drug_rows
                ]

            if fields in ("all", "guidelines"):
                record["guidelines"] = [
                    {"name": g.get("name"), "url": g.get("url"),
                     "version": g.get("version")}
                    for g in get_guidelines(entity)
                ]

            if fields in ("all", "pairs"):
                if is_gene:
                    pairs = get_gene_drug_pairs(gene=entity)
                else:
                    pairs = get_gene_drug_pairs(drug_name=entity)
                    if not pairs and entity.isupper():
                        pairs = get_gene_drug_pairs(gene=entity)
                record["gene_drug_pairs"] = [
                    {"genesymbol": p.get("genesymbol"), "drugid": p.get("drugid"),
                     "cpiclevel": p.get("cpiclevel"), "clinpgxlevel": p.get("clinpgxlevel"),
                     "pgxtesting": p.get("pgxtesting"), "citations": p.get("citations")}
                    for p in pairs
                ]

            if fields in ("all", "recommendations"):
                if not is_gene:
                    recs = get_recommendations(entity)
                    record["recommendations"] = [
                        {"drugid": r.get("drugid"),
                         "phenotypes": r.get("phenotypes"),
                         "implications": r.get("implications"),
                         "recommendation": r.get("drugrecommendation"),
                         "classification": r.get("classification"),
                         "population": r.get("population")}
                        for r in recs
                    ]
                else:
                    record["recommendations"] = []

        except Exception as e:
            record["error"] = str(e)

        results.append(record)

    return results


# ---------------------------------------------------------------------------
# Usage examples (LLM-friendly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Example 1: Query a single drug ---
    print("=== Single drug: clopidogrel ===")
    out = query("clopidogrel")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:1000])

    # --- Example 2: Query multiple drugs ---
    print("\n=== Batch query: warfarin, codeine ===")
    out = query(["warfarin", "codeine"])
    for item in out:
        print(f"  {item['query']}:")
        print(f"    drug_info:       {len(item.get('drug_info', []))}")
        print(f"    guidelines:      {len(item.get('guidelines', []))}")
        print(f"    gene-drug pairs: {len(item.get('gene_drug_pairs', []))}")
        print(f"    recommendations: {len(item.get('recommendations', []))}")

    # --- Example 3: Query by gene symbol ---
    print("\n=== Gene query: CYP2D6 (pairs only) ===")
    out = query("CYP2D6", fields="pairs")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])

    # --- Example 4: Guidelines only (shows guidelineid fallback) ---
    # simvastatin's guideline is named "SLCO1B1, ABCG2, CYP2C9, and Statins"
    # — found via drug table guidelineid, not name substring match
    print("\n=== Guidelines only: simvastatin ===")
    out = query("simvastatin", fields="guidelines")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:500])

    # --- Example 5: Recommendations only ---
    print("\n=== Recommendations only: codeine ===")
    out = query("codeine", fields="recommendations")
    print(json.dumps(out, indent=2, ensure_ascii=False)[:600])