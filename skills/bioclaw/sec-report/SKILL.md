---
name: sec-report
description: SEC (size-exclusion chromatography) analysis with peak detection, oligomer classification, and publication-quality PDF report generation via Typst templates. Triggers on "SEC", "size exclusion", "chromatography", "oligomer analysis", "protein assembly", "SEC report".
tool_type: python
primary_tool: scipy, matplotlib, typst
---

# SEC Chromatography Analysis & PDF Report Generator

> **CRITICAL: This skill provides a fully automated pipeline script (`sec_pipeline.py`) that produces a publication-quality PDF with text, tables, figures, and analysis. You MUST use this pipeline. Do NOT write your own analysis script. Do NOT generate figures without accompanying text. Do NOT produce a PDF that only contains images — the pipeline generates a complete scientific report with Background, Methods, Results (including text interpretation for each construct), Discussion, and Conclusions sections.**

> **If you write your own code instead of running `sec_pipeline.py`, the report will be of significantly lower quality. The pipeline includes a professional Typst template engine that generates reports comparable to Biomni/Phylo output quality.**

Analyze SEC chromatogram data files and images, detect peaks, classify oligomeric states, and generate a publication-quality PDF report with professional styling (colored section bands, styled tables, callout boxes, page headers/footers, and full-text analysis for every section).

## When To Use This Skill

- User uploads SEC chromatogram data (CSV/TSV/Excel) and/or images
- User asks for SEC profile analysis or oligomer classification
- User wants a PDF report of SEC analysis results
- User mentions "size exclusion", "gel filtration", "SEC", "oligomer", "assembly"
- User provides a ZIP file with SEC data and plots

## Analysis Plan (Present in Chat Before Execution)

Before running the pipeline, present a brief analysis plan to the user in the chat so they can confirm or adjust parameters. This is NOT a UI button — just a chat message.

**Step 0 — Scan the data and present the plan in chat**:

After locating the user's data files, send a message like this:

---

**SEC Analysis Plan**

Found **N** data files and **M** image files.

I will run the automated SEC pipeline which:
1. Detects peaks and classifies oligomeric states for each construct
2. Generates annotated chromatograms, overlay comparison, and zone fraction charts
3. Produces a **publication-quality PDF report** (14+ pages) with full text: Background, Methods, Results (per-construct tables and interpretation), Discussion, and Conclusions

Parameters: void volume = 8.0 mL (Superdex 200 10/300 GL). Reply if you want to change anything, otherwise I'll proceed.

---

If the user does not object within ~5 seconds or says anything affirmative, proceed immediately. Do NOT wait indefinitely.

## Execution Steps (REQUIRED)

Follow these steps exactly. Do NOT skip the pipeline script.

**Step 1 — Install dependencies** (if not present):
```bash
pip install typst 2>/dev/null || pip install --user typst
pip install fpdf2 2>/dev/null || pip install --user fpdf2
```

**Step 2 — Locate the uploaded data**:
Find the user's uploaded file (ZIP, CSV, or directory) under `/workspace/group/`.

**Step 3 — Run the pipeline script**:
```bash
cd /home/node/.claude/skills/sec-report
python3 sec_pipeline.py \
  --input <path-to-uploaded-data-or-zip> \
  --output /workspace/group/sec_analysis/output
```

The script accepts either a ZIP file or a directory as `--input`. It handles extraction, parsing, peak detection, figure generation, and PDF report building automatically. The pipeline will use the Typst template engine for publication-quality output; if Typst is unavailable, it falls back to fpdf2.

By default, the pipeline now produces a **compact user-facing report**. If you ever need the older exhaustive style for debugging or appendix generation, pass:

```bash
  --report-profile full
```

**Step 4 — Send the PDF report to the user** via `send_image` MCP tool:
```
file_path: /workspace/group/sec_analysis/output/SEC_Analysis_Report.pdf
caption: "SEC Analysis Report"
```

**Step 5 — Also send the ranking figure**:
```
file_path: /workspace/group/sec_analysis/output/figures/ranking_summary.png
caption: "Construct Quality Ranking"
```

**Step 6 — Summarize key findings** in chat based on the pipeline's terminal output and the generated `analysis_summary.json`.

## Expected Inputs

| Input | Format | Required |
|-------|--------|----------|
| SEC data files | CSV, TSV, TXT, XLSX | At least one |
| SEC plot images | PNG, JPG, TIFF | Optional |
| ZIP archive | .zip containing above | Optional |

### SEC Data File Format

The parser auto-detects columns. Common formats:

```csv
Volume (mL),UV 280nm (mAU)
0.00,0.5
0.01,0.5
...
```

or tab-separated, or with headers like: `ml`, `mAU`, `elution`, `absorbance`, `A280`, `UV280`

## Expected Outputs

```
sec_analysis/output/
├── SEC_Analysis_Report.pdf          # Complete PDF report with figures
├── figures/
│   ├── <construct>_annotated.png    # Annotated chromatogram per construct
│   ├── comparison_overlay.png       # Normalized overlay (if >1 construct)
│   └── ranking_summary.png          # Quality ranking bar chart
└── analysis_summary.json            # Machine-readable results
```

## Pipeline Details

### Peak Detection
- Savitzky-Golay smoothing (window=15, order=3)
- `scipy.signal.find_peaks` with adaptive height/prominence thresholds
- FWHM via `scipy.signal.peak_widths`
- Area via trapezoidal integration

### Peak Classification (relative, no calibration assumed)
| Elution Region | Classification | Rationale |
|----------------|---------------|-----------|
| Near void volume (V0) | Aggregate | Too large for column resolution |
| V0 + 0.5–2.5 mL | Large Oligomer | High-MW assemblies (rings, etc.) |
| V0 + 2.5–4.5 mL | Oligomer | Trimers, tetramers |
| V0 + 4.5–6.5 mL | Dimer | Heterodimer range |
| V0 + 6.5–9.0 mL | Monomer | Individual chains |
| Beyond | Small Molecule | Buffer components, degradation |

**Default V0 = 8.0 mL** (typical Superdex 200 10/300 GL). Override with `--void-volume`.

### Quality Scoring (0–10)
- Penalized for: aggregation, polydispersity, broad peaks
- Rewarded for: sharp dominant peak, monodispersity
- Score ≥7: high quality | 4–7: moderate | <4: poor

### PDF Report Sections
1. Title Page
2. Executive Summary + Construct Table
3. Background (project context)
4. Methods (analysis parameters)
5. Results (per-construct: peak table + annotated figure + interpretation)
6. Comparative Analysis (overlay + ranking)
7. Discussion (oligomerization patterns, success/failure)
8. Conclusion & Recommendations (next experiments)

## Practical Heuristics

- **Chain A**: ~481 aa -> ~52.8 kDa (avg 110 Da/aa)
- **Chain B**: ~243 aa -> ~26.7 kDa
- **Heterodimer (A+B)**: ~79.5 kDa
- **Ring of N dimers**: ~79.5 × N kDa
- Sharp single peak at expected Ve -> monodisperse, well-behaved
- Broad peak or shoulder -> conformational heterogeneity or mixed states
- Peak at void volume -> aggregation (bad sign)
- Multiple peaks -> sample heterogeneity (may or may not be desired)

## Important Guardrails

- **DO NOT** assign exact molecular weights without a column calibration curve
- **DO NOT** claim definitive oligomeric state from SEC alone
- **DO** use conservative language: "apparent", "consistent with", "suggests"
- **DO** flag uncertainty explicitly
- **DO** recommend orthogonal validation (AUC, SEC-MALS, nsEM, native MS)
- Peak classifications are relative to void volume — they are approximations

## Anti-Patterns

- **Manually writing SEC analysis code instead of running `sec_pipeline.py`** — the pipeline is tested and produces standardized, reproducible outputs including PDF; manual analysis will miss features and produce inconsistent results
- Reporting exact MW from uncalibrated SEC data
- Treating SEC profile as definitive proof of assembly state
- Ignoring void volume peaks (aggregation must always be reported)
- Over-interpreting minor peaks or shoulders

## Troubleshooting

If `sec_pipeline.py` fails:
1. Check the error message — it usually indicates missing data files or unrecognized column headers
2. If the user's data has non-standard column names, pass `--void-volume` explicitly
3. If `fpdf2` is missing, install it first (Step 1)
4. If no CSV/TSV data files are found in the ZIP, the pipeline will report this — ask the user for the correct data format

Only if the pipeline cannot handle the user's specific data format after troubleshooting should you fall back to manual analysis, and in that case explain why the pipeline was insufficient.

## Related Skills

- `structural-biology` — For 3D structure analysis of assembled proteins
- `proteomics` — For mass spec validation of oligomeric states
- `bio-manuscript-pipeline` — For writing full manuscripts incorporating SEC results
- `sds-gel-review` — For complementary SDS-PAGE analysis
- `bio-figure-design` — For designing publication figures from SEC data
