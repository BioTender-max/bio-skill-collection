# PubMed & PubTator3

Search 35M+ biomedical articles and preprints. Find literature by gene, disease, chemical, keyword, or variant.

## Key Tools

### `pubmed_search_articles` — Search literature

```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "query": "myasthenia gravis treatment",
    "genes": ["CHRNE", "RAPSN"],
    "diseases": ["myasthenia gravis"],
    "chemicals": ["immunoglobulin"],
    "keywords": ["autoimmune"],
    "max_results": 20
  }
}
```

**Arguments:**
- `query` (str): Free-text search term
- `genes` (list, optional): Filter by NCBI gene symbols (AND logic)
- `diseases` (list, optional): Filter by disease names
- `chemicals` (list, optional): Filter by chemical/drug names
- `keywords` (list, optional): Filter by subject headings
- `max_results` (int, default 20): Results to return

**Returns:** Array of articles with PMID, title, abstract, authors, publication year, DOI

### `pubmed_get_article` — Get full article details

```json
{
  "name": "pubmed_get_article",
  "arguments": {
    "pmid": "35641234",
    "include_full_text": true
  }
}
```

**Arguments:**
- `pmid` (str): PubMed ID
- `include_full_text` (bool, optional): Fetch full article text if available

**Returns:** Article metadata including abstract, full text, MeSH terms, authors, affiliations

### `pubmed_search_preprints` — Search bioRxiv/medRxiv

```json
{
  "name": "pubmed_search_preprints",
  "arguments": {
    "query": "SARS-CoV-2 immune response",
    "max_results": 10
  }
}
```

**Returns:** Preprints from bioRxiv and medRxiv (peer-review pending)

## Use Cases

### Literature Review by Gene

Find all papers mentioning TP53 in cancer:
```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "genes": ["TP53"],
    "diseases": ["cancer"],
    "max_results": 50
  }
}
```

### Mechanistic Deep Dive

Find papers on immune tolerance mechanisms in autoimmune disease:
```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "query": "immune tolerance regulatory T cells",
    "diseases": ["autoimmune"],
    "max_results": 30
  }
}
```

### Safety Signals

Find adverse event reports for a drug:
```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "chemicals": ["your-drug-name"],
    "keywords": ["adverse effect", "toxicity"],
    "max_results": 20
  }
}
```

### Recent Developments

Get latest papers on a topic (combine with OpenTargets for targets):
```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "query": "complement inhibitor immunotherapy 2025",
    "max_results": 20
  }
}
```

## Workflow: Full Literature Review

1. **Find target papers** (search by gene + disease)
2. **Get full text** (use pmid to fetch complete article)
3. **Extract key data** (mechanisms, results, conclusions)
4. **Cross-reference citations** (follow citation trails)
5. **Identify gaps** (what's NOT being studied?)

## Notes

- **Coverage**: 1966–present (MEDLINE indexed articles)
- **Preprints**: bioRxiv (life sciences), medRxiv (medicine) — not yet peer-reviewed
- **MeSH tagging**: Automated by NLM (consistent vocabularies)
- **Full text availability**: ~30% of articles; depends on publisher + open access
- **Citation linking**: Search results include citation counts and related articles

## Rate Limits

- No API key required
- Generous public limits (1,000+ req/day)
- Results cached (30-day TTL)

## Examples

### Example 1: Find papers on Myasthenia Gravis immunotherapy

```json
{
  "method": "tools/call",
  "params": {
    "name": "pubmed_search_articles",
    "arguments": {
      "query": "",
      "diseases": ["myasthenia gravis"],
      "keywords": ["immunotherapy", "treatment"],
      "max_results": 15
    }
  }
}
```

### Example 2: Get full article details for mechanistic understanding

```json
{
  "method": "tools/call",
  "params": {
    "name": "pubmed_get_article",
    "arguments": {
      "pmid": "35641234",
      "include_full_text": true
    }
  }
}
```

### Example 3: Find recent preprints on novel therapeutic targets

```json
{
  "method": "tools/call",
  "params": {
    "name": "pubmed_search_preprints",
    "arguments": {
      "query": "novel drug target autoimmune disease 2025",
      "max_results": 20
    }
  }
}
```
