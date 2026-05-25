---
name: bio-protein-clustering-pangenome
description: Cluster proteins into orthogroups and derive pangenome matrices.
---

# Bio Protein Clustering Pangenome

Cluster proteins into orthogroups and derive pangenome matrices.

## Instructions

1. Cluster proteins. Choose the tool by dataset size and goal:
   - Default for orthology inference up to a few hundred genomes: **OrthoFinder v3** (improved accuracy and lower RAM at scale, supports MSA-based gene trees; supersedes OrthoFinder v2 and OrthoMCL workflows).
   - Very large pangenomes where OrthoFinder is too RAM-heavy: **ProteinOrtho v6.1.7+** as the fast, scalable alternative.
   - Sequence clustering (not strict orthology) and similarity search backbones: **MMseqs2** v15-6f452+. Enable GPU mode (`mmseqs ... --gpu`) on CUDA Turing+ nodes for a ~20× speedup at near-identical sensitivity.
2. Build presence/absence matrix AND an integer copy-number matrix (orthogroup × genome) covering the query AND the close relatives produced by `/bio-phylogenomics`.
3. Compute core/accessory/cloud/singleton partitions.
4. Identify single-copy orthologs for phylogenetic analysis.
5. Discriminate paralogs from orthologs in multi-copy gene families.
6. Calculate pangenome statistics (completeness, orthogroup occupancy).
7. When a query genome or genome set is under study, use the literature-derived analysis playbook to choose an appropriate comparison baseline: closest relatives, a broader clade, environmental references, or a negative/control set.
8. **Genome-property frontier table** — produce `relative_genome_metrics.tsv` with one row per (query + relative) and columns for genome size, contig count, N50, gene count, coding density, GC, tRNA count, rRNA count, and any group-relevant property. Add a column that places the query in the relative distribution (percentile, min/median/max, "record-class" tag) and a column citing the literature reference defining the group's known range.
9. **Synteny / conserved neighborhoods** — for each pair (query, relative) compute conserved gene neighborhoods (e.g., ≥2 collinear orthologs). Tool selection:
   - Pairwise / classical: MCScanX (*Nature Protocols* 2024 updated protocol).
   - Multi-genome at scale (>2 assemblies, up to >3 Gbp, >15% divergence): **ntSynt** (*BMC Biology* 2025, DOI: 10.1186/s12915-025-02455-w) — alignment-free minimizer-graph approach; does not detect duplications.
   - Strain-level work where duplication detection matters: SibeliaZ.
   Save results as `conserved_neighborhoods.tsv` with columns: query_block_id, relative, relative_block_id, members (ortholog IDs), intergenic_spacing_query, intergenic_spacing_relative, spacing_ratio, notes. Flag conserved gene pairs and unusual spacing/expansions.
10. Identify discovery-relevant differences defined by the playbook, including query-specific families, missing expected families, expansions/contractions, unusual sharing patterns, and high-value unknowns. Persist as `family_copy_number_comparison.tsv` (query vs relative-median fold change per family) — coordinated with `bio-annotation`'s family matrix.
11. Annotate candidate orthogroups with `/bio-annotation`; for high-value unknowns, route representatives to `/bio-structure-annotation` when structure-based inference is appropriate.
12. Produce a comparison summary that separates conserved lineage features from unusual or query-specific features and states the baseline used. The summary must report ALL of: genome-property frontier, marker-category presence/copy, family expansions/contractions, synteny conservation/breakage, and ncRNA counts side-by-side with relatives.

## Quick Reference

| Task | Action |
|------|--------|
| Run workflow | Follow the steps in this skill and capture outputs. |
| Validate inputs | Confirm required inputs and reference data exist. |
| Review outputs | Inspect reports and QC gates before proceeding. |
| Tool docs | See `docs/README.md`. |
| References | See `references.md`. |

## Input Requirements

Prerequisites:
- Tools available in the active environment (Pixi/conda/system). See `docs/README.md` for expected tools.
- Protein FASTA inputs are available.
Inputs:
- proteins.faa (FASTA protein sequences)

## Output

- results/bio-protein-clustering-pangenome/orthogroups.tsv
- results/bio-protein-clustering-pangenome/presence_absence.parquet
- results/bio-protein-clustering-pangenome/copy_number_matrix.parquet
- results/bio-protein-clustering-pangenome/relative_genome_metrics.tsv
- results/bio-protein-clustering-pangenome/family_copy_number_comparison.tsv
- results/bio-protein-clustering-pangenome/conserved_neighborhoods.tsv
- results/bio-protein-clustering-pangenome/closest_relative_comparison.tsv
- results/bio-protein-clustering-pangenome/query_specific_candidates.tsv
- results/bio-protein-clustering-pangenome/pangenome_report.md
- results/bio-protein-clustering-pangenome/logs/

## Quality Gates

- [ ] Cluster size distributions meet project thresholds.
- [ ] Matrix completeness meets project thresholds.
- [ ] On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.
- [ ] Verify proteins.faa is non-empty and amino acid encoded.
- [ ] Comparison baseline is justified from literature, phylogeny, taxonomy, or data availability.
- [ ] Query-specific, missing, expanded, and conserved orthogroups are reported separately.
- [ ] Candidate discovery orthogroups have annotation evidence or a recommended follow-up analysis.
- [ ] `relative_genome_metrics.tsv` places each query in the distribution of relatives and notes the literature-defined extreme of the inferred group.
- [ ] `family_copy_number_comparison.tsv` reports per-family fold change vs the relative median for the full annotated family set, not only top candidates.
- [ ] `conserved_neighborhoods.tsv` is produced and includes intergenic spacing for both query and relative sides; broken synteny, unusual spacing, and expansions are flagged.

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
