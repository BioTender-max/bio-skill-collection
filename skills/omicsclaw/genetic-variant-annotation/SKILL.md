---
id: genetic-variant-annotation
name: Genetic Variant Annotation
category: genomics_genetics
short-description: Annotate genomic variants in VCF files with functional effects, clinical significance, and pathogenicity predictions.
detailed-description: Annotate genomic variants in VCF files with functional effects, clinical significance, population frequencies, and pathogenicity predictions. Use when you have VCF files from variant calling and need functional annotation, clinical interpretation, or variant prioritization. Automatically selects between Ensembl VEP (best for human clinical analysis) or SNPEff (best for non-model organisms) based on organism, use case, and computational resources. Handles germline, somatic, and population variants.
starting-prompt: Annotate my VCF file with functional effects and clinical significance . .
---

# Genetic Variant Annotation

Annotate genomic variants in VCF files with functional effects, clinical significance, and pathogenicity predictions.

## When to Use This Skill

Use this skill when you have:
- ✅ **VCF files** from variant calling (GATK, bcftools, FreeBayes, etc.)
- ✅ Need **functional annotation** (gene impact, consequence types)
- ✅ Need **clinical interpretation** (pathogenicity, ClinVar, ACMG classification)
- ✅ Need **variant filtering** by consequence, frequency, or pathogenicity
- ✅ Working with **human, mouse, or 38,000+ other genomes**

**Use cases:**
- Clinical diagnostics (identify pathogenic variants in patient samples)
- Population genetics (annotate with allele frequencies)
- Cancer genomics (somatic variant annotation with COSMIC)
- Research variant prioritization (rank by predicted impact)
- Non-model organism analysis (38,000+ genomes supported)

**Don't use for:**
- ❌ Variant calling (use GATK/bcftools first) → this skill starts with VCF files
- ❌ Structural variant annotation (limited support, use specialized tools)

## Quick Start (Example Data)

Test this skill with example variants:

```python
from load_example_data import load_clinvar_pathogenic_sample
data = load_clinvar_pathogenic_sample()  # Creates test VCF (~10 variants)
print(f"Example VCF created: {data['vcf_path']}")
```

**What you get:**
- **Dataset:** 10 ClinVar pathogenic variants (BRCA1/BRCA2)
- **Expected:** ~6 HIGH impact, ~8 pathogenic classifications
- **Runtime:** VEP ~5 min, SNPEff ~2 min

**Next steps:** Use this VCF in the [Standard Workflow](#standard-workflow) below.

**Optional validation test** (for developers): `python assets/eval/simple_test.py` to verify installation.

**For your own data:** See [Inputs](#inputs) and [Clarification Questions](#clarification-questions).

## Installation

**Choose one annotation tool:**

| Tool | Best For | Installation | Cache/Database Size |
|------|----------|--------------|---------------------|
| **VEP** | Human clinical, comprehensive annotations | `conda install -c bioconda ensembl-vep` | 15-20 GB (one-time) |
| **SNPEff** | Non-model organisms, quick analysis | `conda install -c bioconda snpeff` | 2-5 GB per genome |

**⚠️ FOR AGENTS: If tools are missing, install them automatically:**
```python
# Check and install SNPEff if needed
from run_snpeff import check_snpeff_installation
is_installed, _, _ = check_snpeff_installation()
if not is_installed:
    from install_tools import install_snpeff
    install_snpeff()  # Takes ~2-5 min, installs via conda
```

**For VEP:**
```python
from install_tools import install_vep
install_vep()  # Takes ~5-10 min, then install cache separately
```

**Python dependencies:**
```bash
pip install -r requirements.txt
# Or: pip install pandas numpy pysam cyvcf2 plotnine xlsxwriter
```

**Minimum versions:**
- Python 3.9+
- VEP 110+ or SNPEff 5.1+
- conda (for tool installation)

**VEP cache setup** (if using VEP):
```bash
vep_install -a c -s homo_sapiens -y GRCh38  # Human, ~15-20 GB, ~30-60 min
```

**SNPEff database setup** (if using SNPEff):
```bash
snpEff download GRCh38.105  # Human, ~2-5 GB, ~10 min
```

**For detailed installation:** See [references/installation_guide.md](references/installation_guide.md)

**License:** VEP (Apache 2.0), SNPEff (LGPLv3) - both permit commercial use ✅

## Inputs

**Required:**
- **VCF file:** Variant call format file (bgzipped recommended)
  - Must be valid VCF 4.x format
  - Coordinate-sorted
  - Germline, somatic, or population variants
  - SNVs, indels, or mixed (structural variants have limited support)

**Genome reference:**
- **Human:** GRCh38/hg38 (recommended) or GRCh37/hg19
- **Mouse:** GRCm39 or GRCm38
- **Other:** 38,000+ genomes available in SNPEff

**Optional:**
- Reference FASTA (for validation)
- BED file (for region-specific annotation)
- Custom gene lists (for filtering)

**VCF validation:** First workflow step checks format, coordinates, and reference alleles.

## Outputs

**Analysis objects (Pickle):**
- `analysis_object.pkl` - Complete analysis object for downstream use
  - Load with: `import pickle; obj = pickle.load(open('results/analysis_object.pkl', 'rb'))`
  - Contains: annotated variants DataFrame, gene summaries, tool metadata
  - Required for: downstream pathway enrichment, protein structure mapping, literature mining skills
  - Size: ~1-10 MB depending on variant count

**Annotated variants:**
- `annotated.vep.vcf.gz` or `annotated.snpeff.vcf.gz` - Full VCF with annotations in INFO field
- `all_variants.csv` - All annotated variants in tabular format

**Filtered results:**
- `high_impact_variants.csv` - HIGH impact variants only
- `moderate_impact_variants.csv` - HIGH/MODERATE impact variants
- `rare_variants.csv` - Rare variants (AF < 0.01)
- `filtered_high_impact.vcf.gz` - Filtered VCF (maintains VCF format for downstream tools)

**Gene summaries:**
- `gene_summary.csv` - Variants aggregated per gene (useful for pathway enrichment)

**Visualizations** (PNG + SVG, 300 DPI):
- `consequence_distribution.png/.svg` - Variant types (missense, stop_gained, etc.)
- `impact_by_chromosome.png/.svg` - Impact severity distribution across chromosomes
- `pathogenicity_scores.png/.svg` - CADD, REVEL, SIFT score distributions
- `allele_frequency.png/.svg` - Population frequency distribution
- `gene_burden.png/.svg` - Top genes by variant burden

**Reports:**
- `summary_report.xlsx` - Excel report with multiple sheets (summary statistics, top consequences, top genes, variants)

## Clarification Questions

**⚠️ CRITICAL:** Always ask question #1 first to check if user has provided VCF files.

Before starting, gather:

1. **Input Files** (ASK THIS FIRST):
   - **Do you have specific VCF file(s) to annotate?**
     - If uploaded: Is this the VCF you'd like to annotate?
     - Expected format: VCF/VCF.GZ (variant call format)
   - **Or use example data for testing?**
     - Use `load_clinvar_pathogenic_sample()` (~10 variants, known pathogenic)

2. **Organism and Genome Build**:
   - What organism? (human, mouse, zebrafish, etc.)
   - Which genome assembly? (GRCh38/hg38 recommended for human)
   - **⚠️ Must match VCF reference** - check VCF header: `##reference=`

3. **Primary Use Case** (determines tool selection):
   - Clinical/medical genetics → VEP (comprehensive clinical databases)
   - Population genetics → Either tool works
   - Non-model organism → SNPEff (38,000+ genomes)
   - Quick analysis → SNPEff (faster setup)
   - See [references/tool_selection_guide.md](references/tool_selection_guide.md) for detailed comparison

4. **Annotation Priorities** (select all that apply):
   - Clinical significance (ClinVar, OMIM)
   - Pathogenicity predictions (SIFT, PolyPhen, CADD, REVEL)
   - Population frequencies (gnomAD, 1000 Genomes)
   - Regulatory impacts (ENCODE)
   - Basic consequences only (faster annotation)

5. **Computational Resources**:
   - High-performance (32+ GB RAM) → VEP with full cache
   - Standard (16-32 GB) → VEP or SNPEff
   - Limited (<16 GB) → SNPEff recommended

6. **Output Requirements**:
   - Variant prioritization? → Apply filtering + ACMG classification
   - Gene-level analysis? → Generate gene summaries
   - Clinical reporting? → Excel export with multiple sheets
   - Statistical analysis? → CSV format for downstream tools

## Standard Workflow

> **Note:** Run from the OmicsClaw root directory and add the workflow scripts to `sys.path`:
> ```python
> import sys; import os; sys.path.insert(0, os.path.abspath('knowledge_base/scripts/genetic-variant-annotation'))
> ```

🚨 **MANDATORY: USE SCRIPTS EXACTLY AS SHOWN - DO NOT WRITE INLINE CODE** 🚨

**CRITICAL: Use relative paths (knowledge_base/scripts/genetic-variant-annotation/). DO NOT construct absolute paths like /mnt/knowhow/ or /workspace/.**

This is a 4-step workflow. Scripts handle all complexity automatically.

**Step 1 - Load and validate data:**

```python
# Load example data (or use your own VCF file)
from load_example_data import load_clinvar_pathogenic_sample
data = load_clinvar_pathogenic_sample()
input_vcf = data['vcf_path']

# Validate VCF format
from validate_vcf import validate_vcf, vcf_summary_stats
results = validate_vcf(input_vcf)
if not results['is_valid']:
    print(f"Errors: {results['errors']}")

stats = vcf_summary_stats(input_vcf)
print(f"Total: {stats['total_variants']}, SNVs: {stats['snvs']}, Indels: {stats['indels']}")
```

**✅ VERIFICATION:** You MUST see: `"✓ Data loaded successfully"`

**DO NOT write inline validation code. Use the scripts exactly as shown.**

---

**Step 2 - Run annotation:**

```python
# Select and run annotation tool
from select_tool import select_annotation_tool
tool = select_annotation_tool(organism='human', use_case='clinical', resources='standard')

# Check if tool is installed, install if needed
if tool == 'vep':
    from run_vep import check_vep_installation
    is_installed, _, _ = check_vep_installation()
    if not is_installed:
        print("VEP not found. Installing via conda...")
        from install_tools import install_vep
        install_vep()
        # Note: After VEP install, you must install cache separately
        print("\n⚠️ IMPORTANT: Now install VEP cache:")
        print("  vep_install -a c -s homo_sapiens -y GRCh38")

elif tool == 'snpeff':
    from run_snpeff import check_snpeff_installation
    is_installed, _, _ = check_snpeff_installation()
    if not is_installed:
        print("SNPEff not found. Installing via conda...")
        from install_tools import install_snpeff
        install_snpeff()

# VEP annotation
if tool == 'vep':
    from run_vep import run_vep
    annotated_vcf = run_vep(input_vcf, "annotated.vep.vcf.gz", genome="GRCh38", everything=True, fork=4)
    from parse_vep_output import parse_vep_vcf
    df = parse_vep_vcf("annotated.vep.vcf.gz")

# SNPEff annotation
elif tool == 'snpeff':
    from run_snpeff import run_snpeff
    annotated_vcf = run_snpeff(input_vcf, "annotated.snpeff.vcf.gz", genome="GRCh38.105", canon=True, threads=4)
    from parse_snpeff_output import parse_snpeff_vcf
    df = parse_snpeff_vcf("annotated.snpeff.vcf.gz")
```

**✅ VERIFICATION:** You MUST see: `"✓ Annotation completed successfully!"`

**DO NOT write inline annotation code. Use run_vep() or run_snpeff() as shown.**

**⚠️ DO NOT fall back to VEP API mode** - API mode is 10-100x slower and less full-featured. Always install the tool if missing.

---

**Step 3 - Generate visualizations:**

```python
from filter_variants import filter_by_consequence, filter_by_frequency
from annotate_genes import annotate_gene_summary
from plot_variant_distribution import (
    plot_consequence_distribution,
    plot_impact_by_chromosome,
    plot_pathogenicity_scores,
    plot_allele_frequency,
    plot_gene_burden
)

# Filter variants for analysis
high_impact = filter_by_consequence(df, consequence_levels=['HIGH', 'MODERATE'])
rare = filter_by_frequency(df, max_af=0.01)

# Generate gene-level summaries
gene_df = annotate_gene_summary(df)

# Create visualizations (PNG + SVG)
output_dir = "results"
plot_consequence_distribution(df, f"{output_dir}/consequence_distribution.png")
plot_impact_by_chromosome(df, f"{output_dir}/impact_by_chromosome.png")
plot_pathogenicity_scores(df, f"{output_dir}/pathogenicity_scores.png")
plot_allele_frequency(df, f"{output_dir}/allele_frequency.png")
if gene_df is not None:
    plot_gene_burden(gene_df, output_file=f"{output_dir}/gene_burden.png")
```

**✅ VERIFICATION:** You MUST see: `"Saved: [filename].png"` and `"Saved: [filename].svg"` for each plot

**DO NOT write inline plotting code. Use the plotting functions as shown.**

---

**Step 4 - Export results:**

```python
from export_results import export_all

# Export all results in all formats
export_all(
    df=df,
    gene_df=gene_df,
    original_vcf=input_vcf,
    output_dir="results",
    tool_name=tool
)
```

**✅ VERIFICATION:** You MUST see: `"=== Export Complete ==="`

**DO NOT write custom export code. Use export_all() as shown.**

---

⚠️ **CRITICAL - DO NOT:**
- ❌ **Write inline validation/annotation/plotting/export code** → **STOP: Use the scripts shown above**
- ❌ **Fall back to VEP API mode when tools are missing** → **STOP: Use `install_tools.py` to install via conda**
- ❌ Use absolute paths like `/mnt/knowhow/` or `/workspace/` → use relative paths `scripts/`
- ❌ Skip validation step → catches format errors early
- ❌ Mix genome builds → VCF and annotation database must match (check VCF header)
- ❌ Write custom export code → **STOP: Use `export_all()`**

**If tools are missing:** Use `install_tools.py` to install via conda (~2-10 min). DO NOT use VEP API mode (10-100x slower, less full-featured).

**If scripts fail:** Install missing dependencies, re-run. Only modify scripts if genuinely broken.

## Common Issues

| Issue | Possible Cause | Solution | Details |
|-------|----------------|----------|---------|
| VEP/SNPEff fails to start | Tool not installed or not in PATH | **Use install_tools.py:** `from install_tools import install_snpeff; install_snpeff()` | Takes 2-5 min. DO NOT fall back to VEP API mode (10-100x slower). Verify with `which vep` or `which snpEff` |
| "Cannot find genome" | Database not downloaded | Run `install_vep_cache()` or `download_snpeff_database()` | See [installation_guide.md](references/installation_guide.md) |
| All variants annotated as intergenic | Genome build mismatch (hg19 vs hg38) | Check VCF header `##reference=`, use matching genome build | Use `bcftools annotate --rename-chrs` to convert |
| No pathogenicity scores | Plugins/databases not installed | Install VEP plugins or SnpSift databases | See [vep_best_practices.md](references/vep_best_practices.md) |
| Memory error during annotation | Insufficient RAM or large VCF | Reduce buffer size (`--buffer_size 1000`) or split VCF by chromosome | Use `bcftools view -r chr1` to split |
| "Invalid VCF format" | VCF format errors (tabs, header, etc.) | Run validation step first, check tabs and header completeness | Use `bcftools view -h` to inspect header |
| Chromosome name mismatch | VCF uses "chr1" but database uses "1" | Convert with `bcftools annotate --rename-chrs` | Create mapping file: `chr1 1\nchr2 2\n...` |
| Very slow annotation | Not using cache/database (API mode) | Ensure VEP cache or SNPEff database installed locally | API mode is 10-100x slower |

**For complete troubleshooting:** See [references/troubleshooting_guide.md](references/troubleshooting_guide.md)

**QC checkpoints:**
- **VCF validation:** Ti/Tv ratio 2.0-2.1 (genome) or 2.8-3.0 (exome)
- **Annotation completeness:** 100% variants annotated
- **Expected HIGH impact:** 10-50 per exome (healthy individual)

**For detailed QC thresholds:** See [references/qc_guidelines.md](references/qc_guidelines.md)

## Suggested Next Steps

After annotating variants:

1. **Variant prioritization** → Filter and rank by pathogenicity
   - Use filtering: AF < 0.01, HIGH/MODERATE impact, CADD > 20
   - Apply ACMG classification for clinical reporting

2. **Gene-level analysis** → Aggregate variants per gene
   - Identify genes with high variant burden
   - Prepare for pathway enrichment analysis

3. **Clinical reporting** → Export prioritized variants
   - Excel format with multiple sheets (variants, genes, summary)
   - Include ACMG classifications and ClinVar annotations

4. **Statistical analysis** → Burden testing, association studies
   - Compare variant frequencies between cases and controls
   - Gene-based collapsing analysis

**Related analyses:** Pathway enrichment from gene lists, protein structure mapping, literature mining

## Related Skills

**Upstream** (run these first):
- Variant calling workflows (GATK HaplotypeCaller, bcftools call, FreeBayes)
- Variant quality score recalibration (VQSR)

**Downstream** (run these after):
- Pathway enrichment from gene lists
- Protein structure visualization and impact prediction
- Clinical report generation

**Complementary:**
- Copy number variant (CNV) annotation
- Structural variant annotation (specialized tools)
- Pharmacogenomics annotation (PharmGKB)

## References

### Primary Citations

**Ensembl VEP:**
- McLaren W, et al. (2016) The Ensembl Variant Effect Predictor. *Genome Biology* 17:122. [doi:10.1186/s13059-016-0974-4](https://doi.org/10.1186/s13059-016-0974-4)

**SNPEff:**
- Cingolani P, et al. (2012) A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff. *Fly* 6(2):80-92. [doi:10.4161/fly.19695](https://doi.org/10.4161/fly.19695)

**ACMG Guidelines:**
- Richards S, et al. (2015) Standards and guidelines for the interpretation of sequence variants. *Genetics in Medicine* 17(5):405-424. [PubMed:25741868](https://pubmed.ncbi.nlm.nih.gov/25741868/)

### Documentation

**Tool Selection & Configuration:**
- [Tool Selection Guide](references/tool_selection_guide.md) - VEP vs SNPEff decision matrix, resource requirements
- [VEP Best Practices](references/vep_best_practices.md) - VEP configuration, plugins, optimization
- [SNPEff Best Practices](references/snpeff_best_practices.md) - SNPEff parameters, databases, statistics

**Analysis & Interpretation:**
- [QC Guidelines](references/qc_guidelines.md) - Quality control metrics, expected ranges, red flags
- [Consequence Terms](references/consequence_terms.md) - Sequence Ontology terms reference
- [Pathogenicity Interpretation](references/pathogenicity_interpretation.md) - ACMG/AMP guidelines, classification rules
- [Filtering Strategies](references/filtering_strategies.md) - Clinical vs research filtering approaches

**Setup & Troubleshooting:**
- [Installation Guide](references/installation_guide.md) - Detailed VEP/SNPEff installation instructions
- [Troubleshooting Guide](references/troubleshooting_guide.md) - Common issues, diagnosis steps, solutions
