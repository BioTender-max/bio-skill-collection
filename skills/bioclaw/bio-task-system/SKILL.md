# bio-task-system

**Step 2: Task system design (任务体系构建)**

Identify the main task categories in the field and organize them into a staged difficulty ladder.

## Purpose

1. Find the dominant task taxonomy in the target field
2. Define Level 1-4 task tiers
3. Ensure the task ladder increases in difficulty
4. Prepare the task system for downstream dataset and metric design

## Input Format

```text
topic: [research topic]
paper_count: [number of related papers from Step 1]
```

## Workflow

### Step 2.1: Task taxonomy search

If there is substantial prior work, extract tasks from existing papers.

If there is not enough prior work, borrow the taxonomy from a parent domain and adapt it.

Typical adaptation logic:

- single-cell multi-omics -> spatial multi-omics
- modality alignment -> spatial-cell alignment
- batch integration -> cross-sample integration

### Step 2.2: Task tier design

Define four levels:

- **Level 1**: basic validation task
- **Level 2**: intermediate application task
- **Level 3**: challenge task
- **Level 4**: flagship innovation task

Increase across three dimensions:

1. Data complexity
2. Technical difficulty
3. Biological value

### Step 2.3: Standardize task descriptions

For each task, write:

- definition
- difficulty level
- data requirements
- technical focus
- biological value
- representative methods
- mapped figure

## Output Format

```markdown
# Task System Design

## Task Sources
- Extracted from related papers:
- Borrowed from parent domain:

## Tier Overview
| Level | Task type | Difficulty | Figure |
|-------|-----------|------------|--------|
| 1 | ... | low | Figure 2 |
| 2 | ... | medium | Figure 3 |
| 3 | ... | high | Figure 4 |
| 4 | ... | highest | Figure 5 |

## Detailed Task Descriptions

### Task 1: [task name]
- Definition:
- Difficulty:
- Data requirements:
- Technical focus:
- Biological value:
- Representative methods:
- Mapped figure:

### Task 2: ...

## Progression Rationale
1. Data complexity rises across tasks
2. Technical difficulty rises across tasks
3. Biological value rises across tasks

## Next Step
- Use the task system to search for datasets in Step 3
```

## Example Ladder

- Level 1: vertical integration
- Level 2: horizontal / cross-slice integration
- Level 3: mosaic integration with missing modalities
- Level 4: diagonal integration across platform / resolution / cohort

## Usage

```bash
/bio-task-system "spatial multi-omics integration | paper_count: 5"
```

## Notes

1. Keep the ladder interpretable to reviewers.
2. Avoid adding too many tasks; four well-designed tiers are usually enough.
3. Make sure each task can later be tied to datasets, metrics, and figures.
