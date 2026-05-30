"""
DrugProt - Drug-Protein Relation Query Tool
Query drug/chemical and gene/protein entities to retrieve their relations
from the BioCreative VII DrugProt dataset.

Source: https://zenodo.org/records/5119892
Paper:  https://pmc.ncbi.nlm.nih.gov/articles/PMC10683943/
"""

import os
import json
from collections import defaultdict
from typing import Union

# ---------- Configuration ----------
BASE_DIR = os.environ.get(
    "DRUGPROT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "resources_metadata", "drug_nlp", "DrugProt",
                 "drugprot-gs-training-development"),
)
SPLITS = ["training", "development", "test-background"]


# ---------- Data Loading ----------
def _tsv_rows(path: str):
    """Yield tab-split rows from a TSV file."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts and parts[0]:
                yield parts


def load_dataset(base_dir: str = BASE_DIR, splits: list = SPLITS) -> dict:
    """Load abstracts, entities, and relations into an indexed dict.

    Returns:
        {
          "abstracts": {pmid: {"title": str, "abstract": str}},
          "entities":  {pmid: {eid: {"type", "start", "end", "text"}}},
          "relations": {pmid: [{"type", "arg1", "arg2"}]},
          "name_index": {lowercase_text: [(pmid, eid), ...]},
        }
    """
    abstracts, entities, relations = {}, defaultdict(dict), defaultdict(list)
    name_index = defaultdict(list)

    for split in splits:
        split_dir = os.path.join(base_dir, split)
        if not os.path.isdir(split_dir):
            continue

        # Abstracts
        for fname in os.listdir(split_dir):
            fpath = os.path.join(split_dir, fname)
            if "abstrac" in fname and fname.endswith(".tsv"):
                for row in _tsv_rows(fpath):
                    if len(row) >= 3:
                        abstracts[row[0]] = {"title": row[1], "abstract": row[2]}

            # Entities
            elif "entities" in fname and fname.endswith(".tsv"):
                for row in _tsv_rows(fpath):
                    if len(row) >= 6:
                        pmid, eid, etype, start, end, text = (
                            row[0], row[1], row[2], int(row[3]), int(row[4]), row[5],
                        )
                        entities[pmid][eid] = {
                            "type": etype, "start": start, "end": end, "text": text,
                        }
                        name_index[text.lower()].append((pmid, eid))

            # Relations
            elif "relations" in fname and fname.endswith(".tsv"):
                for row in _tsv_rows(fpath):
                    if len(row) >= 4:
                        relations[row[0]].append({
                            "type": row[1],
                            "arg1": row[2].replace("Arg1:", ""),
                            "arg2": row[3].replace("Arg2:", ""),
                        })

    return {
        "abstracts": abstracts,
        "entities": dict(entities),
        "relations": dict(relations),
        "name_index": dict(name_index),
    }


# ---------- Query ----------
def query_entities(
    dataset: dict,
    names: Union[str, list],
    case_sensitive: bool = False,
) -> list[dict]:
    """Query one or more entity names. Returns a list of result dicts.

    Args:
        dataset: Output of load_dataset().
        names: A single entity name (str) or a list of names.
        case_sensitive: If False (default), matching is case-insensitive.

    Returns:
        [
          {
            "query": str,
            "matches": [
              {
                "pmid": str,
                "entity_id": str,
                "entity_type": str,
                "entity_text": str,
                "relations": [
                  {"relation_type": str, "partner_id": str,
                   "partner_text": str, "partner_type": str, "role": str}
                ],
                "article_title": str,
              }
            ]
          }
        ]
    """
    if isinstance(names, str):
        names = [names]

    results = []
    for name in names:
        key = name if case_sensitive else name.lower()
        hits = dataset["name_index"].get(key, [])

        # Also try substring match if exact match yields nothing
        if not hits and not case_sensitive:
            hits = []
            for idx_key, locs in dataset["name_index"].items():
                if key in idx_key or idx_key in key:
                    hits.extend(locs)

        matches = []
        seen = set()
        for pmid, eid in hits:
            if (pmid, eid) in seen:
                continue
            seen.add((pmid, eid))

            ent = dataset["entities"].get(pmid, {}).get(eid, {})
            rels_raw = dataset["relations"].get(pmid, [])

            # Find relations involving this entity
            rels = []
            for r in rels_raw:
                role, partner_eid = None, None
                if r["arg1"] == eid:
                    role, partner_eid = "arg1(chemical)", r["arg2"]
                elif r["arg2"] == eid:
                    role, partner_eid = "arg2(gene/protein)", r["arg1"]
                if role:
                    partner = dataset["entities"].get(pmid, {}).get(partner_eid, {})
                    rels.append({
                        "relation_type": r["type"],
                        "partner_id": partner_eid,
                        "partner_text": partner.get("text", ""),
                        "partner_type": partner.get("type", ""),
                        "role": role,
                    })

            title = dataset["abstracts"].get(pmid, {}).get("title", "")
            matches.append({
                "pmid": pmid,
                "entity_id": eid,
                "entity_type": ent.get("type", ""),
                "entity_text": ent.get("text", ""),
                "relations": rels,
                "article_title": title,
            })

        results.append({"query": name, "matches": matches})

    return results


def format_results(results: list[dict], max_matches: int = 5) -> str:
    """Format query results into a concise LLM-readable string."""
    lines = []
    for res in results:
        lines.append(f"## Query: \"{res['query']}\" — {len(res['matches'])} match(es)")
        for m in res["matches"][:max_matches]:
            lines.append(f"  PMID: {m['pmid']} | {m['entity_type']} | \"{m['entity_text']}\"")
            lines.append(f"  Title: {m['article_title'][:120]}")
            if m["relations"]:
                for r in m["relations"]:
                    lines.append(
                        f"    → {r['relation_type']}: {r['partner_text']} "
                        f"({r['partner_type']}) [{r['role']}]"
                    )
            else:
                lines.append("    (no annotated relations)")
            lines.append("")
        if len(res["matches"]) > max_matches:
            lines.append(f"  ... and {len(res['matches']) - max_matches} more matches\n")
    return "\n".join(lines)


# ---------- CLI ----------
if __name__ == "__main__":
    import sys

    print("Loading DrugProt dataset ...")
    ds = load_dataset()
    total_ents = sum(len(v) for v in ds["entities"].values())
    total_rels = sum(len(v) for v in ds["relations"].values())
    print(f"Loaded: {len(ds['abstracts'])} abstracts, {total_ents} entities, {total_rels} relations\n")

    # Accept queries from CLI args or use defaults
    queries = sys.argv[1:] if len(sys.argv) > 1 else ["aspirin", "insulin", "p53"]
    results = query_entities(ds, queries)
    print(format_results(results))