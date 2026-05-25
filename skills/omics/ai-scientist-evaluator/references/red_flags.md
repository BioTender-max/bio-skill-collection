# Red flags and common failure modes

Use these as warning signs. A red flag does not always mean rejection, but it
should reduce trust and trigger a closer audit.

## Integrity and provenance red flags

- accession numbers, species names, or references that cannot be verified
- inconsistent sample counts across text, tables, and code
- database versions or tools mentioned but never actually used in the workflow
- suspiciously generic citations that do not support the claim made
- results shown without traceable inputs

## Notebook and code red flags

- notebooks that appear to rely on hidden state or precomputed outputs
- cells skipped without explanation near key results
- figures that do not match the visible code
- no environment specification, no versioning, and no path control
- runtime claims with no hardware, dataset, or command context

## Scientific analysis red flags

- solving an easier question than the user asked
- cherry-picked taxa, genes, or examples without justification
- no controls, baselines, or robustness checks for a central claim
- conclusions that rest on a single fragile analysis step
- no discussion of uncertainty despite noisy or incomplete data

## Biology-specific red flags

- conflating homology with established function
- conflating gene presence with pathway functionality or phenotype
- ignoring contamination, assembly artifacts, or annotation errors
- overinterpreting ecological or evolutionary implications from limited data
- treating surprising hits as truth instead of testing alternative explanations

## Phylogenomics red flags

- weak or missing support values
- poor taxon sampling that could distort placement
- no explanation of marker selection or alignment filtering
- no rooting rationale
- long-branch attraction risks ignored
- functional discussion disconnected from the phylogenetic result

## Viral functional genomics red flags

- translation system gene set never defined
- permissive homology thresholds that inflate completeness
- host contamination not considered for unexpected translation genes
- ranking genomes without controlling for assembly or annotation quality
- biological function inferred from a score without mechanism or caveats

## Methods and software red flags

- a claimed new algorithm is mostly parameter tuning or code optimization
- speedup claims rely on different hardware, smaller inputs, or weaker outputs
- no benchmark against a serious baseline
- no accuracy-fidelity tradeoff analysis
- Nature Methods style novelty language without method substance
- software lacks enough detail to reproduce the benchmark or use the method

## Manuscript red flags

- abstract says more than results support
- methods so compressed that claims are not auditable
- figures chosen for appearance rather than evidence
- journal framing inflated beyond the actual contribution
- limitations omitted where they materially matter
