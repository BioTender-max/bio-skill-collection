# Reporting templates

These templates are meant to be copied into agent outputs.

---

## A) Taxonomy update report (proposals + consensus + releases)

### Summary (5–10 bullets)
- What changed (by domain)
- Effective dates
- Authority/source (ICTV, NCBI, GTDB, UniEuk/ISOP, etc.)
- Practical impacts (pipelines, databases, taxid/name joins)

### Versioned table (required)
Columns:
- Domain
- Authority/source
- Release/proposal identifier
- Date
- Key changes
- Action items / “what breaks”

### Notes (optional)
- Known controversial areas / unresolved conflicts
- Items to monitor next (e.g., pending ICTV proposals or upcoming GTDB releases)

---

## B) Taxonomy assignment report (sequence → taxonomy)

### Provenance block (required)
- tool name + version
- database/source + version/release
- date run
- command lines/settings used
- environment notes:
  - QuickClade: container image tag + digest if available
  - Pixi: pixi.lock hash or pixi.toml revision (if tracked)

### Results table (required)
Minimum columns:
- sample_id
- query_id (bin/contig/genome)
- contig_id (for assembly-level `percontig` screens; blank for whole-genome rows)
- domain_guess
- route
- tool
- tool_version
- db_source
- db_version
- taxonomy_string
- terminal_rank
- ncbi_taxid (blank if not applicable)
- lineage_names
- lineage_taxids
- confidence (numeric or categorical)
- notes (conflicts, merges, caveats)

Required artifacts for assignment workflows:
- `quickclade_percontig.tsv`
- `domain_routing.tsv`
- downstream tool result directories for every routed domain present in the input

### Validation notes (required)
- conflicts across sources (GTDB vs NCBI, ICTV vs NCBI names, etc.)
- merged/deleted taxids encountered and how they were resolved
- sequences needing manual review
