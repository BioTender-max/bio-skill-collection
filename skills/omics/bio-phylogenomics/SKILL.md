---
name: bio-phylogenomics
description: Build marker gene alignments and phylogenetic trees.
---

# Bio Phylogenomics

Build marker gene alignments and phylogenetic trees.

## Instructions

1. Extract marker genes or SSU rRNA sequences.
2. Align with MAFFT v7.5+ and trim with trimAl v1.4 (or ClipKIT when phylogenetically-informed trimming is preferred).
3. Build ML trees with support values. Choose by objective first, then leaf count:
   - Exploratory placement, benchmark iterations, reference-set screening, or any time-bounded analysis: use VeryFastTree v4.0 first, even below ~2,000 taxa. Prefer `VeryFastTree -boot 1000 -threads <n> < alignment.faa > tree.nw` for proteins and add `-nt` for nucleotide alignments.
   - Final or publication-quality trees up to ~2,000 taxa: IQ-TREE v3 (v3.1.2+) for comprehensive model selection, MAST/GTRpmix, UFBoot/SH-aLRT, and defensible final inference.
   - Above ~2,000 taxa, or when memory/runtime is uncertain: VeryFastTree v4.0 (multi-threaded, SIMD, `-disk-computing` for very large trees).
   - Use `iqtree3 -fast` only when VeryFastTree is unavailable or a project explicitly requires IQ-TREE-compatible exploratory output; record that fallback in the report.
4. Post-process trees with ETE v4 (`ete4`):
   - Compute tree statistics (branch lengths, distances, topology metrics).
   - Root, prune, or collapse nodes as needed.
   - Filter by bootstrap support.
   - Add taxonomic or trait annotations.
   - Generate publication-quality visualizations.
13. Use the literature-derived analysis playbook to choose markers, reference sampling, rooting, and placement strategy appropriate for the inferred group.
14. Identify nearest neighbors and closest named relatives for each query sequence/genome when the chosen marker/reference set supports that interpretation.
15. Export a closest-relatives table with support values, distances, taxonomy, reference accessions, and uncertainty notes.
16. **Fetch and persist the close-relative genomes and proteomes** that downstream comparative analyses will use. Save under `results/bio-phylogenomics/relatives/{accession}/genome.fna` and `proteins.faa`, plus `relatives_manifest.tsv` recording accession, source DB, taxonomy, genome size, gene count, and the reason for inclusion. If a relative cannot be downloaded, record the failure explicitly. Without this artifact, the comparative axes downstream cannot run.
17. Use well-supported relatives or a documented broader comparison set to guide downstream comparative analysis with `/bio-protein-clustering-pangenome` and `/bio-annotation`.

## Quick Reference

| Task | Action |
|------|--------|
| Run workflow | Follow the steps in this skill and capture outputs. |
| Validate inputs | Confirm required inputs and reference data exist. |
| Review outputs | Inspect reports and QC gates before proceeding. |
| Tool docs | See `docs/README.md`. |

## Input Requirements

Prerequisites:
- Tools available in the active environment (Pixi/conda/system). See `docs/README.md` for expected tools.
- Marker gene set or alignments available.
Inputs:
- markers.faa (marker genes) or alignments.fasta

## Output

- results/bio-phylogenomics/alignments/
- results/bio-phylogenomics/trees/
- results/bio-phylogenomics/closest_relatives.tsv
- results/bio-phylogenomics/relatives/{accession}/genome.fna
- results/bio-phylogenomics/relatives/{accession}/proteins.faa
- results/bio-phylogenomics/relatives_manifest.tsv
- results/bio-phylogenomics/phylo_report.md
- results/bio-phylogenomics/logs/

## Quality Gates

- [ ] Alignment length and missingness meet project thresholds.
- [ ] Bootstrap support summary meets project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify markers.faa is non-empty and aligned sequences are consistent.
- [ ] Marker and reference choices are justified against the literature-derived analysis playbook.
- [ ] Closest relatives are reported with support/distance metrics or uncertainty is stated.
- [ ] Tree interpretation distinguishes well-supported nearest relatives from weakly supported placements.
- [ ] `relatives_manifest.tsv` is populated and the matching genome/proteome files are present on disk (or each failure is recorded with a reason).

## Examples

### Example 1: Expected input layout

```text
markers.faa (marker genes) or alignments.fasta
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.
