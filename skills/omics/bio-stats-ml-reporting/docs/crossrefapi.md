# Crossref API Usage Guide

**Official Documentation:** https://github.com/fabiobatalha/crossrefapi

**Version:** 1.7.0

**Crossref REST API:** https://www.crossref.org/documentation/

## Installation

```bash
# Via pip
pip install crossrefapi

# Specific version
pip install crossrefapi==1.7.0
```

## Key Features

The crossrefapi library provides Python bindings for Crossref's REST API to:
- Validate DOIs and fetch bibliographic metadata
- Query works (articles, books, datasets) by various criteria
- Access journal information by ISSN
- Retrieve funders, members, and other metadata
- Perform batch queries efficiently

## Common Usage Examples

### 1. Query Works (Publications)

```python
from crossref.restful import Works

works = Works()

# Get a specific work by DOI
doi = '10.1038/nature12373'
work = works.doi(doi)

if work:
    print(f"Title: {work['title'][0]}")
    print(f"Authors: {[a['given'] + ' ' + a['family'] for a in work['author']]}")
    print(f"Published: {work['published-print']['date-parts'][0]}")
    print(f"Journal: {work['container-title'][0]}")
else:
    print(f"DOI {doi} not found")
```

### 2. Search for Works

```python
# Free-text search
results = works.query('machine learning genomics').filter(from_pub_date='2023')

for item in results:
    print(f"DOI: {item['DOI']}")
    print(f"Title: {item['title'][0]}")
    print(f"Year: {item['published-print']['date-parts'][0][0]}")
    print("---")
```

### 3. Filter Works by Multiple Criteria

```python
# Filter by publication date, journal, and content type
results = works.filter(
    from_pub_date='2023-01',
    until_pub_date='2024-12',
    type='journal-article',
    has_abstract=True
).query('bioinformatics')

# Limit results
for i, item in enumerate(results):
    if i >= 10:
        break
    print(f"{item['DOI']}: {item['title'][0]}")
```

### 4. Query Journals by ISSN

```python
from crossref.restful import Journals

journals = Journals()

# Get journal metadata
issn = '1460-2075'  # EMBO Journal
journal = journals.journal(issn)

if journal:
    print(f"Title: {journal['title']}")
    print(f"Publisher: {journal['publisher']}")
    print(f"ISSN: {journal['ISSN']}")
    print(f"Total articles: {journal['total-articles']}")
```

### 5. Get Works from a Specific Journal

```python
# All works from a journal
journal_works = journals.works(issn)

for work in journal_works:
    print(f"{work['DOI']}: {work['title'][0]}")
```

### 6. Validate References

```python
def validate_reference(doi):
    """
    Validate a DOI and return metadata if valid.
    """
    works = Works()
    try:
        work = works.doi(doi)
        if work:
            return {
                'valid': True,
                'doi': doi,
                'title': work.get('title', [''])[0],
                'authors': ', '.join([
                    f"{a.get('given', '')} {a.get('family', '')}"
                    for a in work.get('author', [])
                ]),
                'year': work.get('published-print', {}).get('date-parts', [[None]])[0][0],
                'journal': work.get('container-title', [''])[0]
            }
        else:
            return {'valid': False, 'doi': doi, 'error': 'DOI not found'}
    except Exception as e:
        return {'valid': False, 'doi': doi, 'error': str(e)}


# Validate list of DOIs
dois = [
    '10.1038/nature12373',
    '10.1126/science.1234567',  # May be invalid
    '10.1093/bioinformatics/bty633'
]

validated = [validate_reference(doi) for doi in dois]

for ref in validated:
    if ref['valid']:
        print(f"✓ {ref['doi']}: {ref['title']}")
    else:
        print(f"✗ {ref['doi']}: {ref['error']}")
```

### 7. Batch Reference Validation

```python
import pandas as pd
from time import sleep

def validate_references_batch(dois, delay=1.0):
    """
    Validate multiple DOIs with rate limiting.

    Args:
        dois: List of DOI strings
        delay: Delay between requests in seconds (default: 1.0)

    Returns:
        DataFrame with validation results
    """
    works = Works()
    results = []

    for i, doi in enumerate(dois):
        print(f"Validating {i+1}/{len(dois)}: {doi}")

        try:
            work = works.doi(doi)
            if work:
                results.append({
                    'doi': doi,
                    'valid': True,
                    'title': work.get('title', [''])[0],
                    'year': work.get('published-print', {}).get('date-parts', [[None]])[0][0],
                    'journal': work.get('container-title', [''])[0],
                    'type': work.get('type', ''),
                    'error': None
                })
            else:
                results.append({
                    'doi': doi,
                    'valid': False,
                    'title': None,
                    'year': None,
                    'journal': None,
                    'type': None,
                    'error': 'DOI not found'
                })
        except Exception as e:
            results.append({
                'doi': doi,
                'valid': False,
                'title': None,
                'year': None,
                'journal': None,
                'type': None,
                'error': str(e)
            })

        # Rate limiting
        if i < len(dois) - 1:
            sleep(delay)

    return pd.DataFrame(results)


# Example usage
reference_dois = pd.read_csv('results/bio-stats-ml-reporting/references.tsv', sep='\t')
validated_refs = validate_references_batch(reference_dois['doi'].tolist())

# Save results
validated_refs.to_csv(
    'results/bio-stats-ml-reporting/validated_references.tsv',
    sep='\t',
    index=False
)

# Summary
print(f"Total: {len(validated_refs)}")
print(f"Valid: {validated_refs['valid'].sum()}")
print(f"Invalid: {(~validated_refs['valid']).sum()}")
```

### 8. Select Specific Fields

```python
# Request only specific fields to reduce response size
results = works.query('bioinformatics').select([
    'DOI',
    'title',
    'author',
    'published-print',
    'container-title'
])

for item in results:
    print(item)
```

### 9. Faceted Queries

```python
# Get aggregated statistics
results = works.query('bioinformatics').facet('type', 10)

for facet in results:
    print(f"{facet['value']}: {facet['count']} works")
```

### 10. Sample Random Works

```python
# Get random sample of works (useful for testing)
sample = works.sample(10)

for work in sample:
    print(f"{work['DOI']}: {work['title'][0]}")
```

## Filter Parameters

Common filters (use underscores instead of hyphens):

- `from_pub_date` / `until_pub_date`: Date range (YYYY-MM-DD)
- `type`: Content type (journal-article, book-chapter, etc.)
- `has_abstract`: True/False
- `has_orcid`: True/False
- `has_references`: True/False
- `has_license`: True/False
- `license_url`: Specific license URL
- `issn`: Journal ISSN
- `publisher`: Publisher name

Example:
```python
results = works.filter(
    from_pub_date='2023-01-01',
    until_pub_date='2024-12-31',
    type='journal-article',
    has_abstract=True,
    has_orcid=True
).query('machine learning')
```

## Rate Limiting and Best Practices

### Rate Limits

Crossref's "polite" pool provides:
- Higher rate limits
- Faster response times

To use the polite pool, add your email to requests:

```python
# Not directly supported in crossrefapi, but you can set user agent
# The library handles basic rate limiting internally
```

### Best Practices

1. **Add delays between requests**
   ```python
   from time import sleep
   sleep(1)  # 1 second delay between requests
   ```

2. **Handle errors gracefully**
   ```python
   try:
       work = works.doi(doi)
   except Exception as e:
       print(f"Error: {e}")
   ```

3. **Cache results when possible**
   ```python
   import functools

   @functools.lru_cache(maxsize=1000)
   def get_work_cached(doi):
       works = Works()
       return works.doi(doi)
   ```

4. **Batch process with progress tracking**
   ```python
   from tqdm import tqdm

   results = []
   for doi in tqdm(dois):
       result = validate_reference(doi)
       results.append(result)
       sleep(1)
   ```

## Typical Workflow for Report Generation

```python
#!/usr/bin/env python3
import pandas as pd
from crossref.restful import Works
from time import sleep
import logging

# Setup logging
logging.basicConfig(
    filename='results/bio-stats-ml-reporting/logs/reference_validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_and_format_references(references_file, output_file):
    """
    Validate references and format for report.

    Args:
        references_file: TSV file with 'doi' column
        output_file: Output TSV file
    """
    # Load references
    refs = pd.read_csv(references_file, sep='\t')
    logging.info(f"Loaded {len(refs)} references")

    works = Works()
    validated = []

    for i, row in refs.iterrows():
        doi = row['doi']
        logging.info(f"Validating {i+1}/{len(refs)}: {doi}")

        try:
            work = works.doi(doi)

            if work:
                # Extract metadata
                authors = ', '.join([
                    f"{a.get('family', '')}, {a.get('given', '')}"
                    for a in work.get('author', [])[:3]  # First 3 authors
                ])

                if len(work.get('author', [])) > 3:
                    authors += ' et al.'

                year = work.get('published-print', {}).get('date-parts', [[None]])[0][0]
                title = work.get('title', [''])[0]
                journal = work.get('container-title', [''])[0]

                validated.append({
                    'doi': doi,
                    'valid': True,
                    'citation': f"{authors} ({year}). {title}. {journal}. doi:{doi}",
                    'authors': authors,
                    'year': year,
                    'title': title,
                    'journal': journal
                })

                logging.info(f"✓ Valid: {doi}")
            else:
                validated.append({
                    'doi': doi,
                    'valid': False,
                    'citation': f"[INVALID] {doi}",
                    'authors': None,
                    'year': None,
                    'title': None,
                    'journal': None
                })
                logging.warning(f"✗ Invalid: {doi}")

        except Exception as e:
            validated.append({
                'doi': doi,
                'valid': False,
                'citation': f"[ERROR] {doi}",
                'authors': None,
                'year': None,
                'title': None,
                'journal': None
            })
            logging.error(f"✗ Error validating {doi}: {str(e)}")

        # Rate limiting: 1 request per second
        sleep(1)

    # Save results
    df = pd.DataFrame(validated)
    df.to_csv(output_file, sep='\t', index=False)

    # Summary
    valid_count = df['valid'].sum()
    logging.info(f"Validation complete: {valid_count}/{len(df)} valid")

    return df


# Run validation
validated = validate_and_format_references(
    'results/bio-stats-ml-reporting/references.tsv',
    'results/bio-stats-ml-reporting/validated_references.tsv'
)

# Check for invalid references
invalid = validated[~validated['valid']]
if len(invalid) > 0:
    print(f"WARNING: {len(invalid)} invalid references found:")
    for doi in invalid['doi']:
        print(f"  - {doi}")
```

## Output Format for Reports

Generate formatted citations for markdown reports:

```python
def generate_bibliography_section(validated_refs_file):
    """
    Generate markdown bibliography section from validated references.
    """
    refs = pd.read_csv(validated_refs_file, sep='\t')

    # Filter valid references and sort by year, author
    valid_refs = refs[refs['valid']].sort_values(['year', 'authors'], ascending=[False, True])

    markdown = "## References\n\n"

    for i, ref in enumerate(valid_refs.itertuples(), 1):
        markdown += f"{i}. {ref.citation}\n"

    return markdown


# Add to report
bibliography = generate_bibliography_section(
    'results/bio-stats-ml-reporting/validated_references.tsv'
)

with open('results/bio-stats-ml-reporting/report.md', 'a') as f:
    f.write('\n\n')
    f.write(bibliography)
```

## References

- Python Library: https://github.com/fabiobatalha/crossrefapi
- Crossref REST API: https://www.crossref.org/documentation/
- API Documentation: https://api.crossref.org/swagger-ui/index.html
- Best Practices: https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/
