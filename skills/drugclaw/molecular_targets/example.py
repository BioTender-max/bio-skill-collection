#!/usr/bin/env python3
"""
Skill 16 – CCDI Molecular Targets Platform (Pediatric Oncology)
================================================================
Query the NCI CCDI Molecular Targets Platform, an Open Targets instance
focused on preclinical pediatric oncology data, via its public GraphQL API.

Supports: target (gene), disease/phenotype, drug lookups, and free-text
search.  Entity type is auto-detected from the input string.

API endpoint: https://moleculartargets.ccdi.cancer.gov/api/v4/graphql
No authentication required.
"""

import json
import re
import requests
from typing import Optional, Union

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_URL = "https://moleculartargets.ccdi.cancer.gov/api/v4/graphql"
TIMEOUT = 30  # seconds

# ---------------------------------------------------------------------------
# Entity auto-detection
# ---------------------------------------------------------------------------
_PAT_ENSEMBL = re.compile(r"^ENSG\d{11}$", re.I)
_PAT_DISEASE = re.compile(
    r"^(EFO_\d+|MONDO_\d+|Orphanet_\d+|HP_\d+|OTAR_\d+|DOID_\d+)$", re.I
)
_PAT_DRUG = re.compile(r"^CHEMBL\d+$", re.I)


def detect_entity_type(entity: str) -> str:
    """Return one of 'target', 'disease', 'drug', or 'search'."""
    e = entity.strip()
    if _PAT_ENSEMBL.match(e):
        return "target"
    if _PAT_DISEASE.match(e):
        return "disease"
    if _PAT_DRUG.match(e):
        return "drug"
    return "search"


# ---------------------------------------------------------------------------
# Low-level GraphQL helper
# ---------------------------------------------------------------------------
def _post(query: str, variables: Optional[dict] = None) -> Optional[dict]:
    """POST a GraphQL query; return parsed JSON data or None on error."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    try:
        r = requests.post(BASE_URL, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if "errors" in body:
            print(f"[GraphQL errors] {body['errors']}")
            return None
        return body.get("data")
    except Exception as exc:
        print(f"[MolecularTargets API error] {exc}")
        return None


# ---------------------------------------------------------------------------
# GraphQL query fragments
# ---------------------------------------------------------------------------
_Q_SEARCH = """
query Search($q: String!, $page: Pagination) {
  search(queryString: $q, page: $page) {
    total
    hits {
      id
      entity
      name
      description
    }
  }
}
"""

_Q_TARGET = """
query Target($id: String!) {
  target(ensemblId: $id) {
    id
    approvedSymbol
    approvedName
    biotype
    functionDescriptions
    synonyms { label }
    tractability { label modality value }
    geneticConstraint { constraintType score oe oeLower oeUpper }
  }
}
"""

_Q_TARGETS = """
query Targets($ids: [String!]!) {
  targets(ensemblIds: $ids) {
    id
    approvedSymbol
    approvedName
    biotype
    functionDescriptions
  }
}
"""

_Q_DISEASE = """
query Disease($id: String!) {
  disease(efoId: $id) {
    id
    name
    description
    synonyms { terms relation }
    therapeuticAreas { id name }
    parents { id name }
    children { id name }
  }
}
"""

_Q_DISEASES = """
query Diseases($ids: [String!]!) {
  diseases(efoIds: $ids) {
    id
    name
    description
    therapeuticAreas { id name }
  }
}
"""

_Q_DRUG = """
query Drug($id: String!) {
  drug(chemblId: $id) {
    id
    name
    drugType
    maximumClinicalTrialPhase
    isApproved
    hasBeenWithdrawn
    description
    synonyms
    tradeNames
    mechanismsOfAction {
      rows { mechanismOfAction actionType targets { id approvedSymbol } }
    }
    indications {
      count
      rows { disease { id name } maxPhaseForIndication references { source ids } }
    }
  }
}
"""

_Q_DRUGS = """
query Drugs($ids: [String!]!) {
  drugs(chemblIds: $ids) {
    id
    name
    drugType
    maximumClinicalTrialPhase
    isApproved
    hasBeenWithdrawn
    description
  }
}
"""

_Q_ASSOCIATIONS = """
query Assoc($ensemblId: String!, $page: Pagination) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    associatedDiseases(page: $page) {
      count
      rows {
        score
        disease { id name }
        datasourceScores { componentId score }
      }
    }
  }
}
"""

_Q_DISEASE_TARGETS = """
query DiseaseTargets($efoId: String!, $page: Pagination) {
  disease(efoId: $efoId) {
    id
    name
    associatedTargets(page: $page) {
      count
      rows {
        score
        target { id approvedSymbol approvedName }
        datasourceScores { componentId score }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Public API: search / search_batch / summarize / to_json
# ---------------------------------------------------------------------------
def search(entity: str, *, size: int = 10) -> Optional[dict]:
    """
    Query a single entity.  Auto-detects type from the string:
      ENSG00000141510  -> target lookup
      EFO_0000311      -> disease lookup
      CHEMBL25         -> drug lookup
      anything else    -> free-text search
    Returns the raw GraphQL data dict or None.
    """
    etype = detect_entity_type(entity)
    e = entity.strip()

    if etype == "target":
        return _post(_Q_TARGET, {"id": e})
    elif etype == "disease":
        return _post(_Q_DISEASE, {"id": e})
    elif etype == "drug":
        return _post(_Q_DRUG, {"id": e})
    else:
        return _post(_Q_SEARCH, {"q": e, "page": {"index": 0, "size": size}})


def search_batch(entities: list[str]) -> dict[str, Optional[dict]]:
    """Query a list of entities, return {entity: result_dict}."""
    # Group by type for batch queries where possible
    targets, diseases, drugs, texts = [], [], [], []
    for e in entities:
        t = detect_entity_type(e.strip())
        if t == "target":
            targets.append(e.strip())
        elif t == "disease":
            diseases.append(e.strip())
        elif t == "drug":
            drugs.append(e.strip())
        else:
            texts.append(e.strip())

    results: dict[str, Optional[dict]] = {}

    # Batch targets
    if targets:
        data = _post(_Q_TARGETS, {"ids": targets})
        if data and data.get("targets"):
            by_id = {t["id"]: t for t in data["targets"]}
            for tid in targets:
                results[tid] = {"target": by_id.get(tid)}
        else:
            for tid in targets:
                results[tid] = None

    # Batch diseases
    if diseases:
        data = _post(_Q_DISEASES, {"ids": diseases})
        if data and data.get("diseases"):
            by_id = {d["id"]: d for d in data["diseases"]}
            for did in diseases:
                results[did] = {"disease": by_id.get(did)}
        else:
            for did in diseases:
                results[did] = None

    # Batch drugs
    if drugs:
        data = _post(_Q_DRUGS, {"ids": drugs})
        if data and data.get("drugs"):
            by_id = {d["id"]: d for d in data["drugs"]}
            for cid in drugs:
                results[cid] = {"drug": by_id.get(cid)}
        else:
            for cid in drugs:
                results[cid] = None

    # Free-text (no batch endpoint; one at a time)
    for txt in texts:
        results[txt] = search(txt)

    return results


def get_associations(entity: str, *, size: int = 10) -> Optional[dict]:
    """
    Get target-disease associations.
      ENSG… → diseases associated with target
      EFO…  → targets associated with disease
    """
    etype = detect_entity_type(entity)
    e = entity.strip()
    page = {"index": 0, "size": size}
    if etype == "target":
        return _post(_Q_ASSOCIATIONS, {"ensemblId": e, "page": page})
    elif etype == "disease":
        return _post(_Q_DISEASE_TARGETS, {"efoId": e, "page": page})
    else:
        return None


# ---------------------------------------------------------------------------
# Summarize — compact LLM-readable text
# ---------------------------------------------------------------------------
def summarize(data: Optional[dict], entity: str) -> str:
    """Return a compact, LLM-readable summary string."""
    if not data:
        return f"[{entity}] No results."

    lines: list[str] = []

    # --- search hits ---
    if "search" in data:
        s = data["search"]
        lines.append(f"Search '{entity}': {s['total']} hits")
        for h in s.get("hits", []):
            desc = (h.get("description") or "")[:80]
            lines.append(f"  {h['entity']}|{h['id']}|{h['name']}|{desc}")
        return "\n".join(lines)

    # --- target ---
    if "target" in data and data["target"]:
        t = data["target"]
        sym = t.get("approvedSymbol", "?")
        name = t.get("approvedName", "?")
        bio = t.get("biotype", "?")
        funcs = t.get("functionDescriptions") or []
        func_str = funcs[0][:120] if funcs else ""
        lines.append(f"TARGET {t['id']}|{sym}|{name}|{bio}")
        if func_str:
            lines.append(f"  Function: {func_str}")
        # associations if present
        ad = t.get("associatedDiseases")
        if ad:
            lines.append(f"  Associated diseases ({ad['count']} total):")
            for row in ad.get("rows", []):
                d = row["disease"]
                lines.append(f"    {d['id']}|{d['name']}|score={row['score']:.3f}")
        return "\n".join(lines)

    # --- disease ---
    if "disease" in data and data["disease"]:
        d = data["disease"]
        desc = (d.get("description") or "")[:120]
        lines.append(f"DISEASE {d['id']}|{d['name']}")
        if desc:
            lines.append(f"  {desc}")
        ta = d.get("therapeuticAreas") or []
        if ta:
            lines.append(f"  Therapeutic areas: {', '.join(a['name'] for a in ta)}")
        at = d.get("associatedTargets")
        if at:
            lines.append(f"  Associated targets ({at['count']} total):")
            for row in at.get("rows", []):
                tgt = row["target"]
                lines.append(
                    f"    {tgt['id']}|{tgt['approvedSymbol']}|score={row['score']:.3f}"
                )
        return "\n".join(lines)

    # --- drug ---
    if "drug" in data and data["drug"]:
        dr = data["drug"]
        phase = dr.get("maximumClinicalTrialPhase", "?")
        approved = dr.get("isApproved", False)
        lines.append(
            f"DRUG {dr['id']}|{dr['name']}|type={dr.get('drugType','?')}"
            f"|maxPhase={phase}|approved={approved}"
        )
        desc = (dr.get("description") or "")[:120]
        if desc:
            lines.append(f"  {desc}")
        moa = dr.get("mechanismsOfAction")
        if moa:
            for row in moa.get("rows", []):
                tgts = [
                    t.get("approvedSymbol", t["id"])
                    for t in row.get("targets", [])
                ]
                lines.append(
                    f"  MoA: {row['mechanismOfAction']}"
                    f" ({row.get('actionType','?')}) -> {','.join(tgts)}"
                )
        ind = dr.get("indications")
        if ind and ind.get("rows"):
            lines.append(f"  Indications ({ind['count']}):")
            for row in ind["rows"][:10]:
                dis = row["disease"]
                lines.append(
                    f"    {dis['id']}|{dis['name']}|phase={row.get('maxPhaseForIndication','?')}"
                )
        return "\n".join(lines)

    return f"[{entity}] Unrecognised response shape."


def to_json(data: Optional[dict]) -> list[dict]:
    """Flatten result into a list of dicts suitable for pipeline output."""
    if not data:
        return []

    if "search" in data:
        return data["search"].get("hits", [])
    if "target" in data and data["target"]:
        return [data["target"]]
    if "disease" in data and data["disease"]:
        return [data["disease"]]
    if "drug" in data and data["drug"]:
        return [data["drug"]]
    return []


# ---------------------------------------------------------------------------
# CLI examples
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- 1. Free-text search ---
    print("=" * 60)
    print("1) Free-text search: 'neuroblastoma'")
    data = search("neuroblastoma")
    print(summarize(data, "neuroblastoma"))

    # --- 2. Target by Ensembl ID (TP53) ---
    print("\n" + "=" * 60)
    print("2) Target lookup: ENSG00000141510 (TP53)")
    data = search("ENSG00000141510")
    print(summarize(data, "ENSG00000141510"))

    # --- 3. Disease by EFO ID (neuroblastoma) ---
    print("\n" + "=" * 60)
    print("3) Disease lookup: MONDO_0005072")
    data = search("MONDO_0005072")
    print(summarize(data, "MONDO_0005072"))

    # --- 4. Drug by ChEMBL ID (imatinib) ---
    print("\n" + "=" * 60)
    print("4) Drug lookup: CHEMBL941")
    data = search("CHEMBL941")
    print(summarize(data, "CHEMBL941"))

    # --- 5. Target-disease associations for TP53 ---
    print("\n" + "=" * 60)
    print("5) Associations: ENSG00000141510 (TP53)")
    data = get_associations("ENSG00000141510", size=5)
    print(summarize(data, "ENSG00000141510"))

    # --- 6. Disease-target associations ---
    print("\n" + "=" * 60)
    print("6) Associations: EFO_0000621 (Wilms tumor)")
    data = get_associations("EFO_0000621", size=5)
    print(summarize(data, "EFO_0000621"))

    # --- 7. Batch search ---
    print("\n" + "=" * 60)
    print("7) Batch search")
    batch = search_batch(["ENSG00000141510", "CHEMBL25", "medulloblastoma"])
    for ent, res in batch.items():
        print(summarize(res, ent))
        print()

    # --- 8. JSON output ---
    print("\n" + "=" * 60)
    print("8) JSON output for CHEMBL941")
    data = search("CHEMBL941")
    print(json.dumps(to_json(data), indent=2, default=str)[:600])