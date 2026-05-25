# Using Medical Research Toolkit in OpenClaw

Once installed, the toolkit documentation is automatically available to you.

## Quick Reference

When you ask OpenClaw research questions, it will use the toolkit's database guides to help.

### Example Queries

**Find drugs for a disease:**
> "What drugs are being tested for myasthenia gravis? Include clinical trials and approved drugs."

**Discover targets:**
> "What genes are associated with myasthenia gravis? Find the top targets with evidence."

**Literature search:**
> "Find recent papers on complement inhibitors in myasthenia gravis. What's the latest research?"

**Drug safety check:**
> "Is eculizumab safe? Check FDA adverse events and clinical data."

**Full repurposing analysis:**
> "I want to find drug repurposing candidates for myasthenia gravis. Check: disease targets (OpenTargets), drugs targeting those genes (ChEMBL), ongoing trials (ClinicalTrials), safety profile (OpenFDA), and recent literature (PubMed). Synthesize the results."

## Documentation Access

The toolkit provides:

- **SKILL.md** — Quick start + recipes
- **6 Database Guides** — Detailed references (PubMed, ChEMBL, OpenTargets, etc.)
- **1 Complete Workflow** — Full drug repurposing example
- **Troubleshooting** — Common issues and solutions

All available in the skill files for reference.

## Tips

- **Start simple** — Use a quick recipe from SKILL.md
- **Add filters** — Specify recruitment status, phase, evidence level
- **Cross-reference** — Use one database to find IDs for another
- **Build incrementally** — Combine multiple API calls for deeper analysis

## Offline Access

All documentation is local (no internet required to read):
- SKILL.md — Main guide
- references/*.md — Database deep dives
- scripts/*.md — Complete workflow examples