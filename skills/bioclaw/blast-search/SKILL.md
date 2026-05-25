---
name: blast-search
description: Run BLAST sequence similarity searches. Use when the user asks to BLAST a sequence, find similar sequences, identify a gene/protein, or do homology search. Triggers on "blast", "sequence similarity", "homology", "identify sequence".
---

# BLAST Search

Run NCBI BLAST+ searches inside the BioClaw container.

## When to Use

- User provides a DNA/RNA/protein sequence and wants to find similar sequences
- User asks to identify an unknown sequence
- User wants to check sequence conservation across species

## How to Execute

### 1. Determine BLAST program

| Input | Database | Program |
|-------|----------|---------|
| Nucleotide query | Nucleotide DB | `blastn` |
| Protein query | Protein DB | `blastp` |
| Nucleotide query | Protein DB | `blastx` |
| Protein query | Nucleotide DB | `tblastn` |

### 2. For local BLAST (sequences provided by user)

```bash
# Create query file
cat > /tmp/query.fa << 'EOF'
>query_sequence
ATGCGATCGATCGATCG...
EOF

# Create subject file (if user provides reference)
cat > /tmp/subject.fa << 'EOF'
>reference
ATGCGATCGATCGATCG...
EOF

# Run BLAST
blastn -query /tmp/query.fa -subject /tmp/subject.fa -outfmt 6 -evalue 1e-5
```

### 3. For remote BLAST (against NCBI databases)

Use BioPython's NCBIWWW module:

```python
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

# Read sequence
sequence = "ATGCGATCGATCGATCG..."

# Run remote BLAST
result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
blast_records = NCBIXML.parse(result_handle)

for record in blast_records:
    for alignment in record.alignments[:10]:
        print(f"Title: {alignment.title}")
        for hsp in alignment.hsps:
            print(f"  Score: {hsp.score}, E-value: {hsp.expect}")
            print(f"  Identity: {hsp.identities}/{hsp.align_length} ({hsp.identities/hsp.align_length*100:.1f}%)")
```

### 4. Output format

Present results in a clear table:

```
*BLAST Results (top 10 hits)*

• Hit 1: Homo sapiens TP53 gene (98.5% identity, E=1e-45)
• Hit 2: Mus musculus Trp53 gene (89.2% identity, E=1e-38)
...
```

### 5. Follow-up suggestions

After showing results, suggest:
- Multiple sequence alignment of top hits
- Phylogenetic analysis
- Domain/motif analysis of the query
- Structural comparison if protein
