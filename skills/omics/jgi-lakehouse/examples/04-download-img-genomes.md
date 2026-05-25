# Download Genomes with IMG Taxon OIDs

Download microbial genomes directly from JGI filesystem using IMG taxon OIDs.

## Use Case

Get complete genome packages (FNA, FAA, GFF, annotations) for bacterial/archaeal isolates using their IMG taxon OID.

## Key Discovery

The Lakehouse contains **metadata only**. Actual genome files are on the JGI filesystem:

```
/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz
```

---

## Workflow

### Step 1: Query Lakehouse for Taxon OIDs

```sql
SELECT
    taxon_oid,
    taxon_display_name,
    domain,
    phylum,
    genus,
    species,
    seq_status,
    genome_type
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE domain = 'Bacteria'
  AND genome_type = 'isolate'
  AND is_public = 'Yes'
  AND seq_status = 'Finished'
ORDER BY taxon_oid DESC
LIMIT 20;
```

### Step 2: Check File Availability

```bash
# Check if genome package exists
ls /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/8136918376.tar.gz
```

### Step 3: Download and Extract

```bash
# Copy genome package
cp /clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/8136918376.tar.gz .

# Extract
tar -xzf 8136918376.tar.gz

# View contents
ls 8136918376/
```

---

## Genome Package Contents

Each `{taxon_oid}.tar.gz` contains:

| File | Description |
|------|-------------|
| `{taxon_oid}.fna` | Genome assembly (nucleotide) |
| `{taxon_oid}.genes.fna` | Gene nucleotide sequences |
| `{taxon_oid}.genes.faa` | Protein sequences |
| `{taxon_oid}.gff` | GFF annotations |
| `{taxon_oid}.cog.tab.txt` | COG annotations |
| `{taxon_oid}.pfam.tab.txt` | Pfam domain hits |
| `{taxon_oid}.ko.tab.txt` | KEGG KO annotations |
| `{taxon_oid}.tigrfam.tab.txt` | TIGRFAM annotations |
| `{taxon_oid}.signalp.tab.txt` | Signal peptide predictions |
| `{taxon_oid}.tmhmm.tab.txt` | Transmembrane predictions |
| `{taxon_oid}.intergenic.fna` | Intergenic regions |
| `README.txt` | Package documentation |

---

## Alternative: Per-Taxon Data Directories

For genomes not in tar.gz format, data may be in:

```
/clusterfs/jgi/img_merfs-ro/img_web_data_merfs/{taxon_oid}/assembled/
```

Contents:
- `fna/fna_*.sdb` - Nucleotide sequences (binary format)
- `faa/faa_*.sdb` - Protein sequences (binary format)
- `rRNA_16S.fna` - 16S rRNA sequences (FASTA)
- `taxon_stats.txt` - Genome statistics

---

## Python Script

Use `scripts/download_img_genomes.py` for automated download:

```python
# Query Lakehouse for taxon OIDs
taxon_oids = query_lakehouse_for_bacteria()

# Download from filesystem
for taxon_oid in taxon_oids[:5]:
    tar_path = f"/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/{taxon_oid}.tar.gz"
    if os.path.exists(tar_path):
        shutil.copy(tar_path, f"genomes/{taxon_oid}.tar.gz")
        # Extract...
```

---

## Linking GOLD IDs to IMG Taxon OIDs

```sql
-- Get GOLD ID for a taxon
SELECT taxon_oid, taxon_display_name, sequencing_gold_id, sample_gold_id
FROM "img-db-2 postgresql".img_core_v400.taxon
WHERE taxon_oid = 8136918376;
```

---

## Filesystem Paths Summary

| Path | Contents |
|------|----------|
| `/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/download/` | Tar.gz genome packages |
| `/clusterfs/jgi/img_merfs-ro/img_web_data_merfs/{taxon_oid}/` | Per-taxon data directories |
| `/clusterfs/jgi/img_merfs-ro/img_web/img_web_data/all_img_core_v400.fna` | All genomes in one file (465MB) |

---

## Pitfalls

1. **Not all taxons have tar.gz files** - Check existence before attempting copy
2. **Binary .sdb files** - Data in `img_web_data_merfs` uses binary format, not FASTA
3. **Filesystem access required** - Must be on JGI network/cluster
4. **New genomes may not be packaged** - Very recent additions may only be in data directories
