# Bio-Annotation Tool Documentation

This directory contains practical usage guides for the core bioinformatics tools used in the bio-annotation skill workflow.

## Documentation Overview

Each tool has a dedicated markdown file with comprehensive usage information including installation, command-line options, common examples, and performance tips.

## Available Tool Guides

### [DIAMOND](diamond-usage.md)
**Version**: v2.1.20+
**Purpose**: Accelerated BLAST-compatible sequence aligner (CPU)
**Key features**: 100×–10,000× faster than BLAST; protein and translated-DNA searches
**Documentation**: [diamond-usage.md](diamond-usage.md)
**Official site**: http://www.diamondsearch.org

### MMseqs2 / MMseqs2-GPU (alternative to DIAMOND on CUDA nodes)
**Version**: v15-6f452+
**Purpose**: Iterative sequence search; GPU-accelerated since the 2025 release
**Key features**: ~20× faster than CPU MMseqs2 and 177–199× faster than JackHMMER on CUDA Turing or newer; near-identical sensitivity. Reference: Kallenborn et al., *Nature Methods* 2025, DOI 10.1038/s41592-025-02819-8.
**Use when**: a GPU is available, or when iterative profile searches are needed in place of JackHMMER.

### [TaxonKit](taxonkit-usage.md)
**Version**: v0.20.0+ (required for the March 2025 NCBI rank update: "superkingdom" → "domain", added "realm" for viruses)
**Purpose**: NCBI taxonomy data manipulation toolkit
**Key features**: Taxonomy resolution, lineage queries, TaxID conversion
**Documentation**: [taxonkit-usage.md](taxonkit-usage.md)
**Official site**: https://bioinf.shenwei.me/taxonkit/

### [InterProScan](interproscan-usage.md)
**Version**: v5.77-108.0 (stable); InterProScan 6 (Nextflow) is the forward migration path
**Purpose**: Protein function classification and domain prediction
**Key features**: Integrates multiple signature databases, GO terms, pathway annotations
**Documentation**: [interproscan-usage.md](interproscan-usage.md)
**Official site**: https://www.ebi.ac.uk/interpro/

### [eggNOG-mapper](eggnog-mapper-usage.md)
**Version**: v2.1.13+
**Purpose**: Functional annotation through orthology assignment
**Key features**: Fast genome-wide annotation, COG categories, KEGG pathways; supports MMseqs2 as an internal search backend.
**Documentation**: [eggnog-mapper-usage.md](eggnog-mapper-usage.md)
**Official site**: http://eggnog-mapper.embl.de/

### pyhmmer (preferred HMMER interface)
**Version**: v0.10+
**Purpose**: Python bindings around HMMER 3.4 for profile HMM search
**Key features**: Native SIMD, batch-friendly APIs, no temporary-file overhead. Use for Pfam/TIGRFAM/PHROG/NCVOG/COG scans by default; fall back to `hmmsearch`/`hmmscan` only when an upstream tool requires the CLI.

## Workflow integration

These tools are used together in the bio-annotation workflow:

1. **InterProScan**: domain and family annotation from protein signatures.
2. **eggNOG-mapper**: orthology-based functional annotation with GO, COG, and KEGG.
3. **DIAMOND** (CPU) or **MMseqs2-GPU** (when a GPU is available): sequence similarity search for taxonomy and homology assignment.
4. **pyhmmer**: HMM-based marker-gene and domain-family searches.
5. **TaxonKit**: resolve taxonomy from search-result TaxIDs to full lineages.

## Quick Start Examples

### DIAMOND + TaxonKit Pipeline
```bash
# Sequence alignment with taxonomy
# Prefer a clustered nr database (e.g. clusterednr) for much faster search at
# comparable sensitivity. Check whether a clusterednr build is available under
# $BIO_DB_ROOT before running; if not, build one from a clustered FASTA or
# fall back to full nr and note the choice in the run log.
diamond blastp --query proteins.faa --db clusterednr.dmnd \
  --out results.tsv --outfmt 6 qseqid sseqid staxids evalue bitscore \
  --threads 32 --sensitive

# Resolve taxonomy
cut -f3 results.tsv | taxonkit lineage -n -r | \
  taxonkit reformat -f "{k};{p};{c};{o};{f};{g};{s}" | \
  paste results.tsv - > results_with_taxonomy.tsv
```

### InterProScan Annotation
```bash
# Comprehensive protein annotation
interproscan.sh -i proteins.faa -b interpro_results \
  -f TSV,GFF3 -goterms -iprlookup -pathways -cpu 32
```

### eggNOG-mapper Annotation
```bash
# Orthology-based annotation
emapper.py -i proteins.faa -o eggnog_annotation \
  --data_dir $EGGNOG_DATA_DIR \
  --sensmode very-sensitive \
  --cpu 32 --report_orthologs
```

## Performance Optimization

### Resource Requirements

| Tool | CPU | Memory | Disk Space | Speed |
|------|-----|--------|------------|-------|
| DIAMOND | High | Moderate (8-32GB) | Low | Very Fast |
| TaxonKit | Low | Low (1-2GB) | Low | Very Fast |
| InterProScan | High | High (16-64GB) | Moderate | Slow |
| eggNOG-mapper | High | Moderate (8-32GB) | High (databases) | Fast |

### Optimization Tips

1. **DIAMOND**: Use `--sensitive` mode by default, increase to `--very-sensitive` for divergent sequences
2. **TaxonKit**: Keep taxdump on SSD, use appropriate thread count
3. **InterProScan**: Validate the exact CLI first, use either `-b` or `-d` for output, and select specific analyses with `-appl` when appropriate
4. **eggNOG-mapper**: Use `--dbmem` on high-RAM systems, set appropriate `--tax_scope`

## Database Requirements

### DIAMOND
- **NCBI nr**: ~100-200GB (DIAMOND format)
- **Clustered nr (preferred)**: a sequence-clustered build of nr (e.g. `clusterednr`) — substantially smaller and faster to search at comparable sensitivity. Check whether one is already available under `$BIO_DB_ROOT` before downloading or building. If absent, build with `diamond makedb` from an MMseqs2/CD-HIT-reduced nr FASTA (cluster identity e.g. 70-90% depending on use case).
- **Custom databases**: Variable size
- **Update frequency**: Monthly recommended

### TaxonKit
- **NCBI taxdump**: ~500MB
- **Files needed**: nodes.dmp, names.dmp, merged.dmp, delnodes.dmp
- **Update frequency**: Monthly recommended

### InterProScan
- **InterPro data**: ~30-50GB
- **Components**: Multiple signature databases
- **Update frequency**: Quarterly recommended

### eggNOG-mapper
- **eggNOG database**: ~100GB+
- **Taxonomic-specific**: Variable (10-50GB per scope)
- **Update frequency**: Yearly recommended

## Common Issues and Solutions

### DIAMOND
- **Out of memory**: Reduce `--block-size`, increase `--index-chunks`
- **Slow performance**: Use faster sensitivity mode, reduce `--max-target-seqs`

### TaxonKit
- **Missing TaxIDs**: Update taxdump files, handle with `-F` flag
- **Slow processing**: Increase thread count, check disk I/O

### InterProScan
- **Memory errors**: Increase Java heap size in interproscan.properties
- **Timeout issues**: Split input into smaller batches
- **Immediate startup failure**: Check for mutually exclusive `-b`/`-d` usage, missing `setup.py` initialization, unresolved ProSite binaries, or `*` in the FAA input

### eggNOG-mapper
- **Database download fails**: Use `--resume` flag, check disk space
- **Slow annotation**: Use `--sensmode fast`, enable `--dbmem`

## References

### Official Documentation
- DIAMOND: https://github.com/bbuchfink/diamond/wiki
- TaxonKit: https://bioinf.shenwei.me/taxonkit/usage/
- InterProScan: https://interproscan-docs.readthedocs.io/
- eggNOG-mapper: https://github.com/eggnogdb/eggnog-mapper

### Citations
- **DIAMOND**: Buchfink et al. (2021) Nature Methods. doi:10.1038/s41592-021-01101-x
- **TaxonKit**: Shen & Ren (2021) J Genet Genomics. doi:10.1016/j.jgg.2021.03.006
- **InterProScan**: Jones et al. (2014) Bioinformatics. doi:10.1093/bioinformatics/btu031
- **eggNOG-mapper**: Cantalapiedra et al. (2021) Mol Biol Evol. doi:10.1093/molbev/msab293

## Documentation Updates

**Last Updated**: 2026-03-22
**Documentation Version**: 1.1
**Tool Versions**: See individual files for version-specific information

For the most current information, always refer to the official documentation links provided in each tool's usage guide.

## Additional Resources

### Related Documentation
- See `../SKILL.md` for overall bio-annotation workflow
- See `../summaries/` for example use cases from recent papers

### Support
For tool-specific issues, consult:
- Tool GitHub repositories (Issues section)
- Official documentation websites
- Bioconda package pages
- User communities (Biostars, Stack Overflow)
