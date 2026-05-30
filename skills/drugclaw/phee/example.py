"""
PHEE - Pharmacovigilance Event Extraction Dataset
Category: Drug-centric | Type: Dataset | Subcategory: Drug NLP/Text Mining
Link: https://zenodo.org/records/7689970
Paper: https://arxiv.org/abs/2210.12560

PHEE contains 5,000+ annotated pharmacovigilance events from medical case
reports, covering adverse drug events (ADE) and potential therapeutic events
(PTE) with hierarchical argument structure (Subject, Treatment, Effect).

Access method: Local JSON files downloaded from Zenodo.
"""

import json
import os
import re
from pathlib import Path
from typing import Union

DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_nlp"
    / "PHEE"
    / "data"
    / "json"
)


# ---------------------------------------------------------------------------
# Loading & indexing
# ---------------------------------------------------------------------------

_cache: dict = {}


def _flatten_text(val) -> list[str]:
    """Extract flat string list from PHEE nested text fields.

    Handles both original format (nested lists: [["aspirin"]]) and
    flat format (plain string: "aspirin").
    """
    if val is None:
        return []
    if isinstance(val, str):
        return [val] if val.strip() else []
    if isinstance(val, list):
        out = []
        for item in val:
            if isinstance(item, list):
                out.extend(s for s in item if isinstance(s, str) and s.strip())
            elif isinstance(item, str) and item.strip():
                out.append(item)
        return out
    return []


def _parse_event(ev: dict) -> dict:
    """Normalise one PHEE event into a flat dict."""
    # Handle HuggingFace format where event_data is a JSON string
    if "event_data" in ev and isinstance(ev["event_data"], str):
        try:
            ev = json.loads(ev["event_data"])
        except json.JSONDecodeError:
            pass

    etype = ev.get("event_type", "")

    # Trigger
    trig_raw = ev.get("Trigger") or ev.get("trigger") or {}
    trigger = _flatten_text(trig_raw.get("text"))

    # Subject (main + sub-arguments)
    subj_raw = ev.get("Subject") or ev.get("subject") or {}
    subject_text = _flatten_text(subj_raw.get("text"))
    age = _flatten_text(subj_raw.get("age", {}).get("text") if isinstance(subj_raw.get("age"), dict) else subj_raw.get("age"))
    gender = _flatten_text(subj_raw.get("gender", {}).get("text") if isinstance(subj_raw.get("gender"), dict) else subj_raw.get("gender"))
    race = _flatten_text(subj_raw.get("race", {}).get("text") if isinstance(subj_raw.get("race"), dict) else subj_raw.get("race"))
    population = _flatten_text(subj_raw.get("population", {}).get("text") if isinstance(subj_raw.get("population"), dict) else subj_raw.get("population"))
    disorder = _flatten_text(subj_raw.get("disorder", {}).get("text") if isinstance(subj_raw.get("disorder"), dict) else subj_raw.get("disorder"))

    # Treatment (main + sub-arguments)
    treat_raw = ev.get("Treatment") or ev.get("treatment") or {}
    treatment_text = _flatten_text(treat_raw.get("text"))
    drug = _flatten_text(treat_raw.get("drug", {}).get("text") if isinstance(treat_raw.get("drug"), dict) else treat_raw.get("drug"))
    dosage = _flatten_text(treat_raw.get("dosage", {}).get("text") if isinstance(treat_raw.get("dosage"), dict) else treat_raw.get("dosage"))
    freq = _flatten_text(treat_raw.get("freq", {}).get("text") if isinstance(treat_raw.get("freq"), dict) else treat_raw.get("freq"))
    route = _flatten_text(treat_raw.get("route", {}).get("text") if isinstance(treat_raw.get("route"), dict) else treat_raw.get("route"))
    duration = _flatten_text(treat_raw.get("duration", {}).get("text") if isinstance(treat_raw.get("duration"), dict) else treat_raw.get("duration"))
    treat_disorder = _flatten_text(treat_raw.get("disorder", {}).get("text") if isinstance(treat_raw.get("disorder"), dict) else treat_raw.get("disorder"))
    combination_drug = _flatten_text(treat_raw.get("combination.drug", {}).get("text") if isinstance(treat_raw.get("combination.drug"), dict) else treat_raw.get("combination.drug"))

    # Effect
    eff_raw = ev.get("Effect") or ev.get("effect") or {}
    effect_text = _flatten_text(eff_raw.get("text"))

    return {
        "event_type": etype,
        "trigger": trigger,
        "subject": subject_text,
        "subject_age": age,
        "subject_gender": gender,
        "subject_race": race,
        "subject_population": population,
        "subject_disorder": disorder,
        "treatment": treatment_text,
        "drug": drug,
        "dosage": dosage,
        "freq": freq,
        "route": route,
        "duration": duration,
        "treatment_disorder": treat_disorder,
        "combination_drug": combination_drug,
        "effect": effect_text,
    }


def load_phee(data_dir: str = DATA_DIR) -> list[dict]:
    """Load all PHEE JSON files and return a flat list of processed records.

    Each record: {id, text, split, events: [parsed_event, ...]}.
    Results are cached after first call.
    """
    if "all" in _cache:
        return _cache["all"]

    records: list[dict] = []
    for fname in ("train.json", "dev.json", "test.json"):
        fpath = os.path.join(data_dir, fname)
        if not os.path.exists(fpath):
            continue
        split = fname.replace(".json", "")
        with open(fpath, encoding="utf-8") as f:
            content = f.read().strip()
        # Support both standard JSON (array/object) and JSON Lines formats
        try:
            raw = json.loads(content)
        except json.JSONDecodeError:
            # JSON Lines: one JSON object per line
            raw = []
            for line in content.splitlines():
                line = line.strip()
                if line:
                    raw.append(json.loads(line))
        examples = raw if isinstance(raw, list) else raw.get("data", [])
        for ex in examples:
            # Handle both original (text/events) and HF (context/annotations) formats
            text = ex.get("text") or ex.get("context") or ""
            rec_id = ex.get("id", "")

            raw_events = ex.get("events", [])
            if not raw_events:
                annots = ex.get("annotations", [])
                if annots and isinstance(annots, list):
                    for a in annots:
                        if isinstance(a, dict):
                            raw_events.extend(a.get("events", []))

            parsed = [_parse_event(ev) for ev in raw_events]
            records.append({
                "id": rec_id,
                "text": text,
                "split": split,
                "events": parsed,
            })

    _cache["all"] = records
    print(f"PHEE loaded: {len(records)} sentences from {data_dir}")
    return records


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def _match(entity: str, record: dict) -> bool:
    """Return True if entity appears in any searchable field of the record."""
    pat = re.compile(re.escape(entity), re.IGNORECASE)
    if pat.search(record["text"]):
        return True
    for ev in record["events"]:
        for field in ("drug", "effect", "treatment", "subject",
                      "trigger", "treatment_disorder", "subject_disorder",
                      "combination_drug"):
            if any(pat.search(t) for t in ev.get(field, [])):
                return True
    return False


def search(records: list[dict], entity: str) -> list[dict]:
    """Search PHEE records for a single entity (drug, effect, or free text).

    Returns list of matching records.
    """
    return [r for r in records if _match(entity, r)]


def search_batch(records: list[dict], entities: list[str]) -> dict[str, list[dict]]:
    """Search PHEE records for multiple entities.

    Returns {entity: [matching records]}.
    """
    return {e: search(records, e) for e in entities}


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def summarize(hits: list[dict], entity: str) -> str:
    """Produce a compact LLM-readable summary for one entity's hits."""
    if not hits:
        return f"{entity}: no matching events found."

    ade_count = sum(1 for r in hits for ev in r["events"]
                    if ev["event_type"] == "Adverse_event")
    pte_count = sum(1 for r in hits for ev in r["events"]
                    if ev["event_type"] == "Potential_therapeutic_event")

    drugs: set[str] = set()
    effects: set[str] = set()
    for r in hits:
        for ev in r["events"]:
            drugs.update(d.lower() for d in ev.get("drug", []))
            effects.update(e.lower() for e in ev.get("effect", []))

    parts = [f"{entity}: {len(hits)} sentences ({ade_count} ADE, {pte_count} PTE)"]
    if drugs:
        parts.append(f"  drugs: {', '.join(sorted(drugs)[:10])}")
    if effects:
        parts.append(f"  effects: {', '.join(sorted(effects)[:10])}")
    return "\n".join(parts)


def to_json(hits: list[dict]) -> list[dict]:
    """Convert hit records to JSON-serialisable list."""
    out = []
    for r in hits:
        out.append({
            "id": r["id"],
            "text": r["text"],
            "split": r["split"],
            "events": r["events"],
        })
    return out


# ---------------------------------------------------------------------------
# Main — runnable examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    data = load_phee()

    # 1. Single drug search
    hits = search(data, "phenytoin")
    print(summarize(hits, "phenytoin"))

    # 2. Single adverse effect search
    hits = search(data, "hepatotoxicity")
    print(summarize(hits, "hepatotoxicity"))

    # 3. Batch search
    results = search_batch(data, ["methotrexate", "carbamazepine", "valproate"])
    for entity, h in results.items():
        print(summarize(h, entity))

    # 4. JSON output (first 2 records)
    hits = search(data, "phenytoin")
    import json as _json
    print(_json.dumps(to_json(hits[:2]), indent=2, ensure_ascii=False))
