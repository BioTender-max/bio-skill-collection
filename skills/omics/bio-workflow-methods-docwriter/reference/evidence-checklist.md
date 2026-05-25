# Evidence checklist (what to collect)

## Minimum viable evidence (any workflow system)
- Pipeline repository URL + **commit SHA** (or release tag)
- Exact launch command (copy/paste)
- All config/params files used (e.g., `nextflow.config`, `params.json`, `config.yaml`)
- Workflow engine version (e.g., `nextflow -version`, `snakemake --version`, `cwltool --version`)
- A machine-readable list of **software tools + versions** (one of):
  - pipeline-emitted versions file (preferred)
  - conda env export (`conda env export`)
  - container image names + digests (`docker inspect`, `apptainer inspect`)
- Input dataset identifiers + checksums (or accessions + release dates)
- Reference assets versions (genome build, annotation release, db versions)
- QC reports + thresholds used
- Output directory layout (or a file manifest)

## Nextflow (recommended evidence)
Collect:
- `trace.txt` (or custom name) from `-with-trace`
- `report.html` from `-with-report`
- `timeline.html` from `-with-timeline`
- DAG image from `-with-dag`
- `.nextflow.log`
- `work/` directory *or* at least the task folders referenced in trace/log

How to capture next time (example):
```bash
nextflow run <pipeline> \
  -with-report report.html \
  -with-trace trace.txt \
  -with-timeline timeline.html \
  -with-dag flowchart.png
```

## Snakemake (recommended evidence)
Collect:
- `report.html` from `--report`
- `.snakemake/log/*` (scheduler + job logs)
- workflow files: `Snakefile`, `config.yaml`, profiles
- If you need exact commands, run with `--printshellcmds` and capture stdout/stderr.

How to capture next time (example):
```bash
snakemake --use-conda --cores 16 --printshellcmds --report report.html
```

## CWL / cwltool (recommended evidence)
Collect:
- Provenance Research Object folder produced by CWLProv (PROV traces + packed inputs/outputs)
- Workflow + tool definition files (`*.cwl`)
- Inputs object (`inputs.yml` / `inputs.json`)

How to capture next time (example):
```bash
cwltool --provenance provenance_ro/ workflow.cwl inputs.yml
```

