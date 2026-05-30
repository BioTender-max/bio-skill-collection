"""
GDSC/GDSC2 - Genomics of Drug Sensitivity in Cancer
Category: Drug-centric | Type: Local Dataset | Subcategory: Drug Molecular Property
Link: https://www.cancerrxgene.org/
Cell Model Passports: https://cellmodelpassports.sanger.ac.uk/downloads
Paper: https://academic.oup.com/nar/article/41/D1/D955/1059448

Queries locally downloaded GDSC datasets for drug / cell-line information.
  - screened_compounds: drug name, target, pathway, PubChem CID
  - GDSC1/GDSC2 dose-response: IC50, AUC per drug × cell-line pair
  - Cell Model Passports: cell-line annotations (tissue, cancer type, mutations)

Setup:
  conda install openpyxl   # or: pip install openpyxl
  Run with --download flag first to fetch data, then query directly.
"""

import os, sys, json, glob
from pathlib import Path
import pandas as pd
from typing import Union

try:
    import openpyxl  # noqa: F401 – required by pandas for .xlsx
except ImportError:
    sys.exit(
        "[ERROR] openpyxl is not installed. Run:\n"
        "  pip install openpyxl        # or\n"
        "  conda install openpyxl"
    )

# ── configure path ──────────────────────────────────────────────────
DATA_DIR = os.environ.get(
    "GDSC_DATA_DIR",
    str(
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "drug_molecular_property"
        / "GDSC"
    ),
)

# ── download URLs ───────────────────────────────────────────────────
DOWNLOAD_URLS = {
    # Core drug list (small, ~100 KB)
    "screened_compounds_rel_8.4.csv": (
        "https://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/"
        "current_release/screened_compounds_rel_8.4.csv"
    ),
    # GDSC2 fitted dose-response (large, ~50 MB)
    "GDSC2_fitted_dose_response_27Oct23.xlsx": (
        "https://cog.sanger.ac.uk/cancerrxgene/GDSC_data_8.5/"
        "GDSC2_fitted_dose_response_27Oct23.xlsx"
    ),
    # GDSC1 fitted dose-response (large, ~80 MB)
    "GDSC1_fitted_dose_response_27Oct23.xlsx": (
        "https://cog.sanger.ac.uk/cancerrxgene/GDSC_data_8.5/"
        "GDSC1_fitted_dose_response_27Oct23.xlsx"
    ),
}


# ── download ────────────────────────────────────────────────────────
def download_gdsc_data(data_dir: str = DATA_DIR):
    """Download GDSC data files to *data_dir*."""
    import urllib.request
    os.makedirs(data_dir, exist_ok=True)
    for fname, url in DOWNLOAD_URLS.items():
        dest = os.path.join(data_dir, fname)
        if os.path.exists(dest):
            print(f"[SKIP] {fname} already exists")
            continue
        print(f"[DOWN] {fname} ...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                with open(dest, "wb") as f:
                    while True:
                        chunk = resp.read(512 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
            print(f"  -> saved {dest}")
        except Exception as e:
            print(f"  -> FAILED: {e}")
            print(f"     Manual download:")
            print(f"       wget -O '{dest}' '{url}'")


# ── helpers ─────────────────────────────────────────────────────────
def _load_all_tables(data_dir: str) -> dict[str, pd.DataFrame]:
    """Load every .xlsx / .csv / .tsv in *data_dir* into {filename: DataFrame}."""
    tables: dict[str, pd.DataFrame] = {}
    for fp in sorted(glob.glob(os.path.join(data_dir, "*"))):
        ext = os.path.splitext(fp)[1].lower()
        name = os.path.basename(fp)
        try:
            if ext == ".xlsx":
                xls = pd.ExcelFile(fp)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)
                    key = f"{name}::{sheet}" if len(xls.sheet_names) > 1 else name
                    tables[key] = df
            elif ext == ".csv":
                tables[name] = pd.read_csv(fp)
            elif ext == ".tsv":
                tables[name] = pd.read_csv(fp, sep="\t")
        except Exception as e:
            print(f"[WARN] skip {name}: {e}", file=sys.stderr)
    return tables


def _guess_name_cols(df: pd.DataFrame) -> list[str]:
    """Pick columns likely holding drug / cell-line / gene names."""
    keywords = ("drug", "compound", "name", "cell_line", "model",
                "cosmic", "gene", "target", "pathway", "tissue")
    candidates = []
    for c in df.columns:
        cl = str(c).lower().replace(" ", "_")
        if any(kw in cl for kw in keywords):
            candidates.append(c)
    return candidates or [df.columns[0]]


def _search_df(df: pd.DataFrame, queries: list[str], name_cols: list[str]) -> pd.DataFrame:
    """Case-insensitive substring match across *name_cols*."""
    q_lower = [q.lower().strip() for q in queries]
    mask = pd.Series(False, index=df.index)
    for col in name_cols:
        col_lower = df[col].astype(str).str.lower()
        for q in q_lower:
            mask |= col_lower.str.contains(q, na=False)
    return df.loc[mask]


# ── public API ──────────────────────────────────────────────────────
def query_gdsc(
    entities: Union[str, list[str]],
    data_dir: str = DATA_DIR,
) -> list[dict]:
    """
    Query GDSC data for one or more entities (drug name, cell line, gene target …).

    Parameters
    ----------
    entities : str or list[str]
        Entity name(s) to search (case-insensitive substring match).
    data_dir : str
        Path to the folder with GDSC data files.

    Returns
    -------
    list[dict]
        Each dict: {"source": filename, "match_count": N, "matches": [row, ...]}.
    """
    if isinstance(entities, str):
        entities = [entities]

    tables = _load_all_tables(data_dir)
    if not tables:
        return [{"error": f"No data files found in {data_dir}"}]

    results = []
    for tname, df in tables.items():
        name_cols = _guess_name_cols(df)
        hits = _search_df(df, entities, name_cols)
        if not hits.empty:
            results.append({
                "source": tname,
                "match_count": len(hits),
                "matches": hits.head(50).to_dict(orient="records"),
            })
    return results


# ── CLI ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Example: query well-known cancer drugs and a cell line
    entities = ["Erlotinib", "Nutlin", "A549"]

    print(f"Querying GDSC data for: {entities}")
    print(f"Data dir: {DATA_DIR}\n")

    # Auto-download if data dir is empty or missing
    if not os.path.isdir(DATA_DIR) or not glob.glob(os.path.join(DATA_DIR, "*")):
        print("Data directory is empty — downloading all GDSC data files ...\n")
        download_gdsc_data(DATA_DIR)
        print()

    results = query_gdsc(entities)
    if not results:
        print("No matches found.")
    for blk in results:
        if "error" in blk:
            print(f"[ERROR] {blk['error']}")
            continue
        print(f"── {blk['source']}  ({blk['match_count']} hits) ──")
        for row in blk["matches"][:5]:
            print(json.dumps(row, ensure_ascii=False, default=str))
        if blk["match_count"] > 5:
            print(f"  ... and {blk['match_count'] - 5} more rows")
        print()
