# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import asyncio

from pytest_bdd import given, parsers, scenarios, then, when

from biomcp.articles.autocomplete import (
    Concept,
    Entity,
    EntityRequest,
    autocomplete,
)

scenarios("autocomplete.feature")


@given(
    parsers.parse(
        'I have a valid concept "{concept}" and a valid query "{query}"',
    ),
    target_fixture="entity_request",
)
def entity_request(concept: Concept, query: str):
    return EntityRequest(concept=concept, query=query)


@given(
    parsers.parse(
        'I have a valid concept "{concept}" and an invalid query "{query}"',
    ),
    target_fixture="entity_request",
)
def invalid_query_request(concept: Concept, query: str):
    return EntityRequest(concept=concept, query=query)


@when(
    "I call the Pubtator Autocomplete API",
    target_fixture="entity",
)
def entity(entity_request) -> Entity | None:
    return asyncio.run(autocomplete(request=entity_request))


@then(parsers.parse('the response entity_id should be "{expected_id}"'))
def check_entity_id(entity, expected_id):
    assert entity.entity_id == expected_id


@then(parsers.parse('the response concept should be "{concept}"'))
def check_concept(entity, concept):
    assert entity.concept == concept


@then("the response should be empty")
def check_empty_response(entity):
    assert entity is None

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
