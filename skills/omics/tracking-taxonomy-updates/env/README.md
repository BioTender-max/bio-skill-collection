# Environment setup

This Skill assumes you may run tools locally (HPC, workstation, CI) and want **reproducible installs**.

## Recommended approach
- **QuickClade (BBTools)**: run via Bryce Foster's official BBTools container `bryce911/bbtools:39.84` (Docker or Apptainer/Singularity). As of 2026-05-15, `latest` points to the same digest: `sha256:60d73ca4d99e12434e3ef2135d7441e025272afc5493a580e365a3cbe7fcadc5`.
- **GTDB-Tk, EukCC, vConTACT3, TaxonKit**: manage dependencies via **Pixi** using `pixi.toml`.
- **GVClass**: use the `/bio-viromics` GVClass setup notes for giant-virus routes.

---

## A) QuickClade via container (preferred)

### Docker
```bash
docker pull bryce911/bbtools:39.84
docker run --rm bryce911/bbtools:39.84 quickclade.sh --help
```

For data in the current directory:
```bash
docker run --rm -u "$(id -u):$(id -g)"   -v "$PWD":/work -w /work   bryce911/bbtools:39.84   quickclade.sh contigs.fa percontig out=results.tsv usetree
```

For production runs, pass the spectra explicitly and write the standard per-contig artifact:

```bash
mkdir -p results/taxonomy
docker run --rm -u "$(id -u):$(id -g)" \
  -v "$PWD":/work -w /work \
  bryce911/bbtools:39.84 \
  quickclade.sh contigs.fa percontig ref=references/quickclade.spectra.gz out=results/taxonomy/quickclade_percontig.tsv usetree
```

### Apptainer / Singularity
```bash
apptainer exec docker://bryce911/bbtools:39.84 quickclade.sh --help
```

For data in the current directory:
```bash
apptainer exec --bind "$PWD":/work --pwd /work   docker://bryce911/bbtools:39.84   quickclade.sh contigs.fa percontig out=results.tsv usetree
```

Provenance: record container tag (and digest if available) in outputs.

---

## B) Pixi for GTDB-Tk / EukCC / vConTACT3 / TaxonKit

Pixi docs:
- https://pixi.prefix.dev/
Pixi manifest reference:
- https://pixi.prefix.dev/dev/reference/pixi_manifest/

### Install Pixi
Follow the official Pixi install instructions for your OS.

### Create the environment
From this Skill directory:
```bash
cd ~/.agents/skills/tracking-taxonomy-updates/env
pixi install
```

### Run commands
```bash
pixi run gtdbtk-help
pixi run eukcc-help
pixi run vcontact3-help
pixi run taxonkit-help
```

### Reproducibility tip
If you use this environment in a pipeline, commit:
- `pixi.toml`
- the generated lockfile (e.g., `pixi.lock`), if you create one

---

## C) Data packages you still need to manage explicitly
Even with reproducible tool installs, taxonomy work depends on large external datasets:

- **NCBI Taxdump** (TaxonKit needs this): download and record the dump date.
- **GTDB-Tk reference package**: download the correct reference package for your chosen GTDB release and record the release ID/date.
- **EukCC database**: set `EUKCC2_DB` (or pass `--db`) and record DB version.
- **vConTACT3 reference sets** (if used): record what you used (and from where).
