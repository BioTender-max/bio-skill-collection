"""
16_NCI_DTP_MolTarget – NCI-60 Molecular Target (Protein) Query Skill
Category : Target-centric | Type: Local flat file | Subcategory: Drug Target
Source   : https://wiki.nci.nih.gov/spaces/NCIDTPdata/pages/155845004/Molecular+Target+Data
File     : WEB_DATA_PROTEIN.ZIP  (protein expression across NCI-60 cell lines)

Download:
  Already at: resources_metadata/
               dti/Molecular Target Data/WEB_DATA_PROTEIN.TXT
"""

import csv, os, re, json, io
from pathlib import Path
from collections import defaultdict
from typing import Union

# ── Config ──────────────────────────────────────────────────────────────
DATA_PATH = os.environ.get(
    "NCI_MOLTARGET_DATA",
    str(
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "dti"
        / "Molecular Target Data"
        / "WEB_DATA_PROTEIN.TXT"
    ),
)

# Column names from NCI documentation (protein subset)
COLUMNS = [
    "MOLTID", "GENE", "TITLE", "MOLTNBR", "PANELNBR", "CELLNBR",
    "pname", "cellname", "ENTITY_MEASURED", "GeneID", "UNITS",
    "METHOD", "VALUE", "TEXT",
]

# Known NCI-60 panel names for auto-detection
_PANELS = {
    "breast", "cns", "colon", "leukemia", "melanoma",
    "non-small cell lung", "nsclc", "ovarian", "prostate", "renal",
}

# ── Loader ──────────────────────────────────────────────────────────────

def _find_data_file(path: str) -> str:
    """Resolve DATA_PATH to an actual CSV file."""
    if os.path.isfile(path):
        return path
    if os.path.isdir(path):
        for f in os.listdir(path):
            if f.lower().endswith((".csv", ".txt", "")):
                candidate = os.path.join(path, f)
                if os.path.isfile(candidate):
                    return candidate
    # Try common names next to path
    base = os.path.dirname(path) if os.path.isfile(path) else path
    for name in ["WEB_DATA_PROTEIN.TXT", "WEB_DATA_PROTEIN",
                 "WEB_DATA_PROTEIN.csv",
                 "WEB_DATA_ALL_MT.TXT", "WEB_DATA_ALL_MT",
                 "WEB_DATA_ALL_MT.csv"]:
        p = os.path.join(base, name)
        if os.path.isfile(p):
            return p
    raise FileNotFoundError(
        f"Cannot locate NCI DTP molecular target data at: {path}\n"
        "Download WEB_DATA_PROTEIN.ZIP from NCI DTP wiki and unzip."
    )


def load_data(path: str = DATA_PATH) -> list[dict]:
    """Load NCI DTP molecular target CSV → list[dict].

    The CSV is comma-delimited, headerless; columns follow NCI documentation.
    Some rows may have fewer columns (especially missing TEXT field).
    """
    fpath = _find_data_file(path)
    records = []
    with open(fpath, encoding="utf-8", errors="replace") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            rec = {}
            for i, col in enumerate(COLUMNS):
                rec[col] = row[i].strip() if i < len(row) else ""
            # parse VALUE to float when possible
            try:
                rec["VALUE"] = float(rec["VALUE"])
            except (ValueError, TypeError):
                pass
            records.append(rec)
    return records


# ── Entity auto-detection ───────────────────────────────────────────────

def _detect_type(entity: str) -> str:
    """Guess entity type from its pattern.

    Returns one of: 'moltid', 'geneid', 'panel', 'cellline', 'gene'.
    """
    e = entity.strip()
    if re.fullmatch(r"\d+", e):
        # pure number — could be MOLTID or GeneID; default MOLTID
        return "moltid"
    if e.lower() in _PANELS:
        return "panel"
    # NCI-60 cell lines often contain '/' or '-' (e.g., "NCI-H460", "MDA-MB-231")
    if re.search(r"NCI[/-]|MDA[/-]|SK[/-]|HCC-|HOP-|RPMI|IGROV|CAKI|UO-|SN12|ACHN|TK-10|RXF|OVCAR|UACC|MALME|M14|LOX|HT29|COLO|HCT|SW-|KM12|SF-|SNB|U251|DU-145|PC-3|A498|786-0|HS 578T|BT-549|T-47D|MCF7|K-562|MOLT-4|CCRF-CEM|HL-60|SR|A549|EKVX|NCI/ADR-RES",
                 e, re.IGNORECASE):
        return "cellline"
    return "gene"


# ── Core search ─────────────────────────────────────────────────────────

def search(data: list[dict], entity: str) -> list[dict]:
    """Search records matching a single entity (gene, cell line, panel, MOLTID).

    Auto-detects entity type. Returns matching rows as list[dict].
    """
    etype = _detect_type(entity)
    e = entity.strip()
    e_low = e.lower()

    if etype == "moltid":
        return [r for r in data if r["MOLTID"] == e]
    if etype == "geneid":
        return [r for r in data if r["GeneID"] == e]
    if etype == "panel":
        return [r for r in data if e_low in r["pname"].lower()]
    if etype == "cellline":
        return [r for r in data
                if e_low in r["cellname"].lower()
                or e_low == r["cellname"].lower()]
    # default: gene / protein name — match GENE or ENTITY_MEASURED
    return [r for r in data
            if e_low == r["GENE"].lower()
            or e_low in r["ENTITY_MEASURED"].lower()
            or e_low in r["TITLE"].lower()]


def search_batch(data: list[dict], entities: list[str]) -> dict:
    """Search multiple entities. Returns {entity_str: [rows]}."""
    return {e: search(data, e) for e in entities}


# ── Summarisers (LLM-readable) ─────────────────────────────────────────

def summarize(hits: list[dict], entity: str = "") -> str:
    """Compact one-line-per-measurement text for LLM context.

    Groups by gene → cell line, shows value + units + method.
    """
    if not hits:
        return f"{entity}: no results"

    etype = _detect_type(entity) if entity else "gene"
    lines = [f"=== NCI-60 MolTarget: {entity} ({len(hits)} measurements) ==="]

    if etype in ("gene", "moltid", "geneid"):
        # group by cell line
        by_cell = defaultdict(list)
        for r in hits:
            by_cell[r["cellname"]].append(r)
        for cell in sorted(by_cell):
            vals = by_cell[cell]
            parts = []
            for v in vals[:3]:  # cap per cell
                val = v["VALUE"]
                unit = v["UNITS"] or ""
                meth = v["METHOD"] or ""
                ent = v["ENTITY_MEASURED"] or ""
                parts.append(f"{ent}={val}{unit}({meth})")
            extra = f" +{len(vals)-3}more" if len(vals) > 3 else ""
            lines.append(f"  {cell}: {'; '.join(parts)}{extra}")
    elif etype == "cellline":
        # group by gene
        by_gene = defaultdict(list)
        for r in hits:
            by_gene[r["GENE"]].append(r)
        for gene in sorted(by_gene):
            vals = by_gene[gene]
            parts = []
            for v in vals[:3]:
                val = v["VALUE"]
                unit = v["UNITS"] or ""
                ent = v["ENTITY_MEASURED"] or ""
                parts.append(f"{ent}={val}{unit}")
            extra = f" +{len(vals)-3}more" if len(vals) > 3 else ""
            lines.append(f"  {gene}: {'; '.join(parts)}{extra}")
    elif etype == "panel":
        # group by gene, show cell lines
        by_gene = defaultdict(list)
        for r in hits:
            by_gene[r["GENE"]].append(r)
        for gene in sorted(by_gene)[:30]:
            cells = [f"{v['cellname']}={v['VALUE']}" for v in by_gene[gene][:5]]
            extra = f" +{len(by_gene[gene])-5}more" if len(by_gene[gene]) > 5 else ""
            lines.append(f"  {gene}: {'; '.join(cells)}{extra}")
        remaining = len(by_gene) - 30
        if remaining > 0:
            lines.append(f"  ... and {remaining} more genes")

    return "\n".join(lines)


def to_json(hits: list[dict]) -> list[dict]:
    """Structured JSON-serialisable output for pipeline consumption."""
    return hits


# ── Convenience wrapper ─────────────────────────────────────────────────

def query(data: list[dict], entities: Union[str, list], top_n: int = 0) -> str:
    """Single entry point: accepts str or list, returns LLM-readable text."""
    if isinstance(entities, str):
        entities = [entities]
    parts = []
    for e in entities:
        hits = search(data, e)
        if top_n > 0:
            hits = hits[:top_n]
        parts.append(summarize(hits, e))
    return "\n\n".join(parts)


# ── Main: runnable usage examples ───────────────────────────────────────

if __name__ == "__main__":
    print("Loading NCI DTP molecular target data ...")
    data = load_data()
    print(f"Loaded {len(data)} records.\n")

    # 1) Single gene query — drug target
    print(query(data, "EGFR"))
    print()

    # 2) Single cell line query
    print(query(data, "MCF7"))
    print()

    # 3) Batch query — multiple drug targets
    print(query(data, ["TP53", "BRAF", "HER2"]))
    print()

    # 4) Panel query
    print(query(data, "Breast"))
    print()

    # 5) JSON output for pipeline
    hits = search(data, "EGFR")
    print(f"JSON records for EGFR: {len(hits)}")
    if hits:
        print(json.dumps(to_json(hits[:2]), indent=2))
