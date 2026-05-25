# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""OncoKB API client for variant annotation and curation data.

This module provides access to OncoKB (Precision Oncology Knowledge Base),
which curates oncogenic alterations and therapeutic implications. It handles:
- Gene-level annotations and actionability
- Variant-level therapeutic, diagnostic, and prognostic information
- Evidence-based clinical implications
- Automatic demo vs production server detection

OncoKB provides FDA-recognized precision oncology knowledge with levels of
evidence ranging from FDA-approved therapies to case reports.

Example:
    client = OncoKBClient()
    genes = await client.get_curated_genes()
    annotation = await client.get_gene_annotation("BRAF")
    variant = await client.get_variant_annotation("BRAF", "V600E")
"""

import logging
import os
from typing import Any

from ..http_client import RequestError, request_api

logger = logging.getLogger(__name__)

# OncoKB API endpoints
ONCOKB_DEMO_URL = "https://demo.oncokb.org/api/v1"
ONCOKB_PROD_URL = "https://www.oncokb.org/api/v1"
ONCOKB_TOKEN = os.getenv("ONCOKB_TOKEN")


class OncoKBClient:
    """Client for OncoKB API interactions."""

    def __init__(self):
        """Initialize OncoKB client with appropriate base URL and auth.

        Uses demo server by default. Switches to production server when
        ONCOKB_TOKEN environment variable is set.
        """
        self.base_url = ONCOKB_PROD_URL if ONCOKB_TOKEN else ONCOKB_DEMO_URL
        self.headers = self._build_headers()
        self.is_demo = not bool(ONCOKB_TOKEN)

        if self.is_demo:
            logger.info(
                "Using OncoKB demo server (limited data). Set "
                "ONCOKB_TOKEN env var for full access."
            )

    def _build_headers(self) -> dict[str, str]:
        """Build authorization headers if token is available.

        Returns:
            Dictionary with Authorization header if token present.
        """
        headers = {"Accept": "application/json"}
        if ONCOKB_TOKEN:
            if not ONCOKB_TOKEN.startswith("Bearer "):
                headers["Authorization"] = f"Bearer {ONCOKB_TOKEN}"
            else:
                headers["Authorization"] = ONCOKB_TOKEN
        return headers

    async def get_curated_genes(
        self,
    ) -> tuple[list[dict[str, Any]] | None, RequestError | None]:
        """Get list of all curated genes in OncoKB.

        Returns genes that have been curated with oncogenic mutations
        and/or therapeutic implications.

        Returns:
            Tuple of (gene_list, error). Gene list contains dicts with:
                - entrezGeneId: Entrez gene ID
                - hugoSymbol: HUGO gene symbol
                - oncogene: Boolean indicating oncogene status
                - tsg: Boolean indicating tumor suppressor gene status
        """
        url = f"{self.base_url}/utils/allCuratedGenes"

        try:
            result, error = await request_api(
                url=url,
                request={"_headers": self._headers_json()},
                method="GET",
                domain="oncokb",
                endpoint_key="oncokb_curated_genes",
                cache_ttl=86400,  # Cache for 24 hours
                enable_retry=True,
            )

            if error:
                logger.warning(
                    f"Failed to fetch curated genes from OncoKB: "
                    f"{error.message}"
                )
                return None, error

            if not isinstance(result, list):
                return None, RequestError(
                    code=500,
                    message="Unexpected response format from OncoKB",
                )

            return result, None

        except Exception as e:
            logger.error(
                f"Unexpected error fetching OncoKB curated genes: "
                f"{type(e).__name__}: {e}"
            )
            return None, RequestError(
                code=500,
                message=f"Failed to fetch curated genes: {e}",
            )

    async def get_gene_annotation(
        self, gene: str
    ) -> tuple[dict[str, Any] | None, RequestError | None]:
        """Get comprehensive annotation for a specific gene.

        Provides gene-level information including:
        - Oncogene/TSG classification
        - Summary of alterations and clinical actionability
        - Background information

        Args:
            gene: HUGO gene symbol (e.g., "BRAF", "TP53")

        Returns:
            Tuple of (annotation_data, error). Annotation contains:
                - entrezGeneId: Entrez gene ID
                - hugoSymbol: HUGO gene symbol
                - oncogene: Boolean oncogene status
                - tsg: Boolean tumor suppressor status
                - background: Gene description and function
                - summary: Clinical relevance summary
        """
        url = f"{self.base_url}/genes/{gene}"

        try:
            result, error = await request_api(
                url=url,
                request={"_headers": self._headers_json()},
                method="GET",
                domain="oncokb",
                endpoint_key="oncokb_gene_annotation",
                cache_ttl=3600,  # Cache for 1 hour
                enable_retry=True,
            )

            if error:
                logger.warning(
                    f"Failed to fetch gene annotation for {gene}: "
                    f"{error.message}"
                )
                return None, error

            if not isinstance(result, dict):
                return None, RequestError(
                    code=500,
                    message="Unexpected response format from OncoKB",
                )

            return result, None

        except Exception as e:
            logger.error(
                f"Unexpected error fetching OncoKB annotation for "
                f"{gene}: {type(e).__name__}: {e}"
            )
            return None, RequestError(
                code=500,
                message=f"Failed to fetch gene annotation: {e}",
            )

    async def get_variant_annotation(
        self, gene: str, protein_change: str
    ) -> tuple[dict[str, Any] | None, RequestError | None]:
        """Get clinical annotation for a specific variant.

        Provides variant-level therapeutic, diagnostic, and prognostic
        information with evidence levels.

        Args:
            gene: HUGO gene symbol (e.g., "BRAF")
            protein_change: Protein change notation (e.g., "V600E")

        Returns:
            Tuple of (annotation_data, error). Annotation contains:
                - query: Input query details
                - oncogenic: Oncogenicity classification
                - mutationEffect: Biological effect
                - treatments: Therapeutic implications by cancer type
                - diagnosticImplications: Diagnostic markers
                - prognosticImplications: Prognostic markers
                - highestSensitiveLevel: Highest evidence level
                - highestResistanceLevel: Highest resistance level
        """
        url = f"{self.base_url}/annotate/mutations/byProteinChange"

        params = {
            "hugoSymbol": gene,
            "alteration": protein_change,
            "_headers": self._headers_json(),
        }

        try:
            result, error = await request_api(
                url=url,
                request=params,
                method="GET",
                domain="oncokb",
                endpoint_key="oncokb_variant_annotation",
                cache_ttl=3600,  # Cache for 1 hour
                enable_retry=True,
            )

            if error:
                logger.warning(
                    f"Failed to fetch variant annotation for "
                    f"{gene} {protein_change}: {error.message}"
                )
                return None, error

            if not isinstance(result, dict):
                return None, RequestError(
                    code=500,
                    message="Unexpected response format from OncoKB",
                )

            return result, None

        except Exception as e:
            logger.error(
                f"Unexpected error fetching OncoKB variant annotation "
                f"for {gene} {protein_change}: {type(e).__name__}: {e}"
            )
            return None, RequestError(
                code=500,
                message=f"Failed to fetch variant annotation: {e}",
            )

    def _headers_json(self) -> str:
        """Convert headers dict to JSON string for request_api.

        Returns:
            JSON string representation of headers.
        """
        import json

        return json.dumps(self.headers)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
