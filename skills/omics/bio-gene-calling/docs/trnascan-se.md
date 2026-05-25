# tRNAscan-SE

tRNA gene detection using covariance models and Infernal.

## Official Documentation
- Website: http://lowelab.ucsc.edu/tRNAscan-SE/
- GitHub: https://github.com/UCSC-LoweLab/tRNAscan-SE

## Installation

### Prerequisites
- Perl 5.0 or later
- Infernal (http://eddylab.org/infernal/)

### Installation Steps

```bash
# Install Infernal first
wget http://eddylab.org/infernal/infernal-1.1.5.tar.gz
tar xzf infernal-1.1.5.tar.gz
cd infernal-1.1.5
./configure --prefix=/usr/local
make
make install

# Install tRNAscan-SE
# Via conda (recommended)
conda install -c bioconda trnascan-se

# From source
git clone https://github.com/UCSC-LoweLab/tRNAscan-SE.git
cd tRNAscan-SE
./configure --prefix=/usr/local
make
make install
```

## Key Command-Line Flags

### Search Modes (Organism-Specific)
- `-B` - Bacterial mode
- `-A` - Archaeal mode
- `-E` - Eukaryotic mode (default)
- `-G` - General tRNA mode (all domains)

### Output Options
- `-o FILE` - Save results in tabular format
- `-f FILE` - Save secondary structure output
- `-m FILE` - Save statistics summary
- `-b FILE` - Save results in BED format
- `-a FILE` - Save results in FASTA format
- `-g FILE` - Save results in GTF format

### Search Parameters
- `-H` - Report possible pseudogenes
- `--detail` - Detailed output with scores
- `--thread N` - Number of CPU threads

## Common Usage Examples

### Bacterial tRNA Detection

```bash
tRNAscan-SE -B -o bacteria_trnas.txt -f bacteria_trnas.ss genome.fna
```

### Archaeal tRNA Detection

```bash
tRNAscan-SE -A -o archaea_trnas.txt genome.fna
```

### Eukaryotic tRNA Detection (Default)

```bash
tRNAscan-SE -o eukaryote_trnas.txt -f trna_structures.ss genome.fna
```

### Multi-Format Output

```bash
tRNAscan-SE -B \
    -o results.txt \
    -f structures.ss \
    -b results.bed \
    -a results.fa \
    -g results.gtf \
    genome.fna
```

### Parallel Execution

```bash
tRNAscan-SE -B --thread 8 -o results.txt genome.fna
```

### Include Pseudogenes

```bash
tRNAscan-SE -B -H -o results_with_pseudo.txt genome.fna
```

## Input/Output Formats

**Input:**
- FASTA format (DNA or RNA sequences)
- Single or multi-FASTA files
- Compressed files supported (gzip)

**Output Formats:**

1. **Tabular (-o)** - Standard results table
   - Columns: Sequence, tRNA#, Begin, End, Type, Anticodon, Intron, Score

2. **Secondary Structure (-f)** - Cloverleaf structures
   - ASCII art representation of tRNA folding

3. **FASTA (-a)** - tRNA sequences

4. **BED (-b)** - Genome browser format

5. **GTF (-g)** - Gene annotation format

## Search Modes Explained

### Bacterial Mode (-B)
- Optimized for bacterial genomes
- Uses bacterial-specific covariance models
- Faster than eukaryotic mode

### Archaeal Mode (-A)
- Archaeal-specific models
- Detects archaeal-specific tRNA features
- Handles unusual anticodons

### Eukaryotic Mode (-E)
- Default mode
- Nuclear tRNA genes
- Detects intron-containing tRNAs
- Can identify tRNA-derived SINEs

### General Mode (-G)
- All three domains combined
- Use for mixed samples or unknown organisms
- Slowest but most comprehensive

## Performance Tips

### Speed Optimization
- Use organism-specific mode (-B, -A, or -E)
- Enable multi-threading (--thread)
- General mode (-G) is slowest

### Accuracy Improvements
- Use correct mode for organism type
- Include pseudogenes (-H) for complete annotation
- Check detailed scores (--detail) for borderline hits

### Large Genomes
- Split genome into smaller chunks
- Process scaffolds in parallel
- Use --thread to utilize multiple cores

### Quality Control
- Verify anticodon assignments
- Check for unusual intron positions
- Compare results across search modes
- Expected tRNA counts: ~30-100 per bacterial genome

## Infernal Integration

tRNAscan-SE 2.0 uses Infernal v1.1:
- 100-fold faster than previous versions
- Isotype-specific covariance models
- Improved sensitivity for divergent tRNAs
- Better discrimination of pseudogenes
