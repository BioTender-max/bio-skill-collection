---
name: report-template
description: Publication-quality PDF report generation using Typst templates. Produces professional scientific reports with colored section bands, styled tables, figure captions, callout boxes, and page headers/footers.
---

# Report Template System

Generate publication-quality PDF reports using the BioClaw Typst template engine.

## Quick Start

```python
import sys
sys.path.insert(0, "/home/node/.claude/skills/report-template")
from report_builder import (
    ReportBuilder, typst_table, typst_callout, typst_image,
    typst_metadata_block, typst_metric_cards, typst_pagebreak,
    typst_text, typst_list, typst_bold, typst_italic,
)

report = ReportBuilder(
    title="My Analysis Report",
    subtitle="Project XYZ",
    author="BioClaw",
)

# Add sections with Typst markup
report.add_section("Background", "Description of the project...")

# Add tables
table = typst_table(
    ["Sample", "Value", "Status"],
    [["A", "92.3", "Pass"], ["B", "87.1", "Pass"]],
    caption="Summary of results",
)
report.add_section("Results", table)

# Compile to PDF
report.compile("output/report.pdf")
```

## Available Components

### Tables
```python
typst_table(headers, rows, caption=None)
```

### Callout Boxes
```python
typst_callout(text, title="Note", kind="note")
# kind: "note" (blue), "warning" (yellow), "success" (green), "danger" (red)
```

### Figures
```python
typst_image(path, caption=None, width="100%")
# path is relative to the output directory
```

### Metadata Blocks
```python
typst_metadata_block([("Key", "Value"), ("Date", "2026-04-15")])
```

### Metric Cards
```python
typst_metric_cards([
    {"label": "Samples", "value": "6"},
    {"label": "Quality", "value": "A+"},
])
```

### Text Formatting
```python
typst_text("Plain paragraph")
typst_bold("Bold text")
typst_italic("Italic text")
typst_list(["Item 1", "Item 2"])
typst_enum(["Step 1", "Step 2"])
typst_pagebreak()
```

## Template Features

- Dark navy section heading bands with white text
- Teal sub-heading accents
- Professional page headers and footers with page numbers
- Alternating-row table styling
- Four callout box types (note, warning, success, danger)
- Figure numbering and italic captions
- Key-value metadata blocks
- Metric card rows

## Requirements

- Python package: `typst` (`pip install typst`)
- No system dependencies required
