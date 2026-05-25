# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""Integration tests for external variant data sources."""

import asyncio

import pytest

from biomcp.variants.external import (
    ExternalVariantAggregator,
    TCGAClient,
    ThousandGenomesClient,
)
from biomcp.variants.getter import get_variant


class TestTCGAIntegration:
    """Integration tests for TCGA/GDC API."""

    @pytest.mark.asyncio
    async def test_tcga_real_variant(self):
        """Test real TCGA API with known variant."""
        client = TCGAClient()

        # Try with BRAF V600E - a well-known cancer mutation
        # TCGA can search by gene AA change format
        result = await client.get_variant_data("BRAF V600E")

        print(f"TCGA result: {result}")

        if result:
            print(f"COSMIC ID: {result.cosmic_id}")
            print(f"Tumor types: {result.tumor_types}")
            print(f"Affected cases: {result.affected_cases}")
            print(f"Consequence: {result.consequence_type}")
        else:
            print("No TCGA data found for this variant")


class TestThousandGenomesIntegration:
    """Integration tests for 1000 Genomes via Ensembl."""

    @pytest.mark.asyncio
    async def test_1000g_real_variant(self):
        """Test real 1000 Genomes API with known variant."""
        client = ThousandGenomesClient()

        # Try with a known rsID
        result = await client.get_variant_data("rs7412")  # APOE variant

        print(f"1000 Genomes result: {result}")

        if result:
            print(f"Global MAF: {result.global_maf}")
            print(f"EUR MAF: {result.eur_maf}")
            print(f"AFR MAF: {result.afr_maf}")
            print(f"Consequence: {result.most_severe_consequence}")
            print(f"Ancestral allele: {result.ancestral_allele}")

            # This variant should have frequency data
            assert result.global_maf is not None
        else:
            print("No 1000 Genomes data found")


class TestExternalAggregatorIntegration:
    """Integration tests for the aggregator."""

    @pytest.mark.asyncio
    async def test_aggregator_basic(self):
        """Test aggregator with basic functionality."""
        aggregator = ExternalVariantAggregator()

        # Test with a known variant
        result = await aggregator.get_enhanced_annotations(
            "rs7412",  # APOE variant
            include_tcga=True,
            include_1000g=True,
        )

        print(f"Variant ID: {result.variant_id}")
        print(f"TCGA data: {'Present' if result.tcga else 'Not found'}")
        print(
            f"1000G data: {'Present' if result.thousand_genomes else 'Not found'}"
        )
        print(f"Errors: {result.error_sources}")

        # Should still work
        assert result.variant_id == "rs7412"

    @pytest.mark.asyncio
    async def test_aggregator_partial_failures(self):
        """Test aggregator handles partial failures gracefully."""
        aggregator = ExternalVariantAggregator()

        # Use a variant that might not be in all databases
        result = await aggregator.get_enhanced_annotations(
            "chr1:g.12345678A>G",  # Arbitrary variant
            include_tcga=True,
            include_1000g=True,
        )

        print("Results for arbitrary variant:")
        print(f"- TCGA: {'Found' if result.tcga else 'Not found'}")
        print(
            f"- 1000G: {'Found' if result.thousand_genomes else 'Not found'}"
        )
        print(f"- Errors: {result.error_sources}")

        # Should complete without crashing
        assert result.variant_id == "chr1:g.12345678A>G"


class TestAssemblyParameter:
    """Integration tests for assembly parameter."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_variant_hg19_assembly(self):
        """Test get_variant with hg19 assembly on real API."""
        # Use a well-known variant: BRAF V600E
        variant_id = "rs113488022"

        result = await get_variant(
            variant_id,
            output_json=True,
            include_external=False,
            assembly="hg19",
        )

        # Should return valid JSON
        assert result is not None
        assert len(result) > 0

        # Parse and check for hg19 data
        import json

        data = json.loads(result)
        if data and len(data) > 0:
            variant_data = data[0]
            # BRAF V600E should have hg19 coordinates
            if "hg19" in variant_data:
                print(f"hg19 coordinates: {variant_data['hg19']}")
                assert "start" in variant_data["hg19"]
                assert "end" in variant_data["hg19"]
            else:
                pytest.skip("hg19 data not available in API response")
        else:
            pytest.skip("No data returned from API")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_variant_hg38_assembly(self):
        """Test get_variant with hg38 assembly on real API."""
        # Use the same variant but request hg38
        variant_id = "rs113488022"

        result = await get_variant(
            variant_id,
            output_json=True,
            include_external=False,
            assembly="hg38",
        )

        # Should return valid JSON
        assert result is not None
        assert len(result) > 0

        # Parse and check for hg38 data
        import json

        data = json.loads(result)
        if data and len(data) > 0:
            variant_data = data[0]
            # Should have hg38 coordinates
            if "hg38" in variant_data:
                print(f"hg38 coordinates: {variant_data['hg38']}")
                assert "start" in variant_data["hg38"]
                assert "end" in variant_data["hg38"]
            else:
                pytest.skip("hg38 data not available in API response")
        else:
            pytest.skip("No data returned from API")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_assembly_coordinate_differences(self):
        """Test that hg19 and hg38 return different coordinates for same variant."""
        variant_id = "rs113488022"  # BRAF V600E

        # Get both assemblies
        result_hg19 = await get_variant(
            variant_id,
            output_json=True,
            include_external=False,
            assembly="hg19",
        )

        result_hg38 = await get_variant(
            variant_id,
            output_json=True,
            include_external=False,
            assembly="hg38",
        )

        import json

        data_hg19 = json.loads(result_hg19)
        data_hg38 = json.loads(result_hg38)

        # Both should return data
        if not data_hg19 or not data_hg38:
            pytest.skip("API did not return data for both assemblies")

        # Compare coordinates if available
        if len(data_hg19) > 0 and len(data_hg38) > 0:
            v19 = data_hg19[0]
            v38 = data_hg38[0]

            # BRAF V600E has different coordinates in hg19 vs hg38
            # hg19: chr7:140453136
            # hg38: chr7:140753336
            if "hg19" in v19 and "hg38" in v38:
                print(f"hg19 start: {v19['hg19']['start']}")
                print(f"hg38 start: {v38['hg38']['start']}")

                # Coordinates should be different (BRAF moved between assemblies)
                assert v19["hg19"]["start"] != v38["hg38"]["start"]
            else:
                pytest.skip("Assembly-specific coordinates not in response")


if __name__ == "__main__":
    print("Testing TCGA/GDC...")
    asyncio.run(TestTCGAIntegration().test_tcga_real_variant())

    print("\n" + "=" * 50 + "\n")
    print("Testing 1000 Genomes...")
    asyncio.run(TestThousandGenomesIntegration().test_1000g_real_variant())

    print("\n" + "=" * 50 + "\n")
    print("Testing aggregator...")
    asyncio.run(TestExternalAggregatorIntegration().test_aggregator_basic())

    print("\n" + "=" * 50 + "\n")
    print("Testing aggregator with partial failures...")
    asyncio.run(
        TestExternalAggregatorIntegration().test_aggregator_partial_failures()
    )

    print("\n" + "=" * 50 + "\n")
    print("Testing assembly parameter...")
    asyncio.run(TestAssemblyParameter().test_get_variant_hg19_assembly())
    asyncio.run(TestAssemblyParameter().test_get_variant_hg38_assembly())
    asyncio.run(TestAssemblyParameter().test_assembly_coordinate_differences())

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
