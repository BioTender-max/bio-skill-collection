---
name: bio-annotation
description: Functional annotation and taxonomy inference from sequence homology.
---

# Bio Annotation

Functional annotation and taxonomy inference from sequence homology.

## Instructions

1. Read `docs/README.md` and the relevant tool guides before running anything.
2. When a nucleotide assembly, MAG, genome, or contig FASTA is available, run `/tracking-taxonomy-updates` first for the BBTools-container QuickClade `percontig` domain screen. Use that routing table to choose the right taxonomy/QC path before interpreting protein annotations.
3. For InterProScan, read `docs/interproscan-usage.md` and validate the exact CLI with `--help` or `--version`. Current stable is v5.77-108.0; InterProScan 6 (Nextflow-based) is a forward-looking migration target.
4. Run InterProScan for domain/family annotation.
5. Run eggNOG-mapper v2.1.13+ for orthology-based annotation.
6. Run sequence-vs-database search and resolve taxonomy with TaxonKit v0.20.0+ (required for the March 2025 NCBI rank update that replaces "superkingdom" with "domain" and adds "realm" for viruses).
   - Default CPU path: DIAMOND v2.1.20+. For any search against NCBI **nr**, prefer a clustered nr database (e.g., a `clusterednr` build under `$BIO_DB_ROOT`) — it is dramatically faster than full nr at comparable sensitivity for most annotation tasks. Check whether a clusterednr build is available under the reference root; if not, build one with `diamond makedb` from a clustered FASTA (MMseqs2/CD-HIT-reduced nr) or fall back to full nr and record the choice in the run log.
   - GPU node available (CUDA Turing or newer): MMseqs2-GPU as an alternative to DIAMOND. Published benchmark: 20× faster and ~71× cheaper per query versus 128-core CPU MMseqs2, and 177–199× faster than JackHMMER iterative search for profile-equivalent workflows (Kallenborn et al., *Nature Methods* 2025, DOI: 10.1038/s41592-025-02819-8). Use `mmseqs easy-search` or `easy-taxonomy` with the `--gpu` flag.
7. For domain-specific taxonomy after QuickClade:
   - Bacteria/Archaea -> run GTDB-Tk when genome/MAG-level sequence is available and cross-check NCBI/DIAMOND lineage assignments.
   - Viral/phage -> route to `/bio-viromics`; use PHROG/NCVOG markers and vConTACT3 only for phage/prokaryotic-virus contexts.
   - Giant-virus/Nucleocytoviricota -> route to `/bio-viromics` with GVClass and NCLDV marker-gene phylogeny.
   - Eukaryota -> use EukCC for MAG/genome QC and lineage context; avoid CheckM/GTDB-Tk assumptions.
8. For group-appropriate marker families, run HMM searches against the relevant profile libraries (Pfam, TIGRFAM, COG/arCOG, PHROG/NCVOG for viruses, eukaryotic ribosomal/structural HMMs when applicable). Use `pyhmmer` (Python bindings around HMMER 3.4 with native SIMD and batch-friendly APIs) by default; fall back to the HMMER CLI (`hmmsearch` / `hmmscan`) when an upstream tool requires it. The choice of profile libraries is derived from the literature-derived playbook for the inferred group.
9. Build an annotation-wide feature inventory by genome/contig and by gene family/domain/pathway.
10. **Marker-gene census** — from the literature-derived playbook, list the diagnostic marker / machinery categories for the inferred group (e.g., replication, transcription, translation-related such as ribosomal proteins and translation factors, packaging, capsid/structural, chromatin/SMC/topoisomerase, host-interaction). For EACH query genome and each comparison-set genome supplied, record presence and copy number per category. Save as `marker_census.tsv` (columns: genome, category, family_id, family_name, copy_number, evidence_source, e_value, notes). Expected-but-absent markers are first-class rows, not silent omissions.
11. **Per-family copy-number matrix** — build a Pfam/InterPro/HMM-family × genome integer matrix covering queries AND the supplied relatives. Persist as `family_copy_number_matrix.parquet`. Compute per-family fold change vs the relative median; flag query-specific families, missing-expected families, expansions, and contractions in `family_expansion_candidates.tsv`.
12. For exploratory work, read the literature-derived analysis playbook for the inferred organism or virus group before deciding what to flag.
13. Mine the inventory for discovery candidates relative to that playbook: expected features, missing expected features, rare or expanded families, unusual combinations, annotation/taxonomy conflicts, and high-value unknowns.
14. For specialized inputs such as viruses, organelles, symbionts, pathogens, or poorly characterized lineages, use the feature classes and outlier dimensions reported in the relevant literature rather than a fixed global checklist.
15. Rank discovery candidates by evidence strength, novelty relative to the comparison baseline, confidence, and follow-up value.

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
- Input FASTA and reference DBs are readable.
Inputs:
- proteins.faa (FASTA protein sequences).
- reference_db/ (eggNOG, InterPro, DIAMOND databases + taxdump).

## Output

- results/bio-annotation/annotations.parquet
- results/bio-annotation/domain_routing.tsv
- results/bio-annotation/taxonomy.parquet
- results/bio-annotation/feature_inventory.parquet
- results/bio-annotation/marker_census.tsv
- results/bio-annotation/family_copy_number_matrix.parquet
- results/bio-annotation/family_expansion_candidates.tsv
- results/bio-annotation/discovery_candidates.tsv
- results/bio-annotation/annotation_report.md
- results/bio-annotation/logs/

## Quality Gates

- [ ] Annotation hit rate and taxonomy rank coverage meet project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.
- [ ] Verify proteins.faa does not contain `*` stop symbols before InterProScan, or strip them deliberately.
- [ ] QuickClade domain routing was used when nucleotide assemblies/genomes were available, or the protein-only reason for skipping it is recorded.
- [ ] Verify InterProScan output options are valid: use `-b` or `-d`, never both together.
- [ ] Verify packaged InterProScan installs have been initialized with `python3 setup.py -f interproscan.properties` when required.
- [ ] Verify required InterProScan helper binaries are resolvable, especially `ps_scan.pl`, `pfscan`, and `pfsearch`.
- [ ] Run a small login-node smoke test on 1-2 proteins before submitting a large cluster job.
- [ ] Verify required reference DBs exist under the reference root.
- [ ] Domain-specific taxonomy tools match the route: GTDB-Tk for Bacteria/Archaea, `/bio-viromics` plus vConTACT3/GVClass as appropriate for viruses, and EukCC for Eukaryota.
- [ ] Feature inventory summarizes all annotated and unannotated proteins, not only top hits.
- [ ] `marker_census.tsv` covers every literature-derived marker category for the inferred group with explicit zero rows for absent markers.
- [ ] `family_copy_number_matrix.parquet` includes the query AND the supplied relatives, and `family_expansion_candidates.tsv` flags query-specific, missing-expected, expanded, and contracted families with fold-change vs the relative median.
- [ ] Discovery candidates include evidence fields: gene/protein ID, annotation source, confidence, why notable, and recommended validation.
- [ ] Discovery candidates are justified against the literature-derived playbook and comparison baseline, not only by generic keyword matches.

## Examples

### Example 1: Expected input layout

```text
proteins.faa (FASTA protein sequences).
reference_db/ (eggNOG, InterPro, DIAMOND databases + taxdump).
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: InterProScan fails immediately with CLI or runtime setup errors
**Solution**: Check `docs/interproscan-usage.md` for mutually exclusive output flags, `*` stripping, one-time `setup.py` initialization, and ProSite `PATH` requirements.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.
