"""
WHO Essential Medicines List (EML) – 23rd List (2023)
Category: Drug-centric | Type: DB | Subcategory: Essential Medicines
Link: https://list.essentialmeds.org/
Paper: https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.02

Access method: Local PDF parsed with pypdf -> JSON cache. Then offline search.
Dependency: pip install pypdf
"""

import json, os, re
from pathlib import Path

DATA_DIR = (
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_knowledgebase"
    / "WHO Essential Medicines List"
)
PDF_PATH = str(DATA_DIR / "WHO EML 23rd List (2023).pdf")
CACHE_PATH = str(DATA_DIR / "who_eml_23.json")

# ── patterns ─────────────────────────────────────────────────────────────
# Section header: "1.1.2.  Injectable medicines" or "6.  Anti-infective medicines"
_SEC_RE = re.compile(r'^(\d+(?:\.\d+)*)\.\s{2,}(.+)$')

# Dosage-form keywords that start a dosage line
_DOSE_KW = (
    "Tablet", "Capsule", "Injection", "Oral liquid", "Oral powder",
    "Powder for", "Inhalation", "Solution", "Suppository", "Cream",
    "Ointment", "Syrup", "Gel", "Concentrate", "Drops", "Granules",
    "Suspension", "Patch", "Implant", "Rectal", "Dental", "Topical",
    "Nasal", "Eye", "Ear", "Lozenge", "Infusion", "Transdermal",
    "Vial", "Ampoule", "Mouthwash", "Shampoo", "Lotion", "Pessary",
    "Aerosol", "Chewable", "Dispersible",
)

# Lines to skip entirely
_SKIP = (
    "WHO Model List of Essential Medicines",
    "23rd List (2023)",
    "core list", "complementary list",
    "The core list presents",
    "The complementary list presents",
    "Where the [c] symbol",
    "priority conditions",
)


def _is_section(line):
    """Return (num, title) if section header, else None."""
    m = _SEC_RE.match(line)
    return (m.group(1), m.group(2).strip()) if m else None


def _is_dosage(line):
    """True if line starts with a dosage-form keyword."""
    for kw in _DOSE_KW:
        if line.startswith(kw):
            return True
    return False


def _is_medicine(line):
    """Heuristic: medicine names in WHO EML PDF are lowercase
    (e.g. 'amoxicillin', 'morphine', 'lidocaine + epinephrine (adrenaline)')
    They are NOT section headers and NOT dosage lines."""
    if not line or len(line) < 2 or len(line) > 120:
        return False
    if _is_dosage(line):
        return False
    if _is_section(line):
        return False
    first = line[0]
    if not first.islower():
        return False
    # Medicine names are short (1-8 words), paragraph text is longer
    if len(line.split()) > 8:
        return False
    # Filter paragraph text (common English words that aren't medicine names)
    fw = line.split()[0].rstrip(".,;:")
    if fw in ("the","a","an","and","or","for","in","is","are","as","to",
              "of","on","by","it","its","at","from","with","this","that",
              "may","can","where","which","should","have","has","been",
              "not","each","all","any","these","those","such","if","be"):
        return False
    return True


# ── PDF text extraction ──────────────────────────────────────────────────

def extract_text(pdf_path=PDF_PATH):
    """Extract text from all pages of the WHO EML PDF using pypdf."""
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    parts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    return "\n".join(parts)


# ── parser ───────────────────────────────────────────────────────────────

def parse_text(text):
    """Parse extracted PDF text into list of medicine records.

    PDF layout (repeating):
        <section header>          e.g. "6.2.1.  Access group antibiotics"
        <medicine name>           e.g. "amoxicillin"
        <dosage line>             e.g. "Capsule: 250 mg; 500 mg."
        <dosage line>             e.g. "Oral liquid: 125 mg/5 mL."
        <next medicine name>      ...
    """
    lines = text.split("\n")
    records = []
    sec_num, sec_name = "", ""
    sec_tree = {}          # "18.5" -> "Medicines for diabetes"
    med = ""
    doses = []

    def _full_section(num, name):
        """Build full section path: 'Medicines for diabetes > Oral hypoglycaemic agents'."""
        parts = num.split(".")
        ancestors = []
        for i in range(1, len(parts)):
            pkey = ".".join(parts[:i])
            if pkey in sec_tree:
                ancestors.append(sec_tree[pkey])
        ancestors.append(name)
        # deduplicate adjacent identical names
        deduped = [ancestors[0]]
        for a in ancestors[1:]:
            if a != deduped[-1]:
                deduped.append(a)
        return " > ".join(deduped)

    def flush():
        nonlocal med, doses
        if med:
            # clean medicine name: strip [c] marker, trailing whitespace
            clean_name = med.strip()
            records.append({
                "medicine": clean_name,
                "section_num": sec_num,
                "section_name": sec_name,
                "dosage_forms": [d.rstrip(".").strip() for d in doses if d.strip()],
            })
        med = ""
        doses = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        # skip known noise
        skip = False
        for s in _SKIP:
            if line.startswith(s):
                skip = True; break
        if skip:
            continue

        # section header
        sec = _is_section(line)
        if sec:
            flush()
            sec_num, raw_name = sec
            sec_tree[sec_num] = raw_name
            sec_name = _full_section(sec_num, raw_name)
            continue

        # dosage form line
        if _is_dosage(line):
            doses.append(line)
            continue

        # medicine name
        if _is_medicine(line):
            flush()
            med = line
            continue

        # continuation of previous dosage (rare multi-line dosage)
        if doses and line and not line[0].isupper():
            doses[-1] += " " + line
            continue

    flush()
    return records


# ── build / cache ────────────────────────────────────────────────────────

def build_cache(pdf_path=PDF_PATH, cache_path=CACHE_PATH):
    """Parse PDF and save JSON cache."""
    print(f"Reading {pdf_path} ...")
    text = extract_text(pdf_path)
    print(f"  Extracted {len(text)} chars. Parsing ...")
    records = parse_text(text)
    os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    print(f"  Cached {len(records)} medicines -> {cache_path}")
    return records


def load_eml(cache_path=CACHE_PATH):
    """Load JSON cache. Auto-builds from PDF if missing or empty."""
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            data = json.load(f)
        if data:  # non-empty cache
            return data
        # empty cache from previous failed build – rebuild
        print(f"Cache {cache_path} is empty, rebuilding ...")
    return build_cache(cache_path=cache_path)


# ── search API ───────────────────────────────────────────────────────────

def search(data, entity):
    """Case-insensitive substring on medicine name, section_name, section_num."""
    q = entity.strip().lower()
    if not q:
        return []
    return [r for r in data
            if q in r["medicine"].lower()
            or q in r["section_name"].lower()
            or r["section_num"].startswith(q)]


def search_batch(data, entities):
    """Search multiple entities. Returns {entity: [records]}."""
    return {e: search(data, e) for e in entities}


def summarize(hits, entity=""):
    """Compact LLM-readable summary."""
    if not hits:
        return f"No WHO EML results for '{entity}'."
    out = [f"WHO EML results for '{entity}' ({len(hits)} hits):"]
    for r in hits:
        ds = "; ".join(r["dosage_forms"][:3]) or "see PDF"
        if len(r["dosage_forms"]) > 3:
            ds += f" (+{len(r['dosage_forms'])-3} more)"
        out.append(f"  {r['medicine']} | "
                   f"§{r['section_num']} {r['section_name']} | {ds}")
    return "\n".join(out)


def to_json(hits):
    """Structured output for pipeline use."""
    return hits


# ── examples ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = load_eml()
    print(f"Loaded {len(data)} WHO EML records.\n")

    # single drug name
    print(summarize(search(data, "amoxicillin"), "amoxicillin"))
    print()
    # section keyword
    print(summarize(search(data, "antimalarial"), "antimalarial"))
    print()
    # section number prefix
    print(summarize(search(data, "6.2"), "section 6.2"))
    print()
    # batch search
    for e, h in search_batch(data, ["metformin", "morphine", "ibuprofen"]).items():
        print(summarize(h, e))
        print()
    # JSON
    print("JSON:", json.dumps(to_json(search(data, "aspirin")),
                              indent=2, ensure_ascii=False)[:500])
