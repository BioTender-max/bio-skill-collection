# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Integration tests for OncoKB API.

These tests make real API calls to verify OncoKB integration works correctly.
They use the demo server by default (demo.oncokb.org) which has limited data.
Tests are marked with pytest.mark.integration and gracefully skip if API is
unavailable.

Demo Server Limitations:
- Only has data for BRAF, ROS1, and TP53
- No authentication required
- Limited to basic annotations

Production Server:
- Requires ONCOKB_TOKEN environment variable
- Full cancer gene database
- Complete therapeutic/diagnostic annotations
"""

import os

import pytest

from biomcp.variants.oncokb_client import OncoKBClient


@pytest.mark.integration
class TestOncoKBDemoServer:
    """Integration tests for OncoKB demo server (no auth required)."""

    @pytest.mark.asyncio
    async def test_demo_server_access(self):
        """Test basic access to demo server with curated genes list."""
        # Temporarily remove token to force demo server
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()

            # Verify demo server is being used
            assert client.is_demo is True
            assert "demo.oncokb.org" in client.base_url

            # Fetch curated genes list (this works on demo)
            result, error = await client.get_curated_genes()

            # Skip if demo server is unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB demo server unavailable: {error.message}")

            # Should succeed with curated genes
            assert error is None, f"Expected success but got error: {error}"
            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

            # Find BRAF in the results
            braf = next(
                (g for g in result if g.get("hugoSymbol") == "BRAF"), None
            )
            assert braf is not None, "BRAF should be in demo curated genes"

            print("✓ Demo server access successful")
            print(f"  Total curated genes: {len(result)}")
            print(f"  BRAF gene: {braf.get('hugoSymbol')}")
            print(f"  BRAF Entrez ID: {braf.get('entrezGeneId')}")
            print(f"  BRAF gene type: {braf.get('geneType')}")

        finally:
            # Restore token if it was set
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_demo_gene_limits(self):
        """Test that demo server only has BRAF, ROS1, and TP53."""
        # Temporarily remove token to force demo server
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()
            assert client.is_demo is True

            # Get all curated genes from demo
            result, error = await client.get_curated_genes()

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB demo server unavailable: {error.message}")

            assert error is None, f"Expected success but got error: {error}"
            assert result is not None
            assert isinstance(result, list)

            # Extract gene symbols
            gene_symbols = {g.get("hugoSymbol") for g in result}

            # Demo should have exactly BRAF, ROS1, and TP53
            expected_demo_genes = {"BRAF", "ROS1", "TP53"}
            assert gene_symbols == expected_demo_genes, (
                f"Expected demo genes {expected_demo_genes}, "
                f"got {gene_symbols}"
            )

            print(
                f"✓ Demo server has exactly the expected genes: {gene_symbols}"
            )

            # Verify KRAS is NOT in demo
            assert "KRAS" not in gene_symbols, "KRAS should not be in demo"
            print("✓ Demo correctly excludes non-demo genes like KRAS")

        finally:
            # Restore token if it was set
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_variant_annotation(self):
        """Test variant annotation with BRAF V600E on demo server."""
        # Temporarily remove token to force demo server
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()
            assert client.is_demo is True

            # Request BRAF V600E annotation
            result, error = await client.get_variant_annotation(
                gene="BRAF", protein_change="V600E"
            )

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB demo server unavailable: {error.message}")

            # Should get annotation for this well-known variant
            if error:
                # Some demo servers may not support variant endpoints
                print(
                    f"Note: Variant endpoint returned error: {error.message}"
                )
                pytest.skip("Demo variant endpoint not available")

            assert result is not None
            assert isinstance(result, dict)

            # Check basic annotation fields
            query = result.get("query", {})
            assert query.get("hugoSymbol") == "BRAF"
            assert query.get("alteration") == "V600E"

            # Check if variant is marked as oncogenic
            oncogenic = result.get("oncogenic")
            if oncogenic:
                print(f"✓ BRAF V600E oncogenicity: {oncogenic}")
                # V600E is a well-known oncogenic mutation
                assert "Oncogenic" in oncogenic or "Likely" in oncogenic

            # Check mutation effect
            mutation_effect = result.get("mutationEffect")
            if mutation_effect:
                known_effect = mutation_effect.get("knownEffect")
                print(f"✓ BRAF V600E effect: {known_effect}")

            # Check if it's a hotspot
            hotspot = result.get("hotspot")
            if hotspot is not None:
                print(f"✓ BRAF V600E hotspot: {hotspot}")
                # V600E is a known hotspot
                assert hotspot is True

            print("✓ Variant annotation successful for BRAF V600E")

        finally:
            # Restore token if it was set
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_curated_genes_demo(self):
        """Test fetching curated genes list from demo server."""
        # Temporarily remove token to force demo server
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()
            assert client.is_demo is True

            # Fetch curated genes
            result, error = await client.get_curated_genes()

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB demo server unavailable: {error.message}")

            # Should get a list of genes
            assert error is None, f"Expected success but got error: {error}"
            assert result is not None
            assert isinstance(result, list)

            # Demo should have at least BRAF, ROS1, TP53
            if len(result) > 0:
                print(f"✓ Demo server has {len(result)} curated genes")

                # Check structure of first gene
                first_gene = result[0]
                assert "hugoSymbol" in first_gene
                assert "entrezGeneId" in first_gene

                # Verify demo genes are present
                gene_symbols = {g.get("hugoSymbol") for g in result}
                demo_expected = {"BRAF", "ROS1", "TP53"}

                # At least some demo genes should be present
                found = gene_symbols & demo_expected
                if found:
                    print(f"✓ Found expected demo genes: {found}")

                # Print first few genes
                for gene in result[:5]:
                    symbol = gene.get("hugoSymbol")
                    oncogene = gene.get("oncogene")
                    tsg = gene.get("tsg")
                    print(f"  - {symbol}: oncogene={oncogene}, tsg={tsg}")
            else:
                pytest.skip("Demo server returned empty gene list")

        finally:
            # Restore token if it was set
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token


@pytest.mark.integration
class TestOncoKBProductionServer:
    """Integration tests for OncoKB production server (requires auth)."""

    @pytest.mark.asyncio
    async def test_production_requires_token(self):
        """Test that demo/production server selection works correctly."""
        # Get original token state
        original_token = os.environ.get("ONCOKB_TOKEN")

        try:
            # Test 1: Without token, should use demo
            if original_token:
                del os.environ["ONCOKB_TOKEN"]

            # Need to reload module to pick up env var change
            import importlib

            from biomcp.variants import oncokb_client

            importlib.reload(oncokb_client)

            client_no_token = oncokb_client.OncoKBClient()
            assert client_no_token.is_demo is True
            assert "demo.oncokb.org" in client_no_token.base_url
            print("✓ Without token, client correctly uses demo server")

            # Test 2: With token (invalid), should try production
            os.environ["ONCOKB_TOKEN"] = "invalid_token_for_testing"  # noqa: S105
            importlib.reload(oncokb_client)

            client_with_token = oncokb_client.OncoKBClient()
            assert client_with_token.is_demo is False
            assert "www.oncokb.org" in client_with_token.base_url
            print("✓ With token set, client correctly uses production server")

            # Try to fetch with invalid token - should get auth error
            result, error = await client_with_token.get_curated_genes()

            if error:
                # Expected: auth error with invalid token
                assert error.code in [
                    400,
                    401,
                    403,
                ], f"Expected auth error, got: {error.code}"
                print(
                    f"✓ Production correctly rejects invalid token (HTTP {error.code})"
                )
            else:
                # Unexpected but not a failure - maybe public endpoint
                print(
                    "Note: Production endpoint accessible with invalid token"
                )

        finally:
            # Restore original state
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token
            elif "ONCOKB_TOKEN" in os.environ:
                del os.environ["ONCOKB_TOKEN"]

            # Reload one more time to restore original state
            import importlib

            from biomcp.variants import oncokb_client

            importlib.reload(oncokb_client)

    @pytest.mark.asyncio
    async def test_production_with_token(self):
        """Test production server with valid token (if available)."""
        # Only run if token is set
        if not os.environ.get("ONCOKB_TOKEN"):
            pytest.skip("ONCOKB_TOKEN not set - skipping production test")

        client = OncoKBClient()

        # Should be using production server
        assert client.is_demo is False
        assert "www.oncokb.org" in client.base_url
        print("✓ Using production server with token")

        # Try to fetch curated genes (works on production with token)
        result, error = await client.get_curated_genes()

        # Skip if server unavailable
        if error and error.code in [500, 503, 504]:
            pytest.skip(
                f"OncoKB production server unavailable: {error.message}"
            )

        # Should succeed with valid token
        if error:
            if error.code in [401, 403]:
                pytest.skip(f"Token authentication failed: {error.message}")
            else:
                pytest.fail(f"Unexpected error: {error}")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

        # Find a common cancer gene like EGFR
        egfr = next((g for g in result if g.get("hugoSymbol") == "EGFR"), None)

        print("✓ Production server access successful with token")
        print(f"  Total genes: {len(result)}")
        if egfr:
            print(f"  Sample gene: {egfr.get('hugoSymbol')}")
            print(f"  Entrez ID: {egfr.get('entrezGeneId')}")

    @pytest.mark.asyncio
    async def test_production_curated_genes(self):
        """Test production server has full gene database."""
        # Only run if token is set
        if not os.environ.get("ONCOKB_TOKEN"):
            pytest.skip("ONCOKB_TOKEN not set - skipping production test")

        client = OncoKBClient()
        assert client.is_demo is False

        # Fetch all curated genes
        result, error = await client.get_curated_genes()

        # Skip if server unavailable or auth fails
        if error:
            if error.code in [401, 403]:
                pytest.skip(f"Token authentication failed: {error.message}")
            elif error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB production unavailable: {error.message}")
            else:
                pytest.fail(f"Unexpected error: {error}")

        assert result is not None
        assert isinstance(result, list)

        # Production should have many genes (>700)
        assert (
            len(result) > 100
        ), f"Expected >100 genes in production, got {len(result)}"

        print(f"✓ Production server has {len(result)} curated genes")

        # Check for well-known cancer genes
        gene_symbols = {g.get("hugoSymbol") for g in result}
        expected_genes = {"BRAF", "TP53", "EGFR", "KRAS", "PIK3CA"}

        found = gene_symbols & expected_genes
        assert len(found) == len(
            expected_genes
        ), f"Expected all cancer genes, found: {found}"

        print(f"✓ Found expected cancer genes: {found}")


@pytest.mark.integration
class TestOncoKBErrorHandling:
    """Integration tests for error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_invalid_gene_symbol(self):
        """Test handling of genes not in curated list."""
        # Use demo server for this test
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()

            # Get curated genes list
            result, error = await client.get_curated_genes()

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB server unavailable: {error.message}")

            assert error is None, f"Expected success but got error: {error}"
            assert result is not None

            # Verify an invalid gene like "NOTAREALGENE" is not in the list
            gene_symbols = {g.get("hugoSymbol") for g in result}
            assert "NOTAREALGENE" not in gene_symbols
            print("✓ Invalid gene correctly not in curated genes list")

        finally:
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_empty_query_handling(self):
        """Test handling of empty/missing parameters."""
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()

            # Fetching curated genes requires no parameters
            # This should always work
            result, error = await client.get_curated_genes()

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB server unavailable: {error.message}")

            # Should succeed
            assert error is None, f"Expected success but got error: {error}"
            assert result is not None
            assert isinstance(result, list)
            print(
                f"✓ Curated genes query works without parameters ({len(result)} genes)"
            )

        finally:
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_invalid_variant_format(self):
        """Test handling of invalid variant formats."""
        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()

            # Try with invalid protein change format
            result, error = await client.get_variant_annotation(
                gene="BRAF", protein_change="invalid_format_123"
            )

            # Skip if server unavailable
            if error and error.code in [500, 503, 504]:
                pytest.skip(f"OncoKB server unavailable: {error.message}")

            # Should handle gracefully (may return error or empty result)
            if error:
                print(
                    f"✓ Invalid variant format returns error (HTTP {error.code})"
                )
            else:
                # Some servers may return result with warnings
                assert result is not None
                print("✓ Invalid variant format handled gracefully")

        finally:
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token

    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling of concurrent API requests."""
        import asyncio

        original_token = os.environ.get("ONCOKB_TOKEN")
        if original_token:
            del os.environ["ONCOKB_TOKEN"]

        try:
            client = OncoKBClient()

            # Make multiple concurrent requests
            genes = ["BRAF", "ROS1", "TP53"]
            tasks = [client.get_gene_annotation(gene) for gene in genes]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Check results
            for gene, result in zip(genes, results, strict=False):
                if isinstance(result, Exception):
                    pytest.skip(
                        f"Server error during concurrent test: {result}"
                    )

                data, error = result

                # Skip if server unavailable
                if error and error.code in [500, 503, 504]:
                    pytest.skip(f"OncoKB server unavailable: {error.message}")

                # Should handle concurrent requests
                if data:
                    assert data.get("hugoSymbol") == gene
                    print(f"✓ Concurrent request successful for {gene}")

        finally:
            if original_token:
                os.environ["ONCOKB_TOKEN"] = original_token


if __name__ == "__main__":
    """
    Run integration tests directly for debugging.

    Usage:
        python tests/integration/test_oncokb_integration.py
    """
    import asyncio

    async def run_tests():
        """Run all test classes."""
        print("=" * 70)
        print("OncoKB Integration Tests")
        print("=" * 70)

        # Demo server tests
        print("\n[1/4] Testing Demo Server Access...")
        await TestOncoKBDemoServer().test_demo_server_access()

        print("\n[2/4] Testing Demo Gene Limits...")
        await TestOncoKBDemoServer().test_demo_gene_limits()

        print("\n[3/4] Testing Variant Annotation...")
        await TestOncoKBDemoServer().test_variant_annotation()

        print("\n[4/4] Testing Production Auth Requirement...")
        await TestOncoKBProductionServer().test_production_requires_token()

        print("\n" + "=" * 70)
        print("✓ All integration tests completed")
        print("=" * 70)

    asyncio.run(run_tests())

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
