---
id: clinicaltrials-landscape
name: ClinicalTrials.gov Disease Landscape Scanner
category: literature
short-description: "Query ClinicalTrials.gov API v2 to map the clinical trial landscape for any disease area by mechanism, phase, and sponsor."
detailed-description: "Programmatically query the free ClinicalTrials.gov API v2 to pull all active clinical trials for a disease area, classify by therapeutic mechanism of action, and generate competitive landscape visualizations. Supports any disease with pre-built configs for IBD (Crohn's, UC). Generic mode classifies by intervention type when no disease config exists. Supports filtering by mechanism, phase, sponsor, and status. Exports structured CSVs, publication-quality plots, and pickle objects for downstream analysis. No API key required."
starting-prompt: Show me the current clinical trial landscape for IBD
---

# ClinicalTrials.gov Disease Landscape Scanner

## When to Use This Skill

- **Map competitive landscape** across therapeutic mechanisms for any disease
- **Track specific mechanism classes** (e.g., anti-IL23, anti-TL1A, JAK inhibitors)
- **Identify sponsors** and their pipeline positions by phase
- **Phase distribution analysis** for business development diligence
- **Pipeline monitoring** for a specific sponsor's disease portfolio
- **Pre-built disease configs** available (IBD with 14 mechanism classes); generic mode for any other disease

**Do NOT use for:**
- Detailed single-trial protocol analysis
- Efficacy/safety comparisons (requires literature review skill)

---

## Installation

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|-------------|
| pandas | ≥1.3 | BSD-3 | ✅ Permitted | `pip install pandas` |
| requests | ≥2.25 | Apache-2.0 | ✅ Permitted | `pip install requests` |
| numpy | ≥1.20 | BSD-3 | ✅ Permitted | `pip install numpy` |
| plotnine | ≥0.10 | MIT | ✅ Permitted | `pip install plotnine` |
| plotnine-prism | ≥0.3 | MIT | ✅ Permitted | `pip install plotnine-prism` |
| seaborn | ≥0.11 | BSD-3 | ✅ Permitted | `pip install seaborn` |
| matplotlib | ≥3.4 | PSF | ✅ Permitted | `pip install matplotlib` |
| reportlab | ≥3.6 | BSD | ✅ Permitted | `pip install reportlab` |
| pyyaml | ≥5.0 | MIT | ✅ Permitted | `pip install pyyaml` |

```bash
pip install pandas requests numpy plotnine plotnine-prism seaborn matplotlib reportlab pyyaml
```

**System requirements:** Internet connection for ClinicalTrials.gov API calls.

---

## Inputs

**Required:**
- **Disease / condition terms** — list of conditions to search ClinicalTrials.gov

**Optional:**
- **Disease config** — pre-built config ID (e.g., `"ibd"`) for mechanism taxonomy, or `None` for generic
- **Mechanism filter** — e.g., "Anti-IL-23 (p19)", "Anti-TL1A", "JAK Inhibitor"
- **Sponsor filter** — e.g., "Takeda", "AbbVie"
- **Status filter** — Default: all active (Recruiting + Active not recruiting + Not yet recruiting)
- **Phase filter** — Phase 1, 2, 3, 4

---

## Outputs

**Visualizations (PNG + SVG):**
- `landscape_overview.png/.svg` — 6-panel landscape figure (300 DPI)
  - Mechanism × Phase heatmap, top sponsors, phase stacked bars, mechanism counts, timeline, sponsor type
- `landscape_supplementary.png/.svg` — 4-panel supplementary figure
  - Top 15 countries, study design by phase, enrollment distribution, phase transition funnel

**Results (CSV):**
- `trials_all.csv` — All trials with 46 columns (mechanism, phase, sponsor, geography, study design, arms, endpoints, eligibility, regulatory)
- `trials_by_mechanism.csv` — Mechanism × phase cross-tabulation
- `trials_by_sponsor.csv` — Sponsor summary with trial counts
- `trials_filtered.csv` — Filtered subset (if mechanism/sponsor filter applied)

**Reports:**
- `landscape_report.pdf` — Publication-quality PDF with 24 sections: executive summary, mechanism deep-dives, geographic landscape, study design, phase transition funnel, endpoint comparison, combination therapies, biosimilar assessment, whitespace analysis, and more
- `landscape_report.md` — Markdown version with identical 24-section structure

**Analysis objects (Pickle):**
- `analysis_object.pkl` — Complete landscape for downstream use
  - Load with: `import pickle; obj = pickle.load(open('analysis_object.pkl', 'rb'))`
  - Contains: trials_df (46 columns), mechanism/phase/sponsor distributions, geographic stats, design stats, parameters

---

## Clarification Questions

1. **Data Source** (ASK THIS FIRST):
   - This skill queries the ClinicalTrials.gov API v2 directly (free, no key needed).
   - **Use live API data?** (recommended, ~30 seconds)
   - **Or use cached demo data?** Pre-loaded IBD landscape snapshot for quick demo

2. **Disease Area:**
   - Which disease area to analyze?
     - a) IBD (Inflammatory Bowel Disease) — pre-built config with 14 mechanism classes
     - b) Oncology (generic intervention-type classification)
     - c) Autoimmune / Rheumatology (generic classification)
     - d) Other (specify disease and condition terms)

3. **Scope** *(if IBD selected)*:
   - Which conditions?
     - a) All IBD (Crohn's, UC, and IBD unspecified) — recommended
     - b) Crohn's Disease only
     - c) Ulcerative Colitis only
   - *(If other disease)* — Provide list of condition search terms

4. **Focus:**
   - Any mechanism or sponsor to highlight?
     - *(IBD)* a) Anti-IL-23 — recommended for demo | b) Anti-TL1A | c) All mechanisms
     - *(Other)* Specify or skip highlighting

---

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/clinicaltrials-landscape'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**Step 1 — Load config and query ClinicalTrials.gov:**
```python

from disease_config import load_disease_config, get_default_conditions
from query_clinicaltrials import query_trials

# Load disease config (use "ibd" for IBD, or None for generic)
config = load_disease_config("ibd")

# Get conditions from config or specify manually
conditions = get_default_conditions(config) or ["Crohn's Disease", "Ulcerative Colitis", "Inflammatory Bowel Disease"]

raw_trials = query_trials(
    conditions=conditions,
    statuses=["RECRUITING", "ACTIVE_NOT_RECRUITING", "ENROLLING_BY_INVITATION", "NOT_YET_RECRUITING"],
)
```
**✅ VERIFICATION:** `"✓ Retrieved {N} trials from ClinicalTrials.gov"`

**Step 2 — Classify and compile:**
```python
from classify_mechanisms import classify_all
from compile_trials import compile_trials

classified = classify_all(raw_trials, config=config)
trials_df = compile_trials(classified, output_dir="landscape_results")
```
**DO NOT write inline classification code. The script loads mechanism taxonomy from config.**

**✅ VERIFICATION:** `"✓ Trial data compiled successfully!"`

**Step 3 — Generate visualizations:**
```python
from generate_landscape_plots import generate_landscape_plots

generate_landscape_plots(
    trials_df,
    output_dir="landscape_results",
    highlight_mechanism="Anti-IL-23 (p19)",  # or None for no highlight
    highlight_sponsor=None,                   # or "Takeda" to highlight
    config=config,
)
```
🚨 **DO NOT write inline plotting code. The script handles all 6 panels + PNG/SVG export.** 🚨

**✅ VERIFICATION:** `"✓ All landscape visualizations generated successfully!"`

**Step 4 — Export results:**
```python
from export_all import export_all

export_all(
    trials_df,
    parameters={
        "conditions": conditions,
        "statuses": ["RECRUITING", "ACTIVE_NOT_RECRUITING", "ENROLLING_BY_INVITATION", "NOT_YET_RECRUITING"],
        "highlight_mechanism": "Anti-IL-23 (p19)",
    },
    output_dir="landscape_results",
    config=config,
)
```
**DO NOT write custom export code. Use export_all().**

**✅ VERIFICATION:** `"=== Export Complete ==="`

---

## ⚠️ CRITICAL — DO NOT:

- ❌ **Write inline classification code** → **STOP: Use `classify_all()` from scripts**
- ❌ **Write inline plotting code (ggplot, plt, sns)** → **STOP: Use `generate_landscape_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to scrape ClinicalTrials.gov HTML** → **Use the API via `query_trials()`**

---

## ⚠️ IF SCRIPTS FAIL — Script Failure Hierarchy:

1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

---

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **ConnectionError / Timeout** | ClinicalTrials.gov unreachable | Check internet connection; retry after 30 seconds |
| **HTTP 429 Too Many Requests** | Rate limit exceeded | Increase `RATE_LIMIT_DELAY` in query_clinicaltrials.py |
| **ModuleNotFoundError: plotnine** | Missing visualization package | `pip install plotnine plotnine-prism` |
| **Empty results (0 trials)** | Overly restrictive filters | Broaden condition/status/phase filters |
| **Many "Unclassified" mechanisms** | No disease config or new drugs | Use a disease config (e.g., `"ibd"`) or update `disease_configs/*.yaml` |
| **SVG export failed** | Missing SVG backend | Normal — PNG is always generated as fallback |
| **Sponsor name variants** | Same company, different names | Update `SPONSOR_NORMALIZATION` in compile_trials.py |
| **ModuleNotFoundError: yaml** | Missing pyyaml | `pip install pyyaml` |

---

## Interpretation Guidelines

- **Mechanism classification** is based on intervention names and descriptions — some trials with vague descriptions (e.g., "Study Drug") will be classified as "Other Biologic" or "Unclassified"
- **Phase 2/3** indicates a combined Phase 2/3 study design
- **Sponsor normalization** groups subsidiaries under parent company (e.g., Millennium → Takeda)
- **Industry vs Academic** based on ClinicalTrials.gov `leadSponsor.class` field
- The landscape reflects **registered trials**, not all pipeline programs (pre-IND programs won't appear)
- **Disease configs** provide curated mechanism taxonomies; without config, classification uses generic intervention types

---

## Suggested Next Steps

1. **Deep-dive a mechanism** — Use `literature-preclinical` to review mechanism biology
2. **Track a sponsor's full pipeline** — Use `development-landscape` for broader pipeline view
3. **Biomarker analysis** — Use `lasso-biomarker-panel` to identify response biomarkers from trial data
4. **Export to presentation** — Use landscape_report.md and plots for stakeholder review

---

## Related Skills

- `development-landscape` — Broader, multi-source pipeline landscape for any target
- `literature-preclinical` — Literature review for mechanism biology
- `lasso-biomarker-panel` — Biomarker discovery from expression data

---

## References

- ClinicalTrials.gov API v2: https://clinicaltrials.gov/data-api/api
- ClinicalTrials.gov: https://clinicaltrials.gov/
- See `references/api-parameters.md` for full API parameter reference
- See `references/mechanisms.md` for mechanism taxonomy details
- See `references/output-schema.md` for output column definitions
