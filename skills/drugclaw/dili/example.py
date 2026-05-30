"""
DILI lookup example for canonical packaged resource output.

Default file: resources_metadata/drug_toxicity/DILI/dili.csv
Columns: drug, warning_type, molecule_chembl_id
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Union


DATA_PATH = os.environ.get(
    "DILI_DATA_FILE",
    str(
        Path(__file__).resolve().parents[3]
        / "resources_metadata"
        / "drug_toxicity"
        / "DILI"
        / "dili.csv"
    ),
)


def load_dili(path: str = DATA_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def query_dili(
    entities: Union[str, list[str]],
    data_path: str = DATA_PATH,
) -> list[dict]:
    if isinstance(entities, str):
        entities = [entities]

    path = Path(data_path)
    if not path.exists():
        return [{"error": f"DILI file not found: {path}"}]

    rows = load_dili(str(path))
    matches: list[dict] = []
    for entity in entities:
        q = entity.strip().lower()
        if not q:
            continue
        for row in rows:
            drug = str(row.get("drug", ""))
            if q in drug.lower():
                hit = dict(row)
                hit["query"] = entity
                matches.append(hit)

    if not matches:
        return []

    return [
        {
            "source": path.name,
            "match_count": len(matches),
            "matches": matches[:50],
        }
    ]


if __name__ == "__main__":
    entities = ["acetaminophen", "isoniazid", "troglitazone"]
    print(f"Querying DILI data for: {entities}")
    print(f"Data file: {DATA_PATH}\n")
    print(json.dumps(query_dili(entities), indent=2))
