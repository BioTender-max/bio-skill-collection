---
id: literature-preclinical
name: Preclinical Literature Extraction
category: literature
short-description: "Search for preclinical studies on a target in a disease and extract structured in vitro and in vivo experiment details from each paper."
detailed-description: "Search Consensus (consensus.app) for preclinical (non-clinical) studies on a specific molecular target in a disease context. For each paper, parse the abstract to extract structured details about in vitro experiments (cell lines, assays, findings) and in vivo experiments (animal models, dosing, endpoints, findings). Synthesize results across papers to identify the most common model systems, assays, and concordance between in vitro and in vivo findings."
starting-prompt: Search for recent preclinical studies on CDK4/6 inhibition in triple-negative breast cancer and extract the in vitro and in vivo experiments from each paper.
---

# Preclinical Literature Extraction

Search Consensus (consensus.app) for preclinical studies on a molecular target in a disease, then extract structured in vitro and in vivo experiment details from each paper.

---

## When to Use This Skill

Use this skill when you need to:
- **Survey preclinical evidence** for a drug target in a disease indication
- **Extract in vitro experiments** — cell lines, assays (viability, migration, apoptosis, etc.), key findings
- **Extract in vivo experiments** — animal models (xenograft, PDX, syngeneic, transgenic), endpoints, key findings
- **Identify common model systems** — which cell lines and animal models are most used for your target
- **Compare in vitro vs in vivo concordance** — papers reporting both experiment types
- **Support IND-enabling decisions** — compile preclinical evidence landscape

**Do NOT use this skill for:**
- ❌ Clinical trial literature (use `literature-review` instead)
- ❌ Automated full-text parsing (agent reads full text for top papers after abstract extraction)
- ❌ Meta-analysis or statistical pooling of preclinical results
- ❌ Citation management / formatting only

---

## Installation

### Python (Search + Extraction)
```bash
pip install requests pandas
```

### PDF Report Generation (Optional)
```bash
pip install reportlab
```

### R (Visualization)
```r
install.packages(c("ggplot2", "ggprism", "dplyr", "tidyr", "patchwork"))
# Optional for high-quality SVG:
install.packages("svglite")
```

### Package Licenses

| Software | Version | License | Commercial Use | Installation |
|----------|---------|---------|----------------|--------------|
| requests | ≥2.25 | Apache 2.0 | ✅ Permitted | `pip install requests` |
| pandas | ≥1.3 | BSD | ✅ Permitted | `pip install pandas` |
| reportlab | ≥3.6 | BSD | ✅ Permitted | `pip install reportlab` |
| ggplot2 | ≥3.4 | MIT | ✅ Permitted | `install.packages("ggplot2")` |
| ggprism | ≥1.0.3 | GPL (≥3) | ✅ Permitted | `install.packages("ggprism")` |
| dplyr | ≥1.1 | MIT | ✅ Permitted | `install.packages("dplyr")` |
| tidyr | ≥1.3 | MIT | ✅ Permitted | `install.packages("tidyr")` |
| patchwork | ≥1.1 | MIT | ✅ Permitted | `install.packages("patchwork")` |

**API Requirements:**
- **Consensus API:** Requires `CONSENSUS_API_KEY` environment variable. Get a key at https://consensus.app/home/api/
  ```bash
  export CONSENSUS_API_KEY="your_key_here"
  ```

---

## Inputs

### Required Inputs
1. **Target** — Molecular target name (e.g., `"CDK4/6"`, `"BRAF"`, `"PD-L1"`, `"HER2"`)
2. **Disease** — Disease context (e.g., `"breast cancer"`, `"melanoma"`, `"NSCLC"`)

### Optional Inputs
- **max_results** — Maximum papers to retrieve (default: 50, API max per query: 50)
- **years** — Search last N years (default: 5)

---

## Outputs

### Generated Files

| File | Description |
|------|-------------|
| `preclinical_search_results.csv` | All papers with metadata (PMID, DOI, title, abstract, etc.) |
| `experiment_extraction.csv` | Per-paper extraction: experiment type, cell lines, assays, models, endpoints, findings |
| `preclinical_synthesis_report.md` | Structured markdown report with narrative synthesis, frequency tables, hyperlinked references, and full-text insights |
| `preclinical_synthesis_report.pdf` | Publication-quality PDF with Introduction, Methods, Results, Conclusions |
| `preclinical_plots.png` | 4-panel visualization (300 DPI) |
| `preclinical_plots.svg` | Vector format (with graceful fallback) |
| `analysis_object.pkl` | Complete analysis object for downstream use |

**Analysis object (pickle):**
- `analysis_object.pkl` — Contains search results, experiments, synthesis
  - Load with: `import pickle; obj = pickle.load(open('analysis_object.pkl', 'rb'))`

---

## Clarification Questions

🚨 **ALWAYS ask Question 1 FIRST.**

### 1. **Target and Disease** (ASK THIS FIRST):
   - Do you have a specific **target** and **disease** to search?
     - If so: provide the target name and disease
   - **Or use an example search to try the skill?**
     - a) CDK4/6 in triple-negative breast cancer
     - b) KRAS in pancreatic cancer
     - c) PD-L1 in non-small cell lung cancer
     - d) BRAF in melanoma

> 🚨 **IF EXAMPLE SEARCH SELECTED:** All parameters are pre-defined (last 5 years, 50 results). **DO NOT ask questions 2-3.** Proceed directly to Step 1.

**Questions 2-3 are ONLY for users providing their own target/disease:**

### 2. **Search Parameters:**
   - Date range? (default: last 5 years)
     - a) Last 3 years
     - b) Last 5 years (default)
     - c) Last 10 years

### 3. **Results Scope:**
   - Maximum papers to retrieve?
     - a) 20 (quick scan)
     - b) 50 (standard, default)

### 4. **Full-Text Depth:**
   - How many papers should be reviewed in full text?
     - a) Up to 30 papers (default — deeper analysis, takes longer)
     - b) Up to 10 papers (faster, focuses on highest-impact papers)
     - c) All available open-access papers (comprehensive, slowest)

---

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/literature-preclinical'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline Consensus/PubMed API code** → **STOP: Use `search_preclinical()`**
- ❌ **Write inline extraction code** → **STOP: Use `extract_all_experiments()`**
- ❌ **Write inline plotting code (ggplot, ggsave, etc.)** → **STOP: Use `generate_all_plots()`**
- ❌ **Write custom export code** → **STOP: Use `export_all()`**
- ❌ **Try to install svglite** → script handles SVG fallback automatically

**Steps 1-4 are automated (scripts). Step 5 is agent-guided (manual full-text reading).**

**Step 1 — Search for preclinical studies:**
```python
import sys

from preclinical_search import search_preclinical

results = search_preclinical(
    target="CDK4/6",
    disease="triple-negative breast cancer",
    max_results=50,
    years=5,
    output_dir="preclinical_results"
)
```
**DO NOT write inline Consensus API code. Use the script.**

**Step 2 — Extract in vitro and in vivo experiments:**
```python
from extract_experiments import extract_all_experiments

experiments = extract_all_experiments(results, output_dir="preclinical_results")
```
🚨 **DO NOT write inline extraction code. The script handles all keyword matching.** 🚨

**Step 3 — Generate visualizations:**
```r
source("scripts/generate_plots.R")
generate_all_plots(input_dir = "preclinical_results", output_dir = "preclinical_results")
```
🚨 **DO NOT write inline plotting code (ggplot, ggsave, etc.). Just source the script.** 🚨

**The script handles PNG + SVG export with graceful fallback for SVG dependencies.**

**Step 4 — Synthesize and export results:**
```python
from preclinical_synthesis import synthesize_preclinical, export_all

synthesis = synthesize_preclinical(results, experiments, target="CDK4/6")
export_all(results, experiments, synthesis,
           target="CDK4/6", disease="triple-negative breast cancer",
           output_dir="preclinical_results")
```
**DO NOT write custom export code. Use export_all().**

**Step 5 — Full-text deep dive (top papers):**

Read the **[full-text enrichment guide](references/full-text-enrichment-guide.md)** and follow its instructions to read full text for the top papers (default: up to 30). Replace the `## Full-Text Insights` placeholder in the report with per-paper findings.

🚨 **DO NOT skip this step. Select papers based on the criteria in the guide.** 🚨

**✅ VERIFICATION — You should see:**
- After Step 1: `"✓ Literature search completed successfully!"`
- After Step 2: `"✓ Experiment extraction completed successfully!"`
- After Step 3: `"✓ All plots generated successfully!"`
- After Step 4: `"=== Export Complete ==="`
- After Step 5: Report contains `## Full-Text Insights` section with per-paper details

**❌ IF YOU DON'T SEE THESE:** You wrote inline code. Stop and use the scripts.

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **"CONSENSUS_API_KEY not set"** | API key missing | `export CONSENSUS_API_KEY='your_key_here'` — get key at https://consensus.app/home/api/ |
| **"Invalid or expired API key"** | Bad API key | Verify your CONSENSUS_API_KEY is valid and not expired |
| **"HTTP 429: Rate limited"** | Consensus rate limit exceeded | Script handles retries with exponential backoff. Wait and retry if persists |
| **"No results found"** | Query too specific or target name mismatch | Try alternative target names (e.g., "CDK4" vs "CDK4/6" vs "cyclin-dependent kinase 4") |
| **"experiment_extraction.csv not found"** | Step 2 not run before Step 3 | Run Steps 1-2 (Python) before Step 3 (R) |
| **"Most papers classified as unclassified"** | Abstracts don't contain expected keywords | Expected for some targets — check if papers use different terminology |
| **"Missing R package: ggprism"** | R packages not installed | `install.packages(c("ggplot2", "ggprism", "dplyr", "tidyr", "patchwork"))` |
| **SVG export failed** | Missing svglite dependency | Normal — script falls back to base R svg() device. PNG always generated |
| **"PDF skipped"** | Missing reportlab package | `pip install reportlab`. Markdown report always generated regardless |

⚠️ **IF SCRIPTS FAIL — Script Failure Hierarchy:**
1. **Fix and Retry (90%)** — Install missing package, re-run script
2. **Modify Script (5%)** — Edit the script file itself, document changes
3. **Use as Reference (4%)** — Read script, adapt approach, cite source
4. **Write from Scratch (1%)** — Only if genuinely impossible, explain why

**NEVER skip directly to writing inline code without trying the script first.**

---

## Suggested Next Steps

After extracting preclinical experiments:

1. **Deep dive** — Read full-text papers for the most relevant "both" papers (in vitro + in vivo)
2. **Expand search** — Try alternative target names or broader disease terms
3. **Functional enrichment** — Use `functional-enrichment-from-degs` on genes from relevant pathways
4. **Literature review** — Use `literature-review` for broader context including clinical studies
5. **Target gene analysis** — Use `chip-atlas-target-genes` to identify transcription factor targets

---

## Related Skills

### Upstream Skills
- **literature-review** — General literature search and synthesis (broader scope)

### Downstream Skills
- **functional-enrichment-from-degs** — Pathway analysis of target-related genes
- **chip-atlas-target-genes** — Identify TF binding targets for your target gene
- **chip-atlas-peak-enrichment** — Check ChIP-seq enrichment near your target

---

## References

### Search Strategy
- **[references/preclinical-search-guide.md]** — Consensus API search strategies, query construction, API parameters

### Extraction Methods
- **[references/experiment-extraction-guide.md]** — Keyword-based extraction approach, dictionaries, limitations

### External Documentation
- **Consensus API:** https://consensus.app/home/api/
