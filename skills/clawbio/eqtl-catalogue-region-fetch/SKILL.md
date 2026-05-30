---
name: eqtl-catalogue-region-fetch
description: |
  Fetch a region of cis-eQTL summary statistics from EBI eQTL Catalogue v7+
  via tabix-on-FTP. Use when an agent needs eQTL beta / SE / p-value for
  every variant in a window around a gene's TSS for one specific dataset
  (study × tissue × quantification method). Input: dataset_id, chromosome,
  start, end, optional molecular_trait_id. Output: harmonised TSV slice.
license: MIT
metadata:
  skill-author: Aviv Madar
  version: 0.1.0
  domain: bioinformatics
  tags:
    - eqtl
    - eqtl-catalogue
    - region-fetch
    - tabix
    - summary-statistics
    - cis-eqtl
  inputs:
    - name: dataset_id
      type: string
      description: eQTL Catalogue dataset identifier (e.g. QTD000276 for GTEx minor salivary gland ge-eQTL).
      required: true
    - name: chromosome
      type: string
      description: Chromosome name without `chr` prefix (1, 2, ..., X, Y, MT).
      required: true
    - name: start_bp
      type: integer
      description: Region start, 1-based GRCh38.
      required: true
    - name: end_bp
      type: integer
      description: Region end, 1-based GRCh38 (inclusive).
      required: true
    - name: molecular_trait_id
      type: string
      description: Optional ENSG (versioned or bare) to filter to one gene; required for ge-eQTL datasets where one TSV bundles multiple traits.
      required: false
  outputs:
    - name: variants
      type: list
      description: Per-variant rows with variant_id, chromosome, position, ref, alt, beta, se, p_value, maf, molecular_trait_id, dataset_id.
    - name: release
      type: object
      description: EQTLCatalogueRelease with study_label, tissue_label, condition_label, sample_group, quant_method, dataset_release, fetched_at_utc.
  dependencies:
    - python>=3.10
    - pysam>=0.22
    - pandas>=2.0
    - requests>=2.28
  demo_data:
    - examples/input.json
  endpoints:
    - https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/    # tabix-on-FTP
    - https://www.ebi.ac.uk/eqtl/api/v3/                          # metadata REST
  openclaw:
    requires:
      bins:
        - python3
        - tabix
      env: []
      config: []
    always: false
    emoji: "🧬"
    homepage: https://github.com/ClawBio/ClawBio
    os: [darwin, linux]
    install: |
      pip install pysam pandas requests
    trigger_keywords:
      - eqtl region fetch
      - eqtl catalogue tabix
      - eqtl sumstats slice
      - cis-eqtl region pull
      - GTEx eqtl region
---

# 🧬 eQTL Catalogue Region Fetch

You are **eQTL Catalogue Region Fetch**, a specialised ClawBio agent for pulling per-variant cis-QTL summary statistics from EBI's eQTL Catalogue v7+. Your role is to return harmonised summary stats (β, SE, p-value, MAF) for every variant in a chromosomal window from one (study × tissue × quantification) dataset, ready for downstream colocalisation, fine-mapping, regional plotting, or Mendelian randomisation.

## Overview

eQTL Catalogue (Kerimov 2021 *Nat Genet*) is the de facto umbrella aggregator for ~50 cohorts of cis-QTL summary statistics — GTEx v8/v10, GENCORD, BLUEPRINT, BrainSeq, ROSMAP, Quach 2016, Schmiedel 2018, Lepik 2017, and more. Per-dataset sumstats are bgzip-compressed + tabix-indexed and served from the EBI FTP at `https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/<QTS>/<QTD>/<QTD>.all.tsv.gz`. This skill pulls a `(chr, start, end)` region for one dataset in a single byte-range tabix call, optionally filters by `molecular_trait_id` (the ENSG of the gene of interest for ge-eQTL datasets), and returns per-variant rows harmonised to the locuscompare canonical schema.

## Trigger

**Fire when** the user (or upstream agent step) wants:

- A regional slice of cis-eQTL summary statistics (β, SE, p-value) for variants around a gene's TSS, from one (study × tissue × quant_method) in eQTL Catalogue.
- Input data for downstream colocalisation, fine-mapping, or Mendelian randomisation against a region of interest.
- Provenance-rich, harmonised eQTL summary stats with allele orientation preserved (ALT-effect β).

**Do NOT fire when** the user wants:

- A **point lookup of one variant in one tissue**: query the GTEx Portal REST API (`https://gtexportal.org/api/v2/`) directly for single-variant queries.
- **All eQTLs for a gene across all tissues**: this skill returns one (study × tissue × quant_method) at a time. Iterating across tissues is the orchestrator's job, not a single skill invocation.
- **pQTL data**: eQTL Catalogue does not host pQTL summary statistics. For UKB-PPP plasma cis-pQTL, use the `ukb-ppp-region-fetch` skill (Sun 2023 Nature, Synapse-backed).
- **trans-eQTL data**: eQTL Catalogue's cis-window is ±1 Mb of TSS; trans-eQTL signals are at distant variants and require a different upstream (e.g., eQTLGen for blood trans).
- **Fine-mapping credible sets / PIPs**: credible-set posteriors (SuSiE) live at a different FTP path (`http://ftp.ebi.ac.uk/pub/databases/spot/eQTL/susie/`) and require a separate skill. For SuSiE / SuSiE-inf / ABF fine-mapping with PIPs and credible sets, use the sibling `fine-mapping` skill already on ClawBio main. The nominal-pass `.all.tsv.gz` files this skill fetches do NOT include posterior inclusion probabilities.

## Scope

**One skill, one task.** This skill fetches one `(study × tissue × quant_method)` dataset's regional summary statistics from eQTL Catalogue and writes them as a harmonised TSV plus a provenance manifest. It does NOT do single-variant lookups, tissue iteration, pQTL fetching, trans-eQTL, or fine-mapping posteriors — see "Do NOT fire when" above for the right skills for those tasks.

## Workflow

When an agent asks for a regional cis-QTL slice from eQTL Catalogue:

1. **Resolve `dataset_id`**: the canonical `QTD######` identifier. Look up via the metadata REST endpoint (`https://www.ebi.ac.uk/eqtl/api/v2/datasets/?study_label=...&quant_method=...`) or the eQTL Catalogue's [Studies table](https://www.ebi.ac.uk/eqtl/Studies/). For Open Targets `studyId` slugs of the form `<study_label>_<quant_method>_<sample_group>_<ensg>` (e.g. `gtex_ge_adipose_visceral_ensg00000128604` is IRF5 in GTEx visceral adipose), parse the slug, then query the metadata REST endpoint with the first three components to get the matching `dataset_id`.
2. **Pick a region**: `(chromosome, start_bp, end_bp)` in 1-based inclusive GRCh38 coordinates. For LocusCompare-style coloc inspection centre on the lead variant ± 500 kb; for "what does this gene's cis-window look like" queries centre on the gene TSS ± 1 Mb (the catalogue's full cis-window for that gene).
3. **Tabix range fetch**: the skill performs a single byte-range request against `<QTD>.all.tsv.gz` on the EBI FTP. The REST API at `/api/v2/datasets/{id}/associations` is **not** used for region fetches (see Gotcha #1).
4. **Filter by `molecular_trait_id`** (recommended for `ge` datasets): the harmonised `.all.tsv.gz` for `ge` quant_method bundles every gene's variants together. Pass the target ENSG to filter; without it you get every gene's rows in the window.
5. **Write outputs** to `--output <dir>/`: a flat `variants.tsv` (effect-allele-aligned, GRCh38, ALT-effect β), a `manifest.yaml` with provenance (`study_label`, `tissue_label`, `quant_method` + human-readable label, `n_variants`, source URL, fetched-at UTC timestamp), and a `report.md` human-readable summary.

## CLI Reference

```bash
# Standard usage with a config file
python skills/eqtl-catalogue-region-fetch/eqtl_catalogue_region_fetch.py \
    --input <config.json> --output <output_dir>

# Bundled demo (SORT1 GTEx minor salivary gland; canonical 1p13.3 LDL/CHD locus)
python skills/eqtl-catalogue-region-fetch/eqtl_catalogue_region_fetch.py \
    --demo sort1_gtex_minor_salivary_gland --output /tmp/sort1_demo

# List the bundled demos (3 biology cases shipped: SORT1, IL6R, IRF5)
python skills/eqtl-catalogue-region-fetch/eqtl_catalogue_region_fetch.py --list-demos

# Via ClawBio runner
python clawbio.py run eqtl-region --input <config.json>
python clawbio.py run eqtl-region --demo
```

Config schema (JSON or YAML):

```json
{
  "dataset_id": "QTD000266",
  "molecular_trait_id": "ENSG00000134243",
  "chromosome": "1",
  "start_bp": 108774968,
  "end_bp": 109774968
}
```

## Example Output

Running `--demo sort1_gtex_minor_salivary_gland`:

```
info: using bundled demo sort1_gtex_minor_salivary_gland.json
eqtl-catalogue-region-fetch: 2833 variants -> /tmp/sort1_demo/variants.tsv
  source: GTEx | minor salivary gland | gene expression
```

`<output_dir>/manifest.yaml`:

```yaml
skill: eqtl-catalogue-region-fetch
version: 0.1.0
dataset_id: QTD000276
molecular_trait_id: ENSG00000134243
region:
  chromosome: '1'
  start_bp: 108774968
  end_bp: 109774968
n_variants: 2833
release:
  study_label: GTEx
  tissue_label: minor salivary gland
  condition_label: naive
  sample_group: minor_salivary_gland
  quant_method: ge
  quant_method_label: gene expression
  dataset_release: ''
  fetched_at_utc: '2026-05-06T15:50:33Z'
outputs:
  variants_tsv: variants.tsv
```

`<output_dir>/variants.tsv` (first three rows shown):

```
variant_id              chromosome  position_bp  allele_a  allele_b  beta        se        p          maf       molecular_trait_id  study_id
1_108774974_TCTAC_T     1           108774974    TCTAC     T         -0.119495   0.138769  0.390778   0.170139  ENSG00000134243     QTD000276
1_108775337_C_T         1           108775337    C         T          0.0777385  0.112256  0.489859   0.3125    ENSG00000134243     QTD000276
1_108775606_G_T         1           108775606    G         T         -0.166496   0.212651  0.435087   0.0729167 ENSG00000134243     QTD000276
```

`<output_dir>/report.md`:

```markdown
# eqtl-catalogue-region-fetch report

- **Dataset:** `QTD000276`
- **Source:** GTEx | minor salivary gland | quantification = gene expression
- **Region:** chr1:108,774,968-109,774,968
- **Molecular trait:** ENSG00000134243
- **Variants returned:** 2833
- **Output TSV:** variants.tsv
```

## Gotchas

1. **Use FTP tabix, not the REST API, for regional fetches.** The eQTL Catalogue v2 REST API at `/api/v2/datasets/{id}/associations` silently truncates regional fetches to one side of TSS and ignores `pos_min` / `pos_max` query parameters. This skill fetches via tabix on the canonical FTP `.all.tsv.gz`, which serves the full strand-aware cis-window correctly. Do NOT swap the fetcher to REST.

2. **Cis-window is ±1 Mb of strand-aware TSS in genomic coordinates.** The upstream pipeline computes cis-eQTLs only for variants within ±1 Mb of the gene's transcription start site. For `+` strand genes TSS = `gene.start` (lower coord). For `−` strand genes TSS = `gene.end` (higher coord). When querying a window in genomic coords that extends beyond ±1 Mb of TSS, expect zero rows on the far side. This is correct biology, not a bug.

3. **`molecular_trait_id` filter is required for `ge` eQTL files.** The harmonised `ge` `.all.tsv.gz` bundles every gene's variant rows together. Querying a chromosomal region without a gene filter returns variants for all genes in that region (potentially thousands of rows per variant). Always pass the target Ensembl gene ID. Other quant methods (`tx`, `txrev`, `exon`, `leafcutter`) have similar bundling behavior on `molecular_trait_id` (transcript / intron / exon ID).

4. **β is reported on the ALT allele.** Do NOT compare effect sizes across datasets without explicit allele harmonisation. The skill preserves `ref` / `alt` columns; downstream tools (e.g., TwoSampleMR `harmonise_data`) flip signs when alleles are swapped. Cross-dataset comparisons (eQTL β vs GWAS β at the same variant) without harmonisation can silently invert direction.

5. **Quantification methods are not interchangeable.**
   - `ge` (gene expression): gene-level, the most common eQTL definition
   - `tx` (transcript): per-isoform abundance
   - `txrev` (transcript usage): proportional, not abundance
   - `exon` (exon expression): per-exon read count
   - `leafcutter` (splice junction): splice-QTL on intron excision ratio

   These represent distinct biology. A `txrev` row is NOT a `ge` eQTL. The skill's manifest carries the raw `quant_method` code AND a human-readable label per the `CLAUDE.md` expansion rule.

## Safety

**Not for clinical decisions.** This skill returns research-grade summary statistics from public databases. Do not use the output for direct clinical decision-making, diagnosis, or treatment selection without independent validation by a qualified clinician.

**Effect estimates may not generalise across populations.** The ancestry of the source study is recorded in the dataset metadata (`sample_group`, `population` fields where present). Effect sizes from a single-ancestry study should not be assumed to apply to other ancestries without appropriate harmonisation and trans-ancestry validation.

## Agent Boundary

The skill returns harmonised summary statistics (β, SE, p-value) for variants in a chromosomal window from one (study × tissue × quant_method) dataset. The agent should:

- **Use the output as input to colocalisation, fine-mapping, or Mendelian randomisation tooling.** These are the appropriate downstream methods for inferring causal effects.
- **NOT make causal-effect claims directly from a single eQTL p-value.** A low p-value at a variant means statistical association, not causation. Causal interpretation requires colocalisation or MR analysis with proper instrumental-variable assumptions.
- **NOT cherry-pick variants by p-value alone.** Statistical inference requires the full credible set / window context.
- **NOT compare effect sizes across datasets without harmonising effect alleles.** The skill normalises within one dataset; cross-dataset comparison requires a harmonisation step (e.g., TwoSampleMR `harmonise_data`).
- **Surface tissue, quant_method, and sample size in the user-facing reply** alongside any β / p-value the agent quotes. The same variant in IAV-stimulated monocytes (Quach 2016, N=198) and in resting monocytes (BLUEPRINT, N=191) is a different biological measurement, even though the genomic position is identical. Per the user-friendly enum-expansion rule (`CLAUDE.md`), expand all three fields when reporting: `quantification = gene expression (ge); tissue = monocyte (UBERON:0000235); n_samples = 198`.
- **NOT silently swap tissues or quantification methods.** If the user asked for `monocyte / ge` and the dataset is `monocyte / txrev`, the agent must say so explicitly and ask whether to proceed.

## Citations

- Kerimov et al. (2021). *A compendium of uniformly processed human gene expression and splicing quantitative trait loci.* Nat Genet 53, 1290-1299. doi:10.1038/s41588-021-00924-w
- Per-dataset citation list at <https://www.ebi.ac.uk/eqtl/Studies/>.
