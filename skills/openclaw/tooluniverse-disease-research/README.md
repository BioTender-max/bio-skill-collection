# ToolUniverse Disease Research Skill

Generate comprehensive, detailed disease research reports with full source citations using 100+ ToolUniverse tools.

## Key Principles

1. **Report-First**: Create a markdown file first, then populate it during research
2. **Progressive Updates**: Update the report file after each research dimension
3. **Full Citations**: Every data point references its source tool
4. **Comprehensive**: Use ALL relevant tools, not just a subset
5. **No Process Display**: Don't show the search process, just deliver the report

## Workflow

```
User: "Research Parkinson's disease"

Agent (internal actions - NOT shown to user):
1. Create "parkinsons_disease_research_report.md"
2. Research each of 10 dimensions
3. Update report file after each dimension
4. Track all tool usage for references

Agent (to user):
→ Presents final comprehensive report
```

## Report Structure (10 Sections)

| # | Section | Tools Used | Content |
|---|---------|------------|---------|
| 1 | Identity & Classification | OSL, OLS, UMLS, ICD, SNOMED | IDs, synonyms, hierarchy |
| 2 | Clinical Presentation | OpenTargets, HPO, MedlinePlus | Phenotypes, symptoms |
| 3 | Genetic Basis | OpenTargets, ClinVar, GWAS | Genes, variants, associations |
| 4 | Treatment Landscape | OpenTargets, ClinicalTrials, GtoPdb | Drugs, trials, pipeline |
| 5 | Pathways & Mechanisms | Reactome, HumanBase, GTEx, HPA | Pathways, PPI, expression |
| 6 | Literature | PubMed, OpenAlex, Europe PMC | Publications, trends |
| 7 | Similar Diseases | OpenTargets | Related conditions |
| 8 | Cancer-Specific | CIViC | Variants, evidence (if cancer) |
| 9 | Pharmacology | GtoPdb | Targets, interactions |
| 10 | Drug Safety | OpenTargets, FAERS | Warnings, adverse events |

## Citation Format

Every data point includes its source:

```markdown
| Gene | Score | Source |
|------|-------|--------|
| APOE | 0.92 | OpenTargets_get_associated_targets_by_disease_efoId |
```

## Report Size

A comprehensive disease report should include:
- 500+ individual data points
- All 10 sections populated
- Complete references section
- 2000+ lines for major diseases

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete protocol with tool usage |
| `TOOLS_REFERENCE.md` | Tool documentation and examples |
| `EXAMPLES.md` | Sample report outputs |
| `README.md` | This overview |

## When to Use

- User asks about any disease/syndrome
- Need comprehensive disease intelligence
- Want detailed report with citations
- Researching disease mechanisms, genetics, or treatments
