"""
DailyMed - Current Drug Prescribing Information
Category: Drug-centric | Type: DB | Subcategory: Drug Labeling/Info
Link: https://dailymed.nlm.nih.gov/dailymed/spl-resources.cfm

API docs: https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm
No API key required.
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from typing import Union

BASE_URL = "https://dailymed.nlm.nih.gov/dailymed/services/v2"


# ── core helpers ──────────────────────────────────────────────

def search_drug_labels(drug_name: str, limit: int = 5) -> list[dict]:
    """Search SPL labels by drug name. Returns list of label summaries."""
    params = urllib.parse.urlencode({"drug_name": drug_name, "pagesize": limit})
    url = f"{BASE_URL}/spls.json?{params}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read()).get("data", [])


def _xml_to_dict(element: ET.Element) -> dict:
    """Recursively convert an XML Element to a dict (text + children)."""
    tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag
    d: dict = {}
    if element.attrib:
        d["@attr"] = dict(element.attrib)
    children = list(element)
    if children:
        for child in children:
            ctag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            cval = _xml_to_dict(child)
            if ctag in d:
                if not isinstance(d[ctag], list):
                    d[ctag] = [d[ctag]]
                d[ctag].append(cval)
            else:
                d[ctag] = cval
    elif element.text and element.text.strip():
        return element.text.strip()
    return d


def _fetch_xml(url: str) -> dict:
    """Fetch a DailyMed XML endpoint and parse to dict."""
    with urllib.request.urlopen(url, timeout=15) as r:
        tree = ET.parse(r)
    return _xml_to_dict(tree.getroot())


def get_label_detail(set_id: str) -> dict:
    """Get full SPL label detail by set ID (XML-only endpoint → parsed dict)."""
    url = f"{BASE_URL}/spls/{set_id}.xml"
    return _fetch_xml(url)


def get_ndc_info(ndc: str, limit: int = 5) -> list[dict]:
    """Search SPL labels associated with an NDC code."""
    params = urllib.parse.urlencode({"ndc": ndc, "pagesize": limit})
    url = f"{BASE_URL}/spls.json?{params}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read()).get("data", [])


# ── batch wrapper ─────────────────────────────────────────────

def search_batch(entities: list[str], limit: int = 3) -> dict[str, list[dict]]:
    """Search multiple drug names in one call. Returns {entity: [results]}."""
    out: dict[str, list[dict]] = {}
    for e in entities:
        try:
            out[e] = search_drug_labels(e, limit=limit)
        except Exception as exc:
            out[e] = [{"error": str(exc)}]
    return out


# ── compact summariser (LLM-friendly) ────────────────────────

def summarize(results: list[dict], entity: str) -> str:
    """One-line-per-hit summary for LLM consumption."""
    if not results:
        return f"[{entity}] No results."
    lines = [f"[{entity}] {len(results)} hit(s):"]
    for r in results:
        title = r.get("title", "N/A")
        setid = r.get("setid", "")
        lines.append(f"  - {title}  (setid={setid})")
    return "\n".join(lines)


# ── convenience entry point ───────────────────────────────────

def query(entities: Union[str, list[str]], limit: int = 3) -> str:
    """
    Accept a single entity string or a list of entity strings.
    Returns a concise text summary suitable for LLM context.
    """
    if isinstance(entities, str):
        entities = [entities]
    results = search_batch(entities, limit=limit)
    blocks = [summarize(hits, ent) for ent, hits in results.items()]
    return "\n\n".join(blocks)


# ── runnable examples ─────────────────────────────────────────

if __name__ == "__main__":
    # --- single entity ---
    print(query("metformin"))

    # --- multiple entities ---
    print(query(["aspirin", "lisinopril", "atorvastatin"]))

    # --- get detail for first hit ---
    hits = search_drug_labels("metformin", limit=1)
    if hits:
        detail = get_label_detail(hits[0]["setid"])
        title = detail.get("title", "N/A")
        pub = detail.get("published_date", "N/A")
        print(f"\nDetail → title={title}  published={pub}")
        # print(json.dumps(detail, indent=2, ensure_ascii=False)[:800])  # inspect full structure

    # --- NDC lookup ---
    # ndc_hits = get_ndc_info("0002-4462")
    # for item in ndc_hits:
    #     print(f"  NDC → {item.get('title')}  (setid={item.get('setid')})")