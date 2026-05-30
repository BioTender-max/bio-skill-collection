"""
49 · PharmGKB / ClinPGx – Pharmacogenomics Knowledge Curation
Category: Drug-related (indirect) | Type: REST API | Subcategory: Pharmacogenomics
Link: https://www.clinpgx.org/
APIs:
  ClinPGx  – https://api.clinpgx.org/v1   (gene/chemical/variant detail; no key)
  CPIC     – https://api.cpicpgx.org/v1   (gene-drug pairs, guidelines; PostgREST)

ClinPGx (successor to PharmGKB, July 2025) curates pharmacogenomics
relationships — genetic variants <-> drug-response phenotypes — plus CPIC
clinical implementation guidelines.

This module exposes search / search_batch / summarize / to_json following the
standard skill interface.  Input entity type is auto-detected.
"""

import urllib.request
import urllib.parse
import json
import re
import time

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CLINPGX_BASE = "https://api.clinpgx.org/v1"
CPIC_BASE    = "https://api.cpicpgx.org/v1"
_HEADERS     = {"User-Agent": "AgentLLM-Skill/49 (ClinPGx query)"}
_TIMEOUT     = 20
_MAX_HITS    = 50
_DELAY       = 0.55   # respect ClinPGx 2 req/s limit


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _get_json(url: str):
    """GET *url* -> parsed JSON with rate-limit pause."""
    time.sleep(_DELAY)
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read())


def _safe(url: str, fallback=None):
    """GET with silent fallback on error."""
    try:
        return _get_json(url)
    except Exception as exc:
        print(f"  [WARN] {url}  ->  {exc}")
        return fallback if fallback is not None else {}


def _detect_type(entity: str) -> str:
    """Classify input: clinpgx_id | rsid | gene_symbol | drug_name."""
    e = entity.strip()
    if re.match(r"^PA\d+$", e, re.IGNORECASE):
        return "clinpgx_id"
    if re.match(r"^rs\d+$", e, re.IGNORECASE):
        return "rsid"
    if re.match(r"^[A-Z][A-Z0-9\-]{1,14}$", e):
        return "gene_symbol"
    return "drug_name"


# ---------------------------------------------------------------------------
# ClinPGx API  (gene / chemical / variant detail)
# ---------------------------------------------------------------------------
def search_gene(symbol: str) -> list:
    """Search gene by symbol -> list of gene dicts."""
    qs = urllib.parse.urlencode({"symbol": symbol, "view": "max"})
    data = _safe(f"{CLINPGX_BASE}/data/gene?{qs}", {})
    return data.get("data", []) if isinstance(data, dict) else []


def get_gene_detail(pa_id: str) -> dict:
    """Fetch gene by ClinPGx accession (PA128)."""
    data = _safe(f"{CLINPGX_BASE}/data/gene/{pa_id}?view=max", {})
    return data.get("data", {}) if isinstance(data, dict) else {}


def search_drug(name: str) -> list:
    """Search chemical/drug by name -> list of chemical dicts."""
    qs = urllib.parse.urlencode({"name": name, "view": "max"})
    data = _safe(f"{CLINPGX_BASE}/data/chemical?{qs}", {})
    return data.get("data", []) if isinstance(data, dict) else []


def get_drug_detail(pa_id: str) -> dict:
    """Fetch chemical by ClinPGx accession (PA448515)."""
    data = _safe(f"{CLINPGX_BASE}/data/chemical/{pa_id}?view=max", {})
    return data.get("data", {}) if isinstance(data, dict) else {}


def search_variant(rsid: str) -> list:
    """Search variant by rsID (rs4244285) -> list."""
    qs = urllib.parse.urlencode({"symbol": rsid, "view": "max"})
    data = _safe(f"{CLINPGX_BASE}/data/variant?{qs}", {})
    return data.get("data", []) if isinstance(data, dict) else []


def lookup_by_id(pa_id: str) -> dict:
    """Try gene, then chemical for a PA-prefixed accession."""
    g = get_gene_detail(pa_id)
    if g:
        return {"type": "gene", "data": g}
    c = get_drug_detail(pa_id)
    if c:
        return {"type": "chemical", "data": c}
    return {}


# ---------------------------------------------------------------------------
# CPIC API  (gene-drug pairs – PostgREST syntax)
# ---------------------------------------------------------------------------
def get_cpic_pairs_by_gene(gene_symbol: str) -> list:
    """Get CPIC gene-drug pairs for a gene via pair_view (PostgREST).

    Example: https://api.cpicpgx.org/v1/pair_view?genesymbol=eq.CYP2D6
    """
    qs = urllib.parse.urlencode({"genesymbol": f"eq.{gene_symbol}"})
    data = _safe(f"{CPIC_BASE}/pair_view?{qs}", [])
    return data if isinstance(data, list) else []


def get_cpic_pairs_by_drug(drug_name: str) -> list:
    """Get CPIC gene-drug pairs for a drug via pair_view (PostgREST).

    Uses ilike for case-insensitive substring match.
    Example: https://api.cpicpgx.org/v1/pair_view?drugname=ilike.*warfarin*
    """
    qs = urllib.parse.urlencode({"drugname": f"ilike.*{drug_name}*"})
    data = _safe(f"{CPIC_BASE}/pair_view?{qs}", [])
    return data if isinstance(data, list) else []


# ---------------------------------------------------------------------------
# Relationship extraction from gene/chemical detail objects
# ---------------------------------------------------------------------------
def _extract_related_chemicals(gene_obj: dict) -> list:
    """Pull related drug info embedded in a gene detail response."""
    out = []
    # ClinPGx gene objects may contain cross-refs under various keys
    for key in ("relatedChemicals", "chemicals", "cpicPairs",
                "dosingGuidelines", "guideline"):
        items = gene_obj.get(key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    out.append(item)
    return out


def _extract_related_genes(chem_obj: dict) -> list:
    """Pull related gene info embedded in a chemical detail response."""
    out = []
    for key in ("relatedGenes", "genes", "cpicPairs",
                "dosingGuidelines", "guideline"):
        items = chem_obj.get(key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    out.append(item)
    return out


# ---------------------------------------------------------------------------
# Unified search
# ---------------------------------------------------------------------------
def search(entity: str) -> dict:
    """Auto-detect entity type and query ClinPGx + CPIC.

    Returns dict with keys:
        entity, entity_type, genes, chemicals, variants,
        cpic_pairs, related
    """
    etype = _detect_type(entity)
    result = {
        "entity": entity,
        "entity_type": etype,
        "genes": [],
        "chemicals": [],
        "variants": [],
        "cpic_pairs": [],
        "related": [],      # cross-refs extracted from detail objects
    }

    if etype == "clinpgx_id":
        info = lookup_by_id(entity.strip())
        if info.get("type") == "gene":
            gdata = info["data"]
            result["genes"] = [gdata]
            sym = gdata.get("symbol", "")
            result["related"] = _extract_related_chemicals(gdata)
            if sym:
                result["cpic_pairs"] = get_cpic_pairs_by_gene(sym)
        elif info.get("type") == "chemical":
            cdata = info["data"]
            result["chemicals"] = [cdata]
            result["related"] = _extract_related_genes(cdata)

    elif etype == "rsid":
        result["variants"] = search_variant(entity.strip())

    elif etype == "gene_symbol":
        sym = entity.strip().upper()
        genes = search_gene(sym)
        result["genes"] = genes
        if genes:
            result["related"] = _extract_related_chemicals(genes[0])
        result["cpic_pairs"] = get_cpic_pairs_by_gene(sym)

    else:  # drug_name
        name = entity.strip()
        chems = search_drug(name)
        result["chemicals"] = chems
        if chems:
            result["related"] = _extract_related_genes(chems[0])
        result["cpic_pairs"] = get_cpic_pairs_by_drug(name)

    return result


def search_batch(entities: list) -> dict:
    """Run search() for each entity.  Returns dict[entity -> result]."""
    return {e: search(e) for e in entities}


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def _fmt_gene(g: dict) -> str:
    sym = g.get("symbol", "?")
    gid = g.get("id", "?")
    name = g.get("name", "")
    cpic = "yes" if g.get("hasCpicGuideline") or g.get("cpicGene") else "no"
    return f"{sym} ({gid}) {name} | cpic={cpic}"


def _fmt_chemical(c: dict) -> str:
    cid = c.get("id", "?")
    name = c.get("name", "?")
    types = ", ".join(c.get("types", [])) if c.get("types") else ""
    return f"{name} ({cid}) type=[{types}]"


def _fmt_variant(v: dict) -> str:
    vid = v.get("id", "?")
    sym = v.get("symbol", v.get("name", "?"))
    genes = ", ".join(
        g.get("symbol", g.get("id", "?"))
        for g in (v.get("genes", []) or [])
    ) or "N/A"
    loc = v.get("location", "")
    return f"{sym} ({vid}) gene={genes} loc={loc}"


def _fmt_cpic_pair(p: dict) -> str:
    gene = p.get("genesymbol", "?")
    drug = p.get("drugname", p.get("drug", "?"))
    level = p.get("cpiclevel", p.get("cpicLevel", ""))
    pgx_testing = p.get("pgxtesting", "")
    guideline = p.get("guidelinename", p.get("guideline", ""))
    # CPIC schema update: clinpgxlevel replaces pgkbcalevel
    ca_level = p.get("clinpgxlevel", p.get("pgkbcalevel", ""))
    parts = [f"{gene} <-> {drug}"]
    if level:
        parts.append(f"CPIC-level={level}")
    if ca_level:
        parts.append(f"CA-level={ca_level}")
    if pgx_testing:
        parts.append(f"testing={pgx_testing}")
    if guideline:
        parts.append(f"guideline={guideline}")
    return " | ".join(parts)


def _fmt_related(r: dict) -> str:
    """Format a related cross-ref object (could be gene, drug, guideline)."""
    name = r.get("name", r.get("symbol", r.get("title", "?")))
    rid = r.get("id", "")
    obj_cls = r.get("objCls", r.get("type", ""))
    parts = [name]
    if rid:
        parts[0] += f" ({rid})"
    if obj_cls:
        parts.append(f"[{obj_cls}]")
    return " ".join(parts)


def summarize(result: dict, entity: str = None) -> str:
    """One-line-per-hit compact text suitable for LLM context."""
    label = entity or result.get("entity", "?")
    lines = [f"=== ClinPGx: {label} (type={result.get('entity_type','?')}) ==="]

    for g in result.get("genes", [])[:_MAX_HITS]:
        lines.append("  [Gene] " + _fmt_gene(g))

    for c in result.get("chemicals", [])[:_MAX_HITS]:
        lines.append("  [Drug] " + _fmt_chemical(c))

    for v in result.get("variants", [])[:_MAX_HITS]:
        lines.append("  [Var]  " + _fmt_variant(v))

    pairs = result.get("cpic_pairs", [])[:_MAX_HITS]
    if pairs:
        lines.append(f"  -- CPIC Pairs ({len(pairs)}) --")
        for p in pairs:
            lines.append("    " + _fmt_cpic_pair(p))

    related = result.get("related", [])[:20]
    if related:
        lines.append(f"  -- Related ({len(related)}) --")
        for r in related:
            lines.append("    " + _fmt_related(r))

    if len(lines) == 1:
        lines.append("  (no results)")
    return "\n".join(lines)


def to_json(result: dict) -> str:
    """Return search result as indented JSON string."""
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Single-entity queries ------------------------------------------------
    print(">>> search('CYP2D6')  [gene symbol]")
    r1 = search("CYP2D6")
    print(summarize(r1))

    print("\n>>> search('warfarin')  [drug name]")
    r2 = search("warfarin")
    print(summarize(r2))

    print("\n>>> search('rs4244285')  [variant rsID]")
    r3 = search("rs4244285")
    print(summarize(r3))

    print("\n>>> search('PA128')  [ClinPGx accession]")
    r4 = search("PA128")
    print(summarize(r4))

    # --- Batch query ----------------------------------------------------------
    print("\n>>> search_batch(['CYP2C19', 'clopidogrel'])")
    batch = search_batch(["CYP2C19", "clopidogrel"])
    for ent, res in batch.items():
        print(summarize(res, ent))
        print()

    # --- JSON output (trimmed) ------------------------------------------------
    print(">>> to_json (trimmed):")
    r1_small = {k: (v[:2] if isinstance(v, list) else v)
                for k, v in r1.items()}
    print(to_json(r1_small))