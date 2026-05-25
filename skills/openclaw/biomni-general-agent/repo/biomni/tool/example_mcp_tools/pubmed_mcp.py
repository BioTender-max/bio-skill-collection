# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os

from Bio import Entrez
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

Entrez.email = os.getenv("NCBI_EMAIL") or "YOUR_EMAIL"
mcp = FastMCP("pubmed-live")


class Article(BaseModel):
    pmid: str
    title: str | None = None
    journal: str | None = None
    year: str | None = None
    abstract: str | None = None


@mcp.tool()
def search_pubmed(query: str, max_results: int = 10) -> list[Article]:
    ids = Entrez.read(Entrez.esearch(db="pubmed", term=query, retmax=max_results))["IdList"]
    summaries = Entrez.read(Entrez.esummary(db="pubmed", id=",".join(ids))) if ids else []
    articles: list[Article] = []
    for s in summaries:
        articles.append(
            Article(pmid=s["Id"], title=s["Title"], journal=s.get("FullJournalName", ""), year=s.get("PubDate", "")[:4])
        )
    return articles


@mcp.tool()
def get_article_abstract(pmid: str) -> str:
    with Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text") as h:
        return h.read()


if __name__ == "__main__":
    mcp.run()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
