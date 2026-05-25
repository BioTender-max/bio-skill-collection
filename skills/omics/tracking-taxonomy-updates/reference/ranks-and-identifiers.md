# Ranks and identifiers (get these right)

Taxonomy is hierarchical, but **rank schemas differ** across cellular life vs viruses, and databases use many **“no rank”** clades.

---

## 1) Ranks are not universal

### Cellular organisms (NCBI-style)
Common named ranks you’ll see:
- root → **domain** → (optional kingdom and other clades) → phylum → class → order → family → genus → species
Plus many intermediates: subphylum, subclass, infraorder, etc.

NCBI also uses many nodes as **“no rank”** (clade/group).
Rule: **preserve** these rather than forcing them into a named rank.

### Viruses (ICTV/NCBI-style)
Viruses are “acellular” in NCBI’s rank model; ICTV defines a hierarchy commonly including:
- acellular root / viruses → **realm** → kingdom → phylum → class → order → family → genus → species → below species (isolates, etc.)

Rule: when reporting viruses, include the highest available rank (often **realm**) and note whether names are ICTV binomials vs legacy names.

---

## 2) NCBI taxids (Taxonomy IDs): how to use them

### What a taxid is
- A stable-ish integer identifier for a node in the NCBI taxonomy tree.
- Appears in GenBank/RefSeq metadata and is widely used for joins.

### Best practice storage schema
Whenever you store taxonomy metadata, store all of:
- `ncbi_taxid`
- `scientific_name`
- `rank`
- `lineage_names` (semicolon-delimited)
- `lineage_taxids` (semicolon-delimited)
- `taxonomy_source = "NCBI Taxonomy"`
- `taxonomy_snapshot_date` (or taxdump date)

Reason: names/ranks can change even when the taxid stays the same.

### Merges/deletions
Taxids can be merged into other taxids or deleted.
Rule:
- If merged: store both the **original taxid** and the **current taxid**
- If deleted: mark as **needs-review** and re-resolve by name + sequence evidence

---

## 3) TaxonKit patterns you should know

Assume you have an NCBI taxdump available (TaxonKit needs it).

### taxid → lineage
- `taxonkit lineage taxids.txt`

### lineage (names/ranks) in a fixed format
Example: print only major ranks (fill missing with empty):
- `taxonkit lineage taxids.txt | taxonkit reformat -f "{d};{k};{p};{c};{o};{f};{g};{s}"`

### name → taxid
Useful when the user provides names:
- `taxonkit name2taxid names.txt`

### track changes / merges
Use TaxonKit’s taxid-change tracking when available in your installation, and always surface warnings.

(See tool details and install notes in [tools.md](tools.md).)
