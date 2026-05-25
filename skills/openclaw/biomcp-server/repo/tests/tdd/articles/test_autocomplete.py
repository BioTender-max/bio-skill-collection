# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from biomcp.articles.autocomplete import Entity, EntityRequest, autocomplete


async def test_autocomplete(anyio_backend, http_cache):
    # new cache for each call
    assert http_cache.count == 0

    # gene (compare using entity_id directly)
    request = EntityRequest(concept="gene", query="her2")
    entity = await autocomplete(request=request)
    assert entity.entity_id == "@GENE_ERBB2"

    # variant
    request = EntityRequest(concept="variant", query="BRAF V600E")
    assert await autocomplete(request=request) == Entity(
        _id="@VARIANT_p.V600E_BRAF_human",
        biotype="variant",
        name="p.V600E",
    )

    # disease
    request = EntityRequest(concept="disease", query="lung adenocarcinoma")
    assert await autocomplete(request=request) == Entity(
        _id="@DISEASE_Adenocarcinoma_of_Lung",
        biotype="disease",
        name="Adenocarcinoma of Lung",
        match="Multiple matches",
    )

    assert http_cache.count == 3

    # duplicate request uses the cached response
    request = EntityRequest(concept="gene", query="her2")
    entity = await autocomplete(request=request)
    assert entity.entity_id == "@GENE_ERBB2"
    assert http_cache.count == 3

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
