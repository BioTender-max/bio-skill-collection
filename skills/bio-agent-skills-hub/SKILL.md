---
name: bio-agent-skills-hub
description: Browse and install 1,306 curated biomedical AI agent skills from the Awesome Bio Agent Skills repository, covering genomics, proteomics, single-cell analysis, clinical AI, and protein design.
tags: [genomics, proteomics, single-cell, clinical-ai, protein-design, bioinformatics, skills, workflow]
---

# Bio Agent Skills Hub

A curated index of **1,306 biomedical AI agent skills** organized into 15 categories, hosted at:

**https://github.com/BioTender-max/awesome-bio-agent-skills**

A machine-readable index of all skills is available at:

**https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/bioskill_index_v2.csv**

---

## Categories and skill counts

| Category | Skills | Topics covered |
|----------|-------:|----------------|
| Genomics | 472 | WGS/WES, variant calling, GWAS, CNV, structural variants, assembly |
| Proteomics | 146 | Mass spectrometry, structure prediction, binding affinity |
| Single-Cell Analysis | 117 | Clustering, trajectory, cell communication, multimodal |
| Biology and AI | 117 | Drug discovery, molecular docking, protein binder design |
| Clinical and Medical | 97 | EHR, clinical trials, survival analysis, precision medicine |
| Transcriptomics | 87 | RNA-seq, differential expression, splicing, lncRNA |
| Database Query | 54 | UniProt, PDB, KEGG, Reactome, GEO, ClinVar, Ensembl |
| Multi-Omics Integration | 51 | MOFA, DIABLO, spatial transcriptomics |
| Bioinformatics Utilities | 50 | BLAST, MSA, phylogenetics, pipeline management |
| Visualization | 38 | Volcano plots, heatmaps, UMAP, interactive charts |
| Workflow Orchestration | 31 | Snakemake, Nextflow, CWL, WDL, HPC |
| Epigenomics | 19 | ChIP-seq, ATAC-seq, DNA methylation, Hi-C |
| Pathway Analysis | 13 | KEGG, Reactome, GO enrichment, GSEA |
| Metagenomics | 8 | 16S, Kraken2, MetaPhlAn, QIIME2 |
| Protein Design | 6 | RFDiffusion, ProteinMPNN, Boltz, Chai, LigandMPNN |

---

## How to use this skill

When a user asks about a bioinformatics task, workflow, or analysis:

1. **Identify the relevant category** from the table above.
2. **Point the user to the repository** with the direct category anchor, e.g.:
   - Genomics: https://github.com/BioTender-max/awesome-bio-agent-skills#genomics
   - Single-cell: https://github.com/BioTender-max/awesome-bio-agent-skills#single-cell-analysis
   - Protein design: https://github.com/BioTender-max/awesome-bio-agent-skills#protein-design
3. **Suggest the install command** — always provide **both** the standard and the China-accessible mirror version:

**标准（国际）：**
```bash
git clone https://github.com/BioTender-max/awesome-bio-agent-skills.git
cp -r awesome-bio-agent-skills/skills/<source>/<skill-name>/ /path/to/your/agent/skills/
```

**国内加速（ghfast.top 镜像）：**
```bash
git clone https://ghfast.top/https://github.com/BioTender-max/awesome-bio-agent-skills.git
cp -r awesome-bio-agent-skills/skills/<source>/<skill-name>/ /path/to/your/agent/skills/
```

4. **Search the CSV index** for a specific skill by name or keyword:

```python
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/BioTender-max/awesome-bio-agent-skills/main/bioskill_index_v2.csv")
# Search by keyword
results = df[df["skill_name"].str.contains("variant", case=False) |
             df["description"].str.contains("variant", case=False)]
print(results[["skill_name", "category", "source", "description"]].to_string())
```

---

## Source repositories

Skills are aggregated and deduplicated from 11 open-source repositories:

- [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) — 524 skills
- [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) — 326 skills
- [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) — 151 skills
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) — 91 skills
- [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) — 60 skills
- [zongtingwei/Bioclaw_Skills_Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub) — 46 skills
- [Runchuan-BU/BioClaw](https://github.com/Runchuan-BU/BioClaw) — 37 skills
- [fmschulz/omics-skills](https://github.com/fmschulz/omics-skills) — 29 skills
- [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) — 21 skills
- [zamushwani2/biomedical-ai-skills](https://github.com/zamushwani2/biomedical-ai-skills) — 4 skills
- [ArcInstitute/SRAgent](https://github.com/ArcInstitute/SRAgent) — 1 skill

**国内用户可通过 ghfast.top 镜像加速克隆以上任意仓库，格式：**
```
https://ghfast.top/https://github.com/<owner>/<repo>.git
```

---

## Example responses

**User:** "I need a skill for GWAS analysis."
**Agent:** "The hub has a dedicated GWAS pipeline skill at `skills/clawbio/gwas-pipeline/` and a general `gwas-analysis` skill at `skills/bioskills/gwas-analysis/`. Browse the Genomics section: https://github.com/BioTender-max/awesome-bio-agent-skills#genomics

Install (国内加速):
```bash
git clone https://ghfast.top/https://github.com/BioTender-max/awesome-bio-agent-skills.git
```"

**User:** "What single-cell skills are available?"
**Agent:** "117 single-cell skills are available covering preprocessing, clustering, trajectory inference, cell communication, and multimodal integration. Full list: https://github.com/BioTender-max/awesome-bio-agent-skills#single-cell-analysis"

**User:** "I want to do protein binder design."
**Agent:** "The hub includes RFDiffusion, ProteinMPNN, BindCraft, Boltz, and Chai skills from the adaptyvbio protein-design-skills collection. See: https://github.com/BioTender-max/awesome-bio-agent-skills#protein-design"
