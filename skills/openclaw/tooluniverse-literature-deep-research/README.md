# Literature Deep Research Skill (Enhanced)

> Comprehensive literature research with **target disambiguation**, **evidence grading**, **mandatory completeness checklist**, and **biological model synthesis**. Produces detailed reports focused on content, not methodology.

**Type**: Strategy Skill (for AI agents)  
**Version**: 5.0.0  
**Last Updated**: 2026-02-04

---

## Key Features (v5.0)

| Feature | Description |
|---------|-------------|
| **Target Disambiguation** | Resolve IDs, synonyms, naming collisions BEFORE literature search |
| **Evidence Grading** | T1-T4 tiers for every claim (mechanistic → mention) |
| **Mandatory Completeness** | 15 required sections; must state "limited evidence" if empty |
| **Collision-Aware Search** | High-precision seeds + negative filters for ambiguous names |
| **Citation-Network First** | For sparse targets, expand via citations before broad keyword search |
| **Biological Model** | Synthesize evidence into 3-5 testable hypotheses |
| **Report-Only Output** | Methodology in separate appendix only if requested |
| **Scalable Bibliography** | Narrative stays readable; full bibliography in JSON/CSV |

---

## When to Use This Skill

Apply when users:
- Ask "what does the literature say about [target/topic]?"
- Need comprehensive literature coverage on a biological target
- Request target profiles or druggability assessments
- Want research gaps and testable hypotheses identified
- Need literature for grant writing with evidence grades

---

## Workflow Overview

```
Phase 0: CLARIFY
  └─ Is this a biological target? What scope? Methods appendix needed?

Phase 1: TARGET DISAMBIGUATION (default ON for biological targets)
  ├─ Resolve official IDs (UniProt, Ensembl, NCBI, ChEMBL)
  ├─ Gather synonyms + identify naming collisions
  ├─ Get protein architecture, expression, pathways
  └─ Output: Target Profile + Collision-aware search plan

Phase 2: LITERATURE SEARCH (internal - not shown in report)
  ├─ High-precision seed queries (build mechanistic core)
  ├─ Citation network expansion from seeds
  ├─ Collision-filtered broader queries
  └─ Theme clustering + evidence grading

Phase 3: REPORT SYNTHESIS
  ├─ Progressive writing with mandatory sections
  ├─ Apply evidence grades (T1-T4)
  └─ Generate biological model + testable hypotheses

OUTPUT:
  - [topic]_report.md (main deliverable)
  - [topic]_bibliography.json (full papers)
  - methods_appendix.md (only if requested)
```

---

## Evidence Grading System

| Tier | Symbol | Criteria | Example |
|------|--------|----------|---------|
| **T1** | ★★★ | Mechanistic study with direct evidence | CRISPR KO + rescue |
| **T2** | ★★☆ | Functional study showing role | siRNA phenotype |
| **T3** | ★☆☆ | Association/screen hit | GWAS, DepMap |
| **T4** | ☆☆☆ | Review/mention/text-mined | Review article |

**In report**:
```markdown
ATP6V1A drives lysosomal acidification [★★★: PMID:12345678] and regulates
autophagy [★★☆: PMID:23456789].
```

---

## Mandatory Report Sections

**ALL 15 sections required** - state "limited evidence" if data unavailable:

1. **Identity/Aliases** - IDs, synonyms, collisions
2. **Protein Architecture** - Domains, isoforms, sites
3. **Complexes/Partners** - Interactors with evidence type
4. **Subcellular Localization** - Locations with confidence
5. **Expression Profile** - Tissues, specificity
6. **Core Mechanisms** - Function with evidence grades
7. **Model Organism Evidence** - KO phenotypes or "none found"
8. **Human Genetics/Variants** - Constraints, ClinVar, GWAS
9. **Disease Links** - With evidence strength grades
10. **Pathogens** - Or "none identified"
11. **Key Assays/Readouts** - Available assays
12. **Research Themes** - ≥3 papers per theme
13. **Open Questions/Gaps** - What's unknown
14. **Biological Model** - Integrated synthesis + 3-5 hypotheses
15. **Conclusions** - Confidence assessment

---

## Output Files

| File | Content | Generated |
|------|---------|-----------|
| `[topic]_report.md` | Main narrative report | Always (default deliverable) |
| `[topic]_bibliography.json` | Full deduplicated papers | Always |
| `[topic]_bibliography.csv` | Tabular bibliography | Always |
| `methods_appendix.md` | Methodology details | Only if user requests |

---

## Files in This Skill

| File | Purpose |
|------|---------|
| **[SKILL.md](SKILL.md)** | Complete strategy guide |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | One-page cheat sheet |
| **[TOOL_NAMES_REFERENCE.md](TOOL_NAMES_REFERENCE.md)** | Database tool names |
| **README.md** | Overview (this file) |

---

## Tool Categories Used

### Literature Search
`PubMed_search_articles`, `EuropePMC_search_articles` (use `source='PPR'` for preprints), `openalex_literature_search`, `SemanticScholar_search_papers`

### Citation Analysis (with fallbacks)
`PubMed_get_cited_by` → `EuropePMC_get_citations`
`PubMed_get_related` → `SemanticScholar_search_papers`

### Annotation (fills gaps when literature sparse)
`UniProt_*`, `InterPro_get_protein_domains`, `GTEx_*`, `HPA_*`, `GO_*`, `Reactome_*`, `OpenTargets_*`

---

## What Changed in v5.0

| Previous | Enhanced |
|----------|----------|
| Literature search first | Target disambiguation first (default ON) |
| All papers treated equally | Evidence grading (T1-T4) |
| Optional sections | Mandatory completeness checklist |
| Simple keyword search | Collision-aware query strategy |
| Keyword expansion | Citation-network-first for sparse targets |
| Embedded methodology | Report-only; methodology in appendix |
| Inline bibliography | Separate scalable JSON/CSV files |
| Descriptive report | Biological model + testable hypotheses |
| Any OA check method | Best-effort OA with clear labeling |

---

## Quality Checklist (Must Pass)

- [ ] All 15 mandatory sections present (or marked "limited evidence")
- [ ] Evidence grades applied to all major claims
- [ ] Target identifiers resolved
- [ ] Naming collisions documented
- [ ] ≥3 papers per research theme (or noted as insufficient)
- [ ] Biological model synthesized
- [ ] ≥3 testable hypotheses with experiments
- [ ] Bibliography files generated
- [ ] Methodology NOT in main report

---

## Example: What Makes a Good Report

**Section with proper evidence grading**:
```markdown
## 6. Core Mechanisms

### 6.1 Molecular Function
ATP6V1A is the catalytic A subunit of the V-ATPase complex, responsible for 
ATP hydrolysis that drives proton translocation [★★★: PMID:12345678].

**Evidence Quality**: Strong (5 mechanistic, 2 functional studies)

### 6.2 Biological Role  
V-ATPase acidification of lysosomes is essential for:
- Autophagosome-lysosome fusion [★★★: PMID:23456789]
- mTORC1 activation via amino acid sensing [★★☆: PMID:34567890]
- Bone resorption by osteoclasts [★★★: PMID:45678901]
```

**Testable hypothesis**:
```markdown
| # | Hypothesis | Perturbation | Readout | Expected | Priority |
|---|------------|--------------|---------|----------|----------|
| 1 | ATP6V1A loss impairs autophagy | siRNA knockdown | LC3 puncta, p62 levels | ↑LC3-II, ↑p62 | HIGH |
| 2 | V-ATPase inhibition blocks mTORC1 | Bafilomycin A1 | S6K phosphorylation | ↓pS6K | HIGH |
```

---

## Getting Started

1. Read [SKILL.md](SKILL.md) for complete strategy
2. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) during execution
3. Check [TOOL_NAMES_REFERENCE.md](TOOL_NAMES_REFERENCE.md) for exact tool names

---

*Version 5.0.0 - Enhanced with target disambiguation, evidence grading, and biological model synthesis*
