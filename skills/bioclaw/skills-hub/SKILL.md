---
name: skills-hub
description: Browse and install community skills from the BioClaw Skills Hub. Use when a user's task is not covered by built-in skills, or when the user asks about available skills, advanced workflows, or specialized analysis pipelines. Triggers on "skills hub", "more skills", "install skill", "community skills", "find a skill for".
---

# Skills Hub Browser

Search, browse, and install community-contributed skills from the [BioClaw Skills Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub).

The Hub contains 70+ specialized bioinformatics skills organized into domains. Skills downloaded from the Hub are cached locally so they persist for the rest of the session.

## When to Use

- User requests an analysis not covered by the built-in skills listed in your system prompt
- User asks "what other skills are available" or "do you have a skill for X"
- User needs a specialized pipeline (e.g., protein design, EHR analysis, spatial transcriptomics workflows beyond the built-in)

## Hub Structure

The Hub organizes skills into these domains:

| Domain | Examples |
|--------|----------|
| `core-bioinformatics` | alignment-and-mapping, read-qc, sequence-io, database-access |
| `transcriptomics` | bulk-rna-expression, differential-expression |
| `single-cell-and-spatial` | scrna-preprocessing, spatial-transcriptomics, cell-annotation |
| `epigenomics-and-regulation` | atac-seq, chip-seq, dna-methylation |
| `genomics-and-variation` | variant-calling, genome-assembly, long-read-genomics |
| `metagenomics-and-microbiome` | metagenomics, phylogenetics, microbial-community |
| `proteomics-and-metabolomics` | mass-spec, metabolomics |
| `multi-omics-and-systems` | multi-omics-integration, pathway-analysis |
| `protein-design` | alphafold2-multimer, proteinmpnn, rfdiffusion, boltzgen |
| `ehr-analysis` | electronic health record analysis |

## How to Execute

### Step 1: Fetch the taxonomy (skill index)

```bash
curl -sL "https://raw.githubusercontent.com/zongtingwei/Bioclaw_Skills_Hub/main/catalog/taxonomy.yaml"
```

This returns the full skill catalog organized by domain. Use it to find the skill name that matches the user's need.

### Step 2: List skills in a specific domain

```bash
curl -sL "https://api.github.com/repos/zongtingwei/Bioclaw_Skills_Hub/contents/skills/<domain>" | python3 -c "
import json, sys
for item in json.load(sys.stdin):
    if item['type'] == 'dir':
        print(item['name'])
"
```

Replace `<domain>` with a domain name from the table above.

### Step 3: Download and read a skill

```bash
# Download the SKILL.md
DOMAIN="<domain>"
SKILL="<skill-name>"
CACHE_DIR="/workspace/group/.hub-skills/${SKILL}"
mkdir -p "${CACHE_DIR}"
curl -sL "https://raw.githubusercontent.com/zongtingwei/Bioclaw_Skills_Hub/main/skills/${DOMAIN}/${SKILL}/SKILL.md" \
  -o "${CACHE_DIR}/SKILL.md"
```

Then read the downloaded skill:
```
read_file({ file_path: "/workspace/group/.hub-skills/<skill-name>/SKILL.md" })
```

### Step 4: Install dependencies (if needed)

Some Hub skills require extra Python packages. Check the SKILL.md for a "Preferred Tools" or "Dependencies" section. Install with:

```bash
pip install <package> --quiet 2>/dev/null
```

### Step 5: Execute the skill

Follow the workflow described in the downloaded SKILL.md, just like any built-in skill.

## Important Notes

- Always check built-in skills first before fetching from the Hub
- Downloaded skills are cached in `/workspace/group/.hub-skills/` for the session
- The Hub is a community resource — skills may reference tools not installed in the container; install them with pip/apt as needed
- If GitHub is unreachable, inform the user and suggest using built-in skills instead
