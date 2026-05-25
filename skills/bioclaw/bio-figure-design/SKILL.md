# bio-figure-design

**Step 6: Figure design (Figure 详细设计)**

Design the manuscript figures panel by panel, including the figure logic, panel content, and caption intent.

## Purpose

1. Design Figure 1 as the method / framework overview
2. Design Figures 2-N as task-driven application figures
3. Plan supplementary figures
4. Draft figure captions
5. Keep figure logic synchronized with manuscript claims

## Input Format

```text
topic: [research topic]
task_system: [task system]
dataset_catalog: [dataset catalog]
metric_system: [metric system]
analysis_system: [analysis system]
target_journal: [optional, default nat-communications]
```

## Workflow

### Step 6.1: Design Figure 1

Figure 1 should explain the overall method and paper framing:

- Panel a: method / model overview
- Panel b: data or modality overview
- Panel c: task overview
- Panel d: metric overview
- Panel e: analysis overview

The goal is to make the full manuscript logic visible in one figure.

### Step 6.2: Design Figures 2-N

Each application figure should be task-first:

- one major task per figure
- panel a: data flow / experimental setup
- panels b-d: quantitative evaluation
- panel e or later: qualitative / biological validation

This keeps the paper organized around claims rather than around plots.

### Step 6.3: Supplementary figures

Use supplementary figures for:

- ablations
- robustness checks
- extra markers
- extended datasets
- alternative parameter settings

### Step 6.4: Caption planning

Every figure should have a caption plan that explains:

- what each panel shows
- what claim it supports
- what dataset it uses
- what metric or biological conclusion it demonstrates

## Output Format

```markdown
# Figure Designs

## Figure 1: Framework Overview
- Panel a:
- Panel b:
- Panel c:
- Panel d:
- Panel e:
- Caption intent:

## Figure 2: [Task 1]
- Panel a:
- Panel b:
- Panel c:
- Panel d:
- Panel e:
- Caption intent:

## Figure 3: [Task 2]
...

## Supplementary Figures
- Supplementary Figure 1:
- Supplementary Figure 2:

## Design Notes
- visual consistency
- panel ordering logic
- expected take-home message per figure

## Next Step
- Use the figure plan to draft manuscript text in Step 7
```

## Figure Design Principles

1. One main claim per figure
2. Quantitative evidence should appear before broad interpretation
3. Biological validation should be visible, not hidden
4. Reviewer-facing clarity matters more than decorative complexity
5. Figure order should match the manuscript story

## Usage

```bash
/bio-figure-design "topic: spatial multi-omics integration | task_system: [...] | dataset_catalog: [...] | metric_system: [...] | analysis_system: [...] | target_journal: nat-communications"
```

## Notes

1. Keep Figure 1 conceptual and clean.
2. For application figures, tie every panel to a concrete task and metric.
3. Do not overload a figure if a supplementary figure can carry the extra material.
