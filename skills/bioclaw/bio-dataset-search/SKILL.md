# bio-dataset-search

**Step 3: Dataset search and task matching (数据集搜索与匹配)**

Find suitable datasets for each task and map datasets to the task system defined earlier in the manuscript pipeline.

## Purpose

1. Extract datasets from related papers when possible
2. Search public repositories directly when needed
3. Normalize dataset metadata into a common structure
4. Match datasets to tasks in a defendable way

## Input Format

```text
topic: [research topic]
task_system: [task system from Step 2]
paper_count: [number of related papers]
existing_papers: [optional list of related papers]
```

## Workflow

### Step 3.1: Extract datasets from existing work

If `paper_count >= 5`, start from the strongest existing papers.

Read Methods / Data Availability sections and extract:

- dataset name
- data source
- platform
- modality
- sample scale
- download path
- annotation availability

### Step 3.2: Search datasets directly

If there is not enough prior work, search repositories such as:

- GEO
- ArrayExpress
- project-specific public portals

Use keyword sets built from:

- topic
- modality
- tissue / disease
- benchmark intent

### Step 3.3: Normalize dataset metadata

For each dataset, record:

- source
- platform
- species
- tissue / disease
- sample size
- feature count
- modalities
- annotation quality
- histology / region metadata
- format
- preprocessing needs
- recommended task fit

### Step 3.4: Match datasets to tasks

A good match should satisfy:

1. Every major task has at least one viable dataset
2. Dataset structure matches the task's technical assumptions
3. Download remains feasible
4. Metadata quality is sufficient for evaluation
5. Prefer at least one backup dataset per important task

## Output Format

```markdown
# Dataset Catalog

## Data Sources
- Extracted from related papers:
- Direct repository search:
- Borrowed from adjacent domains:

## Dataset Entries

### Dataset 1: [name]
- Source:
- Platform:
- Species:
- Tissue / disease:
- Modalities:
- Sample scale:
- Annotation quality:
- Download URL:
- Format:
- Recommended tasks:
- Why it fits:

## Dataset-Task Mapping
| Task | Recommended dataset | Why it fits | Notes |
|------|---------------------|-------------|-------|
| ... | ... | ... | ... |

## Acquisition Notes
- GEO download hints
- Public portal download hints

## Preprocessing Recommendations
| Dataset | Preprocessing needs | Suggested skill / tool |
|---------|---------------------|------------------------|
| ... | ... | ... |

## Next Step
- Build the metric system in Step 4
```

## Usage

```bash
/bio-dataset-search "spatial multi-omics integration | paper_count: 5 | task_system: [task system from Step 2]"
```

## Notes

1. Prefer datasets already used in related work when possible.
2. Verify links before committing them to the benchmark plan.
3. Capture QC and annotation metadata whenever available.
4. Match datasets to tasks based on actual experimental needs, not just popularity.
