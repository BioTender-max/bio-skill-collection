"""
openFDA Human Drug – Structured Drug Prescribing Information
Category: Drug-centric | Type: API | Subcategory: Drug Labeling/Info
Endpoint: https://api.fda.gov/drug/label.json
Docs: https://open.fda.gov/apis/drug/label/
No API key required (≤1 000 req/day, ≤240 req/min).
"""

import urllib.request, urllib.parse, json
from typing import Union

BASE_URL = "https://api.fda.gov/drug/label.json"


# ── core helpers ────────────────────────────────────────────────

def _get(params: str) -> dict:
    url = f"{BASE_URL}?{params}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())


def _extract(label: dict) -> dict:
    """Flatten one label result into an LLM-friendly dict."""
    fda = label.get("openfda", {})
    return {
        "brand_name":       fda.get("brand_name", ["N/A"])[0],
        "generic_name":     fda.get("generic_name", ["N/A"])[0],
        "manufacturer":     fda.get("manufacturer_name", ["N/A"])[0],
        "route":            fda.get("route", ["N/A"])[0],
        "substance_name":   fda.get("substance_name", ["N/A"])[0],
        "product_type":     fda.get("product_type", ["N/A"])[0],
        "indications":      (label.get("indications_and_usage") or ["N/A"])[0][:500],
        "contraindications": (label.get("contraindications") or ["N/A"])[0][:300],
        "warnings":         (label.get("warnings") or ["N/A"])[0][:300],
        "dosage":           (label.get("dosage_and_administration") or ["N/A"])[0][:300],
        "adverse_reactions": (label.get("adverse_reactions") or ["N/A"])[0][:300],
    }


# ── public API ──────────────────────────────────────────────────

def search_drug(query: Union[str, list[str]], limit: int = 3) -> dict:
    """
    Search drug labels by brand/generic name OR indication text.
    Accepts a single string or a list of strings.
    Returns {query_term: [extracted_labels]}.
    """
    if isinstance(query, str):
        query = [query]
    results = {}
    for q in query:
        sq = urllib.parse.quote(f'openfda.brand_name:"{q}" OR openfda.generic_name:"{q}"')
        try:
            data = _get(f"search={sq}&limit={limit}")
            results[q] = [_extract(r) for r in data.get("results", [])]
        except Exception as e:
            results[q] = [{"error": str(e)}]
    return results


def search_by_indication(query: Union[str, list[str]], limit: int = 3) -> dict:
    """
    Search labels whose indications_and_usage mention the given condition(s).
    Accepts a single string or a list of strings.
    Returns {condition: [extracted_labels]}.
    """
    if isinstance(query, str):
        query = [query]
    results = {}
    for q in query:
        sq = urllib.parse.quote(f'indications_and_usage:"{q}"')
        try:
            data = _get(f"search={sq}&limit={limit}")
            results[q] = [_extract(r) for r in data.get("results", [])]
        except Exception as e:
            results[q] = [{"error": str(e)}]
    return results


def count_by_route(top_n: int = 10) -> list[dict]:
    """Top N administration routes across all labels."""
    try:
        data = _get(f"count=openfda.route.exact&limit={top_n}")
        return data.get("results", [])
    except Exception as e:
        return [{"error": str(e)}]


def summarize(results: dict) -> str:
    """Return a compact, LLM-readable text summary of search results."""
    lines = []
    for term, labels in results.items():
        lines.append(f"### {term}")
        if not labels or "error" in labels[0]:
            lines.append(f"  No results or error: {labels}")
            continue
        for i, lb in enumerate(labels, 1):
            lines.append(f"  [{i}] {lb['brand_name']} ({lb['generic_name']})")
            lines.append(f"      Route: {lb['route']} | Mfr: {lb['manufacturer']}")
            lines.append(f"      Indications: {lb['indications'][:200]}...")
    return "\n".join(lines)


# ── runnable examples ───────────────────────────────────────────

if __name__ == "__main__":
    # --- Example 1: single drug lookup ---
    r = search_drug("ASPIRIN", limit=1)
    print(summarize(r))

    # --- Example 2: batch drug lookup ---
    r = search_drug(["METFORMIN", "LISINOPRIL"], limit=2)
    print(summarize(r))

    # --- Example 3: single indication search ---
    r = search_by_indication("hypertension", limit=2)
    print(summarize(r))

    # --- Example 4: batch indication search ---
    r = search_by_indication(["diabetes", "migraine"], limit=2)
    print(summarize(r))

    # --- Example 5: top routes ---
    routes = count_by_route(5)
    for rt in routes:
        if "error" in rt:
            print(f"  Error: {rt['error']}")
        else:
            print(f"  {rt['term']}: {rt['count']}")

    # --- Example 6: raw JSON for downstream use ---
    raw = search_drug("IBUPROFEN", limit=1)
    print(json.dumps(raw, indent=2, ensure_ascii=False))