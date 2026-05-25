# JGI Lakehouse Usage Examples

**Read these before writing queries.** Each example documents pitfalls discovered through real usage.

## Examples (Markdown - read directly)

| File | Use Case | Key Pitfalls |
|------|----------|--------------|
| `01-find-16s-rrna-genes.md` | Find 16S rRNA genes by taxonomy | `family` field unreliable; sequences not in DB |
| `03-cross-database-joins.md` | Join GOLD, IMG, SRA tables | Wrong column names; `master_study_id` not `study_id` |
| `04-download-img-genomes.md` | Download genomes with IMG taxon OIDs | Use JGI filesystem, not Lakehouse for sequences |
| `05-query-numg-metagenome-proteins.md` | Query metagenome proteins + Pfam in NUMG | Join with `oid` + `gene_oid`; not for isolates |

## Quick Pitfall Reference

| What You Might Try | Correct Approach |
|-------------------|------------------|
| `project.ecosystem` | Join to `study` via `master_study_id` |
| `WHERE family = 'X'` | Use `LIKE '%X%'` on `taxon_display_name` |
| `experiment_id` | Use `exp_oid` |
| `experiment_name` | Use `exp_name` |
| `sra_experiment_v2.platform` | Use `library_instrument` |
| Get sequences from Lakehouse | Download from JGI filesystem |
| `numg-iceberg.faa` for isolates | Use JGI filesystem (metagenomes only in numg-iceberg) |
| `gene_ko_terms` with `K00025` | Use `KO:K00025` |
| `LOWER(pfam_family) = 'pfam00001'` | Use exact `pfam_family = 'pfam00001'` |
| Isolate benchmark counts drift | Include `obsolete_flag = 'No'` |
| `IMG.gene_feature` for production queries | Prefer `img_core_v400` fallback if view expansion fails |
| `show_schemas()` default output | Use higher limit to avoid truncation |

## Python Scripts (optional)

For automated workflows, see:
- `find_16s_rrna_genes.py` - Batch 16S gene search

See also `../scripts/`:
- `download_img_genomes.py` - Download genomes with IMG taxon OIDs from JGI filesystem

These use `scripts/rest_client.py` which handles job polling automatically.

## Prerequisites

```bash
export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
```
