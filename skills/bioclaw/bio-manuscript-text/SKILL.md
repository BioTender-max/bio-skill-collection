# bio-manuscript-text

**Step 7: Manuscript drafting (论文文案生成)**

Draft the main manuscript text from the figure plan, metric system, and analysis system.

## Purpose

1. Write the Introduction
2. Draft the Results around the figure logic
3. Draft the Discussion
4. Draft the Methods skeleton

## Input Format

```text
topic: [research topic]
figure_designs: [figure design document]
innovation: [innovation summary]
base_work: [related prior work]
metric_system: [metric system]
analysis_system: [analysis system]
paper_count: [number of related papers]
related_papers: [optional list]
target_journal: [target journal]
```

## Workflow

### Step 7.1: Write the Introduction

Use a five-paragraph structure:

1. field background
2. related work
3. limitations of current methods
4. introduce the proposed method
5. significance and broader impact

### Step 7.2: Write the Results

Organize the Results around figure order:

- Figure 1: framework / method overview
- Figure 2-N: one main task or claim per figure

For each figure section, explain:

- setup
- quantitative findings
- qualitative or biological findings
- take-home message

### Step 7.3: Write the Discussion

Cover:

- method strengths
- comparison to prior methods
- biological implications
- limitations
- future directions

### Step 7.4: Write the Methods skeleton

Include at minimum:

- preprocessing
- model architecture
- training strategy
- metrics
- biological analyses
- baselines

## Output Format

```markdown
# Manuscript Text

## INTRODUCTION
### Paragraph 1: Field background
### Paragraph 2: Related work
### Paragraph 3: Current limitations
### Paragraph 4: Our method
### Paragraph 5: Significance

## RESULTS
### 2.1 Framework overview
### 2.2 Task 1 / Figure 2
### 2.3 Task 2 / Figure 3
### 2.4 Task 3 / Figure 4
### 2.5 Task 4 / Figure 5

## DISCUSSION
- strengths
- comparisons
- biological implications
- limitations
- future work

## METHODS
- preprocessing
- model
- training
- metrics
- biological analyses
- baselines
```

## Writing Principles

1. Make the manuscript track the figure logic.
2. Keep claims tied to evidence.
3. Separate technical and biological claims clearly.
4. Prefer reviewer-friendly clarity over stylistic complexity.

## Usage

```bash
/bio-manuscript-text "topic: spatial multi-omics integration | figure_designs: [...] | innovation: [...] | base_work: [...] | paper_count: 5 | target_journal: nat-communications"
```

## Notes

1. Do not draft text before the figure logic is stable.
2. Every Results subsection should map to a figure.
3. Keep Methods detailed enough that later implementation planning remains consistent.
