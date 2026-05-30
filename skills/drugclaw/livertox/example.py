#!/usr/bin/env python3

"""
LiverTox lookup example for canonical packaged resource output.

Default file: resources_metadata/drug_toxicity/LiverTox/livertox.json
Schema: [{"drug": "...", "title": "...", "ncbi_book_id": "..."}]
"""

from __future__ import annotations

import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_toxicity"
    / "LiverTox"
    / "livertox.json"
)


def load_documents(path: Path = DATA_PATH) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [dict(row) for row in payload if isinstance(row, dict)]


def lookup_entities(entities: list[str]) -> dict[str, list[dict]]:
    docs = load_documents()
    results: dict[str, list[dict]] = {}
    for entity in entities:
        q = entity.strip().lower()
        matches: list[dict] = []
        for row in docs:
            drug = str(row.get("drug", ""))
            title = str(row.get("title", ""))
            if q and (q in drug.lower() or q in title.lower()):
                book_id = str(row.get("ncbi_book_id", "")).strip()
                snippet = title
                if book_id:
                    snippet += f" (NCBI Books ID: {book_id})"
                matches.append({"section": title or drug, "snippet": snippet})
        results[entity] = matches[:5]
    return results


if __name__ == "__main__":
    demo_entities = ["acetaminophen", "amoxicillin"]
    print(json.dumps(lookup_entities(demo_entities), indent=2))
