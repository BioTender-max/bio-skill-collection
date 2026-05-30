"""
ADReCS - Adverse Drug Reaction Classification System (v3.3)
Category: Drug-centric | Type: Local DB | Subcategory: Adverse Drug Reaction (ADR)
Link: https://www.bio-add.org/ADReCS/
Paper: https://academic.oup.com/nar/article/43/D1/D907/2437234

Provides hierarchical ADR classification integrating FAERS, SIDER, and
MedDRA terminology.  Supports search by drug name, BADD drug ID, DrugBank
ID, ATC code, CAS RN, PubChem CID, KEGG ID, ADR term, ADReCS ID, MedDRA
code, or MeSH ID.

Access method: Local flat files downloaded from ADReCS v3.3.
"""

import os
import re
import pandas as pd
from pathlib import Path
from typing import Optional, Union

# ── Data paths ──────────────────────────────────────────────────────────
DATA_DIR = str(
    Path(__file__).resolve().parents[3] / "resources_metadata" / "adr" / "ADReCS"
)

DRUG_ADR_FILE = os.path.join(DATA_DIR, "Drug_ADR_v3.3.txt")
DRUG_INFO_FILE = os.path.join(DATA_DIR, "Drug_information_v3.3.xlsx")
ADR_ONTOLOGY_FILE = os.path.join(DATA_DIR, "ADR_ontology_v3.3.xlsx")
QUANT_FILE = os.path.join(DATA_DIR, "ADReCS_Drug_ADR_relations_quantification_v3.3.txt")

# ── Column-name normalisation helpers ───────────────────────────────────

def _norm(col: str) -> str:
    """Lower-case, strip, collapse whitespace/underscores to single _."""
    return re.sub(r"[\s_]+", "_", col.strip().lower())


def _find_col(df: pd.DataFrame, *patterns: str) -> Optional[str]:
    """Return the first column whose normalised name contains any pattern."""
    normed = {c: _norm(c) for c in df.columns}
    for pat in patterns:
        pat_l = pat.lower()
        for orig, n in normed.items():
            if pat_l in n:
                return orig
    return None


# ── Loaders ─────────────────────────────────────────────────────────────

_cache: dict = {}


def _read_txt(path: str) -> pd.DataFrame:
    """Read a tab- or comma-separated text file with header auto-detection."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        first = fh.readline()
    sep = "\t" if "\t" in first else ","
    return pd.read_csv(path, sep=sep, dtype=str, on_bad_lines="skip")


def load_drug_adr(path: str = DRUG_ADR_FILE) -> pd.DataFrame:
    """Load the main Drug–ADR association table."""
    if "drug_adr" not in _cache:
        _cache["drug_adr"] = _read_txt(path)
    return _cache["drug_adr"]


def load_drug_info(path: str = DRUG_INFO_FILE) -> pd.DataFrame:
    """Load Drug_information spreadsheet (drug metadata)."""
    if "drug_info" not in _cache:
        _cache["drug_info"] = pd.read_excel(path, dtype=str)
    return _cache["drug_info"]


def load_adr_ontology(path: str = ADR_ONTOLOGY_FILE) -> pd.DataFrame:
    """Load ADR_ontology spreadsheet (ADR hierarchy)."""
    if "adr_ont" not in _cache:
        _cache["adr_ont"] = pd.read_excel(path, dtype=str)
    return _cache["adr_ont"]


def load_quant(path: str = QUANT_FILE) -> pd.DataFrame:
    """Load Drug–ADR quantification (severity / frequency)."""
    if "quant" not in _cache:
        _cache["quant"] = _read_txt(path)
    return _cache["quant"]


# ── Entity auto-detection ───────────────────────────────────────────────

_PATTERNS = [
    (re.compile(r"^BADD_D\d+$", re.I),        "badd_id"),
    (re.compile(r"^DB\d{5,}$", re.I),          "drugbank_id"),
    (re.compile(r"^[A-Z]\d{2}[A-Z]{2}\d{2}$"),"atc_code"),
    (re.compile(r"^\d{2,5}-\d{2}-\d$"),        "cas_rn"),
    (re.compile(r"^CID\d+$", re.I),            "pubchem_id"),
    (re.compile(r"^D\d{5}$"),                   "kegg_id"),
    (re.compile(r"^\d{2}\.\d{2}"),             "adrecs_id"),     # e.g. 08.06.02.001
    (re.compile(r"^1\d{7}$"),                   "meddra_code"),   # 8-digit MedDRA PT
    (re.compile(r"^D\d{6,}$"),                  "mesh_id"),       # MeSH descriptor
    (re.compile(r"^\d{3,}$"),                   "pubchem_id"),   # bare PubChem CID (last)
]


def detect_entity_type(entity: str) -> str:
    """Return a type tag based on prefix/pattern, or 'text' for free text."""
    e = entity.strip()
    for pat, tag in _PATTERNS:
        if pat.match(e):
            return tag
    return "text"


# ── Column-mapping helpers (resolved lazily per DataFrame) ──────────────

def _drug_adr_cols(df: pd.DataFrame) -> dict:
    """Identify key columns in the Drug_ADR table."""
    return {
        "drug_id":   _find_col(df, "drug_id", "drug id", "badd"),
        "drug_name": _find_col(df, "drug_name", "drug name"),
        "adrecs_id": _find_col(df, "adrecs_id", "adrecs id", "adr_id", "adr id"),
        "adr_term":  _find_col(df, "adr_term", "adr_name", "adr term", "adverse"),
    }


def _drug_info_cols(df: pd.DataFrame) -> dict:
    return {
        "drug_id":     _find_col(df, "drug_id", "drug id", "badd"),
        "drug_name":   _find_col(df, "drug_name", "drug name"),
        "drugbank_id": _find_col(df, "drugbank"),
        "atc_code":    _find_col(df, "atc"),
        "cas_rn":      _find_col(df, "cas"),
        "pubchem_id":  _find_col(df, "pubchem"),
        "kegg_id":     _find_col(df, "kegg"),
        "synonyms":    _find_col(df, "synonym"),
    }


# ── Core search ─────────────────────────────────────────────────────────

def _isin(series: pd.Series, value: str) -> pd.Series:
    """Case-insensitive exact match on a string Series."""
    return series.fillna("").str.strip().str.lower() == value.strip().lower()


def _icontains(series: pd.Series, value: str) -> pd.Series:
    """Case-insensitive substring match."""
    return series.fillna("").str.lower().str.contains(value.strip().lower(), regex=False)


def _resolve_drug_ids(entity: str, etype: str, info_df: pd.DataFrame) -> list[str]:
    """Map an external ID or drug name to BADD Drug IDs via Drug_information."""
    cols = _drug_info_cols(info_df)
    col_map = {
        "drugbank_id": cols["drugbank_id"],
        "atc_code":    cols["atc_code"],
        "cas_rn":      cols["cas_rn"],
        "pubchem_id":  cols["pubchem_id"],
        "kegg_id":     cols["kegg_id"],
    }
    target_col = col_map.get(etype)
    if target_col and target_col in info_df.columns:
        mask = _icontains(info_df[target_col], entity)
        ids = info_df.loc[mask, cols["drug_id"]].dropna().unique().tolist()
        if ids:
            return ids
    # fallback: try drug name / synonyms
    for c in [cols["drug_name"], cols["synonyms"]]:
        if c and c in info_df.columns:
            mask = _icontains(info_df[c], entity)
            ids = info_df.loc[mask, cols["drug_id"]].dropna().unique().tolist()
            if ids:
                return ids
    return []


def search(entity: str,
           drug_adr_df: Optional[pd.DataFrame] = None,
           drug_info_df: Optional[pd.DataFrame] = None,
           adr_ont_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Search ADReCS for a single entity.

    Parameters
    ----------
    entity : str
        Drug name, BADD ID, DrugBank ID, ATC code, CAS RN, PubChem CID,
        KEGG ID, ADR term, ADReCS ID, MedDRA code, or MeSH ID.
    drug_adr_df : DataFrame, optional
        Pre-loaded Drug_ADR table (loaded automatically if None).
    drug_info_df : DataFrame, optional
        Pre-loaded Drug_information table.
    adr_ont_df : DataFrame, optional
        Pre-loaded ADR_ontology table.

    Returns
    -------
    DataFrame  — matching Drug–ADR rows (empty if nothing found).
    """
    if drug_adr_df is None:
        drug_adr_df = load_drug_adr()
    if drug_info_df is None:
        drug_info_df = load_drug_info()
    if adr_ont_df is None:
        adr_ont_df = load_adr_ontology()

    etype = detect_entity_type(entity)
    da_cols = _drug_adr_cols(drug_adr_df)

    # ── Direct match in Drug_ADR table ──────────────────────────────
    if etype == "badd_id" and da_cols["drug_id"]:
        mask = _isin(drug_adr_df[da_cols["drug_id"]], entity)
        if mask.any():
            return drug_adr_df.loc[mask].reset_index(drop=True)

    if etype == "adrecs_id" and da_cols["adrecs_id"]:
        mask = _icontains(drug_adr_df[da_cols["adrecs_id"]], entity)
        if mask.any():
            return drug_adr_df.loc[mask].reset_index(drop=True)

    if etype == "meddra_code":
        # try in ADR ontology first to get ADReCS IDs, then join
        mc = _find_col(adr_ont_df, "meddra")
        ai = _find_col(adr_ont_df, "adrecs_id", "adrecs id", "adr_id")
        if mc and ai:
            ont_hits = adr_ont_df.loc[_icontains(adr_ont_df[mc], entity), ai].dropna().unique()
            if len(ont_hits) and da_cols["adrecs_id"]:
                mask = drug_adr_df[da_cols["adrecs_id"]].fillna("").isin(ont_hits)
                if mask.any():
                    return drug_adr_df.loc[mask].reset_index(drop=True)

    if etype == "mesh_id":
        mi = _find_col(adr_ont_df, "mesh")
        ai = _find_col(adr_ont_df, "adrecs_id", "adrecs id", "adr_id")
        if mi and ai:
            ont_hits = adr_ont_df.loc[_icontains(adr_ont_df[mi], entity), ai].dropna().unique()
            if len(ont_hits) and da_cols["adrecs_id"]:
                mask = drug_adr_df[da_cols["adrecs_id"]].fillna("").isin(ont_hits)
                if mask.any():
                    return drug_adr_df.loc[mask].reset_index(drop=True)

    # ── Resolve external drug IDs via Drug_information ──────────────
    if etype in ("drugbank_id", "atc_code", "cas_rn", "pubchem_id", "kegg_id"):
        badd_ids = _resolve_drug_ids(entity, etype, drug_info_df)
        if badd_ids and da_cols["drug_id"]:
            mask = drug_adr_df[da_cols["drug_id"]].fillna("").str.strip().str.upper().isin(
                [b.strip().upper() for b in badd_ids]
            )
            if mask.any():
                return drug_adr_df.loc[mask].reset_index(drop=True)

    # ── Free-text: search drug name then ADR term ───────────────────
    # try drug name in Drug_ADR
    if da_cols["drug_name"]:
        mask = _icontains(drug_adr_df[da_cols["drug_name"]], entity)
        if mask.any():
            return drug_adr_df.loc[mask].reset_index(drop=True)

    # try ADR term in Drug_ADR
    if da_cols["adr_term"]:
        mask = _icontains(drug_adr_df[da_cols["adr_term"]], entity)
        if mask.any():
            return drug_adr_df.loc[mask].reset_index(drop=True)

    # try resolving via drug_info synonyms
    badd_ids = _resolve_drug_ids(entity, "text", drug_info_df)
    if badd_ids and da_cols["drug_id"]:
        mask = drug_adr_df[da_cols["drug_id"]].fillna("").str.strip().str.upper().isin(
            [b.strip().upper() for b in badd_ids]
        )
        if mask.any():
            return drug_adr_df.loc[mask].reset_index(drop=True)

    return pd.DataFrame()


def search_batch(entities: list[str], **kwargs) -> dict[str, pd.DataFrame]:
    """Search multiple entities; returns {entity: DataFrame}."""
    # load once, share across calls
    drug_adr_df = kwargs.pop("drug_adr_df", None) or load_drug_adr()
    drug_info_df = kwargs.pop("drug_info_df", None) or load_drug_info()
    adr_ont_df = kwargs.pop("adr_ont_df", None) or load_adr_ontology()
    return {
        e: search(e, drug_adr_df=drug_adr_df,
                  drug_info_df=drug_info_df,
                  adr_ont_df=adr_ont_df)
        for e in entities
    }


# ── Output helpers ──────────────────────────────────────────────────────

def summarize(hits: pd.DataFrame, entity: str, max_rows: int = 30) -> str:
    """
    One-line-per-row compact summary suitable for an LLM context window.

    Format:  DRUG_NAME | ADR_TERM (ADReCS_ID)
    """
    if hits.empty:
        return f"{entity}: no results"

    cols = _drug_adr_cols(hits)
    lines = [f"=== ADReCS results for '{entity}' ({len(hits)} rows) ==="]
    for _, row in hits.head(max_rows).iterrows():
        drug = row.get(cols["drug_name"], "") if cols["drug_name"] else ""
        adr  = row.get(cols["adr_term"], "")  if cols["adr_term"]  else ""
        aid  = row.get(cols["adrecs_id"], "") if cols["adrecs_id"] else ""
        parts = [p for p in [str(drug).strip(), str(adr).strip()] if p]
        if aid and str(aid).strip():
            parts.append(f"({str(aid).strip()})")
        lines.append(" | ".join(parts) if parts else str(row.to_dict()))
    if len(hits) > max_rows:
        lines.append(f"... and {len(hits) - max_rows} more rows")
    return "\n".join(lines)


def to_json(hits: pd.DataFrame) -> list[dict]:
    """Convert hit DataFrame to a list of dicts for pipeline use."""
    return hits.to_dict(orient="records")


# ── CLI demo ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading ADReCS v3.3 data ...")
    da = load_drug_adr()
    di = load_drug_info()
    ao = load_adr_ontology()
    print(f"  Drug_ADR:        {da.shape[0]:>8,} rows  cols={list(da.columns)}")
    print(f"  Drug_information:{di.shape[0]:>8,} rows  cols={list(di.columns)}")
    print(f"  ADR_ontology:    {ao.shape[0]:>8,} rows  cols={list(ao.columns)}")
    print()

    # ── Single-entity searches ──────────────────────────────────────
    for q in ["aspirin", "BADD_D00142", "DB00945", "headache", "08.06"]:
        etype = detect_entity_type(q)
        hits = search(q, drug_adr_df=da, drug_info_df=di, adr_ont_df=ao)
        print(f"[{etype:>12}] {q}  →  {len(hits)} hits")
        print(summarize(hits, q, max_rows=5))
        print()

    # ── Batch search ────────────────────────────────────────────────
    batch = search_batch(["metformin", "ibuprofen"],
                         drug_adr_df=da, drug_info_df=di, adr_ont_df=ao)
    for ent, df in batch.items():
        print(f"Batch: {ent} → {len(df)} hits")

    # ── JSON output ─────────────────────────────────────────────────
    sample = search("aspirin", drug_adr_df=da, drug_info_df=di, adr_ont_df=ao)
    print(f"\nJSON sample (first 2): {to_json(sample.head(2))}")
