#!/usr/bin/env python3
"""
Example: Find 16S rRNA genes for a bacterial family in JGI Lakehouse

This example demonstrates how to:
1. Query IMG/M for 16S rRNA genes by taxonomic family
2. Handle the common pitfall of mismatched taxon IDs
3. Use name pattern matching when family field is inconsistent

IMPORTANT NOTES:
- The Lakehouse contains gene METADATA but NOT actual DNA sequences
- To get sequences, use gene_oid to query IMG/M web interface or download genomes
- The `family` field in taxon table is not consistently populated
- Use name pattern matching as a reliable alternative

Usage:
    export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)
    python find_16s_rrna_genes.py [family_name_pattern]

Example:
    python find_16s_rrna_genes.py Rhodobacter
    python find_16s_rrna_genes.py Bacill
    python find_16s_rrna_genes.py Pseudomonas
"""

import os
import sys

# Add parent scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from rest_client import query, query_all


def find_16s_by_family_pattern(name_patterns: list[str], limit: int = 100) -> list[dict]:
    """
    Find 16S rRNA genes by taxon name patterns.

    Args:
        name_patterns: List of name patterns to match (e.g., ['Rhodobacter', 'Paracoccus'])
        limit: Maximum genes to return

    Returns:
        List of gene records with taxon info
    """
    # Build WHERE clause for name patterns
    pattern_clauses = " OR ".join([
        f"t.taxon_display_name LIKE '%{p}%'" for p in name_patterns
    ])

    sql = f'''
    SELECT
        g.gene_oid,
        g.taxon,
        t.taxon_display_name,
        t.genus,
        t.family,
        g.product_name,
        g.dna_seq_length,
        g.locus_tag,
        g.start_coord,
        g.end_coord,
        g.strand
    FROM "img-db-2 postgresql".img_core_v400.gene g
    JOIN "img-db-2 postgresql".img_core_v400.taxon t ON g.taxon = t.taxon_oid
    WHERE g.locus_type = 'rRNA'
      AND g.product_name LIKE '%16S%'
      AND ({pattern_clauses})
    ORDER BY t.genus, t.taxon_display_name
    LIMIT {limit}
    '''

    return query(sql, timeout=300, limit=limit)


def find_16s_by_family_field(family_name: str, limit: int = 100) -> list[dict]:
    """
    Find 16S rRNA genes using the family field (less reliable).

    NOTE: The family field is not consistently populated in IMG/M.
    Use find_16s_by_family_pattern() for more reliable results.

    Args:
        family_name: Exact family name (e.g., 'Rhodobacteraceae')
        limit: Maximum genes to return

    Returns:
        List of gene records
    """
    sql = f'''
    SELECT
        g.gene_oid,
        g.taxon,
        t.taxon_display_name,
        t.genus,
        t.family,
        g.product_name,
        g.dna_seq_length,
        g.locus_tag
    FROM "img-db-2 postgresql".img_core_v400.gene g
    JOIN "img-db-2 postgresql".img_core_v400.taxon t ON g.taxon = t.taxon_oid
    WHERE g.locus_type = 'rRNA'
      AND g.product_name LIKE '%16S%'
      AND t.family = '{family_name}'
    LIMIT {limit}
    '''

    return query(sql, timeout=300, limit=limit)


def get_taxon_count_by_family(family_name: str) -> int:
    """Count taxons with the given family name."""
    sql = f'''
    SELECT COUNT(*) as cnt
    FROM "img-db-2 postgresql".img_core_v400.taxon
    WHERE family = '{family_name}'
    '''
    rows = query(sql)
    return rows[0]['cnt'] if rows else 0


def summarize_results(genes: list[dict]) -> dict:
    """Summarize gene results by genus."""
    by_genus = {}
    for g in genes:
        genus = g.get('genus', 'Unknown')
        if genus not in by_genus:
            by_genus[genus] = []
        by_genus[genus].append(g)

    return {
        'total_genes': len(genes),
        'unique_genera': len(by_genus),
        'by_genus': by_genus,
        'length_range': (
            min(g['dna_seq_length'] for g in genes) if genes else 0,
            max(g['dna_seq_length'] for g in genes) if genes else 0
        )
    }


def main():
    # Default patterns for Rhodobacteraceae family
    default_patterns = [
        'Rhodobacter',
        'Paracoccus',
        'Ruegeria',
        'Roseobacter',
        'Dinoroseobacter',
        'Phaeobacter',
        'Rhodobacteraceae',
        'Rhodobacterales'
    ]

    # Use command line arg or defaults
    if len(sys.argv) > 1:
        patterns = [sys.argv[1]]
        print(f"Searching for 16S rRNA genes matching: {sys.argv[1]}")
    else:
        patterns = default_patterns
        print("Searching for 16S rRNA genes from Rhodobacteraceae family")
        print(f"Using patterns: {', '.join(patterns[:4])}...")

    print()

    # Method 1: Using name patterns (RECOMMENDED)
    print("=" * 60)
    print("Method 1: Name pattern matching (RECOMMENDED)")
    print("=" * 60)

    genes = find_16s_by_family_pattern(patterns, limit=200)

    if not genes:
        print("No genes found!")
        return

    summary = summarize_results(genes)

    print(f"\nFound {summary['total_genes']} 16S rRNA genes")
    print(f"From {summary['unique_genera']} genera")
    print(f"Length range: {summary['length_range'][0]}-{summary['length_range'][1]} bp")

    print("\nBy genus:")
    for genus, genus_genes in sorted(summary['by_genus'].items()):
        print(f"\n  {genus}: {len(genus_genes)} genes")
        for g in genus_genes[:2]:
            print(f"    - {g['taxon_display_name'][:45]}")
            print(f"      gene_oid: {g['gene_oid']} | {g['dna_seq_length']}bp")
        if len(genus_genes) > 2:
            print(f"    ... ({len(genus_genes) - 2} more)")

    # Show how to get sequences
    print("\n" + "=" * 60)
    print("HOW TO GET ACTUAL SEQUENCES")
    print("=" * 60)
    print("""
The Lakehouse contains metadata only. To get sequences:

1. IMG/M Web Interface:
   https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=GeneDetail&gene_oid={gene_oid}

2. Download genome and extract by coordinates:
   - Get scaffold_oid from gene record
   - Download genome FASTA from IMG
   - Extract region: start_coord to end_coord on strand
""")

    # Example gene for reference
    if genes:
        g = genes[0]
        print(f"Example gene_oid for lookup: {g['gene_oid']}")
        print(f"  Organism: {g['taxon_display_name']}")
        print(f"  Length: {g['dna_seq_length']} bp")
        if g.get('locus_tag'):
            print(f"  Locus tag: {g['locus_tag']}")


if __name__ == "__main__":
    if not os.environ.get("DREMIO_PAT"):
        print("ERROR: DREMIO_PAT environment variable not set")
        print("Run: export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)")
        sys.exit(1)

    main()
