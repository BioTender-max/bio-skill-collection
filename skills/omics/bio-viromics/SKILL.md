---
name: bio-viromics
description: Detect, classify, and QC viral contigs.
---

# Bio Viromics

Detect, classify, and QC viral contigs.

## Instructions

1. Start from `/tracking-taxonomy-updates` QuickClade domain routing when assemblies, MAGs, genomes, or contigs have not already been screened. Viral, virus-like, mixed, or low-confidence contigs enter this skill; bacterial/archaeal and eukaryotic rows stay on their domain-specific routes unless later evidence contradicts the triage.
2. Run virus detection with geNomad v1.8+ (use as primary plasmid-and-virus classifier).
3. Run CheckV v1.0.1 for completeness, contamination, and host-removal QC.
4. Infer the likely viral group from QuickClade, detection output, taxonomy hints, genome statistics, and marker/similarity evidence.
5. Search the literature for that viral group and write a short analysis playbook: typical reference sets, markers, comparative analyses, genome features, plots, and outlier signals used by scientists studying that group.
6. Choose taxonomy, clustering, phylogenetic, and comparative methods from the playbook:
   - For bacteriophage and prokaryotic-virus gene-sharing taxonomy: vConTACT3 v3.0 (hierarchical genus-to-order assignment, >95% ICTV agreement; supersedes vConTACT2).
   - For Nucleocytoviricota / giant viruses: gvclass v1.0 for genus-level classification combined with marker-gene phylogenies of NCLDV core genes.
   - For RNA viruses, ssDNA viruses, or other groups not well-served by vConTACT3: use group-specific markers, phylogenomics, and protein-family approaches from the literature playbook rather than forcing a phage-oriented workflow.
7. For prokaryotic-virus discovery, VirSorter2 v2.2.4 is a complementary detector to geNomad; combine with CheckV QC to remove false positives.
8. For each viral genome or high-quality viral contig, call genes and annotate proteins when needed, then inspect the annotation set according to the playbook rather than a fixed global feature list.
9. Compare each query viral genome to the literature-supported reference set. Report what matches expectations, what is missing, what is expanded, what is query-specific, and which patterns are likely artifacts.
10. **Genome-size frontier** — for each query, compute where the genome size and gene count sit within the distribution of close relatives AND the literature-reported extremes for the inferred viral group. State percentile, distance from the group median, and whether the query approaches or exceeds known record-class sizes (cite the paper that defines that record). This applies even when the query is mid-distribution — the placement itself is the finding.
11. Produce an interesting-findings table. If no strong discovery candidates are found, state that explicitly and list the literature-derived checks performed.

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
- Input contigs are available.
Inputs:
- contigs.fasta
- results/taxonomy/domain_routing.tsv when available

## Output

- results/bio-viromics/viral_contigs.fasta
- results/bio-viromics/domain_routing_review.tsv
- results/bio-viromics/checkv_results/
- results/bio-viromics/group_comparison_results/
- results/bio-viromics/analysis_playbook.md
- results/bio-viromics/viral_taxonomy.tsv
- results/bio-viromics/comparison_baseline.tsv
- results/bio-viromics/closest_relatives.tsv
- results/bio-viromics/viral_discovery_candidates.tsv
- results/bio-viromics/viral_feature_inventory.tsv
- results/bio-viromics/genome_size_frontier.tsv
- results/bio-viromics/viromics_report.md
- results/bio-viromics/logs/

## Quality Gates

- [ ] CheckV quality thresholds meet project standards.
- [ ] Contamination flags are below thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify contigs.fasta is non-empty.
- [ ] QuickClade domain-routing evidence was reviewed for assembly/MAG/genome inputs, or the absence of a prior screen is corrected before final classification.
- [ ] Verify viral reference DBs exist under the reference root.
- [ ] Literature-derived analysis playbook names the inferred viral group, cited sources, standard analyses, and chosen/skipped methods.
- [ ] Chosen comparison method is appropriate for the inferred viral group; phage-oriented tools are not used for non-phage groups without literature support.
- [ ] Discovery scan covers the feature classes and outlier dimensions identified in the playbook.
- [ ] Closest-relative or reference-set context is reported for every high-quality viral genome where references are available.
- [ ] `genome_size_frontier.tsv` places each query in the size/gene-count distribution of close relatives and the literature-defined group extremes, with cited references.
- [ ] Report includes candidate discoveries with evidence, confidence, relative comparison, and follow-up checks, or a credible negative finding.

## Examples

### Example 1: Expected input layout

```text
contigs.fasta
```

## Troubleshooting

**Issue**: Missing inputs or reference databases
**Solution**: Verify paths and permissions before running the workflow.

**Issue**: Low-quality results or failed QC gates
**Solution**: Review reports, adjust parameters, and re-run the affected step.
