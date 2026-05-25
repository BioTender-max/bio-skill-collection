# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""
Pydantic models for OncoKB API responses.

OncoKB provides precision oncology knowledge base with gene and variant
annotations for cancer therapeutics, diagnostics, and prognostics.
"""

from typing import Union

from pydantic import BaseModel, Field


class OncoKBGene(BaseModel):
    """
    OncoKB curated gene information.

    Represents a gene in the OncoKB knowledge base with genomic
    coordinates, identifiers, and clinical summaries.

    Attributes:
        grch37_isoform: Ensembl transcript ID for GRCh37/hg19
        grch37_ref_seq: RefSeq transcript ID for GRCh37
        grch38_isoform: Ensembl transcript ID for GRCh38/hg38
        grch38_ref_seq: RefSeq transcript ID for GRCh38
        entrez_gene_id: NCBI Entrez Gene identifier
        hugo_symbol: HUGO Gene Nomenclature Committee symbol
        gene_type: Gene classification (ONCOGENE, TSG, etc.)
        highest_sensitive_level: Highest therapeutic sensitivity level
        highest_resistance_level: Highest therapeutic resistance level
        summary: Brief clinical summary of the gene
        background: Detailed biological background and mechanisms
    """

    grch37_isoform: str | None = Field(None, alias="grch37Isoform")
    grch37_ref_seq: str | None = Field(None, alias="grch37RefSeq")
    grch38_isoform: str | None = Field(None, alias="grch38Isoform")
    grch38_ref_seq: str | None = Field(None, alias="grch38RefSeq")
    entrez_gene_id: int = Field(..., alias="entrezGeneId")
    hugo_symbol: str = Field(..., alias="hugoSymbol")
    gene_type: str | None = Field(None, alias="geneType")
    highest_sensitive_level: str | None = Field(
        None, alias="highestSensitiveLevel"
    )
    highest_resistance_level: str | None = Field(
        None, alias="highestResistanceLevel"
    )
    summary: str | None = None
    background: str | None = None

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBQuery(BaseModel):
    """
    Query parameters used for OncoKB annotation request.

    Attributes:
        id: Optional query identifier
        reference_genome: Reference genome version (GRCh37 or GRCh38)
        hugo_symbol: HUGO gene symbol
        entrez_gene_id: NCBI Entrez Gene ID
        alteration: Variant alteration string (e.g., V600E)
        alteration_type: Type of alteration
        sv_type: Structural variant type
        tumor_type: Cancer type or tissue
        consequence: Variant consequence
        protein_start: Protein position start
        protein_end: Protein position end
        hgvs: HGVS notation
        hgvs_info: Additional HGVS information
        canonical_transcript: Canonical transcript flag
    """

    id: str | None = None
    reference_genome: str | None = Field(None, alias="referenceGenome")
    hugo_symbol: str | None = Field(None, alias="hugoSymbol")
    entrez_gene_id: int | None = Field(None, alias="entrezGeneId")
    alteration: str | None = None
    alteration_type: str | None = Field(None, alias="alterationType")
    sv_type: str | None = Field(None, alias="svType")
    tumor_type: str | None = Field(None, alias="tumorType")
    consequence: str | None = None
    protein_start: int | None = Field(None, alias="proteinStart")
    protein_end: int | None = Field(None, alias="proteinEnd")
    hgvs: str | None = None
    hgvs_info: str | None = Field(None, alias="hgvsInfo")
    canonical_transcript: bool | None = Field(
        None, alias="canonicalTranscript"
    )

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBMutationEffect(BaseModel):
    """
    Biological effect of a mutation.

    Attributes:
        known_effect: Known effect classification (e.g., Gain-of-function)
        description: Detailed biological description with citations
        citations: Associated PubMed IDs and abstracts
    """

    known_effect: str | None = Field(None, alias="knownEffect")
    description: str | None = None
    citations: dict[str, list[str]] = Field(default_factory=dict)

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBMainType(BaseModel):
    """
    Main tumor type classification.

    Attributes:
        id: Tumor type identifier
        name: Main tumor type name
        tumor_form: Form of tumor (SOLID or LIQUID)
    """

    id: int | None = None
    name: str | None = None
    tumor_form: str | None = Field(None, alias="tumorForm")

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBTumorType(BaseModel):
    """
    Detailed tumor type information.

    Attributes:
        id: Tumor type identifier
        code: OncoTree code for the tumor type
        color: Display color for visualization
        name: Full tumor type name
        main_type: Main tumor type classification
        tissue: Tissue of origin
        children: Child tumor types in hierarchy
        parent: Parent tumor type code
        level: Level in OncoTree hierarchy
        tumor_form: Form of tumor (SOLID or LIQUID)
    """

    id: int | None = None
    code: str | None = None
    color: str | None = None
    name: str | None = None
    main_type: OncoKBMainType | None = Field(None, alias="mainType")
    tissue: str | None = None
    children: dict = Field(default_factory=dict)
    parent: str | None = None
    level: int | None = None
    tumor_form: str | None = Field(None, alias="tumorForm")

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBAbstract(BaseModel):
    """
    Publication abstract reference.

    Can be either a simple string or structured with link and text.

    Attributes:
        link: URL to the publication
        abstract: Abstract text or citation
    """

    link: str | None = None
    abstract: str | None = None

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBTherapeuticImplication(BaseModel):
    """
    Therapeutic implication for a variant in a tumor type.

    Attributes:
        level_of_evidence: OncoKB evidence level (LEVEL_1, LEVEL_2, etc.)
        alterations: List of alterations with this implication
        tumor_type: Associated tumor type information
        pmids: PubMed IDs supporting this implication
        abstracts: Abstract references (can be strings or structured)
        description: Detailed therapeutic description
        drugs: List of therapeutic drugs
    """

    level_of_evidence: str | None = Field(None, alias="levelOfEvidence")
    alterations: list[str] = Field(default_factory=list)
    tumor_type: OncoKBTumorType | None = Field(None, alias="tumorType")
    pmids: list[str] = Field(default_factory=list)
    abstracts: list[Union[str, OncoKBAbstract]] = Field(default_factory=list)
    description: str | None = None
    drugs: list[dict] = Field(default_factory=list)

    class Config:
        """Pydantic configuration."""

        populate_by_name = True


class OncoKBVariantAnnotation(BaseModel):
    """
    Comprehensive variant annotation from OncoKB.

    Represents clinical and biological annotations for a specific
    variant, including oncogenicity, mutation effects, therapeutic
    implications, and diagnostic/prognostic information.

    Attributes:
        query: Original query parameters
        gene_exist: Whether the gene exists in OncoKB
        variant_exist: Whether the variant exists in OncoKB
        allele_exist: Whether the allele exists
        oncogenic: Oncogenicity classification
        mutation_effect: Biological effect of the mutation
        highest_sensitive_level: Highest sensitivity evidence level
        highest_resistance_level: Highest resistance evidence level
        highest_diagnostic_implication_level: Highest diagnostic level
        highest_prognostic_implication_level: Highest prognostic level
        highest_fda_level: Highest FDA approval level
        other_significant_sensitive_levels: Other sensitivity levels
        other_significant_resistance_levels: Other resistance levels
        hotspot: Whether variant is a known hotspot
        exon: Exon number if applicable
        gene_summary: Summary of gene biology
        variant_summary: Summary of variant characteristics
        tumor_type_summary: Tumor-type specific summary
        prognostic_summary: Prognostic implications
        diagnostic_summary: Diagnostic implications
        diagnostic_implications: Detailed diagnostic implications
        prognostic_implications: Detailed prognostic implications
        treatments: Therapeutic treatment information
    """

    query: OncoKBQuery | None = None
    gene_exist: bool | None = Field(None, alias="geneExist")
    variant_exist: bool | None = Field(None, alias="variantExist")
    allele_exist: bool | None = Field(None, alias="alleleExist")
    oncogenic: str | None = None
    mutation_effect: OncoKBMutationEffect | None = Field(
        None, alias="mutationEffect"
    )
    highest_sensitive_level: str | None = Field(
        None, alias="highestSensitiveLevel"
    )
    highest_resistance_level: str | None = Field(
        None, alias="highestResistanceLevel"
    )
    highest_diagnostic_implication_level: str | None = Field(
        None, alias="highestDiagnosticImplicationLevel"
    )
    highest_prognostic_implication_level: str | None = Field(
        None, alias="highestPrognosticImplicationLevel"
    )
    highest_fda_level: str | None = Field(None, alias="highestFdaLevel")
    other_significant_sensitive_levels: list[str] = Field(
        default_factory=list, alias="otherSignificantSensitiveLevels"
    )
    other_significant_resistance_levels: list[str] = Field(
        default_factory=list, alias="otherSignificantResistanceLevels"
    )
    hotspot: bool | None = None
    exon: str | None = None
    gene_summary: str | None = Field(None, alias="geneSummary")
    variant_summary: str | None = Field(None, alias="variantSummary")
    tumor_type_summary: str | None = Field(None, alias="tumorTypeSummary")
    prognostic_summary: str | None = Field(None, alias="prognosticSummary")
    diagnostic_summary: str | None = Field(None, alias="diagnosticSummary")
    diagnostic_implications: list[OncoKBTherapeuticImplication] = Field(
        default_factory=list, alias="diagnosticImplications"
    )
    prognostic_implications: list[OncoKBTherapeuticImplication] = Field(
        default_factory=list, alias="prognosticImplications"
    )
    treatments: list[OncoKBTherapeuticImplication] = Field(
        default_factory=list
    )

    class Config:
        """Pydantic configuration."""

        populate_by_name = True

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
