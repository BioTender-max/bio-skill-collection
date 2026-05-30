---
name: bio-agent-skills-hub
description: >-
  Discover and invoke 1,676 deduplicated biomedical AI agent skills from the
  Awesome Bio Agent Skills repository (20 source repos, 15 categories). Use this
  skill as a router whenever a user needs a bioinformatics/biomedical task
  (genomics, transcriptomics, single-cell, proteomics, protein design, clinical,
  epigenomics, multi-omics, pathway, metagenomics, database queries,
  visualization, workflows): search the index, locate the best-matching skill,
  fetch its SKILL.md, and follow it.
tags: [genomics, transcriptomics, single-cell, proteomics, protein-design, clinical-ai, epigenomics, multi-omics, pathway, metagenomics, database-query, visualization, workflow, bioinformatics, skills, router, index]
---

# Bio Agent Skills Hub

A **router/index skill** over **1,676 deduplicated biomedical AI agent skills**, aggregated and
deduplicated from **20 open-source repositories** into **15 categories**. Each skill is a
self-contained `SKILL.md` folder compatible with Claude-based agent frameworks.

- Repository: **https://github.com/BioTender-max/awesome-bio-agent-skills**
- Machine-readable index (authoritative): **`https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/bioskill_index_v3.csv`** (1,676 rows)

> This skill does **not** duplicate the 1,676 skills. It tells the agent how to (1) **search** the
> index, (2) **locate** the single best-matching skill, (3) **fetch** that skill's `SKILL.md` on
> demand, and (4) **follow** it. Skill bodies are fetched from GitHub on demand; a `git clone`
> fallback (incl. a China mirror) is provided for offline / bulk / private use.

---

## How to use this skill (router workflow)

When a user asks for any bioinformatics task, workflow, or analysis:

### Step 1 — Search the index to find candidate skills

The index has columns: `skill_name, folder_name, source_repo, category, description, file_count, archive_path`.
`archive_path` = `<source_repo>/<folder_name>` and is the path under `skills/`.

Search **`skill_name` + `description` + `category` + `source_repo`** together (descriptions contain
rich "Use when..." text), and present ranked candidates with their **category** and **`archive_path`**
so the right one can be chosen:

```python
import pandas as pd

# Authoritative v3 index. Prefer a local copy if this skill bundles one; else read from GitHub raw.
INDEX_URL = "https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/bioskill_index_v3.csv"
df = pd.read_csv(INDEX_URL)   # 1,676 rows

def search_skills(query, category=None, source=None, top=15):
    """Keyword search over name+description+category+source. Returns candidate skills."""
    q = query.lower()
    hay = (df["skill_name"].fillna("") + " | " +
           df["description"].fillna("") + " | " +
           df["category"].fillna("") + " | " +
           df["source_repo"].fillna("")).str.lower()
    hits = df[hay.str.contains(q, regex=False)].copy()
    if category:
        hits = hits[hits["category"] == category]
    if source:
        hits = hits[hits["source_repo"] == source]
    # rank: name match first, then description match
    hits["_name_hit"] = hits["skill_name"].str.lower().str.contains(q, regex=False)
    hits = hits.sort_values(["_name_hit", "file_count"], ascending=[False, False])
    return hits[["skill_name", "category", "source_repo", "archive_path", "description"]].head(top)

print(search_skills("variant calling").to_string(index=False))
```

If nothing matches, broaden the query (try a synonym), or filter by `category` (see the table below)
and browse that category's README section.

### Step 2 — Fetch the chosen skill's SKILL.md (content on demand)

Once you pick a candidate's `archive_path` (e.g. `bioskills/clair3-variants`):

```python
import urllib.request

archive_path = "bioskills/clair3-variants"   # from the search result
url = f"https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/skills/{archive_path}/SKILL.md"
skill_md = urllib.request.urlopen(url, timeout=30).read().decode()
print(skill_md)   # read it, then follow its instructions
```

Some skills ship supporting files (`scripts/`, `references/`); list a folder via the GitHub API or
clone it (Step 3) if you need them.

### Step 3 — Offline / bulk / private fallback (clone)

If raw fetch is unavailable, or you want all supporting files, clone and copy the skill folder:

**Standard (international):**
```bash
git clone https://github.com/BioTender-max/awesome-bio-agent-skills.git
cp -r awesome-bio-agent-skills/skills/<archive_path>/ /path/to/your/agent/skills/
```

**China-accelerated (ghfast.top mirror)** — prepend the mirror to the GitHub URL; works for cloning
this or any source repo (`https://ghfast.top/https://github.com/<owner>/<repo>.git`):
```bash
git clone https://ghfast.top/https://github.com/BioTender-max/awesome-bio-agent-skills.git
cp -r awesome-bio-agent-skills/skills/<archive_path>/ /path/to/your/agent/skills/
```

---

## Categories (15) — counts and where to browse

Filter searches with the `category` **key** (left column). README section links jump to the
browsable table for that category.

| Category (`key`) | Skills | README section | Topics |
|------------------|-------:|----------------|--------|
| `genomics` | 526 | [Genomics](https://github.com/BioTender-max/awesome-bio-agent-skills#genomics) | WGS/WES, variant calling, GWAS, CNV, structural variants, alignment, assembly |
| `biology-other` | 236 | [Biology and AI](https://github.com/BioTender-max/awesome-bio-agent-skills#biology-and-ai) | Drug discovery, molecular docking, protein binder design, cheminformatics |
| `proteomics` | 167 | [Proteomics](https://github.com/BioTender-max/awesome-bio-agent-skills#proteomics) | Mass spectrometry, structure prediction (AlphaFold/ESM), binding affinity |
| `clinical` | 152 | [Clinical and Medical](https://github.com/BioTender-max/awesome-bio-agent-skills#clinical-and-medical) | EHR, clinical trials, survival analysis, ACMG, precision medicine |
| `single-cell` | 144 | [Single-Cell Analysis](https://github.com/BioTender-max/awesome-bio-agent-skills#single-cell-analysis) | scRNA-seq QC, clustering, trajectory, cell communication, spatial, multimodal |
| `transcriptomics` | 97 | [Transcriptomics](https://github.com/BioTender-max/awesome-bio-agent-skills#transcriptomics) | Bulk RNA-seq, differential expression, splicing, lncRNA, isoforms |
| `bioinformatics-general` | 86 | [Bioinformatics Utilities](https://github.com/BioTender-max/awesome-bio-agent-skills#bioinformatics-utilities) | BLAST, MSA, phylogenetics, sequence utilities, stats libraries |
| `multi-omics` | 69 | [Multi-Omics Integration](https://github.com/BioTender-max/awesome-bio-agent-skills#multi-omics-integration) | MOFA, DIABLO, integration, spatial multi-omics |
| `database-query` | 63 | [Database Query](https://github.com/BioTender-max/awesome-bio-agent-skills#database-query) | UniProt, PDB, KEGG, Reactome, GEO, ClinVar, Ensembl, dbSNP |
| `visualization` | 48 | [Visualization](https://github.com/BioTender-max/awesome-bio-agent-skills#visualization) | Volcano plots, heatmaps, UMAP, genome tracks, interactive charts |
| `workflow` | 38 | [Workflow Orchestration](https://github.com/BioTender-max/awesome-bio-agent-skills#workflow-orchestration) | Snakemake, Nextflow, CWL, WDL, HPC orchestration, lab automation |
| `epigenomics` | 19 | [Epigenomics](https://github.com/BioTender-max/awesome-bio-agent-skills#epigenomics) | ChIP-seq, ATAC-seq, DNA methylation, Hi-C, chromatin state |
| `pathway` | 15 | [Pathway Analysis](https://github.com/BioTender-max/awesome-bio-agent-skills#pathway-analysis) | KEGG, Reactome, GO enrichment, GSEA |
| `metagenomics` | 9 | [Metagenomics](https://github.com/BioTender-max/awesome-bio-agent-skills#metagenomics) | 16S, Kraken2/Bracken, MetaPhlAn, QIIME2 |
| `protein-design` | 7 | [Protein Design](https://github.com/BioTender-max/awesome-bio-agent-skills#protein-design) | RFdiffusion, ProteinMPNN, Boltz, Chai, LigandMPNN |

---

## Source repositories (20)

Skills are aggregated and deduplicated from these repositories. Use the `source_repo` **key** to
filter the index. (`bio-agent-skills-hub` is this self-referential hub entry.)

| Source repo (`source_repo`) | Skills | Focus |
|-----------------------------|-------:|-------|
| `bioskills` — [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | 536 | Systematic bioinformatics suite from QC to multi-omics. |
| `openclaw` — [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | 359 | Medical AI library aggregating 12 specialized sub-repositories. |
| `sciagent` — [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | 154 | Statistics, databases, and clinical decision skills. |
| `kdense` — [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 102 | General scientific computing and HPC workflow skills. |
| `neuroclaw` — [CUHK-AIM-Group/NeuroClaw](https://github.com/CUHK-AIM-Group/NeuroClaw) | 86 | Neuroimaging: sMRI, fMRI, dMRI, EEG (BIDS, FreeSurfer, FSL, fMRIPrep). |
| `clawbio` — [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | 63 | Bioinformatics workflow orchestration for GWAS and single-cell. |
| `labclaw` — [wu-yc/LabClaw](https://github.com/wu-yc/LabClaw) | 59 | Lab automation and biomedical research skills. |
| `drugclaw` — [QSong-github/DrugClaw](https://github.com/QSong-github/DrugClaw) | 57 | Drug intelligence: DTI, ADR, DDI, pharmacogenomics, repurposing. |
| `nobel` — [ChrisLou-bioinfo/nobel-medicine-minds](https://github.com/ChrisLou-bioinfo/nobel-medicine-minds) | 55 | Cognitive frameworks of Nobel Medicine laureates as SKILL.md. |
| `bioclaw_hub` — [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) | 46 | Ten-category biological skills hub. |
| `bioclaw` — [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) | 37 | Core bioinformatics tools and database query skills. |
| `omics` — [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) | 29 | Single-cell and spatial omics specialized skills. |
| `omicsclaw` — [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | 28 | 6-omics domain skills: spatial, scRNA, bulk RNA, genomics, proteomics, metabolomics. |
| `adaptyv` — [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | 21 | Protein design toolkit: RFdiffusion, ProteinMPNN, Boltz, Chai. |
| `pantheon` — [aristoteleo/PantheonOS](https://github.com/aristoteleo/PantheonOS) | 18 | Single-cell and spatial transcriptomics (Dynamo/Spateo team). |
| `evoskills` — [EvoScientist/EvoSkills](https://github.com/EvoScientist/EvoSkills) | 13 | Research-lifecycle skills: ideation, planning, execution, writing, review. |
| `medgeclaw` — [xjtulyc/MedgeClaw](https://github.com/xjtulyc/MedgeClaw) | 7 | Biomedical research skills with dashboard, RStudio, JupyterLab integration. |
| `zamushwani` — [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) | 4 | Cancer multi-omics analysis skills in R. |
| `bio-agent-skills-hub` — [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | 1 | Self-referential hub skill that indexes this collection. |
| `sragent` — [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) | 1 | Intelligent SRA and GEO dataset retrieval. |

---

## Example interactions

**User:** "I need a GWAS pipeline."
**Agent:** `search_skills("gwas")` → top hit `bio-workflows-gwas-pipeline` (`genomics`,
`bioskills/gwas-pipeline`); also `gwas-pipeline` (`clawbio/gwas-pipeline`) and `plink2-gwas-analysis`
(`sciagent/plink2-gwas-analysis`). Fetch
`https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/skills/bioskills/gwas-pipeline/SKILL.md` and follow it. Browse more: https://github.com/BioTender-max/awesome-bio-agent-skills#genomics

**User:** "Preprocess and cluster my scRNA-seq data."
**Agent:** `search_skills("scrna preprocessing", category="single-cell")` →
`scrna-preprocessing-clustering` (`bioclaw/scrna-preprocessing-clustering`). Fetch its SKILL.md and
follow it. 144 single-cell skills total: https://github.com/BioTender-max/awesome-bio-agent-skills#single-cell-analysis

**User:** "Design a protein binder backbone."
**Agent:** `search_skills("rfdiffusion")` → `rfdiffusion` (`protein-design`, `adaptyv/rfdiffusion`).
Related: `proteinmpnn` (`adaptyv/proteinmpnn`), `bindcraft` (`adaptyv/bindcraft`). Fetch the SKILL.md
for the chosen tool. Browse: https://github.com/BioTender-max/awesome-bio-agent-skills#protein-design

**User:** "Call variants from long reads."
**Agent:** `search_skills("variant calling", category="genomics")` →
`bio-long-read-sequencing-clair3-variants` (`bioskills/clair3-variants`); for short reads see
`bio-variant-calling-deepvariant` (`bioskills/deepvariant`). Fetch and follow.

---

## Notes

- The index (`bioskill_index_v3.csv`) is the single source of truth for what exists and where; always
  resolve `archive_path` from it rather than guessing folder names.
- Counts above (1,676 skills / 20 sources / 15 categories) match the repository README and index.
- Content fetch requires network access and a public repository; use the clone fallback otherwise.
