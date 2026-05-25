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

# EHR/FHIR Integration

**ID:** `biomedical.clinical.ehr_fhir_integration`
**Version:** 1.0.0
**Status:** Production
**Category:** Clinical / Healthcare Interoperability

---

## Overview

The **EHR/FHIR Integration Skill** provides comprehensive tools for working with Electronic Health Records (EHR) using the HL7 FHIR (Fast Healthcare Interoperability Resources) standard. Built on **fhir.resources**, **fhir-py**, and **SMART on FHIR** libraries, this skill enables extraction, transformation, and analysis of clinical data across healthcare systems.

Healthcare data remains siloed across disparate EHR systems (Epic, Cerner, Meditech). FHIR provides a modern, RESTful API standard enabling interoperability. This skill bridges AI applications with clinical data sources, supporting research, clinical decision support, and population health analytics.

---

## Key Capabilities

### 1. FHIR Resource Operations

| Operation | Description | Use Case |
|-----------|-------------|----------|
| **Read** | Retrieve single resource | Get patient record |
| **Search** | Query resources with parameters | Find patients by condition |
| **Create** | Add new resources | Log observations |
| **Update** | Modify existing resources | Update care plans |
| **Batch** | Multiple operations in one request | Bulk data extraction |

### 2. Supported FHIR Resources

| Category | Resources | Description |
|----------|-----------|-------------|
| **Clinical** | Patient, Condition, Observation, Procedure | Core clinical data |
| **Medications** | MedicationRequest, MedicationAdministration | Drug orders and administration |
| **Diagnostics** | DiagnosticReport, ImagingStudy, Specimen | Lab and imaging results |
| **Care Provision** | CarePlan, CareTeam, Goal | Treatment planning |
| **Documents** | DocumentReference, Composition | Clinical documents |
| **Administrative** | Encounter, Practitioner, Organization | Operational data |

### 3. Integration Patterns

| Pattern | Description | Technology |
|---------|-------------|------------|
| **SMART on FHIR** | OAuth2-based app launch | Patient/provider portals |
| **Bulk Data Export** | Async large-scale extraction | Population health |
| **CDS Hooks** | Clinical decision support triggers | Real-time alerts |
| **Subscriptions** | Event-driven notifications | Data synchronization |
| **MCP Server** | Model Context Protocol integration | LLM agent access |

---

## Technical Specifications

### Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fhir_server` | `str` | Required | FHIR server base URL |
| `resource_type` | `str` | Required | FHIR resource type |
| `patient_id` | `str` | `None` | Patient identifier |
| `search_params` | `dict` | `{}` | Search query parameters |
| `auth_method` | `str` | `smart` | Authentication method |

### Output Formats

| Format | Description |
|--------|-------------|
| FHIR JSON | Native FHIR resource bundles |
| Pandas DataFrame | Tabular analysis format |
| CSV/Excel | Export formats |
| Synthea-compatible | Synthetic data generation |

---

## Usage

### Command Line Interface

```bash
python fhir_client.py \
    --server https://fhir.example.org/r4 \
    --resource Patient \
    --search "name=Smith&birthdate=gt1980-01-01" \
    --output patients.json
```

### Python Library Integration

```python
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle
import fhirpy

# Initialize FHIR client
client = fhirpy.SyncFHIRClient(
    url='https://fhir.example.org/r4',
    authorization='Bearer <access_token>'
)

# Search for patients with diabetes
conditions = client.resources('Condition').search(
    code='http://snomed.info/sct|44054006'  # Type 2 Diabetes
).fetch_all()

# Get patient details
patient_ids = set(c.subject.reference.split('/')[-1] for c in conditions)
patients = [
    client.resources('Patient').search(_id=pid).first()
    for pid in patient_ids
]

# Retrieve observations for a patient
patient_id = 'example-patient-123'
observations = client.resources('Observation').search(
    subject=f'Patient/{patient_id}',
    code='http://loinc.org|2339-0'  # Glucose
).fetch_all()

# Process as pandas DataFrame
import pandas as pd

data = []
for obs in observations:
    data.append({
        'date': obs.effectiveDateTime,
        'value': obs.valueQuantity.value,
        'unit': obs.valueQuantity.unit,
        'code': obs.code.coding[0].display
    })

df = pd.DataFrame(data)
print(df.describe())
```

### SMART on FHIR Authentication

```python
from fhirclient import client
from fhirclient.models.patient import Patient

# SMART on FHIR configuration
settings = {
    'app_id': 'my_app',
    'api_base': 'https://fhir.example.org/r4',
    'redirect_uri': 'http://localhost:8080/callback',
    'scope': 'patient/*.read launch/patient'
}

smart = client.FHIRClient(settings=settings)

# Get authorization URL for user
auth_url = smart.authorize_url

# After OAuth callback
smart.handle_callback(callback_url)

# Access patient data
patient = Patient.read(smart.patient_id, smart.server)
print(f"Patient: {patient.name[0].given[0]} {patient.name[0].family}")

# Access observations
observations = Observation.where(
    struct={'subject': f'Patient/{smart.patient_id}'}
).perform_resources(smart.server)
```

### LLM Agent Integration (LangChain)

```python
from langchain.tools import tool
import fhirpy

@tool
def query_patient_data(
    patient_id: str,
    data_type: str = "all",
    date_range: str = None
) -> str:
    """
    Retrieves patient clinical data from EHR via FHIR.

    Accesses conditions, medications, observations, and procedures
    for a specific patient.

    Args:
        patient_id: Patient FHIR ID
        data_type: Type of data (conditions, medications, observations, all)
        date_range: Optional date filter (e.g., "2024-01-01..2024-12-31")

    Returns:
        JSON summary of patient clinical data
    """
    client = fhirpy.SyncFHIRClient(
        url=os.environ['FHIR_SERVER_URL'],
        authorization=f"Bearer {os.environ['FHIR_ACCESS_TOKEN']}"
    )

    result = {"patient_id": patient_id}

    if data_type in ["conditions", "all"]:
        conditions = client.resources('Condition').search(
            subject=f'Patient/{patient_id}'
        ).fetch_all()
        result["conditions"] = [
            {"code": c.code.coding[0].display, "status": c.clinicalStatus.coding[0].code}
            for c in conditions
        ]

    if data_type in ["medications", "all"]:
        meds = client.resources('MedicationRequest').search(
            subject=f'Patient/{patient_id}',
            status='active'
        ).fetch_all()
        result["medications"] = [
            {"name": m.medicationCodeableConcept.coding[0].display,
             "dosage": m.dosageInstruction[0].text if m.dosageInstruction else None}
            for m in meds
        ]

    if data_type in ["observations", "all"]:
        # Get vital signs
        vitals = client.resources('Observation').search(
            subject=f'Patient/{patient_id}',
            category='vital-signs',
            _sort='-date',
            _count=10
        ).fetch_all()
        result["recent_vitals"] = [
            {"type": v.code.coding[0].display,
             "value": v.valueQuantity.value if hasattr(v, 'valueQuantity') else None,
             "date": v.effectiveDateTime}
            for v in vitals
        ]

    return json.dumps(result, indent=2, default=str)

@tool
def search_patients_by_criteria(
    conditions: list = None,
    medications: list = None,
    age_range: tuple = None,
    lab_criteria: dict = None
) -> str:
    """
    Searches for patients matching clinical criteria via FHIR.

    Useful for cohort identification and clinical trial matching.

    Args:
        conditions: List of SNOMED codes for conditions
        medications: List of RxNorm codes for medications
        age_range: Tuple of (min_age, max_age)
        lab_criteria: Dict of lab tests with ranges

    Returns:
        List of matching patient IDs with summary data
    """
    client = fhirpy.SyncFHIRClient(
        url=os.environ['FHIR_SERVER_URL'],
        authorization=f"Bearer {os.environ['FHIR_ACCESS_TOKEN']}"
    )

    patient_ids = set()

    # Search by conditions
    if conditions:
        for condition_code in conditions:
            conds = client.resources('Condition').search(
                code=f'http://snomed.info/sct|{condition_code}'
            ).fetch_all()
            for c in conds:
                patient_ids.add(c.subject.reference.split('/')[-1])

    # Filter by other criteria
    results = []
    for pid in patient_ids:
        patient = client.resources('Patient').search(_id=pid).first()
        if age_in_range(patient, age_range) and meets_criteria(pid, client, medications, lab_criteria):
            results.append({
                "id": pid,
                "name": f"{patient.name[0].given[0]} {patient.name[0].family}",
                "birthDate": patient.birthDate
            })

    return json.dumps({"matching_patients": results, "count": len(results)})
```

### FHIR MCP Server Integration

```python
# Using FHIR MCP Server for LLM integration
# Install: pip install fhir-mcp-server

from mcp import Server
from fhir_mcp_server import FHIRMCPServer

# Configure MCP server with FHIR endpoint
mcp_server = FHIRMCPServer(
    fhir_base_url="https://fhir.example.org/r4",
    auth_token=os.environ['FHIR_ACCESS_TOKEN']
)

# Available tools exposed to LLM
# - search_patients
# - get_patient
# - get_patient_conditions
# - get_patient_medications
# - get_patient_observations
# - search_conditions
# - search_observations
```

### Integration with Anthropic Claude

```python
import anthropic
import fhirpy

client = anthropic.Client()

def clinical_summary_with_claude(patient_id: str):
    """Generates clinical summary from FHIR data using Claude."""

    # Extract FHIR data
    fhir_client = fhirpy.SyncFHIRClient(
        url=os.environ['FHIR_SERVER_URL'],
        authorization=f"Bearer {os.environ['FHIR_ACCESS_TOKEN']}"
    )

    patient = fhir_client.resources('Patient').search(_id=patient_id).first()
    conditions = fhir_client.resources('Condition').search(
        subject=f'Patient/{patient_id}'
    ).fetch_all()
    meds = fhir_client.resources('MedicationRequest').search(
        subject=f'Patient/{patient_id}', status='active'
    ).fetch_all()
    labs = fhir_client.resources('Observation').search(
        subject=f'Patient/{patient_id}', category='laboratory', _count=20
    ).fetch_all()

    # Prepare clinical data for Claude
    clinical_data = {
        "patient": {
            "name": f"{patient.name[0].given[0]} {patient.name[0].family}",
            "birthDate": patient.birthDate,
            "gender": patient.gender
        },
        "conditions": [c.code.coding[0].display for c in conditions],
        "medications": [m.medicationCodeableConcept.coding[0].display for m in meds],
        "labs": [
            {"test": l.code.coding[0].display,
             "value": l.valueQuantity.value if hasattr(l, 'valueQuantity') else None}
            for l in labs
        ]
    }

    # Claude generates clinical summary
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""You are a clinical summarization assistant. Review this patient's FHIR data and generate a comprehensive clinical summary.

Patient Data:
{json.dumps(clinical_data, indent=2, default=str)}

Generate:
1. Patient Overview (demographics, relevant social history)
2. Active Problem List (prioritized by clinical significance)
3. Current Medications (with indications mapped to problems)
4. Recent Lab Summary (highlight abnormals with clinical interpretation)
5. Care Gaps (preventive care, monitoring needs)
6. Clinical Synopsis (2-3 sentence summary for handoff)

Format as a structured clinical note."""
            }
        ],
    )

    return message.content[0].text
```

---

## Bulk Data Export

For population health and research analytics:

```python
import requests
import time

def initiate_bulk_export(fhir_server: str, resource_types: list):
    """Initiates FHIR Bulk Data Export ($export operation)."""

    headers = {
        "Accept": "application/fhir+json",
        "Prefer": "respond-async",
        "Authorization": f"Bearer {os.environ['FHIR_ACCESS_TOKEN']}"
    }

    params = {
        "_type": ",".join(resource_types),
        "_outputFormat": "application/ndjson"
    }

    response = requests.get(
        f"{fhir_server}/$export",
        headers=headers,
        params=params
    )

    # Get polling URL from Content-Location header
    polling_url = response.headers['Content-Location']

    # Poll until complete
    while True:
        status = requests.get(polling_url, headers=headers)
        if status.status_code == 200:
            return status.json()['output']  # List of downloadable files
        elif status.status_code == 202:
            time.sleep(10)  # Still processing
        else:
            raise Exception(f"Export failed: {status.text}")

# Usage
files = initiate_bulk_export(
    "https://fhir.example.org/r4",
    ["Patient", "Condition", "Observation", "MedicationRequest"]
)

for file_info in files:
    # Download NDJSON files
    download_and_process(file_info['url'])
```

---

## Methodology

This implementation follows HL7 FHIR standards:

> **HL7 FHIR R4.** *Fast Healthcare Interoperability Resources.* http://hl7.org/fhir/R4/

> **SMART on FHIR.** *OAuth2-based Authorization for FHIR.* https://docs.smarthealthit.org/

Key design principles:

1. **R4 compliance:** Follows FHIR R4 specification (most widely adopted)
2. **US Core profiles:** Compatible with US Core Implementation Guide
3. **OAuth2/SMART:** Standards-based authentication
4. **Bulk Data support:** Large-scale data extraction capability

---

## Dependencies

```
fhir.resources>=7.0.0
fhirpy>=1.4.0
fhirclient>=4.1.0
pandas>=2.0.0
requests>=2.28.0
```

Install with:
```bash
pip install fhir.resources fhirpy fhirclient pandas requests
```

---

## Security & Compliance

- **HIPAA compliance:** Encrypted transport, audit logging
- **OAuth2/SMART:** Standards-based authentication
- **Consent management:** Respect patient consent directives
- **Data minimization:** Request only necessary resources/elements

---

## Supported FHIR Servers

| Server | Type | Notes |
|--------|------|-------|
| HAPI FHIR | Open source | Self-hosted |
| Microsoft Azure FHIR | Cloud | Azure integration |
| Google Cloud Healthcare | Cloud | GCP integration |
| AWS HealthLake | Cloud | AWS integration |
| Epic | Commercial | MyChart integration |
| Cerner | Commercial | Millennium integration |

---

## Related Skills

- **Clinical NLP:** For unstructured clinical text extraction
- **Trial Eligibility Agent:** For patient-trial matching
- **Clinical Note Summarization:** For document generation
- **Medical Imaging AI:** For DICOM/FHIR integration

---

## External Resources

- [HL7 FHIR](https://www.hl7.org/fhir/)
- [SMART on FHIR](https://docs.smarthealthit.org/)
- [fhir.resources](https://github.com/nazrulworld/fhir.resources)
- [FHIR MCP Server](https://github.com/wso2/fhir-mcp-server)

---

## Author

**MD BABU MIA**
*Artificial Intelligence Group*
*Icahn School of Medicine at Mount Sinai*
md.babu.mia@mssm.edu


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->