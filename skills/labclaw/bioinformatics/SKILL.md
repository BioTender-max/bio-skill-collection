# Bioinformatics Analysis

## Overview
Computational biology and genomics analysis pipelines. GENERAL: not locked to any specific tool — use Scanpy, Seurat, DESeq2, or any appropriate package.

## Common Workflows

### RNA-seq Analysis
1. Quality control (FastQC, MultiQC)
2. Alignment (STAR, HISAT2) or pseudo-alignment (Salmon, kallisto)
3. Quantification (featureCounts, Salmon quant)
4. Normalization (DESeq2 vst/rlog, edgeR TMM)
5. Differential expression (DESeq2, edgeR, limma-voom)
6. Visualization (volcano plot, MA plot, heatmap)
7. Pathway analysis (clusterProfiler GO/KEGG, GSEA)

### scRNA-seq Analysis (Scanpy / Seurat)
1. Quality control (filter cells: mito%, gene count, UMI count)
2. Normalization (library size, log1p)
3. Feature selection (highly variable genes)
4. Dimensionality reduction (PCA → UMAP/tSNE)
5. Clustering (Leiden, Louvain)
6. Marker identification (Wilcoxon, t-test)
7. Cell type annotation (manual markers or automated)
8. Trajectory analysis (PAGA, diffusion pseudotime)

### GWAS / Genomics
1. Quality control (MAF, HWE, call rate, relatedness)
2. Association testing (PLINK, REGENIE)
3. Multiple testing correction (Bonferroni, FDR)
4. Manhattan plot, Q-Q plot
5. Fine-mapping, colocalization

## Key Databases
- GEO (Gene Expression Omnibus): public expression datasets
- TCGA (The Cancer Genome Atlas): cancer genomics
- GTEx (Genotype-Tissue Expression): tissue-specific expression
- ClinVar: clinical variant interpretations
- UniProt: protein sequences and annotations
- Ensembl: genome annotation

## File Formats
| Format | Content | Tools |
|--------|---------|-------|
| FASTQ | Raw sequencing reads | FastQC, Trimmomatic |
| BAM/SAM | Aligned reads | samtools, IGV |
| VCF | Variant calls | bcftools, GATK |
| h5ad | AnnData (scRNA-seq) | Scanpy |
| RDS | R object | Seurat, DESeq2 |
| BED | Genomic regions | bedtools |
