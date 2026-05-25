---
name: bio-structure-annotation
description: Structure prediction and structure-based annotation.
---

# Bio Structure Annotation

Structure prediction and structure-based annotation.

## Instructions

1. Run a fast embedding screen with TM-Vec to triage candidate proteins by remote homology before incurring structure-prediction cost.
2. Predict structures on a GPU node. AlphaFold3 is intentionally not part of this stack (non-commercial license, large VRAM footprint, no clear quality gap for the workflows in this repo). Use:
   - **Boltz-2** (MIT license; CUDA; NVIDIA cuEquivariance kernels) as the default predictor — joint structure-and-affinity, ~1000× faster than FEP for binding-affinity estimation, comparable accuracy to AF3 on benchmarked complexes.
   - **ColabFold** v1.5.5+ with an **MMseqs2-GPU** MSA backend when a wider MSA than Boltz-2 builds is required (≈31.8× faster MSA generation versus the standard AF2 pipeline; *Nature Protocols* 2025, DOI: 10.1038/s41596-024-01060-5).
   - **ESMFold** for fast monomer pre-screening only (15–20 GB VRAM; lower accuracy than Boltz-2).
3. Search predicted or experimental structures with **Foldseek v9+**. Use `--gpu 1` on CUDA Turing or newer for the ProstT5-backed search (4–27× speedup). Consider Foldseek-Multimer when complex-vs-complex search is needed.
4. Annotate hits and route high-value unknowns back to `/bio-annotation` for sequence-side context, or to comparative analyses via `/bio-protein-clustering-pangenome`.

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
- Reference DB root: set `BIO_DB_ROOT` (default `/media/shared-expansion/db/` on WSU).
- Protein FASTA inputs are available.
Inputs:
- proteins.faa (FASTA protein sequences)

## Output

- results/bio-structure-annotation/structures/
- results/bio-structure-annotation/structure_hits.tsv
- results/bio-structure-annotation/structure_report.md
- results/bio-structure-annotation/logs/

## Quality Gates

- [ ] Prediction success rate meets project thresholds.
- [ ] Search hit thresholds meet project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.
- [ ] Verify Foldseek databases exist under the reference root.

## Examples

### Example 1: Expected input layout

```text
proteins.faa (FASTA protein sequences)
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.