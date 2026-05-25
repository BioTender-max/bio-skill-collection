---
name: tracking-taxonomy-updates
description: Track and reconcile taxonomy updates across NCBI, GTDB, ICTV, and community eukaryote frameworks with versioned provenance.
---

# Tracking Taxonomy Updates

Use authoritative sources to report taxonomy changes with explicit versions, dates, and provenance.

## Instructions

1. Determine scope (domain, timeframe, output type).
2. Pull authoritative updates and release notes.
3. Extract versioned changes and impacts.
4. If assigning taxonomy for any assembly, MAG, SAG, isolate genome, bin set, or contig FASTA, start with a QuickClade first-pass domain screen through the BBTools container. Save both per-input and `percontig` results before choosing downstream tools.
5. Route from the QuickClade domain screen:
   - Bacteria or Archaea -> run GTDB-Tk for genome taxonomy. If the GTDB-Tk reference package is missing, set up/download it under the project/reference DB root, set `GTDBTK_DATA_PATH`, and record the release before running classification.
   - Viral or virus-like -> route to `/bio-viromics`; use vConTACT3 for phage/prokaryotic-virus gene-sharing taxonomy and GVClass for giant-virus/Nucleocytoviricota candidates.
   - Eukaryota -> run EukCC for eukaryotic MAG/genome QC and taxonomy context.
   - Mixed, low-confidence, or conflicting domains -> split or flag contigs for manual review before domain-specific classification.
6. Normalize IDs and taxonomy strings across tools.
7. Deliver a versioned report with conflicts flagged.

## Quick Reference

| Task | Action |
|------|--------|
| Sources | See `reference/sources.md` |
| Tools | See `reference/tools.md` |
| IDs/ranks | See `reference/ranks-and-identifiers.md` |
| Report template | See `reference/report-template.md` |
| QA checklist | See `reference/qa-checklist.md` |
| Environment | See `env/README.md` |

## Domain Triage Contract

QuickClade is the required first pass for sequence-to-taxonomy assignment unless the user explicitly supplies a trusted domain label and asks to skip triage. It is a router, not the final authority.

Persist:
- `results/taxonomy/quickclade_percontig.tsv`
- `results/taxonomy/domain_routing.tsv`
- downstream tool outputs under `results/taxonomy/{gtdbtk,eukcc,vcontact3,gvclass}/`

Minimum `domain_routing.tsv` columns:
- `sample_id`
- `query_id`
- `contig_id`
- `quickclade_domain`
- `quickclade_taxonomy`
- `quickclade_confidence`
- `route`
- `downstream_tool`
- `review_flag`
- `notes`

## Input Requirements

- Domain(s) and timeframe
- Source systems to compare (NCBI/GTDB/ICTV/etc.)
- Sequences or genomes (for assignment workflows)

## Output

- Versioned taxonomy update summary
- Conflict report across sources
- Standardized taxonomy assignment table (when applicable)
- QuickClade per-contig domain screen and routing table for sequence assignment workflows

## Quality Gates

- [ ] Every “latest” claim includes date, version, and authority
- [ ] Stable identifiers used for joins (taxids, GTDB IDs)
- [ ] Provenance captured (tool version, DB release, run date)
- [ ] QuickClade was run first for assembly/MAG/genome assignment workflows, with container tag and reference spectra recorded.
- [ ] Per-contig QuickClade results were persisted and used to choose downstream tools.
- [ ] Bacteria/Archaea routes include GTDB-Tk outputs and the GTDB reference release; missing GTDB-Tk databases were installed or explicitly reported as blockers.
- [ ] Viral routes distinguish phage/prokaryotic viruses from giant-virus/Nucleocytoviricota candidates before choosing vConTACT3 or GVClass.
- [ ] Eukaryotic routes use EukCC rather than prokaryotic QC/taxonomy tools.

## Examples

### Example 1: Update scan scope

```text
Domains: Bacteria + Archaea
Timeframe: last 12 months
Output: summary table + pipeline impact notes
```

## Troubleshooting

**Issue**: Conflicting taxonomy between sources
**Solution**: Report both with explicit conflict flags and provenance.

**Issue**: Missing stable IDs
**Solution**: Resolve via TaxonKit and capture merged/deleted taxid warnings.
