<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Clinical Note Summarization

**ID:** `biomedical.clinical.note_summarization`
**Version:** 1.1.0
**Status:** Production
**Category:** Clinical AI / Documentation

---

## Overview

The **Clinical Note Summarization Skill** converts unstructured clinical text (dictations, progress notes, discharge summaries) into structured **SOAP** format with explicit guardrails for accuracy, missing data, and contradictions. It is designed for documentation support workflows that require consistent structure, traceability, and safe handling of PHI.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `patient_context` | dict | Optional metadata (age, sex, encounter type, PMH). Avoid PHI unless required. |
| `note_text` | str | Raw clinical note text (dictation, OCR, or EHR export). |
| `output_format` | str | `markdown` or `json` (recommended for downstream validation). |

**Recommended minimum input:** `note_text` plus encounter type and age.

---

## Outputs

### SOAP Summary (Markdown)

- `Subjective` - HPI, ROS, symptoms, and patient-reported history
- `Objective` - vitals, exam findings, labs/diagnostics
- `Assessment` - problems with ICD-10 suggestions when supported
- `Plan` - actions per problem with timing and responsible role

### Optional JSON Schema

```json
{
  "soap": {
    "subjective": ["..."] ,
    "objective": ["..."] ,
    "assessment": [
      {"problem": "...", "icd10": "...", "evidence": "..."}
    ],
    "plan": [
      {"action": "...", "responsible_role": "...", "timing": "..."}
    ]
  },
  "alerts": ["..."],
  "missing_information": ["..."]
}
```

---

## Workflow

1. **Normalize input** - identify vitals, labs, meds, and timelines; standardize units.
2. **Extract structure** - map content into SOAP sections.
3. **Validate** - check for contradictions, missing fields, and medication duplication.
4. **Output** - return structured SOAP and a data gaps checklist.

---

## Prompt Template

Use `prompt.md` as the canonical system prompt. It enforces:
- No invention of data
- Explicit contradictions and missing info
- Problem-linked assessment and plan

---

## Integration Examples

### LangChain

```python
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

with open("prompt.md") as f:
    system_prompt = f.read()

template = PromptTemplate.from_template(
    system_prompt + "\n\nClinical Note:\n{note}\n\nStructured SOAP:"
)

chain = template | ChatOpenAI(model="gpt-4")
result = chain.invoke({"note": clinical_note_text})
```

### Direct API (OpenAI)

```python
import openai

with open("prompt.md") as f:
    system_prompt = f.read()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Structure this note:\n{note}"}
    ]
)
```

---

## Guardrails

- **No hallucinations**: If not stated, say "not provided".
- **No clinical decisions**: This is documentation assistance only.
- **PHI safety**: Use HIPAA-compliant environments; avoid logging raw notes.
- **Auditability**: Store prompt and model metadata for traceability.

---

## Validation Hooks

- Compare extracted vitals/labs against source text.
- Flag missing allergies, meds, or discharge plan.
- Require clinician review before EHR insertion.

---

## Files

| File | Description |
|------|-------------|
| `prompt.md` | System prompt template for SOAP structuring |
| `usage.py` | Example integration script |

---

## Supported Models

| Provider | Model | Performance |
|----------|-------|-------------|
| OpenAI | gpt-4, gpt-4-turbo | Excellent |
| Anthropic | claude-3-opus, claude-3-sonnet | Excellent |
| Google | gemini-1.5-pro | Good |
| Open Source | Llama 3 70B, Mixtral 8x22B | Good (fine-tuning recommended) |

---

## Related Skills

- **Trial Eligibility Screening**: Use structured notes for matching.
- **Medical Coding**: ICD-10/CPT assignment from structured output.

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->