# Drug Research Skill Enhancement - Implementation Roadmap

Quick reference guide for implementing the 15 proposed skill enhancements.

---

## Executive Summary

| Status | Count | Items |
|--------|-------|-------|
| ✅ **Ready to implement** (existing tools) | 6 | #1, 2, 5, 8, 13, 14 |
| ⚠️ **Partial support** (need workarounds) | 4 | #3, 6, 7, 9 |
| 🔧 **Need new tools** (2 parsers) | 2 | #6, 7 |
| ❌ **Blocked** (external partnerships) | 3 | #4, 11 (partial), 12 (partial) |

**Total Tool Coverage**: 67% with existing tools → 87% with 2 new parsers

---

## Phase 1: Implement with Existing Tools (Week 1)

### ✅ 1. Patent & Exclusivity (#1) - 4 hours
**Section**: 8.3  
**Tools**: `FDA_OrangeBook_*` suite  
**Implementation**:
```python
# 1. Get approval history
approval = FDA_OrangeBook_get_approval_history(app_number)
# 2. Get exclusivity types
exclusivity = FDA_OrangeBook_get_exclusivity(brand_name)
# 3. Check generic status
generics = FDA_OrangeBook_check_generic_availability(brand_name)
# 4. Calculate patent cliff from approval_date + exclusivity periods
# 5. Document limitation: "Exact dates require Orange Book file download"
```

**Output**: Approval timeline, exclusivity types, generic availability, estimated patent cliff

---

### ✅ 2. Real-World Evidence (#2) - 3 hours
**Section**: 9.4 (new subsection)  
**Tools**: `search_clinical_trials`, `PubMed_search_articles`  
**Implementation**:
```python
# 1. Query observational studies
rwe_trials = search_clinical_trials(study_type="OBSERVATIONAL", intervention=drug)
# 2. Search RWE literature
rwe_pubs = PubMed_search_articles(query=f"{drug} (real-world OR observational)")
# 3. Extract effectiveness vs efficacy comparisons
# 4. Document adherence patterns, off-label use
```

**Output**: RWE trial counts, real-world effectiveness studies, adherence data

---

### ✅ 3. Biomarkers & Diagnostics (#5) - 3 hours
**Section**: 5.6 (new)  
**Tools**: `fda_pharmacogenomic_biomarkers`, `DailyMed_get_spl_by_setid`, `PharmGKB_*`  
**Implementation**:
```python
# 1. Get FDA biomarker requirements
biomarkers = fda_pharmacogenomic_biomarkers(drug_name=drug)
# 2. Parse label for companion diagnostics
spl = DailyMed_get_spl_by_setid(setid)
# Extract: "testing required", "approved diagnostic device"
# 3. Get PharmGKB response predictors
annotations = PharmGKB_get_clinical_annotations(gene_id)
```

**Output**: Required testing, approved diagnostics, response predictors, evidence levels

---

### ✅ 4. Formulation Comparison (#8) - 2 hours
**Section**: 2.5 (enhancement)  
**Tools**: `DailyMed_search_spls`, `DailyMed_parse_clinical_pharmacology`  
**Implementation**:
```python
# 1. Search for all formulations
all_spls = DailyMed_search_spls(drug_name)
# 2. Filter by formulation type (IR, ER, XR)
formulations = [spl for spl in all_spls if "extended" in spl.title or "immediate" in spl.title]
# 3. For each: extract PK parameters (Tmax, Cmax, AUC)
# 4. Create comparison table
```

**Output**: IR vs ER comparison table with PK parameters and dosing

---

### ✅ 5. Quality Control Metrics (#13) - 2 hours
**Section**: 11.3 (new subsection)  
**Tools**: Metadata from all tools  
**Implementation**:
```python
# 1. Track timestamps from all tool calls
# 2. Flag data >5 years old as "potentially outdated"
# 3. Compare contradictory values (e.g., half-life from different sources)
# 4. Apply evidence hierarchy to resolve contradictions
# 5. Calculate completeness score
```

**Output**: Source recency table, contradiction resolution, completeness score

---

### ✅ 6. Comparative Analysis (#14) - 4 hours
**Section**: 10.5 (new)  
**Tools**: `ChEMBL_get_bioactivity_by_chemblid`, `search_clinical_trials`, `FAERS_*`  
**Implementation**:
```python
# 1. Identify comparator drugs (user provides or infer from ATC class)
comparators = ["erlotinib", "gefitinib"]  # Example
# 2. For each: run abbreviated tool chain (identity, targets, trials, AEs)
# 3. Create comparison tables: potency, trial counts, AE rates
# 4. Search for head-to-head trials
head_to_head = search_clinical_trials(intervention=f"{drug} AND {comparator}")
```

**Output**: Drug class comparison table, differentiation factors, head-to-head data

---

**Phase 1 Total**: 18 hours (~2-3 days)

---

## Phase 2: Workarounds for Partial Support (Week 2)

### ⚠️ 7. Drug Combinations (#3) - 3 hours
**Section**: 6.7 (new)  
**Tools**: `search_clinical_trials`, `DailyMed_get_spl_by_setid`, manual XML parsing  
**Implementation**:
```python
# 1. Search combination trials
combo_trials = search_clinical_trials(intervention=f"{drug} AND {other_drug}")
# 2. Get full SPL XML
spl_xml = DailyMed_get_spl_by_setid(setid)
# 3. Manual parse for: "combination with", "co-administered", "concurrent"
# 4. Extract regimens: drug A 100mg + drug B 50mg QD
```

**Output**: Approved combinations, regimen schedules, synergy notes

---

### ⚠️ 8. Drug-Food Interactions (#6) - 2 hours
**Section**: 6.5.2 (new subsection)  
**Tools**: `DailyMed_get_spl_by_setid`, manual XML parsing  
**Implementation**:
```python
# 1. Get full SPL XML
spl_xml = DailyMed_get_spl_by_setid(setid)
# 2. Search for section: drug_and_or_food_interactions, food_effect
# 3. Extract mentions: grapefruit, alcohol, high-fat meal, dairy
# 4. Parse severity and recommendations
```

**Output**: Food interaction table with effects and recommendations

---

### ⚠️ 9. Special Populations (#7) - 3 hours
**Section**: 8.5 (new)  
**Tools**: `DailyMed_get_spl_by_setid`, manual XML parsing  
**Implementation**:
```python
# 1. Get full SPL XML
spl_xml = DailyMed_get_spl_by_setid(setid)
# 2. Extract sections: pediatric_use, geriatric_use, pregnancy, nursing_mothers
# 3. Parse structured data:
#    - Pediatric: age groups, dosing adjustments
#    - Pregnancy: category, risk summary
#    - Lactation: excretion data, recommendations
```

**Output**: Special populations tables with dosing and safety for each group

---

### ⚠️ 10. Regulatory Timeline (#9) - 2 hours
**Section**: 8.6 (new)  
**Tools**: `FDA_OrangeBook_get_approval_history`, manual label parsing  
**Implementation**:
```python
# 1. Get US approval history
approval = FDA_OrangeBook_get_approval_history(app_number)
# 2. Parse label for: priority review, breakthrough, orphan, accelerated
# 3. Extract major label changes from approval history (supplements)
# 4. Document limitation: "EMA/PMDA data not available"
```

**Output**: US regulatory timeline, approval pathway, PMRs, major label changes

---

**Phase 2 Total**: 10 hours (~1.5 days)

---

## Phase 3: Develop New Parser Tools (Week 3)

### 🔧 11. DailyMed_parse_special_populations - 8 hours

**Tool Spec**:
```json
{
  "name": "DailyMed_parse_special_populations",
  "type": "DailyMedSPLParserTool",
  "description": "Parse pediatric, geriatric, pregnancy, lactation sections from SPL XML into structured format",
  "parameter": {
    "type": "object",
    "required": ["operation", "setid"],
    "properties": {
      "operation": {"const": "parse_special_populations"},
      "setid": {"type": "string", "format": "uuid"},
      "populations": {
        "type": "array",
        "items": {"enum": ["pediatric", "geriatric", "pregnancy", "lactation"]},
        "default": ["pediatric", "geriatric", "pregnancy", "lactation"]
      }
    }
  },
  "return_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["success", "error"]},
      "pediatric": {
        "type": "object",
        "properties": {
          "age_groups": {"type": "array"},
          "dosing": {"type": "array"},
          "safety_notes": {"type": "array"}
        }
      },
      "geriatric": {
        "type": "object",
        "properties": {
          "dosing_adjustments": {"type": "array"},
          "warnings": {"type": "array"}
        }
      },
      "pregnancy": {
        "type": "object",
        "properties": {
          "category": {"type": "string"},
          "risk_summary": {"type": "string"},
          "data": {"type": "array"}
        }
      },
      "lactation": {
        "type": "object",
        "properties": {
          "excretion": {"type": "string"},
          "risk_summary": {"type": "string"},
          "recommendation": {"type": "string"}
        }
      }
    }
  }
}
```

**Implementation Steps**:
1. Add to `src/tooluniverse/data/dailymed_tools.json`
2. Implement parser in `src/tooluniverse/dailymed_tool.py`
3. Add section code mapping: `pediatric_use` → `34076-0`, `geriatric_use` → `34082-8`
4. Test with multiple set_ids
5. Add test cases to `tests/unit/test_dailymed_tool.py`

---

### 🔧 12. DailyMed_parse_drug_food_interactions - 4 hours

**Tool Spec**:
```json
{
  "name": "DailyMed_parse_drug_food_interactions",
  "type": "DailyMedSPLParserTool",
  "description": "Parse drug-food interaction sections from SPL XML. Returns food/beverage interactions with effects and recommendations",
  "parameter": {
    "type": "object",
    "required": ["operation", "setid"],
    "properties": {
      "operation": {"const": "parse_drug_food_interactions"},
      "setid": {"type": "string", "format": "uuid"}
    }
  },
  "return_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "interactions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "food_item": {"type": "string"},
            "effect": {"type": "string"},
            "mechanism": {"type": "string"},
            "recommendation": {"type": "string"},
            "severity": {"type": "string"}
          }
        }
      },
      "count": {"type": "integer"}
    }
  }
}
```

**Implementation Steps**:
1. Add to `src/tooluniverse/data/dailymed_tools.json`
2. Implement parser in `src/tooluniverse/dailymed_tool.py`
3. Search for keywords: grapefruit, alcohol, food, meal, dairy, caffeine
4. Extract effect magnitude: "increase", "decrease", percentage values
5. Test with drugs known to have food interactions (e.g., warfarin, statins)

---

**Phase 3 Total**: 12 hours (~1.5 days)

---

## Phase 4: Blocked (External Partnerships Required)

### ❌ 13. Pharmacoeconomics (#4)
**Status**: Cannot implement without commercial data sources  
**Required**: REDBOOK API license, ICER partnership  
**Alternative**: Document as "Not available via public APIs" with manual resource links

---

### ❌ 14. DrugBank / ATC Code Mapping (#11, partial)
**Status**: Partial implementation possible (70% coverage without these)  
**Required**: DrugBank API license (commercial), WHO ATC API access  
**Alternative**: Note limitation in report; 70% ID coverage is acceptable

---

### ❌ 15. Mechanism Visualization (#12, partial)
**Status**: Can link to external diagrams, cannot retrieve images  
**Required**: Reactome/KEGG image retrieval API (may not exist)  
**Alternative**: Provide clickable links to interactive diagrams (acceptable UX)

---

## Testing Plan

For each phase, test with these compounds:

| Compound | Rationale |
|----------|-----------|
| **Elacestrant** | Original feedback case; tests all new sections |
| **Metformin** | Mature drug; all data available; good baseline |
| **Osimertinib** | Biomarker-dependent; tests Section 5.6 |
| **Warfarin** | Drug-food interactions; tests Section 6.5.2 |
| **Investigational** | ChEMBL only; tests graceful degradation |

**Test Checklist Per Compound**:
- [ ] All new sections populated
- [ ] Fallbacks work when data unavailable
- [ ] Evidence tiers correct
- [ ] Citations present
- [ ] Completeness audit runs
- [ ] No validation errors

---

## Timeline Summary

| Phase | LOE | Deliverables |
|-------|-----|--------------|
| **Phase 1** | 2-3 days | 6 enhancements with existing tools |
| **Phase 2** | 1.5 days | 4 workaround implementations |
| **Phase 3** | 1.5 days | 2 new parser tools |
| **Phase 4** | N/A | Document 3 blocked items |
| **Testing** | 1 day | 5 compounds × 4 enhancements |
| **Documentation** | 0.5 day | Update SKILL.md, examples |

**Total**: 6.5-7.5 days to implement 12/15 enhancements (80%)

---

## Success Metrics

After implementation:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Section completeness | 95%+ | All 15 sections in template |
| Tool coverage | 85%+ | 13/15 enhancements implemented |
| Evidence quality | 70%+ T1/T2 | Evidence tier distribution |
| Fallback success | 100% | All fallback chains work |
| Test pass rate | 100% | All 5 test compounds pass |

---

## Maintenance Plan

**Monthly**:
- Check for new DailyMed/FDA tool releases
- Update fallback chains if APIs change
- Add new comparator drugs to competitive analysis

**Quarterly**:
- Re-test with latest tool versions
- Update evidence tier thresholds if needed
- Review completeness audit checklist

**Yearly**:
- Reassess blocked items (Phases 4) for API availability
- Update regulatory timeline sources (EMA, PMDA)
- Benchmark against industry standards

---

## Next Steps

**Recommended Sequence**:

1. **Week 1**: Implement Phase 1 (6 items with existing tools)
   - Start with #5 (Biomarkers) - highest clinical value
   - End with #14 (Comparative) - most complex

2. **Week 2**: Implement Phase 2 (4 workarounds)
   - Validate XML parsing approach
   - Document limitations clearly

3. **Week 3**: Develop Phase 3 (2 new parsers)
   - Test parser tools independently first
   - Integrate into skill workflow

4. **Week 4**: Testing & documentation
   - Run all 5 test compounds
   - Update SKILL.md with new sections
   - Write EXAMPLES.md with real outputs

**Total**: 4 weeks to production-ready skill with 80% enhancement coverage

---

## Questions?

- Which phase should we start with?
- Do you want to prioritize certain enhancements?
- Should we test with specific compounds of interest?
