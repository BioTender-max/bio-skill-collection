---
name: bio-tools
description: Biology research tools reference. Always available inside agent containers.
---

# Bio Tools Reference

You are running inside a BioClaw container with the following biology tools pre-installed.

**Layout:** Runnable plot/PyMOL scripts live under `templates/` (synced to `/home/node/.claude/skills/bio-tools/templates/`).

## Quick Reference

### Sequence Search
```bash
# Nucleotide BLAST
blastn -query input.fa -subject ref.fa -outfmt 6 -evalue 1e-5

# Protein BLAST
blastp -query protein.fa -subject ref_protein.fa -outfmt 6

# Translate then search
blastx -query nucleotide.fa -subject protein_db.fa -outfmt 6
```

### Read Alignment
```bash
# Index reference
bwa index reference.fa

# Align short reads
bwa mem reference.fa reads_R1.fq reads_R2.fq > aligned.sam

# Long reads
minimap2 -a reference.fa long_reads.fq > aligned.sam

# SAM to sorted BAM
samtools view -bS aligned.sam | samtools sort -o sorted.bam
samtools index sorted.bam
```

### Quality Control
```bash
# FastQC report
fastqc reads.fq -o qc_output/

# FASTA/FASTQ stats
seqtk comp reads.fq | head
seqtk size reads.fq
```

### Genome Arithmetic
```bash
# Intersect two BED files
bedtools intersect -a regions.bed -b features.bed

# Coverage
bedtools coverage -a regions.bed -b aligned.bam

# Get FASTA from BED regions
bedtools getfasta -fi reference.fa -bed regions.bed
```

### Python Quick Recipes

```python
# Read FASTA/FASTQ
from Bio import SeqIO
for record in SeqIO.parse("input.fa", "fasta"):
    print(record.id, len(record.seq))

# Fetch from NCBI
from Bio import Entrez
Entrez.email = "bioclaw@example.com"
handle = Entrez.efetch(db="nucleotide", id="NM_000546", rettype="fasta")
record = SeqIO.read(handle, "fasta")

# Differential expression
from pydeseq2 import DeseqDataSet, DeseqStats
dds = DeseqDataSet(counts=count_matrix, metadata=metadata, design="~condition")
dds.deseq2()
stat_res = DeseqStats(dds, contrast=["condition", "treated", "untreated"])
stat_res.summary()

# Single-cell RNA-seq
import scanpy as sc
adata = sc.read_h5ad("data.h5ad")
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.tl.pca(adata)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Molecular structures
from rdkit import Chem
from rdkit.Chem import Descriptors
mol = Chem.MolFromSmiles("CC(=O)OC1=CC=CC=C1C(=O)O")  # Aspirin
print(f"MW: {Descriptors.MolWt(mol):.1f}")
print(f"LogP: {Descriptors.MolLogP(mol):.2f}")
```

## Important Notes

- For remote BLAST against NCBI, use `Bio.Blast.NCBIWWW.qblast()` — this sends the query over the network
- For large files, prefer streaming with `SeqIO.parse()` over `SeqIO.read()`
- **Plots**: Save to `/workspace/group/plot.png` with `dpi=150, bbox_inches="tight"`. For publication-ready figures, use `cnsplots` or `pyGenomeTracks` (see below).
- Write output files to `/workspace/group/` so the user can access them
- **Versioning**: When re-running analysis, save to `output/YYYY-MM-DD/` to avoid overwriting; update `_latest.md` with paths to newest outputs

## Reusable Figure Templates

Prefer these built-in scripts when creating common BioClaw figures, instead of writing one-off plotting code from scratch.

### Volcano Plot Template
Path:

```bash
/home/node/.claude/skills/bio-tools/templates/volcano_plot_template.py
```

Example:

```bash
python /home/node/.claude/skills/bio-tools/templates/volcano_plot_template.py \
  --input /workspace/group/counts.csv \
  --output /workspace/group/volcano_plot.png \
  --title "Differential Expression Volcano Plot"
```

Expected columns by default: `gene`, `log2FC`, `pvalue`

### QC Summary Plot Template
Path:

```bash
/home/node/.claude/skills/bio-tools/templates/qc_summary_plot_template.py
```

Example:

```bash
python /home/node/.claude/skills/bio-tools/templates/qc_summary_plot_template.py \
  --input /workspace/group/qc_metrics.csv \
  --output /workspace/group/qc_summary.png \
  --title "Sequencing QC Summary"
```

Expected sample column by default: `sample`

Useful metric columns: `total_reads`, `q30_pct`, `gc_pct`, `duplication_pct`

### PyMOL Render Template
Path:

```bash
/home/node/.claude/skills/bio-tools/templates/pymol_render_template.py
```

Examples:

```bash
python /home/node/.claude/skills/bio-tools/templates/pymol_render_template.py \
  --input 1M17 \
  --output /workspace/group/1m17_render.png \
  --highlight-selection "resn AQ4"
```

```bash
python /home/node/.claude/skills/bio-tools/templates/pymol_render_template.py \
  --input /workspace/group/structure.pdb \
  --output /workspace/group/structure_render.png \
  --style cartoon
```

### Inline Plot Snippets (Heatmap, PCA, Bar)

When the built-in scripts don't fit, use these patterns. Save to `/workspace/group/<name>.png`.

**Heatmap** (rows=genes, columns=samples):
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("/workspace/group/expression.csv", index_col=0)
sns.heatmap(np.log1p(df).iloc[:50], cmap='RdBu_r', center=0)
plt.savefig("/workspace/group/heatmap.png", dpi=150, bbox_inches="tight")
```

**PCA scatter** (columns: PC1, PC2, condition):
```python
import pandas as pd
import matplotlib.pyplot as plt
coords = pd.read_csv("/workspace/group/pca_coords.csv")
for c in coords['condition'].unique():
    sub = coords[coords['condition'] == c]
    plt.scatter(sub['PC1'], sub['PC2'], label=c)
plt.legend()
plt.savefig("/workspace/group/pca.png", dpi=150, bbox_inches="tight")
```

**Bar plot** (columns: gene, count):
```python
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("/workspace/group/top_genes.csv").head(20).sort_values('count', ascending=True)
plt.barh(df['gene'], df['count'])
plt.savefig("/workspace/group/barplot.png", dpi=150, bbox_inches="tight")
```

## Publication-Ready Plots (cnsplots)

**cnsplots** provides Cell/Nature/Science journal-style figures. Use for volcano, bar, box, violin, heatmap, etc.

```python
import cnsplots as cns
import pandas as pd
import numpy as np

# Volcano plot (columns: gene, log2FC, pvalue or padj)
df = pd.read_csv("/workspace/group/counts.csv")
df["-log10(p)"] = -np.log10(df["pvalue"].clip(lower=1e-300))  # or use padj
cns.figure(height=200, width=200)
cns.volcanoplot(data=df, x="log2FC", y="-log10(p)", symbol="gene")
cns.savefig("/workspace/group/volcano_cns.png")
```

```python
# Boxplot with Mann-Whitney test
cns.figure(150, 150)
cns.boxplot(data=df, x="group", y="value", pairs="all")
cns.savefig("/workspace/group/boxplot.png")
```

```python
# Heatmap from AnnData (single-cell)
import scanpy as sc
adata = sc.read_h5ad("/workspace/group/data.h5ad")
cns.figure(200, 200)
cns.heatmapplot(adata, row_cluster=True, col_cluster=True, cmap="bwr")
cns.savefig("/workspace/group/heatmap_cns.png")
```

See [cnsplots docs](https://cnsplots.farid.one/) for more: violin, scatter, survival, ROC, GSEA, etc.

## Genome Browser Tracks (pyGenomeTracks)

**pyGenomeTracks** plots genome browser tracks (BED, BigWig, GTF, etc.). BEDTools must be installed (already in container).

```bash
# 1. Create config from your files
make_tracks_file --trackFiles /workspace/group/peaks.bed /workspace/group/coverage.bw -o /workspace/group/tracks.ini

# 2. Plot a region (chr:start-end)
pyGenomeTracks --tracks /workspace/group/tracks.ini --region chr1:1000000-4000000 -o /workspace/group/genome_tracks.png --dpi 150
```

Supported file types: `.bed`, `.bw` (bigwig), `.gtf`, `.gff`, `.arcs`, `.links`. Edit `tracks.ini` to adjust track colors, heights, titles.
