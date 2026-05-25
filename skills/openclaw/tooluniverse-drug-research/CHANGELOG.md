# Drug Research Skill Update - February 2026

## Overview

Updated `tooluniverse-drug-research` skill based on elacestrant case study feedback. These improvements address real-world gaps in completeness, mechanism depth, safety reporting, and fallback resilience.

---

## Major Changes

### 1. Enhanced Report Template

**Added Sections**:
- **Section 2.4**: Salt Forms & Polymorphs
- **Section 2.5**: Structure Visualization
- **Section 6.6**: Dose Modification Guidance

**Rationale**: Address chemistry CMC gaps and safety dosing guidance missing from original reports.

---

### 2. FDA Label Core Fields Bundle (NEW)

**Location**: After Compound Disambiguation

**Purpose**: Establish authoritative baseline from FDA labels before predictive tools.

**Core Sections to Retrieve**:
- `mechanism_of_action`, `pharmacodynamics` → Section 3.1
- `chemistry` → Section 2.4
- `clinical_pharmacology`, `pharmacokinetics` → Section 4
- `drug_interactions` → Section 6.5
- `dosage_and_administration`, `warnings_and_cautions` → Section 6.6
- `pharmacogenomics` → Section 7
- `clinical_studies` → Section 5.5
- `description`, `inactive_ingredients` → Section 2.5

**Workflow Change**: Retrieve these early (after set_id obtained) to enable fallbacks.

---

### 3. PATH 1 (Chemistry) - Enhanced CMC Coverage

**Old Workflow**:
```
PubChem properties → ADMETAI predictions → solubility/lipophilicity
```

**New Workflow**:
```
PubChem properties → ADMETAI predictions → solubility/lipophilicity →
DailyMed chemistry section (salt forms, polymorphs) →
DailyMed description (formulation, excipients)
```

**New Requirements**:
- pKa (experimental or label-based)
- Salt forms documented with CIDs
- 2D structure image embedded (PubChem link)
- Formulation details (dosage forms, excipients)

**Output Changes**: Section 2.4 and 2.5 now populated with CMC data.

---

### 4. PATH 2 (Targets & Mechanism) - FDA MOA + Activity-Derived Targets

**Old Workflow**:
```
ChEMBL_get_bioactivity_by_chemblid →
ChEMBL_get_target_by_chemblid →
DGIdb → PubChem
```

**New Workflow**:
```
DailyMed MOA/pharmacodynamics (FDA label text) →
ChEMBL_search_activities (get activity records) →
Extract unique target_chembl_id (filter to pChEMBL ≥ 6.0) →
ChEMBL_get_target for each target →
DGIdb → PubChem
```

**Critical Changes**:
- **AVOID `ChEMBL_get_molecule_targets`** - returns unfiltered, irrelevant targets
- **Use activity-derived targets instead** - filter to potent activities only
- **Quote FDA label MOA verbatim** in Section 3.1
- **Add target selectivity table** including mutant forms (e.g., ESR1 Y537S for endocrine drugs)

**Type Normalization**: Convert all ChEMBL IDs to strings before API calls.

---

### 5. PATH 3 (ADMET) - Dependency Gate with FDA Label Fallback

**Old Workflow**:
```
ADMETAI tools → (if fail: document "predictions unavailable")
```

**New Workflow**:
```
ADMETAI tools → (if fail: AUTOMATIC FALLBACK) →
DailyMed clinical_pharmacology/pharmacokinetics →
DailyMed drug_interactions (CYP data) →
PubMed PK papers
```

**Critical Change**: **Dependency Gate** - Never leave Section 4 as "predictions unavailable".

**Fallback Evidence Tiers**:
- ADMET-AI predictions: ★★☆
- FDA label PK: ★★★
- PubMed PK studies: ★★☆

**Output Changes**: Section 4 always populated with either predictions OR label data OR literature PK.

---

### 6. PATH 4 (Clinical Trials) - Accurate Phase Counting

**Old Workflow**:
```
search_clinical_trials → extract NCT IDs, phases, statuses
```

**New Workflow**:
```
search_clinical_trials (full result set) →
COMPUTE PHASE COUNTS (count by Phase 1/2/3/4, status) →
COMPUTE INDICATION BREAKDOWN (top 5 conditions) →
SELECT REPRESENTATIVE TRIALS (top 5 Phase 3, top 3 recruiting) →
get_clinical_trial_conditions_and_interventions →
extract_clinical_trial_outcomes (if available)
```

**Critical Changes**:
- Section 5.2 must show **actual counts by phase/status in table format**
- Separate by indication when relevant (e.g., "312 diabetes trials, 87 PCOS trials")
- Clearly label "representative trials" vs "all trials"
- List top 5 Phase 3 completed trials (by enrollment or recency)

**Output Example**:
```markdown
### 5.2 Clinical Trial Landscape

| Phase | Total | Completed | Recruiting | Terminated |
|-------|-------|-----------|------------|------------|
| Phase 4 | 89 | 72 | 12 | 3 |
| Phase 3 | 156 | 134 | 15 | 5 |
| Phase 2 | 203 | 178 | 18 | 4 |
| Phase 1 | 67 | 61 | 4 | 2 |

**Total Registered Trials**: 515 (as of 2026-02-04)
**Primary Indications**: Type 2 diabetes (312), PCOS (87), Cancer (45)

### Representative Trials
**Top 5 Completed Phase 3 Trials**:
- NCT00123456: UKPDS (n=3,867, completed 1998)
- ...
```

---

### 7. PATH 5 (Safety) - Comprehensive FAERS + Dose Modifications

**Old Workflow**:
```
FAERS reactions → seriousness → outcomes → deaths → age distribution
```

**New Workflow**:
```
FAERS reactions → seriousness (report counts + breakdown) → outcomes → deaths → age distribution →
DailyMed drug_interactions (DDI table) →
DailyMed dosage_and_administration + warnings (dose mod triggers)
```

**New FAERS Requirements**:
- **Date window**: Document report date range (e.g., "2004Q1 - 2026Q1")
- **Seriousness breakdown**: Table showing serious vs non-serious counts + percentage
- **Limitations paragraph**: Small N, reporting bias, causality not established, incomplete data

**New Dose Modification Section (6.6)**:
- ALT/AST thresholds (when to hold/discontinue)
- Renal impairment dosing by eGFR
- Hepatic impairment dosing by Child-Pugh
- CYP3A inhibitor/inducer adjustments

**Output Example**: See PATH 5 section in skill.

---

### 8. PATH 6 (Pharmacogenomics) - Fallback for PharmGKB Failures

**Old Workflow**:
```
PharmGKB_search_drugs → get_drug_details → get_clinical_annotations → get_dosing_guidelines
```

**New Workflow**:
```
PharmGKB tools → (if fail: AUTOMATIC FALLBACK) →
DailyMed pharmacogenomics section →
DailyMed clinical_pharmacology (PGx notes) →
PubMed PGx papers
```

**Critical Change**: Document tool failures; don't leave Section 7 empty.

**Output Changes**:
- If PharmGKB unavailable: "PharmGKB API unavailable; using label PGx + literature [★★★/★★☆]"
- Always populate Section 7 with either PharmGKB data OR label data OR "No PGx associations identified"

---

## 9. Type Normalization & Error Prevention (NEW)

**Location**: Before Evidence Grading System

**Purpose**: Prevent validation errors from numeric IDs.

**Critical Rule**: Convert all IDs to strings before API calls.

**Example**:
```python
# Convert all IDs to strings
chembl_ids = [str(id) for id in chembl_ids]
nct_ids = [str(id) for id in nct_ids]
pmids = [str(id) for id in pmids]
```

**Pre-Call Checklist**:
- [ ] All ID parameters are strings
- [ ] Lists contain strings, not ints/floats
- [ ] No `None` or `null` values in required fields

---

## 10. Automated Completeness Audit (NEW)

**Location**: After Evidence Grading, before Fallback Chains

**Purpose**: Flag missing data and recommend specific tool calls.

**Audit Process**:
1. Review each section against minimum requirements
2. Flag missing data with tool call recommendations
3. Document tool failures and fallback attempts
4. Generate completeness score (% of requirements met)

**Output**: Append audit report to Section 11 (Data Sources & Methodology).

**Audit Template**:
```markdown
## Report Completeness Audit

**Overall Completeness**: 85% (17/20 minimum requirements met)

### Missing Data Items
| Section | Missing Item | Recommended Action |
|---------|--------------|-------------------|
| 2 | Salt forms | Call `DailyMed_get_spl_sections_by_setid` (chemistry) |
| 3 | Mutant ESR1 binding | Filter ChEMBL activities for ESR1 Y537S |
| 5 | Phase count breakdown | Compute counts from search_clinical_trials results |

### Tool Failures Encountered
| Tool | Error | Fallback Used |
|------|-------|---------------|
| PharmGKB_search_drugs | API timeout | DailyMed label PGx [✓] |

### Data Confidence Assessment
| Section | Confidence | Evidence Tier | Notes |
|---------|-----------|---------------|-------|
| 1. Identity | High | ★★★ | PubChem + ChEMBL confirmed |
| 7. PGx | Low | ★☆☆ | PharmGKB unavailable; label only |
```

---

## Updated Section Completeness Checklists

### Section 2 (Chemistry)
**Added**:
- [ ] Salt forms documented (or "Parent compound only")
- [ ] 2D structure image embedded (PubChem link)
- [ ] Formulation details if available (dosage forms, excipients)

### Section 3 (Mechanism)
**Added**:
- [ ] FDA label MOA text quoted (if approved drug)
- [ ] Target selectivity table (including mutant forms if relevant)

### Section 4 (ADMET)
**Added**:
- [ ] **If ADMET-AI fails, fallback to FDA label PK sections** (do NOT leave "predictions unavailable")

### Section 5 (Clinical)
**Added**:
- [ ] **Actual counts by phase/status in table format** (NOT just representative trial list)
- [ ] Indication breakdown by counts
- [ ] Representative trial list clearly labeled

### Section 6 (Safety)
**Added**:
- [ ] FAERS seriousness breakdown (serious vs non-serious counts)
- [ ] FAERS date window documented
- [ ] FAERS limitations paragraph
- [ ] Dose modification triggers (ALT/AST, renal/hepatic, CYP adjustments)

### Section 7 (PGx)
**Added**:
- [ ] **If PharmGKB fails, fallback to label PGx + literature** (document failure)

---

## Updated Quick Reference Table

**Added**:
- Salt forms: `DailyMed_get_spl_sections_by_setid` (chemistry)
- Formulation: `DailyMed_get_spl_sections_by_setid` (description, inactive_ingredients)
- FDA MOA: `DailyMed_get_spl_sections_by_setid` (mechanism_of_action)
- Phase counts: **Compute from `search_clinical_trials` results**
- Dose mods: `DailyMed_get_spl_sections_by_setid` (dosage_and_administration, warnings)

**Deprecated**:
- ~~`ChEMBL_get_molecule_targets`~~ → Use `ChEMBL_search_activities` instead

**Evidence Tiers**: Added to table for quick reference.

---

## Key Improvements Summary (NEW SECTION)

Added before "Additional Resources" to summarize changes:

1. **Chemistry Completeness**: Salt/polymorph, pKa, structure image, formulation
2. **Mechanism Depth**: FDA label MOA, mutant target selectivity, activity-derived targets
3. **Clinical Trial Accuracy**: Actual phase counts, indication breakdown, representative trials
4. **Safety Completeness**: FAERS seriousness + date + limitations, dose modification triggers
5. **Fallback Resilience**: ADMET-AI → FDA PK, PharmGKB → label PGx, type normalization
6. **Quality Control**: Automated completeness audit, missing data recommendations

---

## Testing Recommendations

To validate these improvements, run the updated skill on:

1. **Elacestrant** (original test case) - verify all gaps addressed
2. **Metformin** (mature drug) - verify fallbacks work when tools succeed
3. **Investigational compound** (ChEMBL only) - verify graceful degradation when label unavailable
4. **PharmGKB failure case** - verify PGx fallback works

---

## Migration Notes

**For existing reports**:
- Re-run with updated skill to add missing sections
- Sections 2.4, 2.5, 6.6 will be new additions
- Section 5.2 will show actual counts instead of trial lists
- Section 11 will include completeness audit

**For new reports**:
- Follow updated workflow from start
- Retrieve FDA label core fields early
- Use type normalization consistently
- Run completeness audit before finalization

---

## File Size

- **Original**: ~750 lines
- **Updated**: 1104 lines (+47%)
- **Reason**: Added FDA label bundle, type normalization, completeness audit, expanded examples

Still within acceptable range for a comprehensive research skill.

---

**Change Author**: AI Assistant  
**Based On**: Elacestrant case study feedback (February 2026)  
**Status**: Ready for testing
