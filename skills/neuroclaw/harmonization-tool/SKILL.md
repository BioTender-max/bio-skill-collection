---
name: harmonization-tool
description: "Use this skill whenever the user wants to remove site/scanner/batch effects from neuroimaging features before running downstream models, run mega-analysis across multiple datasets, or evaluate models with leave-site-out / site-stratified protocols. Triggers include: 'harmonize', 'ComBat', 'CovBat', 'site effect', 'scanner effect', 'batch effect', 'leave-site-out', 'mega-analysis', 'multi-site', 'cross-site', 'neuroHarmonize'. This is a horizontal cross-cutting layer between dataset skills and model skills."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
layer: subagent
skill_type: tool
dependencies:
  - claw-shell
---
# Harmonization Tool Skill (Cross-Site Feature Alignment Layer)

## Overview
`harmonization-tool` is the NeuroClaw cross-cutting layer that sits **between** dataset skills (ABIDE, ADHD-200, ABCD, HCP, UKB, ...) and model skills (BrainGNN, BNT, IBGNN, LGGNN, BrainNetCNN, FM-APP, SVM, SpaceNet, ...).

Its job: take subject-level features extracted by dataset skills and remove **technical / batch variance** introduced by site, scanner, field strength, sequence, or dataset, while **preserving biological variance** (age, sex, diagnosis, ...).

This is the prerequisite for any honest **mega-analysis** that pools individual-participant data (IPD) across sites or datasets.

This skill follows NeuroClaw hierarchy:
- Defines **WHAT to do**, not low-level implementation details.
- Does **not** execute direct shell commands itself.
- Delegates all execution via `claw-shell`.

**Research use only.**

---

## When to Use This Skill

Trigger this skill when the user asks for any of:
- "harmonize features across sites / scanners / datasets"
- "ComBat / ComBat-GAM / CovBat / neuroHarmonize / neuroCombat"
- "remove site effect / scanner effect / batch effect"
- "mega-analysis on ABIDE / ADHD-200 / ABCD / multi-site"
- "leave-site-out cross-validation"
- "site-stratified split"
- "cross-site generalization"
- "IPD pooling across cohorts"

Do **NOT** trigger for:
- Single-site, single-scanner studies (no batch variable exists)
- Pure preprocessing requests (delegate to `fmri-skill` / `smri-skill`)
- Model training itself (delegate to model skills via `run_models`)

---

## Position in the NeuroClaw Pipeline

```
[dataset-skill]  →  feature matrix + meta (site, scanner, age, sex, dx)
                                |
                                v
                    [harmonization-tool]   ← this skill
                                |
                                v
              harmonized feature matrix + same meta
                                |
                                v
                   [model-skill via run_models]
```

The **model code itself does not change**. Models read harmonized features from disk just like they read raw features. A `run_models --harmonize <method>` flag (added later in `run_models`) orchestrates the insertion.

---

## Core Workflow (Never Bypassed)

1. **Resolve inputs**: confirm a feature matrix and a metadata table are available, or coordinate with the relevant dataset skill to produce them.
2. **Validate IO schema** via `scripts/io_schema.py` — feature shape, required meta columns (`subject_id`, `site`, `dataset`, plus protected covariates `age`, `sex`, `dx` if applicable).
3. **Diagnose site effect** before harmonization with `scripts/diagnostics.py` — quantify how much variance is explained by `site` per feature; this is the baseline.
4. **Choose method** via `scripts/harmonize.py --method {none,site-covar,combat,combat-gam,covbat}` based on:
   - feature granularity (ROI scalar vs connectome vs voxel)
   - covariate structure (linear vs non-linear age effect)
   - whether second-order moments matter (FC connectivity → CovBat)
5. **Choose evaluation protocol** via `scripts/splitters/`:
   - `leave_site_out.py` — strictest, evaluates cross-site generalization
   - `site_stratified.py` — 80/10/10 with per-site stratification (compatible with the project default 80/10/10 protocol)
6. **Run harmonization**, persist harmonized features + manifest.
7. **Re-diagnose** site effect after harmonization. Report before/after site R² per feature.
8. **Hand off** harmonized features to the requested model skill via `run_models`.

Do not skip steps 3 and 7 — they are the only honest way to know whether harmonization actually worked.

---

## IO Contract (Standard Across All Dataset Skills)

All dataset skills feeding into this layer must produce, or be wrappable to produce, the following.

**Features** (one of):
- `(N, F)` ndarray — ROI-level scalars (e.g. cortical thickness, ALFF, ReHo)
- `(N, R, R)` ndarray — connectome / FC matrix
- `(N, V)` sparse — voxel-level (rare; usually delegate to dataset-specific compression first)

**Metadata** (`pandas.DataFrame`, one row per subject):

| column | required | description |
|---|---|---|
| `subject_id` | yes | unique within the cohort |
| `dataset` | yes | e.g. `ABIDE-I`, `ADHD-200`, `ABCD` |
| `site` | yes | site / scanner identifier; the **batch** variable to remove |
| `scanner` | optional | scanner make / model |
| `field_strength` | optional | 1.5T / 3T / 7T |
| `age` | recommended | protected biological covariate |
| `sex` | recommended | protected biological covariate |
| `dx` | task-dependent | protected biological covariate (case/control etc.) |

**Convention**: any column listed in `--protected` is preserved (its variance is not removed). The column passed to `--batch` (default `site`) is what gets harmonized away.

---

## Methods Catalog

| Method | When to use | Notes |
|---|---|---|
| `none` | Single-site or sanity baseline | No-op, used for A/B comparison |
| `site-covar` | Quick first pass | Linear regression, `site` as covariate, residualize |
| `combat` | ROI-level features, cohort with similar age range | Empirical Bayes; the field's de facto standard |
| `combat-gam` | Wide age range (kids + adults, lifespan) | ComBat with spline on age — avoids over-aggressive linear adjustment |
| `covbat` | Connectome / FC features where second-order structure matters | Harmonizes mean, variance, and covariance |

Default recommendation: **`combat-gam`** when age range > 20 years, **`combat`** otherwise.

---

## Splitters

Two evaluation protocols are bundled. Use them **in addition to** model skills' own splitting logic, not instead of, when site effects are a concern.

- **leave-site-out** (`splitters/leave_site_out.py`):
  Hold out one site at a time as test set, train on the rest. Strictest cross-site generalization. Use for headline mega-analysis claims.

- **site-stratified 80/10/10** (`splitters/site_stratified.py`):
  Default project split protocol (per [feedback-cv-protocol](memory/feedback-cv-protocol.md)) but stratified per site, so each site appears in train/val/test in proportion. Compatible with all existing model skills.

**Important**: the harmonization fit must be done on the train split only, then **applied** to val/test. Fitting harmonization on the full dataset before splitting leaks information. The wrappers in `scripts/adapters/` enforce this via separate `fit` and `transform` entry points.

---

## Outputs

For each harmonization run, the skill writes:

```
<out_dir>/
├── harmonized_features.npy        # same shape as input
├── meta.csv                       # passthrough metadata
├── manifest.json                  # method, params, protected, batch, train indices, run_id, timestamp
├── site_effect_before.csv         # per-feature site R² before
├── site_effect_after.csv          # per-feature site R² after
└── diagnostics_report.html        # before/after summary plots (optional)
```

The `manifest.json` is the source of truth for downstream KG provenance — see KG integration below.

---

## KG Integration (Provenance, not Pollution)

Harmonization metadata enters the NeuroClaw KG via a **three-layer separation** that keeps the scientific main graph clean:

- **Layer 1 (main scientific KG)**: every `Claim` derived from harmonized features carries:
  - `harmonization_method` (e.g. `combat-gam`)
  - `evaluation_protocol` (e.g. `leave-site-out`)
  - `dataset_scope` (list of cohorts pooled)
  - **No** raw `site` / `scanner` nodes added unless the Claim is explicitly site-conditional.
- **Layer 2 (acquisition context, side-graph)**: `Site`, `Scanner`, `Sequence` nodes live here, linked from Claims only when the Claim is conditional on them.
- **Layer 3 (provenance manifest, file-level)**: full `manifest.json` per run, addressed by `run_id`. Not loaded into the graph; referenced by URI.

**Default convention**: a Claim **without** `harmonization_method=raw` is assumed to be derived from harmonized features. Raw-feature Claims are explicitly tagged.

This contract preserves the four KG differentiators (dual-source, Claim-as-first-class, KG iteration, evidence-weighted edges) and turns "cross-site robustness" into a first-class signal: Claims reproducible across more sites get higher evidence weight.

---

## Pilot: ABIDE × BrainGNN (Phase 1)

The first end-to-end exercise compares three protocols on ABIDE I+II for autism classification with BrainGNN:

| Run | Harmonization | Split | Purpose |
|---|---|---|---|
| (a) | `none` | random 80/10/10 | Optimistic baseline (likely site-leaked) |
| (b) | `none` | site-stratified 80/10/10 | Honest within-site baseline (no harmonization) |
| (c) | `combat` / `combat-gam` | site-stratified 80/10/10 | Test whether harmonization keeps signal while removing site |

Read the diagnostic gap (a) − (b) as the **site-leakage budget**, and (c) − (b) as the **harmonization gain**.

ABIDE features are not extracted in this repo yet by `abide-skill`'s end-to-end
pipeline. The pilot script `scripts/pilot_abide_style.py` instead fetches
the ABIDE I CPAC ROI time series via `scripts/fetch_abide_rois_robust.py`
(2 GB, 7 atlases, idempotent) and builds connectomes via Pearson correlation:

  - `--source synthetic` (5 sites, controlled signal — pipeline validation)
  - `--source adhd200` (real cohort, in-repo proxy)
  - `--source abide --abide-atlas {rois_aal,rois_cc200,rois_cc400,...}`

### Real-data result: ABIDE I, aal_116, N=639, 10 sites, 3 seeds, plain ComBat

| Metric | (a) random | (b) site-strat no harm | (c) combat + site-strat |
|---|---|---|---|
| test acc (mean) | 0.626 | 0.682 | 0.688 |
| test AUC (mean) | 0.657 | 0.749 | 0.750 |
| site R² (per-edge mean) | 0.070 | 0.070 | **0.007** |

- **Site-leakage budget (a)−(b): −5.7pp ± 3.3pp** (negative!). ABIDE has near-balanced dx within every site, so random splitting does not hand the model a site→dx shortcut. The reverse appears: site-stratified actually helps generalization because train sees every site's covariate distribution.
- **Harmonization gain (c)−(b): +0.5pp ± 2.7pp**, AUC +0.001 ± 0.013 — neutral. ComBat strips site information cleanly (R² 0.070 → 0.007) without damaging dx signal.
- **AUC ≈ 0.75 with LR + aal_116 + plain ComBat** is in the same band as published BrainGNN / IBGNN / BNT numbers on ABIDE I. The bottleneck on this dataset is signal, not model.

### Real-data result: ADHD-200, aal_116, N=669, 6 sites, 3 seeds, plain ComBat

| Metric | (a) random | (b) site-strat no harm | (c) combat + site-strat |
|---|---|---|---|
| test acc (mean) | 0.665 | 0.542 | 0.527 |
| site R² (per-edge mean) | 0.090 | 0.090 | **0.006** |

- **Site-leakage budget (a)−(b): +11.5pp ± 1.8pp** — large. ADHD-200 has severe site × dx coupling (e.g. WashU is 0% ADHD, NYU is 55% ADHD), so random splitting offers a free shortcut.
- **Harmonization gain (c)−(b): −1.5pp ± 2.1pp** — neutral, with a tilt toward negative because removing site also removes the dx variance that lived in the site channel.
- ComBat with `dx` in `protected` keeps as much dx variance as the data permit; it cannot recover what is statistically confounded.

### Two cohorts, one lesson

The ADHD-200 case is what most "site effect" diagrams in the literature look like:
random splits hide a +11.5pp shortcut. The ABIDE case is the inverse: site-stratified
splits **help**, and harmonization is roughly free. You cannot tell which regime your
cohort is in without running the diagnostic.

That is the value harmonization-tool delivers — not "+X accuracy", but a reproducible
audit that tells you whether your benchmark is honest. Reproduce with:

```bash
python skills/harmonization-tool/scripts/pilot_abide_style.py --source abide   --abide-atlas rois_aal --method combat --seeds 42 7 123
python skills/harmonization-tool/scripts/pilot_abide_style.py --source adhd200 --method combat --seeds 42 7 123
```

Outputs land in `runs/harmonization_pilot_{abide,adhd200}/`.

---

## Phase 2 Rollout

Once the pilot validates the contract, harmonization becomes a `run_models` flag and applies to every model skill without code changes:

- Graph models: BrainGNN, IBGNN, LGGNN, BNT, ComBrainTF, Hierarchical
- Voxel / classical: SVM, SpaceNet, K-means, Hierarchical clustering
- Foundation: FM-APP, NeuroStorm

Dataset rollout order: ABIDE I+II → ADHD-200 → ABCD → HCP-EP → UCLA-CNP → multi-cohort mega-analysis.

---

## Hard Rules

1. **Never** fit harmonization on the full dataset before splitting — fit on train, transform val/test.
2. **Never** harmonize away a protected covariate. If `dx` is the prediction target, `dx` must be in `--protected`.
3. **Always** report site R² before and after. A run without diagnostics is not deliverable.
4. **Never** bypass the IO contract. New dataset skills must be wrappable to the standard schema first.
5. **Always** persist the `manifest.json` — Layer 3 provenance is the audit trail.

---

## Scripts

- `scripts/io_schema.py` — IO contract validation
- `scripts/harmonize.py` — CLI dispatcher: `--method`, `--batch`, `--protected`, `--features`, `--meta`, `--out`
- `scripts/adapters/neuroharmonize_wrapper.py` — neuroHarmonize (ComBat / ComBat-GAM)
- `scripts/adapters/neurocombat_wrapper.py` — neuroCombat (raw ComBat reference)
- `scripts/adapters/covbat_wrapper.py` — CovBat for connectome features
- `scripts/splitters/leave_site_out.py` — LOSO splitter
- `scripts/splitters/site_stratified.py` — site-stratified 80/10/10 splitter
- `scripts/diagnostics.py` — site-effect quantification (per-feature R² of `site` vs feature, before/after)
- `scripts/loaders/adhd200_real.py` — ADHD-200 real-cohort loader (aal_116, 669 subjects across 6 sites)
- `scripts/loaders/abide_real.py` — ABIDE I real-cohort loader (any of 7 CPAC atlases, 639 subjects across 10 sites at aal_116)
- `scripts/fetch_abide_rois_robust.py` — concurrent + retry-safe ABIDE I CPAC ROI downloader; fills `data/abide/ABIDE_pcp/cpac/filt_noglobal/<atlas>/`
- `scripts/pilot_abide_style.py` — three-way pilot driver, supports `--source synthetic|adhd200|abide`
