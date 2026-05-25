# ClinicalTrials.gov

Search 400,000+ clinical trials. Find active studies by condition, intervention, phase, recruitment status, and more.

## Key Tools

### `ctg_search_studies` — Search trials with filters

```json
{
  "name": "ctg_search_studies",
  "arguments": {
    "condition": "myasthenia gravis",
    "intervention": "immunoglobulin",
    "recruitment_status": "RECRUITING",
    "study_type": "INTERVENTIONAL",
    "phase": "PHASE2",
    "max_results": 20
  }
}
```

**Arguments:**
- `condition` (str): Disease/condition name (auto-mapped to MeSH)
- `intervention` (str, optional): Drug/procedure/behavioral intervention
- `recruitment_status` (str, optional): `RECRUITING`, `ACTIVE_NOT_RECRUITING`, `ENROLLING_BY_INVITATION`, `NOT_YET_RECRUITING`, `CLOSED_TO_ACCRUAL`, `CLOSED_TO_ACCRUAL_AND_INTERVENTION`, `TEMPORARILY_CLOSED_FOR_RECRUITMENT`, `WITHDRAWN`, `SUSPENDED`, `TERMINATED`, `COMPLETED`
- `study_type` (str, optional): `INTERVENTIONAL`, `OBSERVATIONAL`, `EXPANDED_ACCESS`
- `phase` (str, optional): `PHASE1`, `PHASE2`, `PHASE3`, `PHASE4`, `EARLY_PHASE1`
- `max_results` (int, default 20): Trials to return

**Returns:** Array of trials with NCT ID, title, status, recruitment info, locations

### `ctg_get_study` — Get trial details

```json
{
  "name": "ctg_get_study",
  "arguments": {
    "nct_id": "NCT05123456"
  }
}
```

**Arguments:**
- `nct_id` (str): Trial NCT identifier (e.g., NCT05123456)

**Returns:** Full trial metadata: description, eligibility, locations, contacts, outcomes, status

### `ctg_search_by_condition` — Search by disease only

```json
{
  "name": "ctg_search_by_condition",
  "arguments": {
    "condition": "multiple sclerosis",
    "max_results": 30
  }
}
```

**Returns:** All trials for given condition (any status/phase)

### `ctg_search_by_intervention` — Search by drug/intervention

```json
{
  "name": "ctg_search_by_intervention",
  "arguments": {
    "intervention": "monoclonal antibody",
    "condition": "myasthenia gravis"
  }
}
```

**Returns:** Trials using specific intervention (optionally filtered by condition)

### `ctg_get_study_metadata` — Get available fields

```json
{
  "name": "ctg_get_study_metadata",
  "arguments": {}
}
```

**Returns:** Complete list of searchable/filterable fields for advanced queries

## Use Cases

### Find Active Trials for Disease

```json
{
  "name": "ctg_search_studies",
  "arguments": {
    "condition": "myasthenia gravis",
    "recruitment_status": "RECRUITING",
    "max_results": 20
  }
}
```

### Find Trials by Drug

```json
{
  "name": "ctg_search_by_intervention",
  "arguments": {
    "intervention": "eculizumab",
    "max_results": 15
  }
}
```

### Find Trials by Phase (Phase 3 + Phase 4 only)

```json
{
  "name": "ctg_search_studies",
  "arguments": {
    "condition": "primary progressive multiple sclerosis",
    "phase": "PHASE3",
    "recruitment_status": "RECRUITING",
    "max_results": 10
  }
}
```

### Get Trial Details

```json
{
  "name": "ctg_get_study",
  "arguments": {
    "nct_id": "NCT05123456"
  }
}
```

This returns:
- Full description and rationale
- Inclusion/exclusion criteria
- Primary and secondary outcomes
- Contact information
- Study locations
- Funding source
- Current enrollment

### Find Observational Studies (Non-Interventional)

```json
{
  "name": "ctg_search_studies",
  "arguments": {
    "condition": "myasthenia gravis",
    "study_type": "OBSERVATIONAL",
    "max_results": 20
  }
}
```

## Workflow: Trial Landscape Analysis

1. **Find active trials** for your condition
2. **Filter by phase** (Phase 2 vs 3 vs 4)
3. **Filter by recruitment** status (actively recruiting?)
4. **Check inclusion/exclusion** criteria (what populations?)
5. **Identify gaps** (what's NOT being studied?)
6. **Contact investigators** (trial contacts in metadata)

## Data Fields

**Available fields for filtering:**
- condition
- intervention (drug, procedure, behavioral, dietary, etc.)
- recruitment_status
- study_type (interventional, observational, expanded access)
- phase (Phase 1, 2, 3, 4)
- age (min/max eligible age)
- gender (all, female, male)
- accepts_healthy_volunteers (true/false)
- keyword (custom keywords)
- funding_source (NIH, industry, university, etc.)
- study_results (has results posted?)

## Notes

- **Coverage**: Registered trials (global, including outside US)
- **Registration requirement**: FDA mandates registration for investigational drugs
- **Results**: ~60% of trials post results (optional, becoming more common)
- **Updates**: Trials updated in real-time as status changes
- **Locations**: Multi-center trials list all participating centers

## Rate Limits

- No API key required
- Public endpoint
- Results cached (30-day TTL)

## Examples

### Example 1: Find myasthenia gravis trials that are actively recruiting

```json
{
  "method": "tools/call",
  "params": {
    "name": "ctg_search_studies",
    "arguments": {
      "condition": "myasthenia gravis",
      "recruitment_status": "RECRUITING",
      "max_results": 20
    }
  }
}
```

### Example 2: Find complement inhibitor trials in any autoimmune disease

```json
{
  "method": "tools/call",
  "params": {
    "name": "ctg_search_by_intervention",
    "arguments": {
      "intervention": "complement inhibitor",
      "max_results": 30
    }
  }
}
```

### Example 3: Get full details for a specific trial

```json
{
  "method": "tools/call",
  "params": {
    "name": "ctg_get_study",
    "arguments": {
      "nct_id": "NCT05123456"
    }
  }
}
```

### Example 4: Find Phase 3 trials for primary progressive MS

```json
{
  "method": "tools/call",
  "params": {
    "name": "ctg_search_studies",
    "arguments": {
      "condition": "primary progressive multiple sclerosis",
      "phase": "PHASE3",
      "recruitment_status": "RECRUITING",
      "max_results": 10
    }
  }
}
```
