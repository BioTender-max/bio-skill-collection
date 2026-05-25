# Infernal `cmsearch` for rRNA and ncRNA detection

Infernal applies covariance models (CMs) to search nucleotide sequences for RNA homologs. In this workflow it replaces `barrnap` as the default rRNA caller because Rfam covariance models cover all three domains of life plus organellar variants, and are kept current.

- **Project page:** http://eddylab.org/infernal/
- **Rfam database:** https://rfam.org/
- **Recommended version:** Infernal v1.1.5+
- **Citation:** Nawrocki & Eddy (2013) *Bioinformatics* 29:2933.

## Installation

```bash
conda install -c bioconda infernal
# Rfam.cm covariance model library
wget https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.cm.gz
gunzip Rfam.cm.gz
cmpress Rfam.cm
```

## Rfam models for ribosomal RNA

Select the model set by the inferred domain of life. Run `cmsearch` once per model or pass a pre-pressed CM library with the relevant accessions selected via `cmscan --tblout` filtering.

| Domain | SSU rRNA | LSU rRNA | 5S | 5.8S | Notes |
|--------|----------|----------|----|------|-------|
| Bacteria | RF00177 (16S) | RF02541 (23S) | RF00001 | — | — |
| Archaea | RF01959 (16S) | RF02540 (23S) | RF00001 | — | — |
| Eukaryotes | RF01960 (18S) | RF02543 (28S) | RF00001 | RF00002 | — |
| Metazoan mitochondria | RF02555 (12S) | RF02546 (16S) | — | — | Use when calling mitochondrial contigs |

## Default search

```bash
cmsearch --rfam --cut_ga --nohmmonly \
  --tblout output.tbl \
  Rfam.cm assembly.fna > output.cmsearch
```

`--cut_ga` applies Rfam gathering thresholds (recommended default). If no hits are found, rerun without `--cut_ga` and record both the default and relaxed results in `ncRNA_census.tsv`.

## Quality gates

- Report counts per Rfam accession per assembly in `ncRNA_census.tsv`.
- A credible negative finding (default and relaxed thresholds both empty) is a required result.
- For metagenomic assemblies, allow multiple hits per contig and record their coordinates for downstream annotation.
