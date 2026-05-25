# OpenFDA

Access FDA data on drugs, devices, and adverse events. Check drug safety, adverse events, and FDA approvals.

## Key Tools

### `openfda_search_adverse_events` — Search FDA adverse event reports (FAERS)

```json
{
  "name": "openfda_search_adverse_events",
  "arguments": {
    "drug_name": "eculizumab",
    "reaction": "hemolysis",
    "seriousness": "serious",
    "limit": 20
  }
}
```

**Arguments:**
- `drug_name` (str, optional): Drug generic name
- `reaction` (str, optional): Adverse reaction/side effect name
- `seriousness` (str, optional): `serious`, `nonserious`, or omit for both
- `limit` (int, optional, default 10): Records to return

**Returns:** FDA adverse event reports with:
- Reaction type and severity
- Outcome (hospitalization, death, etc.)
- Report date
- Patient age/gender (when available)

### `openfda_get_adverse_event` — Get detailed adverse event report

```json
{
  "name": "openfda_get_adverse_event",
  "arguments": {
    "safety_report_id": "12345678"
  }
}
```

**Arguments:**
- `safety_report_id` (str): Unique safety report ID (from search)

**Returns:** Full adverse event details with all fields

### `openfda_search_drug_labels` — Search FDA drug labels

```json
{
  "name": "openfda_search_drug_labels",
  "arguments": {
    "drug_name": "eculizumab",
    "section": "warnings"
  }
}
```

**Arguments:**
- `drug_name` (str): Drug name
- `section` (str, optional): `warnings`, `contraindications`, `adverse_reactions`, `dosage`, etc.
- `limit` (int, optional): Labels to return

**Returns:** Drug labels (FDA-approved package inserts) for the drug

### `openfda_get_drug_label` — Get full drug label

```json
{
  "name": "openfda_get_drug_label",
  "arguments": {
    "set_id": "1234567890abcdef",
    "section": "warnings"
  }
}
```

**Arguments:**
- `set_id` (str): Label set ID (from search)
- `section` (str, optional): Filter to specific section

**Returns:** Complete FDA-approved label with:
- Indications and usage
- Warnings and precautions
- Adverse reactions
- Drug interactions
- Dosage and administration
- Black box warnings

### `openfda_search_device_events` — Search device adverse events (MAUDE)

```json
{
  "name": "openfda_search_device_events",
  "arguments": {
    "device_name": "pacemaker",
    "problem": "malfunction",
    "limit": 20
  }
}
```

**Returns:** Medical device adverse event reports

## Use Cases

### Check Drug Safety Profile

```json
{
  "name": "openfda_search_adverse_events",
  "arguments": {
    "drug_name": "your-candidate-drug",
    "limit": 50
  }
}
```

Look for:
- Common vs rare adverse events
- Serious outcomes (hospitalization, death)
- Trends over time

### Check Contraindications and Warnings

```json
{
  "name": "openfda_search_drug_labels",
  "arguments": {
    "drug_name": "your-candidate-drug",
    "section": "contraindications"
  }
}
```

Then get full label:
```json
{
  "name": "openfda_get_drug_label",
  "arguments": {
    "set_id": "label_id_from_search"
  }
}
```

### Find Drugs with Specific Adverse Event

```json
{
  "name": "openfda_search_adverse_events",
  "arguments": {
    "reaction": "hemolysis",
    "limit": 50
  }
}
```

Returns all drugs with this adverse event (helps identify class effects)

### Search by Seriousness

```json
{
  "name": "openfda_search_adverse_events",
  "arguments": {
    "drug_name": "eculizumab",
    "seriousness": "serious",
    "limit": 50
  }
}
```

Serious outcomes include:
- Death
- Life-threatening
- Hospitalization
- Disability
- Congenital anomaly

## Data Fields

**Adverse event records:**
- Reaction (adverse event name)
- Outcome (death, hospitalization, recovery, etc.)
- Seriousness
- Report date
- Patient age, gender (partial data)
- Concurrent medications
- Drug dose and route
- Indication

**Drug label sections:**
- Indications and usage
- Dosage and administration
- Warnings and precautions
- Contraindications
- Adverse reactions (frequency listed)
- Drug interactions
- Use in special populations (pregnancy, pediatric, etc.)
- How supplied
- Storage

**Adverse event statistics:**
- Total reports for drug
- Serious vs non-serious
- By reaction type
- By outcome

## Workflow: Drug Safety Assessment

1. **Search adverse events** for candidate drug
2. **Count serious events** (is it rare or frequent?)
3. **Check for class effects** (do all drugs in class have this?)
4. **Get drug label** (what do FDA docs say?)
5. **Compare with literature** (PubMed search for case reports)
6. **Check clinical trial safety** (ClinicalTrials.gov trial details)
7. **Risk assessment** (is benefit worth the risk?)

## Important Notes

- **FAERS limitations**: Under-reporting, ~1-10% of actual events
- **Label warnings**: FDA-approved text, reflects current safety data
- **Black box warnings**: Most serious FDA warning category
- **Drug interactions**: Listed in label, check before combining drugs
- **Special populations**: Pregnancy, pediatric, geriatric dosing often different

## Rate Limits

- No API key required (basic)
- Optional API key for higher rate limits (get from https://open.fda.gov/apis/)
- Results cached (30-day TTL)

## Examples

### Example 1: Check safety profile of eculizumab

```json
{
  "method": "tools/call",
  "params": {
    "name": "openfda_search_adverse_events",
    "arguments": {
      "drug_name": "eculizumab",
      "limit": 50
    }
  }
}
```

### Example 2: Find FDA-approved indications for eculizumab

```json
{
  "method": "tools/call",
  "params": {
    "name": "openfda_search_drug_labels",
    "arguments": {
      "drug_name": "eculizumab",
      "section": "indications_and_usage"
    }
  }
}
```

### Example 3: Get full FDA label including warnings

```json
{
  "method": "tools/call",
  "params": {
    "name": "openfda_get_drug_label",
    "arguments": {
      "set_id": "label_id_from_previous_search"
    }
  }
}
```

### Example 4: Find all drugs with hemolysis adverse events

```json
{
  "method": "tools/call",
  "params": {
    "name": "openfda_search_adverse_events",
    "arguments": {
      "reaction": "hemolysis",
      "limit": 50
    }
  }
}
```

Shows which drugs cause this adverse event (class effect screening)
