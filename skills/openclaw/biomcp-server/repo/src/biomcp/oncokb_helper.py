# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Helper module for OncoKB integration across tools.

This module centralizes OncoKB annotation logic to avoid duplication
and provides human-readable markdown formatting of OncoKB data.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def get_oncokb_annotation_for_variant(
    gene: str, variant: str
) -> str | None:
    """Get OncoKB annotation for a specific variant.

    Fetches clinical annotation including oncogenicity, mutation effect,
    and therapeutic implications from OncoKB API.

    Args:
        gene: HUGO gene symbol (e.g., "BRAF")
        variant: Protein change notation (e.g., "V600E")

    Returns:
        Formatted markdown annotation or None if unavailable
    """
    if not gene or not variant:
        return None

    try:
        from biomcp.variants.oncokb_client import OncoKBClient

        client = OncoKBClient()
        annotation, error = await client.get_variant_annotation(gene, variant)

        if error or not annotation:
            logger.warning(
                f"Failed to get OncoKB annotation for {gene} {variant}"
            )
            return None

        return _format_variant_annotation(annotation)

    except Exception as e:
        logger.warning(
            f"Failed to get OncoKB annotation for {gene} {variant}: {e}"
        )
        return None


async def get_oncokb_summary_for_genes(
    genes: list[str],
) -> str | None:
    """Get OncoKB summary for multiple genes.

    Fetches gene annotations from the curated genes list and aggregates
    results into a markdown table showing gene type, oncogenicity, and
    clinical actionability.

    Args:
        genes: List of HUGO gene symbols (e.g., ["BRAF", "TP53"])

    Returns:
        Formatted markdown table or None if unavailable
    """
    if not genes:
        return None

    try:
        from biomcp.variants.oncokb_client import OncoKBClient

        client = OncoKBClient()

        # Get all curated genes (cached for 24h)
        curated_genes, error = await client.get_curated_genes()
        if error or not curated_genes:
            logger.info("Failed to fetch OncoKB curated genes")
            return None

        # Build lookup dict by gene symbol
        gene_dict = {
            gene_data["hugoSymbol"]: gene_data for gene_data in curated_genes
        }

        # Filter for requested genes
        annotations: list[tuple[str, dict[str, Any]]] = []
        for gene in genes:
            if gene in gene_dict:
                annotations.append((gene, gene_dict[gene]))
            else:
                logger.debug(f"Gene {gene} not found in OncoKB curated genes")

        if not annotations:
            logger.info("No OncoKB annotations available for genes")
            return None

        return _format_gene_summary(annotations)

    except Exception as e:
        logger.warning(f"Failed to get OncoKB summary for genes: {e}")
        return None


def _format_variant_annotation(annotation: dict[str, Any]) -> str:
    """Format variant annotation as human-readable markdown.

    Args:
        annotation: OncoKB variant annotation response

    Returns:
        Formatted markdown string
    """
    lines: list[str] = []

    # Header section
    _add_header_section(lines, annotation)

    # Basic annotation information
    _add_basic_annotations(lines, annotation)

    # Evidence levels
    _add_evidence_levels(lines, annotation)

    # Clinical implications
    _add_clinical_implications(lines, annotation)

    return "\n".join(lines)


def _add_header_section(lines: list[str], annotation: dict[str, Any]) -> None:
    """Add header section to annotation output."""
    query = annotation.get("query", {})
    gene = query.get("hugoSymbol", "Unknown")
    alteration = query.get("alteration", "Unknown")
    lines.append(f"\n### OncoKB Annotation: {gene} {alteration}")


def _add_basic_annotations(
    lines: list[str], annotation: dict[str, Any]
) -> None:
    """Add oncogenicity and mutation effect information."""
    # Oncogenicity
    oncogenic = annotation.get("oncogenic", "Unknown")
    if oncogenic:
        lines.append(f"- **Oncogenicity**: {oncogenic}")

    # Mutation effect
    mutation_effect = annotation.get("mutationEffect", {})
    if mutation_effect:
        effect = mutation_effect.get("knownEffect", "Unknown")
        description = mutation_effect.get("description", "")
        lines.append(f"- **Mutation Effect**: {effect}")
        if description:
            # Truncate long descriptions
            if len(description) > 200:
                description = description[:197] + "..."
            lines.append(f"  - {description}")


def _add_evidence_levels(lines: list[str], annotation: dict[str, Any]) -> None:
    """Add evidence level information."""
    sensitive_level = annotation.get("highestSensitiveLevel")
    resistance_level = annotation.get("highestResistanceLevel")

    if sensitive_level:
        lines.append(f"- **Highest Sensitivity Level**: {sensitive_level}")
    if resistance_level:
        lines.append(f"- **Highest Resistance Level**: {resistance_level}")


def _add_clinical_implications(
    lines: list[str], annotation: dict[str, Any]
) -> None:
    """Add therapeutic, diagnostic, and prognostic implications."""
    # Therapeutic implications
    treatments = annotation.get("treatments", [])
    if treatments:
        lines.append("\n**Therapeutic Implications:**")
        for treatment in treatments[:3]:  # Show top 3
            cancer_type = treatment.get("cancerType", "Unknown")
            level = treatment.get("level", "Unknown")
            drugs = treatment.get("drugs", [])
            drug_names = ", ".join([
                d.get("drugName", "") for d in drugs if d.get("drugName")
            ])
            if drug_names:
                lines.append(f"- {cancer_type}: {drug_names} (Level {level})")

    # Diagnostic/prognostic implications
    diagnostic = annotation.get("diagnosticImplications", [])
    prognostic = annotation.get("prognosticImplications", [])

    if diagnostic:
        lines.append(
            f"\n**Diagnostic Implications**: {len(diagnostic)} cancer type(s)"
        )
    if prognostic:
        lines.append(
            f"**Prognostic Implications**: {len(prognostic)} cancer type(s)"
        )


def _format_gene_summary(annotations: list[tuple[str, dict[str, Any]]]) -> str:
    """Format gene annotations as markdown table.

    Args:
        annotations: List of tuples (gene_symbol, annotation_dict)

    Returns:
        Formatted markdown table
    """
    lines = [
        "\n### OncoKB Gene Summary",
        "| Gene | Type | Highest Level | Clinical Implications |",
        "|------|------|---------------|----------------------|",
    ]

    for gene, annotation in annotations:
        # Get gene type from curated genes API format
        gene_type = annotation.get("geneType", "-")
        if gene_type:
            gene_type = gene_type.title()  # ONCOGENE -> Oncogene

        # Get highest sensitive level
        sensitive_level = annotation.get("highestSensitiveLevel", "-")

        # Extract summary (truncated)
        summary = annotation.get("summary", "")
        if summary:
            # Extract first sentence or truncate
            first_sentence = summary.split(". ")[0]
            if len(first_sentence) > 80:
                first_sentence = first_sentence[:77] + "..."
            clinical_info = first_sentence
        else:
            clinical_info = "No summary available"

        lines.append(
            f"| {gene} | {gene_type} | {sensitive_level} | {clinical_info} |"
        )

    return "\n".join(lines)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
