# ChEMBL

Explore 2M+ drugs and compounds. Find approved drugs, bioactivity data, mechanisms of action, and drug-target interactions.

## Key Tools

### `chembl_search_molecules` — Find drugs by name

```json
{
  "name": "chembl_search_molecules",
  "arguments": {
    "query": "eculizumab",
    "max_results": 10
  }
}
```

**Arguments:**
- `query` (str): Drug name or synonym
- `max_results` (int, optional): Results to return

**Returns:** Molecules with ChEMBL ID, IUPAC name, synonyms, drug indication

### `chembl_get_molecule` — Get molecule details

```json
{
  "name": "chembl_get_molecule",
  "arguments": {
    "molecule_id": "CHEMBL2397693"
  }
}
```

**Arguments:**
- `molecule_id` (str): ChEMBL molecule ID

**Returns:** Full molecule data: structure, molecular weight, LogP, MeSH terms, indications, ATC codes, max phase reached

### `chembl_search_targets` — Find proteins by name

```json
{
  "name": "chembl_search_targets",
  "arguments": {
    "query": "acetylcholine receptor",
    "max_results": 10
  }
}
```

**Arguments:**
- `query` (str): Protein/gene name
- `max_results` (int, optional): Results to return

**Returns:** Target proteins with ChEMBL ID, target type, organism

### `chembl_get_target` — Get protein details

```json
{
  "name": "chembl_get_target",
  "arguments": {
    "target_id": "CHEMBL612"
  }
}
```

**Returns:** Target metadata: synonyms, organism, UniProt ID, cross-references

### `chembl_find_drugs_by_target` — Get all drugs targeting a protein

```json
{
  "name": "chembl_find_drugs_by_target",
  "arguments": {
    "target_name": "CHRNE",
    "include_all_mechanisms": true,
    "max_results": 20
  }
}
```

**Arguments:**
- `target_name` (str): Gene symbol or protein name
- `include_all_mechanisms` (bool, optional): Include all known mechanisms (not just primary)
- `max_results` (int, optional): Drugs to return

**Returns:** Drugs targeting the gene with mechanism, max phase, clinical status

### `chembl_find_drugs_by_indication` — Get drugs for a disease

```json
{
  "name": "chembl_find_drugs_by_indication",
  "arguments": {
    "indication": "myasthenia gravis",
    "max_results": 20
  }
}
```

**Arguments:**
- `indication` (str): Disease/indication name
- `max_results` (int, optional): Results to return

**Returns:** Approved and investigational drugs with indication

### `chembl_get_activities` — Get bioactivity data

```json
{
  "name": "chembl_get_activities",
  "arguments": {
    "molecule_id": "CHEMBL25",
    "target_id": "CHEMBL612",
    "max_results": 50
  }
}
```

**Arguments:**
- `molecule_id` (str, optional): Drug identifier
- `target_id` (str, optional): Protein identifier
- `max_results` (int, optional): Activities to return

**Returns:** Bioactivity data: assay type, measurement, units, value, confidence

### `chembl_get_mechanism` — Get drug mechanism of action

```json
{
  "name": "chembl_get_mechanism",
  "arguments": {
    "molecule_id": "CHEMBL2397693"
  }
}
```

**Returns:** Mechanism(s) of action with target, organism, primary/secondary status

### `chembl_get_drug_indications` — Get all indications for drug

```json
{
  "name": "chembl_get_drug_indications",
  "arguments": {
    "molecule_id": "CHEMBL2397693"
  }
}
```

**Returns:** FDA-approved and investigational indications

## Use Cases

### Find Approved Drugs for Disease

```json
{
  "name": "chembl_find_drugs_by_indication",
  "arguments": {
    "indication": "myasthenia gravis",
    "max_results": 20
  }
}
```

### Find Unapproved Drugs Targeting Gene

```json
{
  "name": "chembl_find_drugs_by_target",
  "arguments": {
    "target_name": "CHRNE",
    "include_all_mechanisms": true,
    "max_results": 30
  }
}
```

### Get Bioactivity Data for Target

```json
{
  "name": "chembl_get_activities",
  "arguments": {
    "target_id": "CHEMBL612",
    "max_results": 100
  }
}
```

Returns all compounds tested against this target with potency (IC50, Kd, etc.)

### Find Drug Mechanism of Action

```json
{
  "name": "chembl_get_mechanism",
  "arguments": {
    "molecule_id": "CHEMBL2397693"
  }
}
```

### Repurposing Screening

For a list of genes:
1. Search each gene in ChEMBL (`find_drugs_by_target`)
2. Find all compounds tested against target (`get_activities`)
3. Cross-reference with clinical trials (`ctg_search_by_intervention`)
4. Check safety profile (`openfda_search_adverse_events`)

## Data Fields

**Molecule data includes:**
- SMILES string (chemical structure)
- Molecular weight, LogP (lipophilicity), HBA/HBD (ADME properties)
- Max phase reached (approved vs investigational)
- ATC codes (drug classification)
- Indications (FDA-approved uses)
- Black box warnings
- Synonyms and trade names

**Target data includes:**
- Protein type (enzyme, kinase, GPCR, antibody, etc.)
- Organism (human, mouse, rat, etc.)
- Uniprot ID (link to full protein info)
- Bioassay count (how much data?)

**Bioactivity data includes:**
- Assay type (binding, functional, etc.)
- Measurement type (IC50, Kd, EC50, etc.)
- Value and units
- Confidence score

## Workflow: Drug Repurposing Screen

1. **Pick target gene** (from OpenTargets or UniProt)
2. **Find all drugs targeting it** (`find_drugs_by_target`)
3. **Get bioactivity data** (`get_activities`) — which are most potent?
4. **Check indications** (`get_drug_indications`) — what's it approved for?
5. **Check mechanism** (`get_mechanism`) — how does it work?
6. **Check safety** (`openfda_search_adverse_events`) — any red flags?
7. **Search trials** (`ctg_search_by_intervention`) — any ongoing trials?
8. **Search literature** (`pubmed_search_articles`) — any recent data?

## Notes

- **Coverage**: Approved drugs, clinical candidates, research compounds
- **Bioactivity**: 15M+ activity records across 10K+ assays
- **Max phase**: Highest development stage reached (approved vs Phase 1/2/3)
- **Mechanism annotation**: Human-curated (high quality)
- **Structure**: Chemical structures in SMILES format (machine-readable)

## Rate Limits

- No API key required
- Public endpoint
- Results cached (30-day TTL)

## Examples

### Example 1: Find all drugs approved for Myasthenia Gravis

```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_find_drugs_by_indication",
    "arguments": {
      "indication": "myasthenia gravis",
      "max_results": 20
    }
  }
}
```

### Example 2: Get mechanism of action for eculizumab (Soliris)

```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_search_molecules",
    "arguments": {
      "query": "eculizumab",
      "max_results": 1
    }
  }
}
```

Then use molecule_id from result:
```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_get_mechanism",
    "arguments": {
      "molecule_id": "CHEMBL2397693"
    }
  }
}
```

### Example 3: Find all compounds tested against acetylcholine receptor

```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_search_targets",
    "arguments": {
      "query": "acetylcholine receptor",
      "max_results": 5
    }
  }
}
```

Then get activities:
```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_get_activities",
    "arguments": {
      "target_id": "CHEMBL612",
      "max_results": 100
    }
  }
}
```

### Example 4: Repurposing check for CHRNE gene

```json
{
  "method": "tools/call",
  "params": {
    "name": "chembl_find_drugs_by_target",
    "arguments": {
      "target_name": "CHRNE",
      "include_all_mechanisms": true,
      "max_results": 30
    }
  }
}
```
