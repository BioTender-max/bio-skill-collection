# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from pathlib import Path

from pytest import fixture

from biomcp import http_client


@fixture
def anyio_backend():
    return "asyncio"


class DummyCache:
    def __init__(self):
        self.store = {}

    def set(self, key, value, expire=None):
        self.store[key] = value

    def get(self, key, default=None):
        return self.store.get(key, default)

    @property
    def count(self):
        return len(self.store)

    def close(self):
        self.store.clear()


@fixture
def http_cache():
    cache = DummyCache()
    http_client._cache = cache
    yield cache
    cache.close()


@fixture
def data_dir():
    return Path(__file__).parent.parent / "data"

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
