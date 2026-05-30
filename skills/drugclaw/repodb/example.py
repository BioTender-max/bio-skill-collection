"""
RepoDB Query Tool
Search drug repurposing records by any entity.
Auto-detects entity type by prefix.
"""

import pandas as pd
import json
from pathlib import Path

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_repurposing"
    / "RepoDB"
    / "full.csv"
)
DISPLAY_COLS = ["drug_name", "drugbank_id", "ind_name", "ind_id", "NCT", "status", "phase", "DetailedStatus"]


def load_repodb(path: str = DATA_PATH) -> pd.DataFrame:
    # Try comma first (it's a .csv), fall back to tab
    df = pd.read_csv(path, dtype=str).fillna("")
    # Strip BOM, whitespace from column names
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")
    # Verify expected columns exist
    missing = [c for c in DISPLAY_COLS if c not in df.columns]
    if missing:
        # Retry with tab separator
        df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
        df.columns = df.columns.str.strip().str.lstrip("\ufeff")
        missing = [c for c in DISPLAY_COLS if c not in df.columns]
        if missing:
            raise ValueError(
                f"Columns not found: {missing}. "
                f"Available columns: {list(df.columns)}"
            )
    return df


def search(df: pd.DataFrame, entity: str) -> pd.DataFrame:
    """Search a single entity. Auto-detects type by prefix:
    DB* -> drugbank_id, C+digits -> ind_id, NCT* -> NCT, else -> drug_name/ind_name substring.
    """
    e = entity.strip()
    eu = e.upper()
    if eu.startswith("DB") and eu[2:].isdigit():
        return df[df["drugbank_id"].str.upper() == eu]
    if eu.startswith("C") and eu[1:].isdigit():
        return df[df["ind_id"].str.upper() == eu]
    if eu.startswith("NCT"):
        return df[df["NCT"].str.upper() == eu]
    el = e.lower()
    return df[
        df["drug_name"].str.lower().str.contains(el, na=False) |
        df["ind_name"].str.lower().str.contains(el, na=False)
    ]


def search_batch(df: pd.DataFrame, entities: list[str]) -> dict[str, pd.DataFrame]:
    """Search multiple entities, return {entity: DataFrame}."""
    return {e: search(df, e) for e in entities}


def summarize(hits: pd.DataFrame, entity: str) -> str:
    """Compact text summary for LLM consumption."""
    if hits.empty:
        return f"[{entity}] No records found."
    lines = [f"[{entity}] {len(hits)} records:"]
    for _, r in hits[DISPLAY_COLS].iterrows():
        parts = [f"{r['drug_name']}({r['drugbank_id']}) -> {r['ind_name']}({r['ind_id']})"]
        for col in ("status", "phase", "NCT"):
            if r[col] and r[col] != "NA":
                parts.append(f"{col}={r[col]}")
        lines.append("  " + " | ".join(parts))
    return "\n".join(lines)


def to_json(hits: pd.DataFrame) -> list[dict]:
    """Return records as list of dicts."""
    return hits[DISPLAY_COLS].to_dict(orient="records")


# ============================================================
# Usage Examples (run: python repodb_query.py)
# ============================================================
if __name__ == "__main__":
    df = load_repodb()
    print(f"Loaded {len(df)} records, columns: {list(df.columns)}\n")

    # Example 1: Find all indications for drug "ajmaline"
    hits = search(df, "ajmaline")
    print(summarize(hits, "ajmaline"))
    print()

    # Example 2: Look up by DrugBank ID
    hits = search(df, "DB00879")
    print(summarize(hits, "DB00879"))
    print()

    # Example 3: Look up by UMLS CUI
    hits = search(df, "C0020538")
    print(summarize(hits, "C0020538"))
    print()

    # Example 4: Search by indication name
    hits = search(df, "HIV Infections")
    print(summarize(hits, "HIV Infections"))
    print()

    # Example 5: Batch search multiple entities at once
    results = search_batch(df, ["ajmaline", "DB00879", "C0020538"])
    for entity, hits in results.items():
        print(summarize(hits, entity))
        print()

    # Example 6: Get JSON output for programmatic use
    hits = search(df, "enalapril")
    print(json.dumps(to_json(hits), indent=2))
