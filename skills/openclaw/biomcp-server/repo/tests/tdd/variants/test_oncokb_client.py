# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Comprehensive unit tests for OncoKB client."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from biomcp.http_client import RequestError
from biomcp.variants.oncokb_client import (
    ONCOKB_DEMO_URL,
    ONCOKB_PROD_URL,
    OncoKBClient,
)


# Load mock responses from test data file
def load_mock_responses() -> dict:
    """Load mock OncoKB responses from JSON file."""
    test_data_dir = Path(__file__).parent.parent.parent / "data"
    mock_file = test_data_dir / "oncokb_mock_responses.json"
    with open(mock_file) as f:
        return json.load(f)


@pytest.fixture
def mock_responses():
    """Fixture providing mock OncoKB responses."""
    return load_mock_responses()


class TestOncoKBClient:
    """Test suite for OncoKBClient functionality."""

    def test_client_initialization_demo(self):
        """Test client initializes with demo URL when no token present."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()
            assert client.base_url == ONCOKB_DEMO_URL
            assert client.is_demo is True
            assert "Accept" in client.headers
            assert "Authorization" not in client.headers

    def test_client_initialization_prod(self):
        """Test client switches to production URL when token is set."""
        with (
            patch.dict(os.environ, {"ONCOKB_TOKEN": "test-token"}, clear=True),
            patch("biomcp.variants.oncokb_client.ONCOKB_TOKEN", "test-token"),
        ):
            client = OncoKBClient()
            assert client.base_url == ONCOKB_PROD_URL
            assert client.is_demo is False
            assert "Authorization" in client.headers
            assert client.headers["Authorization"] == "Bearer test-token"

    def test_token_detection_with_bearer_prefix(self):
        """Test that Bearer prefix is not duplicated if already present."""
        with (
            patch.dict(
                os.environ,
                {"ONCOKB_TOKEN": "Bearer existing-token"},
                clear=True,
            ),
            patch(
                "biomcp.variants.oncokb_client.ONCOKB_TOKEN",
                "Bearer existing-token",
            ),
        ):
            client = OncoKBClient()
            assert client.headers["Authorization"] == "Bearer existing-token"
            assert not client.headers["Authorization"].startswith(
                "Bearer Bearer"
            )

    def test_server_selection_demo_mode(self):
        """Test demo server selection when no token is configured."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()
            assert client.base_url == ONCOKB_DEMO_URL
            assert client.is_demo is True

    def test_server_selection_prod_mode(self):
        """Test production server selection when token is configured."""
        token = "my-oncokb-token"  # noqa: S105 - test token
        with (
            patch.dict(os.environ, {"ONCOKB_TOKEN": token}, clear=True),
            patch("biomcp.variants.oncokb_client.ONCOKB_TOKEN", token),
        ):
            client = OncoKBClient()
            assert client.base_url == ONCOKB_PROD_URL
            assert client.is_demo is False

    @pytest.mark.asyncio
    async def test_get_curated_genes_success(self, mock_responses):
        """Test successful retrieval of curated genes list."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            mock_genes = mock_responses["allCuratedGenes"]

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (mock_genes, None)

                result, error = await client.get_curated_genes()

                # Verify result
                assert error is None
                assert result is not None
                assert isinstance(result, list)
                assert len(result) == 3

                # Check BRAF entry
                braf = next(
                    (g for g in result if g["hugoSymbol"] == "BRAF"), None
                )
                assert braf is not None
                assert braf["entrezGeneId"] == 673
                assert braf["geneType"] == "ONCOGENE"
                assert "BRAF" in braf["summary"]

                # Check TP53 entry
                tp53 = next(
                    (g for g in result if g["hugoSymbol"] == "TP53"), None
                )
                assert tp53 is not None
                assert tp53["geneType"] == "TSG"
                assert tp53["entrezGeneId"] == 7157

                # Verify API was called correctly
                mock_request.assert_called_once()
                call_kwargs = mock_request.call_args[1]
                assert call_kwargs["domain"] == "oncokb"
                assert call_kwargs["endpoint_key"] == "oncokb_curated_genes"
                assert call_kwargs["cache_ttl"] == 86400  # 24 hours

    @pytest.mark.asyncio
    async def test_get_curated_genes_api_error(self):
        """Test handling of API errors in get_curated_genes."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            error_response = RequestError(
                code=500, message="Internal server error"
            )

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (None, error_response)

                result, error = await client.get_curated_genes()

                assert result is None
                assert error is not None
                assert error.code == 500
                assert "Internal server error" in error.message

    @pytest.mark.asyncio
    async def test_get_curated_genes_unexpected_format(self):
        """Test handling of unexpected response format."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            # Return dict instead of list
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = ({"error": "not a list"}, None)

                result, error = await client.get_curated_genes()

                assert result is None
                assert error is not None
                assert "Unexpected response format" in error.message

    @pytest.mark.asyncio
    async def test_get_curated_genes_exception_handling(self):
        """Test exception handling in get_curated_genes."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.side_effect = ValueError("Unexpected error")

                result, error = await client.get_curated_genes()

                assert result is None
                assert error is not None
                assert "Failed to fetch curated genes" in error.message

    @pytest.mark.asyncio
    async def test_get_gene_annotation_success(self, mock_responses):
        """Test successful retrieval of BRAF gene annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            mock_annotation = mock_responses["genesByHugoSymbol"][0]

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (mock_annotation, None)

                result, error = await client.get_gene_annotation("BRAF")

                # Verify result
                assert error is None
                assert result is not None
                assert result["hugoSymbol"] == "BRAF"
                assert result["entrezGeneId"] == 673
                assert result["geneType"] == "ONCOGENE"
                assert "geneAliases" in result
                assert "BRAF1" in result["geneAliases"]

                # Verify API was called correctly
                mock_request.assert_called_once()
                call_kwargs = mock_request.call_args[1]
                assert call_kwargs["domain"] == "oncokb"
                assert call_kwargs["endpoint_key"] == "oncokb_gene_annotation"
                assert call_kwargs["cache_ttl"] == 3600  # 1 hour

    @pytest.mark.asyncio
    async def test_get_gene_annotation_multiple_genes(self, mock_responses):
        """Test annotation retrieval for multiple different genes."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            # Test BRAF
            braf_annotation = mock_responses["genesByHugoSymbol"][0]
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (braf_annotation, None)
                result, error = await client.get_gene_annotation("BRAF")
                assert error is None
                assert result["hugoSymbol"] == "BRAF"

            # Test ROS1
            ros1_annotation = mock_responses["genesByHugoSymbol"][1]
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (ros1_annotation, None)
                result, error = await client.get_gene_annotation("ROS1")
                assert error is None
                assert result["hugoSymbol"] == "ROS1"
                assert result["geneType"] == "ONCOGENE"

            # Test TP53
            tp53_annotation = mock_responses["genesByHugoSymbol"][2]
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (tp53_annotation, None)
                result, error = await client.get_gene_annotation("TP53")
                assert error is None
                assert result["hugoSymbol"] == "TP53"
                assert result["geneType"] == "TSG"

    @pytest.mark.asyncio
    async def test_get_gene_annotation_api_error(self):
        """Test handling of API errors in get_gene_annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            error_response = RequestError(code=404, message="Gene not found")

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (None, error_response)

                result, error = await client.get_gene_annotation("INVALID")

                assert result is None
                assert error is not None
                assert error.code == 404

    @pytest.mark.asyncio
    async def test_get_gene_annotation_unexpected_format(self):
        """Test handling of unexpected response format in gene annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            # Return list instead of dict
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (["not", "a", "dict"], None)

                result, error = await client.get_gene_annotation("BRAF")

                assert result is None
                assert error is not None
                assert "Unexpected response format" in error.message

    @pytest.mark.asyncio
    async def test_get_variant_annotation_success(self, mock_responses):
        """Test successful retrieval of BRAF V600E variant annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            mock_annotation = mock_responses["variantAnnotation"][
                "BRAF_V600E_melanoma"
            ]

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (mock_annotation, None)

                result, error = await client.get_variant_annotation(
                    "BRAF", "V600E"
                )

                # Verify result
                assert error is None
                assert result is not None

                # Check query details
                query = result["query"]
                assert query["hugoSymbol"] == "BRAF"
                assert query["alteration"] == "V600E"
                assert query["entrezGeneId"] == 673

                # Check oncogenicity
                assert result["oncogenic"] == "Oncogenic"
                assert result["mutationEffect"]["knownEffect"] == (
                    "Gain-of-function"
                )

                # Check evidence levels
                assert result["highestSensitiveLevel"] == "LEVEL_1"
                assert result["highestFdaLevel"] == "LEVEL_Fda2"
                assert result["hotspot"] is True

                # Check treatments
                treatments = result["treatments"]
                assert len(treatments) > 0
                dabrafenib_treatment = treatments[0]
                assert dabrafenib_treatment["level"] == "LEVEL_1"
                assert len(dabrafenib_treatment["drugs"]) > 0
                assert dabrafenib_treatment["drugs"][0]["drugName"] == (
                    "Dabrafenib"
                )

                # Verify API was called correctly
                mock_request.assert_called_once()
                call_kwargs = mock_request.call_args[1]
                assert call_kwargs["domain"] == "oncokb"
                assert (
                    call_kwargs["endpoint_key"] == "oncokb_variant_annotation"
                )
                assert call_kwargs["cache_ttl"] == 3600  # 1 hour

    @pytest.mark.asyncio
    async def test_get_variant_annotation_parameters(self):
        """Test that variant annotation sends correct parameters."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (
                    {"query": {}, "oncogenic": "Oncogenic"},
                    None,
                )

                await client.get_variant_annotation("BRAF", "V600E")

                # Verify parameters
                call_kwargs = mock_request.call_args[1]
                request_params = call_kwargs["request"]
                assert request_params["hugoSymbol"] == "BRAF"
                assert request_params["alteration"] == "V600E"
                assert "_headers" in request_params

    @pytest.mark.asyncio
    async def test_get_variant_annotation_api_error(self):
        """Test handling of API errors in get_variant_annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            error_response = RequestError(
                code=404, message="Variant not found"
            )

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (None, error_response)

                result, error = await client.get_variant_annotation(
                    "BRAF", "INVALID"
                )

                assert result is None
                assert error is not None
                assert error.code == 404

    @pytest.mark.asyncio
    async def test_get_variant_annotation_exception_handling(self):
        """Test exception handling in get_variant_annotation."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.side_effect = RuntimeError("Network error")

                result, error = await client.get_variant_annotation(
                    "BRAF", "V600E"
                )

                assert result is None
                assert error is not None
                assert "Failed to fetch variant annotation" in error.message

    def test_headers_json_formatting(self):
        """Test that headers are properly formatted as JSON."""
        with (
            patch.dict(os.environ, {"ONCOKB_TOKEN": "test-token"}, clear=True),
            patch("biomcp.variants.oncokb_client.ONCOKB_TOKEN", "test-token"),
        ):
            client = OncoKBClient()
            headers_json = client._headers_json()

            # Should be valid JSON
            parsed = json.loads(headers_json)
            assert "Accept" in parsed
            assert "Authorization" in parsed
            assert parsed["Authorization"] == "Bearer test-token"

    @pytest.mark.asyncio
    async def test_error_handling_graceful_degradation(self):
        """Test that all methods gracefully handle errors and return None."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            # Simulate complete API failure
            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = (
                    None,
                    RequestError(code=503, message="Service unavailable"),
                )

                # All methods should return None without raising exceptions
                genes_result, genes_error = await client.get_curated_genes()
                assert genes_result is None
                assert genes_error is not None

                gene_result, gene_error = await client.get_gene_annotation(
                    "BRAF"
                )
                assert gene_result is None
                assert gene_error is not None

                (
                    variant_result,
                    variant_error,
                ) = await client.get_variant_annotation("BRAF", "V600E")
                assert variant_result is None
                assert variant_error is not None

    @pytest.mark.asyncio
    async def test_caching_behavior(self):
        """Test that caching parameters are correctly set."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = ([], None)

                # Test curated genes - 24 hour cache
                await client.get_curated_genes()
                assert mock_request.call_args[1]["cache_ttl"] == 86400

                # Test gene annotation - 1 hour cache
                mock_request.return_value = ({}, None)
                await client.get_gene_annotation("BRAF")
                assert mock_request.call_args[1]["cache_ttl"] == 3600

                # Test variant annotation - 1 hour cache
                await client.get_variant_annotation("BRAF", "V600E")
                assert mock_request.call_args[1]["cache_ttl"] == 3600

    @pytest.mark.asyncio
    async def test_retry_enabled_for_all_methods(self):
        """Test that retry is enabled for all API methods."""
        with patch.dict(os.environ, {}, clear=True):
            client = OncoKBClient()

            with patch(
                "biomcp.variants.oncokb_client.request_api"
            ) as mock_request:
                mock_request.return_value = ([], None)

                await client.get_curated_genes()
                assert mock_request.call_args[1]["enable_retry"] is True

                mock_request.return_value = ({}, None)
                await client.get_gene_annotation("BRAF")
                assert mock_request.call_args[1]["enable_retry"] is True

                await client.get_variant_annotation("BRAF", "V600E")
                assert mock_request.call_args[1]["enable_retry"] is True

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
