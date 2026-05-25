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

# Clinical Trial Eligibility Agent

**ID:** `biomedical.clinical.trial_eligibility`
**Version:** 1.1.0
**Status:** Production
**Category:** Clinical AI / Trial Matching

---

## Overview

The **Clinical Trial Eligibility Agent** automates patient-to-trial matching by parsing eligibility criteria and evaluating patient data against inclusion/exclusion rules. It reduces manual screening time while preserving traceability and highlighting data gaps.

---

## Inputs

| Field | Type | Notes |
|------|------|------|
| `trial_id` | str | ClinicalTrials.gov NCT number or sponsor protocol ID |
| `patient_summary` | str | Narrative summary of key facts |
| `patient_structured` | dict | Optional FHIR bundle or structured JSON |
| `data_sources` | list[str] | e.g., `clinical_notes`, `labs`, `imaging`, `meds` |

---

## Outputs

### Eligibility Report

- Inclusion criteria status (MET / NOT MET / UNKNOWN)
- Exclusion criteria status (MET / NOT MET / UNKNOWN)
- Evidence snippets and confidence per criterion
- Overall recommendation: `potentially_eligible`, `not_eligible`, or `needs_more_information`
- Data gap checklist

### JSON Schema (Recommended)

```json
{
  "trial_id": "NCT00000000",
  "criteria": [
    {"id": "I-01", "text": "Age >= 18", "status": "MET", "evidence": "Age 58", "confidence": "high"}
  ],
  "eligibility_summary": "potentially_eligible",
  "data_gaps": ["Latest ECOG score"],
  "alerts": ["Confirm brain MRI within 30 days"]
}
```

---

## Workflow

1. **Acquire protocol** - Pull eligibility section from ClinicalTrials.gov or sponsor PDF.
2. **Parse criteria** - Normalize to structured logic (AND/OR, thresholds, units).
3. **Extract patient facts** - Convert notes and FHIR data into a unified feature map.
4. **Evaluate criteria** - Assign MET/NOT MET/UNKNOWN with evidence.
5. **Summarize gaps** - List missing labs, imaging, or biomarker data.

---

## Example Prompt

```text
Patient summary:
- 58-year-old female
- Stage IIIA NSCLC
- EGFR exon 19 deletion
- Prior osimertinib, progressed after 14 months
- ECOG 1
- No brain metastases
- Creatinine clearance 72 mL/min

Check eligibility for NCT04487080 and list MET/NOT MET/UNKNOWN criteria.
```

---

## Guardrails

- **No final enrollment decisions**: results are advisory only.
- **Cite evidence** for each criterion.
- **Surface unknowns** rather than inferring.
- **PHI handling**: use de-identified data and HIPAA-compliant environments.

---

## Integration Patterns

### FHIR-Based Matching

```python
from fhir.resources.patient import Patient
from fhir.resources.condition import Condition

def extract_patient_features(fhir_bundle: dict) -> dict:
    features = {}
    for entry in fhir_bundle.get("entry", []):
        resource = entry.get("resource", {})
        if resource.get("resourceType") == "Patient":
            patient = Patient.parse_obj(resource)
            features["age"] = calculate_age(patient.birthDate)
        elif resource.get("resourceType") == "Condition":
            condition = Condition.parse_obj(resource)
            features.setdefault("conditions", []).append(
                condition.code.coding[0].display
            )
    return features
```

---

## Dependencies

```
requests>=2.28
fhir.resources>=6.0
pandas>=1.5
```

---

## References

- TrialGPT (NIH)
- Jin et al. "TrialGPT: Matching Patients to Clinical Trials with Large Language Models" (2023)

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->