"""
MedlinePlus Drug Info – Consumer-Oriented Drug Information Skill
Category: Drug-centric | Type: Public REST API | Subcategory: Drug Labeling/Info
Link: https://medlineplus.gov/druginformation.html

Two endpoints, no API key required:
  1. Web Service (wsearch) – keyword search over health topics, returns XML
     https://wsearch.nlm.nih.gov/ws/query
  2. MedlinePlus Connect – code-based lookup (RxCUI / NDC / drug name), returns JSON
     https://connect.medlineplus.gov/service
"""

import re
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# ── endpoints ────────────────────────────────────────────────────────────────
WS_BASE = "https://wsearch.nlm.nih.gov/ws/query"
CONNECT_BASE = "https://connect.medlineplus.gov/service"

MAX_RESULTS = 50          # cap per query
TIMEOUT = 20              # seconds

# ── input-type detection ─────────────────────────────────────────────────────
_RE_NDC   = re.compile(r"^\d{4,5}-\d{3,4}-\d{1,2}$")     # e.g. 0069-3060-30
_RE_RXCUI = re.compile(r"^\d{5,7}$")                       # e.g. 637188
_RE_ICD10 = re.compile(r"^[A-Z]\d{2}(?:\.\d{1,4})?$")     # e.g. E11.9


def _detect_input(query: str) -> str:
    """Return one of: 'ndc', 'rxcui', 'icd10', 'text'."""
    q = query.strip()
    if _RE_NDC.match(q):
        return "ndc"
    if _RE_RXCUI.match(q):
        return "rxcui"
    if _RE_ICD10.match(q):
        return "icd10"
    return "text"


# ── internal helpers ─────────────────────────────────────────────────────────

def _strip_html(text: str) -> str:
    """Remove HTML tags for plain-text output."""
    return re.sub(r"<[^>]+>", "", text).strip()


def _fetch(url: str) -> bytes:
    """GET with timeout; returns raw bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "AgentLLM-MedlinePlus/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


# ── wsearch (keyword → XML) ────────────────────────────────────────────────

def _wsearch(term: str, retmax: int = 10) -> list[dict]:
    """
    Query the MedlinePlus Web Service (XML).
    Returns list of dicts with keys: title, url, snippet, rank.
    """
    params = urllib.parse.urlencode({
        "db": "healthTopics",
        "term": term,
        "rettype": "brief",
        "retmax": min(retmax, MAX_RESULTS),
    })
    url = f"{WS_BASE}?{params}"
    raw = _fetch(url)
    root = ET.fromstring(raw)

    results = []
    for doc in root.iter("document"):
        rank = doc.attrib.get("rank", "")
        url_val = doc.attrib.get("url", "")
        title = snippet = ""
        for content in doc.iter("content"):
            name = content.attrib.get("name", "")
            text = _strip_html(ET.tostring(content, encoding="unicode", method="text"))
            if name == "title":
                title = text
            elif name == "snippet":
                snippet = text[:300]
            elif name == "FullSummary" and not snippet:
                snippet = text[:300]
        results.append({
            "title": title,
            "url": url_val,
            "snippet": snippet,
            "rank": rank,
        })
    return results


# ── MedlinePlus Connect (code / name → JSON) ───────────────────────────────

def _connect_by_drug_name(drug_name: str) -> list[dict]:
    """Look up drug info by name via MedlinePlus Connect (JSON)."""
    params = urllib.parse.urlencode({
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.88",   # RxNorm system
        "mainSearchCriteria.v.dn": drug_name,
        "knowledgeResponseType": "application/json",
    })
    return _parse_connect_json(f"{CONNECT_BASE}?{params}")


def _connect_by_rxcui(rxcui: str) -> list[dict]:
    """Look up drug info by RxCUI."""
    params = urllib.parse.urlencode({
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.88",
        "mainSearchCriteria.v.c": rxcui,
        "knowledgeResponseType": "application/json",
    })
    return _parse_connect_json(f"{CONNECT_BASE}?{params}")


def _connect_by_ndc(ndc: str) -> list[dict]:
    """Look up drug info by NDC code."""
    params = urllib.parse.urlencode({
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.69",
        "mainSearchCriteria.v.c": ndc,
        "knowledgeResponseType": "application/json",
    })
    return _parse_connect_json(f"{CONNECT_BASE}?{params}")


def _connect_by_icd10(code: str) -> list[dict]:
    """Look up health topic by ICD-10-CM diagnosis code."""
    params = urllib.parse.urlencode({
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.90",
        "mainSearchCriteria.v.c": code,
        "knowledgeResponseType": "application/json",
    })
    return _parse_connect_json(f"{CONNECT_BASE}?{params}")


def _parse_connect_json(url: str) -> list[dict]:
    """Fetch MedlinePlus Connect JSON and return normalised records."""
    raw = _fetch(url)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    entries = data.get("feed", {}).get("entry", [])
    results = []
    for entry in entries:
        title = entry.get("title", {}).get("_value", "")
        link_list = entry.get("link", [])
        link = link_list[0].get("href", "") if isinstance(link_list, list) and link_list else ""
        summary_raw = str(entry.get("summary", {}).get("_value", ""))
        summary = _strip_html(summary_raw)[:400]
        source = ""
        author = entry.get("author", {})
        if isinstance(author, dict):
            source = author.get("name", {}).get("_value", "")
        results.append({
            "title": title,
            "url": link,
            "summary": summary,
            "source": source,
        })
    return results


# ── public API ───────────────────────────────────────────────────────────────

def search(query: str, max_results: int = 10) -> dict:
    """
    Search MedlinePlus for a single entity.
    Auto-detects input type (NDC, RxCUI, ICD-10, or free-text drug name).

    Returns dict:
      {
        "query": str,
        "input_type": str,
        "connect_results": [...],   # from MedlinePlus Connect
        "wsearch_results": [...],   # from keyword web service
      }
    """
    q = query.strip()
    itype = _detect_input(q)

    connect = []
    ws = []
    errors = []

    # MedlinePlus Connect lookup
    try:
        if itype == "ndc":
            connect = _connect_by_ndc(q)
        elif itype == "rxcui":
            connect = _connect_by_rxcui(q)
        elif itype == "icd10":
            connect = _connect_by_icd10(q)
        else:
            connect = _connect_by_drug_name(q)
    except Exception as exc:
        errors.append(f"Connect API error: {exc}")

    # wsearch keyword lookup (skip for pure codes unless connect returned nothing)
    search_term = q
    if itype in ("ndc", "rxcui", "icd10") and connect:
        # use title from connect result as keyword
        if connect[0].get("title"):
            search_term = connect[0]["title"]
        else:
            search_term = None
    if search_term:
        try:
            ws = _wsearch(search_term, retmax=min(max_results, MAX_RESULTS))
        except Exception as exc:
            errors.append(f"wsearch API error: {exc}")

    return {
        "query": q,
        "input_type": itype,
        "connect_results": connect[:MAX_RESULTS],
        "wsearch_results": ws[:MAX_RESULTS],
        "errors": errors,
    }


def search_batch(queries: list[str], max_results: int = 10) -> dict[str, dict]:
    """Search MedlinePlus for a list of entities. Returns {query: result_dict}."""
    return {q: search(q, max_results=max_results) for q in queries}


def summarize(result: dict) -> str:
    """
    Return a compact, LLM-readable text summary for one search() result.
    """
    lines = [f"## MedlinePlus: {result['query']}  (type={result['input_type']})"]

    if result.get("connect_results"):
        lines.append("Connect results:")
        for i, r in enumerate(result["connect_results"][:10], 1):
            line = f"  {i}. {r['title']}"
            if r.get("url"):
                line += f"  | {r['url']}"
            if r.get("summary"):
                line += f"\n     {r['summary'][:200]}"
            lines.append(line)

    if result.get("wsearch_results"):
        lines.append("Health-topic search results:")
        for i, r in enumerate(result["wsearch_results"][:10], 1):
            line = f"  {i}. {r['title']}"
            if r.get("url"):
                line += f"  | {r['url']}"
            if r.get("snippet"):
                line += f"\n     {r['snippet'][:200]}"
            lines.append(line)

    if result.get("errors"):
        lines.append("Errors: " + "; ".join(result["errors"]))

    if not result.get("connect_results") and not result.get("wsearch_results"):
        lines.append("No results found.")

    return "\n".join(lines)


def to_json(result: dict) -> list[dict]:
    """Flatten connect + wsearch results into a single list of dicts."""
    out = []
    for r in result.get("connect_results", []):
        out.append({**r, "_source": "connect"})
    for r in result.get("wsearch_results", []):
        out.append({**r, "_source": "wsearch"})
    return out


# ── main demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- Single entity: drug name ---
    print("=== search('metformin') ===")
    res = search("metformin")
    print(summarize(res))
    print()

    # --- Single entity: RxCUI ---
    print("=== search('637188') (RxCUI for varenicline) ===")
    res = search("637188")
    print(summarize(res))
    print()

    # --- Single entity: NDC ---
    print("=== search('0069-3060-30') (NDC) ===")
    res = search("0069-3060-30")
    print(summarize(res))
    print()

    # --- Single entity: ICD-10 ---
    print("=== search('E11.9') (ICD-10 Type 2 diabetes) ===")
    res = search("E11.9")
    print(summarize(res))
    print()

    # --- Batch ---
    print("=== search_batch(['aspirin', 'ibuprofen', 'E11.9']) ===")
    batch = search_batch(["aspirin", "ibuprofen", "E11.9"])
    for q, r in batch.items():
        print(summarize(r))
        print()

    # --- JSON output ---
    print("=== to_json (aspirin) ===")
    res = search("aspirin")
    for rec in to_json(res)[:3]:
        print(json.dumps(rec, indent=2))