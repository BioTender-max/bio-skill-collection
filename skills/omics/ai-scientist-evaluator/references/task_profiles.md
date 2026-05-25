# Task profiles

Pick the closest profile first. Use the matching weight profile and question
subset.

## scientific-analysis

Use for general bioinformatics or computational biology analyses where the main
job is to answer a scientific question and produce a defensible result.

Primary checks:
- task completion
- methodological rigor
- biological interpretation
- reproducibility
- validation and robustness

## phylogenomics-comparative-genomics

Use for tasks involving taxon selection, ortholog or marker inference,
alignment, tree reconstruction, and evolutionary interpretation.

Primary checks:
- representative sampling
- defensible marker strategy
- support and robustness of tree placement
- meaningful integration of functional interpretation
- clear handling of alternative explanations

## viral-functional-genomics

Use for tasks centered on viral gene content, translation systems, completeness
scoring, or unusual functional repertoires.

Primary checks:
- explicit gene set definition
- contamination and artifact control
- fair completeness scoring
- biologically grounded interpretation
- traceable ranking criteria

## methods-software

Use for algorithm, software, or workflow development tasks where the main claim
is that a new method is faster, better, or more scalable.

Primary checks:
- correct problem formulation
- algorithmic soundness
- implementation quality
- benchmark fairness
- accuracy-fidelity tradeoffs
- evidence for runtime and scalability claims

## manuscript-packaging

Use when the main deliverable is a short communication, methods paper, or other
written research product.

Primary checks:
- claim-evidence alignment
- journal fit
- figure and table quality
- methods transparency
- honest limitations

## Composite tasks

Many AI scientist tasks combine profiles. For example:
- a phylogenomics analysis with a short paper uses
  `phylogenomics-comparative-genomics` plus a manuscript check
- a new method paper with a benchmark notebook uses `methods-software` plus a
  manuscript check
- a viral gene content analysis with a short communication uses
  `viral-functional-genomics` plus a manuscript check

When in doubt, score with the scientific profile first, then add manuscript
comments as a secondary review layer.
