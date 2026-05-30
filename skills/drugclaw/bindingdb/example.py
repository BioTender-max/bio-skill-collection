"""
BindingDB – Drug-Target Binding Affinity Data
Category: Drug-centric | Type: DB | Subcategory: Drug-Target Interaction (DTI)
Link: https://www.bindingdb.org/
Paper: https://academic.oup.com/nar/article/53/D1/D1633/7906836

BindingDB is a public database of measured binding affinities, focusing on
protein–small molecule interactions.  Contains 3.2M data points for 1.4M
compounds and 11.4K targets.

Access method: REST API (JSON).
API docs: https://www.bindingdb.org/rwd/bind/BindingDBRESTfulAPI.jsp
"""

import urllib.request
import urllib.parse
import json
import re

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://bindingdb.org/rest"
TIMEOUT  = 30
MAX_HITS = 50          # cap per query for LLM-readable output

# Regex helpers for entity auto-detection
_RE_UNIPROT = re.compile(
    r"^[OPQ][0-9][A-Z0-9]{3}[0-9]$|^[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$"
)
_RE_PDB = re.compile(r"^[0-9][A-Za-z0-9]{3}$")
_SMILES_CHARS = set("()=#[]@/\\+.")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _detect_type(entity: str) -> str:
    """Classify *entity* as 'uniprot', 'pdb', or 'smiles'."""
    e = entity.strip()
    if _RE_UNIPROT.match(e):
        return "uniprot"
    if _RE_PDB.match(e):
        return "pdb"
    if any(ch in _SMILES_CHARS for ch in e):
        return "smiles"
    # Fallback: treat short uppercase strings as UniProt
    return "uniprot"


def _get_json(url: str) -> dict:
    """Fetch *url* and return parsed JSON dict (empty dict on failure)."""
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            if not raw or raw.strip() == "":
                return {}
            return json.loads(raw)
    except Exception as exc:
        return {"_error": str(exc)}


def _extract_affinities(data: dict) -> list[dict]:
    """Pull the affinities list from any BindingDB response wrapper."""
    for key in data:
        if isinstance(data[key], dict):
            aff = data[key].get("affinities")
            if aff is not None:
                return aff if isinstance(aff, list) else [aff]
    return []


# ---------------------------------------------------------------------------
# Core query functions
# ---------------------------------------------------------------------------

def query_by_uniprot(uniprot_ids: str | list[str], cutoff: int = 10000) -> list[dict]:
    """
    Get binding data for one or more UniProt IDs.
    *uniprot_ids*: single ID string or list of IDs.
    *cutoff*: affinity cutoff in nM (IC50/Ki/Kd ≤ cutoff).
    Returns list of affinity dicts.
    """
    if isinstance(uniprot_ids, list):
        uniprot_ids = ",".join(u.strip() for u in uniprot_ids)
    params = urllib.parse.urlencode({
        "uniprot":  uniprot_ids,
        "cutoff":   cutoff,
        "response": "application/json",
    })
    url = f"{BASE_URL}/getLigandsByUniprots?{params}"
    data = _get_json(url)
    return _extract_affinities(data)


def query_by_pdb(pdb_ids: str | list[str], cutoff: int = 10000,
                 identity: int = 92) -> list[dict]:
    """
    Get binding data for one or more PDB IDs.
    *identity*: sequence-identity cutoff in percent (default 92).
    """
    if isinstance(pdb_ids, list):
        pdb_ids = ",".join(p.strip() for p in pdb_ids)
    params = urllib.parse.urlencode({
        "pdb":      pdb_ids,
        "cutoff":   cutoff,
        "identity": identity,
        "response": "application/json",
    })
    url = f"{BASE_URL}/getLigandsByPDBs?{params}"
    data = _get_json(url)
    return _extract_affinities(data)


def query_by_smiles(smiles: str, cutoff: float = 0.85) -> list[dict]:
    """
    Find binding targets for a compound given its SMILES.
    *cutoff*: Tanimoto similarity cutoff (0–1, default 0.85).
    """
    params = urllib.parse.urlencode({
        "smiles":   smiles,
        "cutoff":   cutoff,
        "response": "application/json",
    })
    url = f"{BASE_URL}/getTargetByCompound?{params}"
    data = _get_json(url)
    return _extract_affinities(data)


# ---------------------------------------------------------------------------
# Unified search interface
# ---------------------------------------------------------------------------

def search(entity: str, cutoff: int = 10000) -> dict:
    """
    Auto-detect entity type and query BindingDB.
    Returns {"entity": ..., "type": ..., "hits": int, "affinities": [...]}.
    """
    etype = _detect_type(entity)
    if etype == "uniprot":
        affs = query_by_uniprot(entity, cutoff=cutoff)
    elif etype == "pdb":
        affs = query_by_pdb(entity, cutoff=cutoff)
    else:
        affs = query_by_smiles(entity, cutoff=cutoff / 10000.0 if cutoff > 1 else cutoff)
    return {
        "entity":     entity,
        "type":       etype,
        "hits":       len(affs),
        "affinities": affs[:MAX_HITS],
    }


def search_batch(entities: list[str], cutoff: int = 10000) -> dict:
    """
    Query BindingDB for each entity in *entities*.
    Returns dict[entity_str, search_result].
    """
    results = {}
    for ent in entities:
        results[ent] = search(ent.strip(), cutoff=cutoff)
    return results


# ---------------------------------------------------------------------------
# LLM-readable output
# ---------------------------------------------------------------------------

def summarize(result: dict) -> str:
    """
    One-line-per-hit compact summary suitable for LLM context.
    *result*: output of search().
    """
    ent   = result.get("entity", "?")
    etype = result.get("type", "?")
    affs  = result.get("affinities", [])
    n     = result.get("hits", len(affs))

    lines = [f"## BindingDB results for '{ent}' (type={etype}, total={n})"]
    if not affs:
        lines.append("  (no binding data found)")
        return "\n".join(lines)

    for a in affs[:MAX_HITS]:
        target  = a.get("query", "?")
        mid     = a.get("monomerid", "?")
        smi     = a.get("smile", "?")
        atype   = a.get("affinity_type", "?")
        aval    = a.get("affinity", "?")
        pmid    = a.get("pmid", "")
        doi     = a.get("doi", "")
        ref     = f"PMID:{pmid}" if pmid else (doi if doi else "")
        lines.append(
            f"  BDB:{mid} | {atype}={aval} nM | target={target} | "
            f"SMILES={smi[:60]} | {ref}"
        )
    if n > MAX_HITS:
        lines.append(f"  ... ({n - MAX_HITS} more entries omitted)")
    return "\n".join(lines)


def to_json(result: dict) -> list[dict]:
    """Return affinities list from a search() result (for pipeline use)."""
    return result.get("affinities", [])


# ---------------------------------------------------------------------------
# Demo / runnable examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # --- Single entity: UniProt ---
    print("=" * 60)
    print("1) Single UniProt query: P35355 (COX-2), cutoff 100 nM")
    print("=" * 60)
    r = search("P35355", cutoff=100)
    print(summarize(r))

    # --- Single entity: PDB ---
    print("\n" + "=" * 60)
    print("2) Single PDB query: 1Q0L, cutoff 100 nM")
    print("=" * 60)
    r = search("1Q0L", cutoff=100)
    print(summarize(r))

    # --- Single entity: SMILES (aspirin) ---
    print("\n" + "=" * 60)
    print("3) SMILES query: aspirin CC(=O)Oc1ccccc1C(O)=O")
    print("=" * 60)
    r = search("CC(=O)Oc1ccccc1C(O)=O", cutoff=8500)
    print(summarize(r))

    # --- Batch query ---
    print("\n" + "=" * 60)
    print("4) Batch query: two UniProt IDs")
    print("=" * 60)
    batch = search_batch(["P00176", "P00183"], cutoff=10000)
    for ent, res in batch.items():
        print(summarize(res))
        print()

    # --- JSON output ---
    print("\n" + "=" * 60)
    print("5) JSON output (first 2 records)")
    print("=" * 60)
    r = search("P35355", cutoff=100)
    for rec in to_json(r)[:2]:
        print(json.dumps(rec, indent=2))