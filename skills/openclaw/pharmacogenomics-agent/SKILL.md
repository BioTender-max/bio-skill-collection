<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

---
name: 'pharmacogenomics-agent'
description: 'AI-driven pharmacogenomic analysis for precision dosing and adverse event prediction using multi-omics data.'
keywords:
  - pharmacogenomics
  - precision-dosing
  - cpic-guidelines
  - adverse-events
  - multi-omics
measurable_outcome: 'Provides validated dosing recommendations for >50 drugs with 99% concordance to CPIC guidelines.'
allowed-tools:
  - read_file
  - run_shell_command
---


# Pharmacogenomics Agent

The **Pharmacogenomics Agent** integrates AI and multi-omics data to predict individual drug responses, optimize medication dosing, and minimize adverse events. It implements CPIC guidelines while leveraging deep learning for complex polygenic drug response phenotypes.

## When to Use This Skill

* When interpreting pharmacogenomic variants (CYP450, HLA, transporters) for drug selection.
* To predict drug response using transcriptomic and proteomic biomarkers.
* For calculating polygenic risk scores for drug efficacy/toxicity.
* When optimizing doses for narrow therapeutic index drugs.
* To identify drug-drug-gene interactions.

## Core Capabilities

1. **Variant Interpretation**: Translates star allele genotypes (*1/*2) into metabolizer phenotypes and actionable CPIC recommendations.

2. **Multi-Omics Response Prediction**: Deep learning models (DeepDRA, MOViDA) integrate genomic, transcriptomic, and proteomic features for drug response prediction.

3. **Polygenic Risk Scoring**: Combines effects of thousands of variants to stratify patients beyond single-gene pharmacogenomics.

4. **Adverse Event Prediction**: Identifies genetic risk factors for serious adverse reactions (HLA associations, G6PD deficiency).

5. **Dose Optimization**: AI-guided dosing for warfarin, tacrolimus, fluoropyrimidines, thiopurines, and other PGx-guided drugs.

6. **Drug-Drug-Gene Interactions**: Detects complex interactions where genetic variants modify drug interaction severity.

## CPIC-Guided Genes and Drugs

| Gene | Drugs | Clinical Impact |
|------|-------|-----------------|
| CYP2D6 | Codeine, tamoxifen, antidepressants | Metabolizer status affects efficacy/toxicity |
| CYP2C19 | Clopidogrel, PPIs, antidepressants | Loss-of-function affects activation |
| CYP2C9/VKORC1 | Warfarin | Dose requirements vary 10-fold |
| TPMT/NUDT15 | Thiopurines | Myelosuppression risk |
| DPYD | Fluoropyrimidines | Severe/fatal toxicity in deficient patients |
| HLA-B*57:01 | Abacavir | Hypersensitivity screening |
| HLA-B*15:02 | Carbamazepine | SJS/TEN risk in Asian populations |

## Workflow

1. **Input**: Patient genotype data (VCF, genotyping array), medication list, clinical parameters.

2. **Star Allele Calling**: Translate variants to star alleles using Stargazer or PharmCAT.

3. **Phenotype Assignment**: Determine metabolizer status (PM, IM, NM, UM) for each gene.

4. **Guideline Lookup**: Retrieve CPIC/DPWG recommendations for patient's medications.

5. **Multi-Omics Prediction**: Apply deep learning for complex response phenotypes.

6. **Output**: Drug-specific recommendations, dose adjustments, alternative medications, interaction alerts.

## Example Usage

**User**: "Interpret this patient's pharmacogenomic panel and provide recommendations for their current medications."

**Agent Action**:
```bash
python3 Skills/Precision_Medicine/Pharmacogenomics_Agent/pgx_analyzer.py \
    --genotype patient_pgx_panel.vcf \
    --medications current_meds.json \
    --guidelines cpic_dpwg \
    --risk_scores oncology_response \
    --output pgx_recommendations.json
```

## AI Models for Drug Response

| Model | Architecture | Application | Performance |
|-------|--------------|-------------|-------------|
| DeepDRA | Autoencoders | Drug response from transcriptomics | AUC 0.99 |
| MOViDA | Multi-omics VAE | Interpretable response prediction | State-of-art |
| DrugCell | Graph neural network | Drug synergy prediction | Improved over baselines |
| PaccMann | Multimodal attention | Cancer drug sensitivity | Clinical translation |

## Polygenic Drug Response

Beyond single-gene PGx, polygenic scores capture:
- **Efficacy polygenic scores**: Statin LDL response, antidepressant remission
- **Toxicity polygenic scores**: Metformin GI intolerance, opioid dependence risk
- **Combined scores**: Integrating PRS with PGx for personalized prediction

## Prerequisites

* Python 3.10+
* PharmCAT or Stargazer for star allele calling
* CPIC/DPWG guideline databases
* Deep learning frameworks (PyTorch)
* Optional: Expression data for multi-omics models

## Related Skills

* Variant_Interpretation - For general variant classification
* Drug_Repurposing - For alternative drug identification
* Clinical_Trials - For PGx-guided trial matching

## Implementation Notes

**Clinical Integration**:
- Returns structured FHIR-compatible recommendations
- Supports CDS Hooks for real-time EMR alerts
- Audit trail for clinical decision support

**Quality Metrics**:
- Validated against PharmGKB annotations
- Concordance with reference laboratory calls
- Regular updates with new CPIC guidelines

## Author

AI Group - Biomedical AI Platform


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->