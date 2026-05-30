"""
FAERS Query Skill — Query FDA Adverse Event Reporting System via openFDA API.

Functions:
  search_adverse_events(drug, limit)  — raw adverse event reports for a drug
  count_reactions(drug, top_n)        — top reported reactions for a drug
  count_reactions_batch(drugs, top_n) — batch version for multiple drugs
  get_metadata()                      — dataset total count & last_updated
  summarize_reactions(result, drug)   — compact text summary (LLM-friendly)
"""

import json
import urllib.parse
import urllib.request
from typing import Union

BASE_URL = "https://api.fda.gov/drug/event.json"


# ── core helpers ────────────────────────────────────────────────────────────

def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


def _drug_query(drug: str) -> str:
    return urllib.parse.quote(f'patient.drug.medicinalproduct:"{drug.upper()}"')


# ── public API ──────────────────────────────────────────────────────────────

def get_metadata() -> dict:
    """Return total report count and last_updated date."""
    data = _get(f"{BASE_URL}?limit=1")
    meta = data.get("meta", {})
    results = meta.get("results", {})
    return {"total": results.get("total"), "last_updated": meta.get("last_updated")}


def search_adverse_events(drug: str, limit: int = 5) -> dict:
    """Return raw adverse-event reports mentioning *drug*."""
    url = f"{BASE_URL}?search={_drug_query(drug)}&limit={limit}"
    return _get(url)


def count_reactions(drug: str, top_n: int = 10) -> list[dict]:
    """Return top-N reactions for *drug* as [{term, count}, ...]."""
    url = (
        f"{BASE_URL}?search={_drug_query(drug)}"
        f"&count=patient.reaction.reactionmeddrapt.exact&limit={top_n}"
    )
    return _get(url).get("results", [])


def count_reactions_batch(
    drugs: Union[list[str], str], top_n: int = 10
) -> dict[str, list[dict]]:
    """Run count_reactions for each drug; return {drug: [{term,count},…]}."""
    if isinstance(drugs, str):
        drugs = [drugs]
    return {d: count_reactions(d, top_n) for d in drugs}


def summarize_reactions(reactions: list[dict], drug: str) -> str:
    """One-line compact summary for LLM consumption."""
    if not reactions:
        return f"{drug}: no reactions found"
    items = ", ".join(f"{r['term']}({r['count']})" for r in reactions)
    return f"{drug}: {items}"


# ── usage examples ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- single entity ---
    drug = "ASPIRIN"
    rxns = count_reactions(drug, top_n=5)
    print(summarize_reactions(rxns, drug))
    # ASPIRIN: Drug ineffective(12345), Headache(9876), ...

    # --- batch entities ---
    drugs = ["ASPIRIN", "IBUPROFEN", "METFORMIN"]
    batch = count_reactions_batch(drugs, top_n=5)
    for d, rxns in batch.items():
        print(summarize_reactions(rxns, d))

    # --- metadata ---
    meta = get_metadata()
    print(f"Total reports: {meta['total']:,}  Updated: {meta['last_updated']}")

    # --- raw reports (single drug) ---
    raw = search_adverse_events("IBUPROFEN", limit=2)
    for rpt in raw.get("results", []):
        drugs_in_rpt = [d.get("medicinalproduct", "") for d in rpt["patient"].get("drug", [])]
        reactions = [r.get("reactionmeddrapt", "") for r in rpt["patient"].get("reaction", [])]
        print(f"  Drugs: {drugs_in_rpt} | Reactions: {reactions}")