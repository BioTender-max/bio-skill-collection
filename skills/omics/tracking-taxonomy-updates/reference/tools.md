# Tool cheat sheets (QuickClade, GTDB-Tk, EukCC, vConTACT3, GVClass, TaxonKit)

This file focuses on **operational usage** and **provenance capture**.

If the user asks “what’s the best tool?”, prefer **domain-appropriate** tools and then cross-check with NCBI taxids for interoperability.

## First-pass routing contract

Run QuickClade first for any assembly, MAG, SAG, isolate genome, bin directory, or unbinned contig FASTA. Use `percontig` for assemblies so mixed-domain contigs are not hidden by a whole-file majority label.

| QuickClade domain signal | Route | Downstream tool |
|---|---|---|
| Bacteria | Prokaryote genome taxonomy | GTDB-Tk |
| Archaea | Prokaryote genome taxonomy | GTDB-Tk |
| Eukaryota | Eukaryotic MAG/genome QC + lineage context | EukCC |
| Viral, virus-like, or phage/prokaryotic virus | Viral analysis | `/bio-viromics` -> vConTACT3 when phage/prokaryotic-virus evidence is supported |
| Nucleocytoviricota, giant virus, NCLDV | Giant-virus analysis | `/bio-viromics` -> GVClass plus marker-gene phylogeny |
| Mixed or low confidence | Review/split | Split contigs or keep as manual-review rows before domain-specific tools |

---

## QuickClade (BBTools / BBMap suite) — fast k-mer taxonomy screen

Authoritative docs:
- https://bbmap.org/tools/quickclade
- BBMap/BBTools home (find QuickClade under Tools):
  https://bbmap.org/

### What it does
- Compares k-mer frequency “spectra” between query sequences and a reference.
- Very fast; good for **first-pass** taxonomy screening for bins/contigs.
- Not a marker-gene phylogeny method; validate when stakes are high.

### Preferred execution (container)
Run QuickClade via the official BBTools container image:

- Container image: `bryce911/bbtools:39.84` (tagged per BBTools release; `latest` points to the same digest as of 2026-05-15)
- Current digest checked 2026-05-15: `sha256:60d73ca4d99e12434e3ef2135d7441e025272afc5493a580e365a3cbe7fcadc5`
- Docker Hub page:
  https://hub.docker.com/r/bryce911/bbtools/

#### Docker examples
Run on a FASTA in the current directory:
```bash
mkdir -p results/taxonomy
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickclade.sh contigs.fa percontig ref=references/quickclade.spectra.gz out=results/taxonomy/quickclade_percontig.tsv usetree
```

Run on a directory of bins:
```bash
mkdir -p results/taxonomy
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickclade.sh bins/ percontig ref=references/quickclade.spectra.gz out=results/taxonomy/quickclade_bins_percontig.tsv usetree
```

#### Apptainer / Singularity examples
Pull + run directly from Docker Hub:
```bash
mkdir -p results/taxonomy
apptainer exec --bind "$PWD":/work --pwd /work \
  docker://bryce911/bbtools:39.84 \
  quickclade.sh contigs.fa percontig ref=references/quickclade.spectra.gz out=results/taxonomy/quickclade_percontig.tsv usetree
```

### Reference spectra (important)
The QuickClade docs show a default reference path that may not exist on your system/container.
Best practice:
- always pass `ref=<spectra.gz>` explicitly, and record which reference you used
- build your own spectra from a reference FASTA using `cladeloader.sh` (BBTools)

---

## GTDB-Tk — prokaryote genome taxonomy (Bacteria/Archaea)

Docs:
- https://ecogenomics.github.io/GTDBTk/

### When to use
- Genome-based taxonomy for MAGs/SAGs/isolate genomes.
- Outputs GTDB taxonomy strings like: `d__Bacteria;p__...;...;s__...`

### Install/run (recommended)
Use **Pixi** for reproducible dependency management (see env/README.md in this Skill).
Always record:
- GTDB-Tk version
- GTDB reference package release ID/date

Note: GTDB-Tk has heavy reference data requirements; plan disk and RAM accordingly.

### Database check
Before classification, verify the reference package exists:

```bash
test -n "${GTDBTK_DATA_PATH:-}" && test -d "$GTDBTK_DATA_PATH"
gtdbtk check_install
```

If it is missing, create a project or shared DB location under `$BIO_DB_ROOT`, install the GTDB-Tk reference package using the current GTDB-Tk documentation or site mirror, export `GTDBTK_DATA_PATH`, then rerun `gtdbtk check_install`. Do not classify with a partial or unknown database.

---

## EukCC — eukaryotic MAG/genome QC + taxonomy context

Docs:
- https://eukcc.readthedocs.io/

### When to use
- Eukaryotic MAGs/genomes where bacterial QC tools are inappropriate.
- Provides completeness/contamination estimates and a taxonomy lineage.

### Install/run (recommended)
Use **Pixi** (see env/README.md) and capture:
- EukCC version
- database location/version (`EUKCC2_DB` or `--db`)

---

## vConTACT3 — viral clustering to support taxonomy inference

Docs:
- https://vcontact3.readthedocs.io/

### When to use
- Phage/prokaryotic-virus contigs/genomes: protein-sharing network clustering supports taxonomy inference.
- Not a replacement for ICTV; interpret results in ICTV context and with hallmark genes/phylogeny.

### Install/run (recommended)
Use **Pixi** (see env/README.md) and capture:
- vConTACT3 version
- database/reference used (if any)
- parameterization (e.g., thresholds, export options)

---

## GVClass — giant-virus / Nucleocytoviricota taxonomy

Docs:
- https://github.com/NeLLi-team/gvclass

### When to use
- Giant-virus, NCLDV, or Nucleocytoviricota candidates from QuickClade, geNomad, hallmark genes, or genome-size/marker evidence.
- Use with marker-gene phylogenies and literature-supported reference sets; do not force vConTACT3 on giant-virus candidates unless the literature justifies it.

### Provenance to capture
- GVClass version or commit
- reference/model bundle version
- run mode and thresholds
- marker-gene phylogeny inputs used for validation

---

## TaxonKit — NCBI taxonomy toolkit for taxids and lineages

Docs:
- https://bioinf.shenwei.me/taxonkit/usage/
- https://github.com/shenwei356/taxonkit

### When to use
- Enrich results with NCBI taxids, ranks, and complete lineages.
- Detect merged/deleted taxids and avoid brittle name-joins.

### Key commands
Taxid → lineage:
```bash
taxonkit lineage taxids.txt
```

Name → taxid:
```bash
taxonkit name2taxid names.txt
```

Lineage reformat:
```bash
taxonkit lineage taxids.txt | taxonkit reformat -f "{d};{k};{p};{c};{o};{f};{g};{s}"
```

### Data requirement
TaxonKit needs the NCBI taxdump on disk; record which dump/snapshot date you used.
