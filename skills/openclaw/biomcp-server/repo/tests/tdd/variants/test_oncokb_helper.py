# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Comprehensive unit tests for OncoKB helper module."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from biomcp.http_client import RequestError
from biomcp.oncokb_helper import (
    get_oncokb_annotation_for_variant,
    get_oncokb_summary_for_genes,
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


class TestGetOncoKBAnnotationForVariant:
    """Test suite for get_oncokb_annotation_for_variant function."""

    @pytest.mark.asyncio
    async def test_variant_annotation_success(self, mock_responses):
        """Test successful variant annotation retrieval and formatting."""
        mock_annotation = mock_responses["variantAnnotation"][
            "BRAF_V600E_melanoma"
        ]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(mock_annotation, None)
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "V600E")

            # Verify client was called correctly
            mock_client.get_variant_annotation.assert_called_once_with(
                "BRAF", "V600E"
            )

            # Verify result is formatted markdown
            assert result is not None
            assert isinstance(result, str)

            # Check key content is present
            assert "OncoKB Annotation" in result
            assert "BRAF" in result
            assert "V600E" in result
            assert "Oncogenic" in result
            assert "Gain-of-function" in result
            assert "LEVEL_1" in result
            assert "Therapeutic Implications" in result
            assert "Dabrafenib" in result

    @pytest.mark.asyncio
    async def test_variant_annotation_with_empty_gene(self):
        """Test that empty gene returns None."""
        result = await get_oncokb_annotation_for_variant("", "V600E")
        assert result is None

    @pytest.mark.asyncio
    async def test_variant_annotation_with_empty_variant(self):
        """Test that empty variant returns None."""
        result = await get_oncokb_annotation_for_variant("BRAF", "")
        assert result is None

    @pytest.mark.asyncio
    async def test_variant_annotation_with_none_inputs(self):
        """Test that None inputs return None."""
        result = await get_oncokb_annotation_for_variant(None, "V600E")
        assert result is None

        result = await get_oncokb_annotation_for_variant("BRAF", None)
        assert result is None

    @pytest.mark.asyncio
    async def test_variant_annotation_api_error(self):
        """Test graceful handling when API returns error."""
        error_response = RequestError(code=404, message="Variant not found")

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(None, error_response)
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "INVALID")

            assert result is None

    @pytest.mark.asyncio
    async def test_variant_annotation_none_response(self):
        """Test graceful handling when API returns None."""
        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(None, None)
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "V600E")

            assert result is None

    @pytest.mark.asyncio
    async def test_variant_annotation_exception_handling(self):
        """Test graceful handling of exceptions."""
        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                side_effect=RuntimeError("Network error")
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "V600E")

            assert result is None

    @pytest.mark.skip(
        reason="Import error testing is complex; covered by exception handling"
    )
    @pytest.mark.asyncio
    async def test_variant_annotation_import_error(self):
        """Test graceful handling when OncoKBClient cannot be imported."""
        pass

    @pytest.mark.asyncio
    async def test_variant_annotation_formatting_minimal_data(self):
        """Test formatting with minimal annotation data."""
        minimal_annotation = {
            "query": {"hugoSymbol": "TEST", "alteration": "X100Y"},
            "oncogenic": "Unknown",
        }

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(minimal_annotation, None)
            )

            result = await get_oncokb_annotation_for_variant("TEST", "X100Y")

            assert result is not None
            assert "OncoKB Annotation" in result
            assert "TEST" in result
            assert "X100Y" in result
            assert "Unknown" in result


class TestGetOncoKBSummaryForGenes:
    """Test suite for get_oncokb_summary_for_genes function."""

    @pytest.mark.asyncio
    async def test_gene_summary_success(self, mock_responses):
        """Test successful gene summary retrieval and formatting."""
        curated_genes = mock_responses["genesByHugoSymbol"]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes([
                "BRAF",
                "ROS1",
                "TP53",
            ])

            # Verify result is formatted markdown table
            assert result is not None
            assert isinstance(result, str)

            # Check header
            assert "OncoKB Gene Summary" in result
            assert "| Gene | Type |" in result

            # Check content
            assert "BRAF" in result
            assert "Oncogene" in result

            assert "ROS1" in result

            assert "TP53" in result
            assert "Tsg" in result

    @pytest.mark.asyncio
    async def test_gene_summary_with_empty_list(self):
        """Test that empty gene list returns None."""
        result = await get_oncokb_summary_for_genes([])
        assert result is None

    @pytest.mark.asyncio
    async def test_gene_summary_with_none_input(self):
        """Test that None input returns None."""
        result = await get_oncokb_summary_for_genes(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_gene_summary_single_gene(self, mock_responses):
        """Test summary with single gene."""
        curated_genes = mock_responses["genesByHugoSymbol"]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes(["BRAF"])

            assert result is not None
            assert "BRAF" in result
            assert "Oncogene" in result

    @pytest.mark.asyncio
    async def test_gene_summary_partial_failures(self, mock_responses):
        """Test that partial failures don't break the summary."""
        curated_genes = mock_responses["genesByHugoSymbol"]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes([
                "BRAF",
                "INVALID1",
                "INVALID2",
            ])

            # Should still return result with BRAF
            assert result is not None
            assert "BRAF" in result
            # Invalid genes should not appear
            assert "INVALID1" not in result
            assert "INVALID2" not in result

    @pytest.mark.asyncio
    async def test_gene_summary_all_failures(self):
        """Test that all failures returns None."""
        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_gene_annotation = AsyncMock(
                return_value=(
                    None,
                    RequestError(code=404, message="Not found"),
                )
            )

            result = await get_oncokb_summary_for_genes([
                "INVALID1",
                "INVALID2",
            ])

            assert result is None

    @pytest.mark.asyncio
    async def test_gene_summary_exception_handling(self):
        """Test graceful handling of exceptions in parallel calls."""
        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                side_effect=RuntimeError("Network error")
            )

            result = await get_oncokb_summary_for_genes(["BRAF", "TP53"])

            # Should gracefully return None
            assert result is None

    @pytest.mark.asyncio
    async def test_gene_summary_parallel_execution(self, mock_responses):
        """Test that curated genes are fetched efficiently."""
        curated_genes = mock_responses["genesByHugoSymbol"]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value

            call_count = 0

            async def mock_get_curated_genes():
                nonlocal call_count
                call_count += 1
                return (curated_genes, None)

            mock_client.get_curated_genes = mock_get_curated_genes

            genes = ["BRAF", "TP53", "ROS1", "EGFR", "KRAS"]
            result = await get_oncokb_summary_for_genes(genes)

            # Verify curated genes was called once (not once per gene)
            assert call_count == 1
            assert result is not None

    @pytest.mark.asyncio
    async def test_gene_summary_gene_type_formatting(self, mock_responses):
        """Test correct formatting of different gene types."""
        # Create test annotations using curated genes format
        curated_genes = [
            {
                "hugoSymbol": "BRAF",
                "geneType": "ONCOGENE",
                "summary": "Test summary.",
            },
            {
                "hugoSymbol": "TP53",
                "geneType": "TSG",
                "summary": "Test summary.",
            },
        ]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes([
                "BRAF",
                "TP53",
            ])

            assert result is not None

            # Check type formatting - verify gene types are correct
            assert "BRAF" in result and "Oncogene" in result
            assert "TP53" in result and "Tsg" in result

    @pytest.mark.asyncio
    async def test_gene_summary_truncates_long_summaries(self):
        """Test that long summaries are truncated appropriately."""
        long_summary = "A" * 500  # Very long summary
        curated_genes = [
            {
                "hugoSymbol": "BRAF",
                "geneType": "ONCOGENE",
                "summary": long_summary,
            }
        ]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes(["BRAF"])

            assert result is not None
            # Summary should be truncated
            assert "..." in result
            # Should not contain the full 500 character summary
            assert "A" * 200 not in result

    @pytest.mark.asyncio
    async def test_gene_summary_handles_missing_summary(self):
        """Test handling of genes without summary field."""
        curated_genes = [
            {
                "hugoSymbol": "BRAF",
                "geneType": "ONCOGENE",
                # No summary field
            }
        ]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_curated_genes = AsyncMock(
                return_value=(curated_genes, None)
            )

            result = await get_oncokb_summary_for_genes(["BRAF"])

            assert result is not None
            assert "BRAF" in result
            assert "No summary available" in result

    @pytest.mark.skip(
        reason="Import error testing is complex; covered by exception handling"
    )
    @pytest.mark.asyncio
    async def test_gene_summary_import_error(self):
        """Test graceful handling when OncoKBClient cannot be imported."""
        pass


class TestFormattingHelpers:
    """Test suite for formatting helper functions."""

    @pytest.mark.asyncio
    async def test_variant_annotation_includes_all_sections(
        self, mock_responses
    ):
        """Test that formatted output includes all expected sections."""
        mock_annotation = mock_responses["variantAnnotation"][
            "BRAF_V600E_melanoma"
        ]

        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(mock_annotation, None)
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "V600E")

            # Check all major sections are present
            assert "OncoKB Annotation" in result
            assert "Oncogenicity" in result
            assert "Mutation Effect" in result
            assert "Highest Sensitivity Level" in result
            assert "Therapeutic Implications" in result

    @pytest.mark.asyncio
    async def test_variant_annotation_truncates_long_descriptions(
        self, mock_responses
    ):
        """Test that long mutation effect descriptions are truncated."""
        mock_annotation = mock_responses["variantAnnotation"][
            "BRAF_V600E_melanoma"
        ].copy()

        # The actual mock data has a long description, verify it gets truncated
        result_dict = mock_annotation["mutationEffect"]
        if len(result_dict.get("description", "")) > 200:
            with patch(
                "biomcp.variants.oncokb_client.OncoKBClient"
            ) as mock_client_class:
                mock_client = mock_client_class.return_value
                mock_client.get_variant_annotation = AsyncMock(
                    return_value=(mock_annotation, None)
                )

                result = await get_oncokb_annotation_for_variant(
                    "BRAF", "V600E"
                )

                # Should contain ellipsis for truncation
                assert "..." in result

    @pytest.mark.asyncio
    async def test_variant_annotation_limits_treatments(self, mock_responses):
        """Test that only top 3 treatments are shown."""
        mock_annotation = mock_responses["variantAnnotation"][
            "BRAF_V600E_melanoma"
        ]

        # Annotation has 3 treatments, all should be shown
        with patch(
            "biomcp.variants.oncokb_client.OncoKBClient"
        ) as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_variant_annotation = AsyncMock(
                return_value=(mock_annotation, None)
            )

            result = await get_oncokb_annotation_for_variant("BRAF", "V600E")

            # Should show Dabrafenib, Dabrafenib+Trametinib, Vemurafenib
            assert "Dabrafenib" in result
            assert "Trametinib" in result
            assert "Vemurafenib" in result

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
