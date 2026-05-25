# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Tests for variant getter module."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from biomcp.constants import DEFAULT_ASSEMBLY
from biomcp.variants import getter


class TestGetVariant:
    """Test the get_variant function."""

    @pytest.mark.asyncio
    async def test_get_variant_default_assembly(self):
        """Test that get_variant defaults to hg19 assembly."""
        mock_response = {
            "_id": "rs113488022",
            "dbsnp": {"rsid": "rs113488022"},
        }

        with patch("biomcp.http_client.request_api") as mock_request:
            mock_request.return_value = (mock_response, None)

            await getter.get_variant("rs113488022")

            # Verify assembly parameter was passed with default value
            call_args = mock_request.call_args
            assert call_args[1]["request"]["assembly"] == "hg19"

    @pytest.mark.asyncio
    async def test_get_variant_hg38_assembly(self):
        """Test that get_variant accepts hg38 assembly parameter."""
        mock_response = {
            "_id": "rs113488022",
            "dbsnp": {"rsid": "rs113488022"},
        }

        with patch("biomcp.http_client.request_api") as mock_request:
            mock_request.return_value = (mock_response, None)

            await getter.get_variant("rs113488022", assembly="hg38")

            # Verify assembly parameter was passed correctly
            call_args = mock_request.call_args
            assert call_args[1]["request"]["assembly"] == "hg38"

    @pytest.mark.asyncio
    async def test_get_variant_hg19_assembly(self):
        """Test that get_variant accepts hg19 assembly parameter explicitly."""
        mock_response = {
            "_id": "rs113488022",
            "dbsnp": {"rsid": "rs113488022"},
        }

        with patch("biomcp.http_client.request_api") as mock_request:
            mock_request.return_value = (mock_response, None)

            await getter.get_variant("rs113488022", assembly="hg19")

            # Verify assembly parameter was passed correctly
            call_args = mock_request.call_args
            assert call_args[1]["request"]["assembly"] == "hg19"

    @pytest.mark.asyncio
    async def test_get_variant_includes_all_fields(self):
        """Test that request includes all required fields."""
        mock_response = {"_id": "rs113488022"}

        with patch("biomcp.http_client.request_api") as mock_request:
            mock_request.return_value = (mock_response, None)

            await getter.get_variant("rs113488022", assembly="hg38")

            # Verify both fields and assembly are in request
            call_args = mock_request.call_args
            request_params = call_args[1]["request"]
            assert "fields" in request_params
            assert request_params["fields"] == "all"
            assert "assembly" in request_params
            assert request_params["assembly"] == "hg38"

    @pytest.mark.asyncio
    async def test_get_variant_with_external_annotations(self):
        """Test that assembly parameter works with external annotations."""
        from biomcp.variants.external import EnhancedVariantAnnotation

        mock_response = {
            "_id": "rs113488022",
            "dbsnp": {"rsid": "rs113488022"},
            "dbnsfp": {"genename": "BRAF"},
        }

        with (
            patch("biomcp.http_client.request_api") as mock_request,
            patch(
                "biomcp.variants.getter.ExternalVariantAggregator"
            ) as mock_aggregator,
        ):
            mock_request.return_value = (mock_response, None)

            # Mock the aggregator with proper EnhancedVariantAnnotation
            mock_enhanced = EnhancedVariantAnnotation(
                variant_id="rs113488022",
                tcga=None,
                thousand_genomes=None,
                cbioportal=None,
                error_sources=[],
            )

            mock_agg_instance = AsyncMock()
            mock_agg_instance.get_enhanced_annotations = AsyncMock(
                return_value=mock_enhanced
            )
            # _extract_gene_aa_change is a regular (non-async) method
            mock_agg_instance._extract_gene_aa_change = Mock(
                return_value="BRAF V600E"
            )
            mock_aggregator.return_value = mock_agg_instance

            await getter.get_variant(
                "rs113488022",
                assembly="hg38",
                include_external=True,
            )

            # Verify assembly was still passed correctly
            call_args = mock_request.call_args
            assert call_args[1]["request"]["assembly"] == "hg38"


class TestVariantDetailsMCPTool:
    """Test the _variant_details MCP tool."""

    @pytest.mark.asyncio
    async def test_variant_details_default_assembly(self):
        """Test that _variant_details defaults to hg19 assembly."""
        with patch("biomcp.variants.getter.get_variant") as mock_get:
            mock_get.return_value = "Variant details"

            await getter._variant_details(
                call_benefit="Testing default assembly",
                variant_id="rs113488022",
            )

            # Verify get_variant was called with default assembly
            mock_get.assert_called_once_with(
                "rs113488022",
                output_json=False,
                include_external=True,
                assembly=DEFAULT_ASSEMBLY,
            )

    @pytest.mark.asyncio
    async def test_variant_details_custom_assembly(self):
        """Test that _variant_details accepts custom assembly parameter."""
        with patch("biomcp.variants.getter.get_variant") as mock_get:
            mock_get.return_value = "Variant details"

            await getter._variant_details(
                call_benefit="Testing hg38 assembly",
                variant_id="rs113488022",
                assembly="hg38",
            )

            # Verify get_variant was called with hg38
            mock_get.assert_called_once_with(
                "rs113488022",
                output_json=False,
                include_external=True,
                assembly="hg38",
            )

    @pytest.mark.asyncio
    async def test_variant_details_with_all_params(self):
        """Test that all parameters are passed through correctly."""
        with patch("biomcp.variants.getter.get_variant") as mock_get:
            mock_get.return_value = "Variant details"

            await getter._variant_details(
                call_benefit="Testing all parameters",
                variant_id="chr7:g.140453136A>T",
                include_external=False,
                assembly="hg19",
            )

            # Verify all params were passed
            mock_get.assert_called_once_with(
                "chr7:g.140453136A>T",
                output_json=False,
                include_external=False,
                assembly="hg19",
            )

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
