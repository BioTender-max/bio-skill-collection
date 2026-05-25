#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path


_SKILL_DIR = Path(__file__).resolve().parent
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))
sys.path.insert(0, str(_SKILL_DIR))
_PROJECT_ROOT = _SKILL_DIR.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_DOWNSTREAM_HANDOFF_TIMEOUT_SECONDS = 60 * 60 * 2


def _purge_foreign_bare_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and _SKILL_DIR not in module_file.parents and module_file != _SKILL_DIR / f"{name}.py":
            sys.modules.pop(name, None)


_purge_foreign_bare_modules(
    "command_builder",
    "errors",
    "executor",
    "outputs_parser",
    "params_builder",
    "pipeline_source",
    "preflight",
    "provenance",
    "reporting",
    "samplesheet_builder",
    "schemas",
)

from command_builder import build_nextflow_command
from errors import ErrorCode, SkillError
from executor import execute_nextflow
from outputs_parser import parse_outputs
from params_builder import build_effective_params, write_params_yaml
from pipeline_source import resolve_pipeline_source
from preflight import check_output_dir_available, check_resume_params_checksum, check_resume_samplesheet_checksum, run_preflight
from provenance import write_provenance_bundle
from reporting import write_check_result, write_report, write_repro_commands, write_result
from samplesheet_builder import validate_and_normalize_samplesheet
from schemas import (
    DEFAULT_PIPELINE_VERSION,
    DEFAULT_PROFILE,
    DEFAULT_TIMEOUT_SECONDS,
    SKILL_NAME,
    SUPPORTED_ALIGNERS,
    SUPPORTED_PROFILES,
    SUPPORTED_PSEUDO_ALIGNERS,
    SUPPORTED_RIBO_TOOLS,
    SUPPORTED_TRIMMERS,
    SUPPORTED_UMI_TOOLS,
)


_DASH_VALUE_OPTIONS = {
    "--extra-trimgalore-args",
    "--extra-fastp-args",
    "--extra-fqlint-args",
    "--extra-star-align-args",
    "--extra-bowtie2-align-args",
    "--extra-salmon-quant-args",
    "--extra-kallisto-quant-args",
    "--rsem-extra-args",
    # GPU container flags (e.g. '--gpus all', '--nv') begin with a dash and would
    # otherwise be misparsed as wrapper options without the dash-value rewrite.
    "--gpu-container-options",
}


class _RnaseqArgumentParser(argparse.ArgumentParser):
    """Allow upstream extra-args values that begin with dashes."""

    def parse_args(self, args: list[str] | None = None, namespace: argparse.Namespace | None = None):
        return super().parse_args(self._normalise_dash_values(args), namespace)

    def parse_known_args(self, args: list[str] | None = None, namespace: argparse.Namespace | None = None):
        return super().parse_known_args(self._normalise_dash_values(args), namespace)

    def _normalise_dash_values(self, args: list[str] | None) -> list[str] | None:
        if args is None:
            return None
        known_options = {option for action in self._actions for option in action.option_strings}
        normalised: list[str] = []
        i = 0
        while i < len(args):
            token = args[i]
            if token in _DASH_VALUE_OPTIONS and i + 1 < len(args):
                value = args[i + 1]
                if value.startswith("-") and value not in known_options:
                    normalised.append(f"{token}={value}")
                    i += 2
                    continue
            normalised.append(token)
            i += 1
        return normalised


def build_parser() -> argparse.ArgumentParser:
    parser = _RnaseqArgumentParser(description="Run nf-core/rnaseq through the ClawBio wrapper.")
    parser.add_argument("--input", help="Path to a valid nf-core/rnaseq samplesheet.csv")
    parser.add_argument("--output", required=True, help="Output directory for wrapper results")
    parser.add_argument("--demo", action="store_true", help="Run the upstream test profile without user FASTQs")
    parser.add_argument("--check", action="store_true", help="Run wrapper preflight only and exit before Nextflow")
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help=(
            "Nextflow execution backend profile. "
            "Common values: docker, singularity, apptainer, podman, conda, mamba, shifter, charliecloud. "
            "Modifier profiles (appended automatically by --prokaryotic / --arm / --rapid-quant): "
            "prokaryotic, arm64, rapid_quant. "
            "nf-core/rnaseq test profiles (test, test_full, test_full_aws) and institutional "
            "profiles (e.g. uppmax, slurm, my_hpc) are passed through unchanged to Nextflow."
        ),
    )
    parser.add_argument("--pipeline-version", default=DEFAULT_PIPELINE_VERSION, help="Pinned remote nf-core/rnaseq tag or commit")
    parser.add_argument("--pipeline-local", default=None, help="Optional local nf-core/rnaseq checkout override")
    parser.add_argument("--resume", action="store_true", help="Attempt checksum-validated Nextflow resume")

    parser.add_argument("--aligner", default=None, choices=sorted(SUPPORTED_ALIGNERS))
    parser.add_argument("--pseudo-aligner", default=None, choices=sorted(SUPPORTED_PSEUDO_ALIGNERS))
    parser.add_argument("--pseudo-aligner-kmer-size", type=int, default=None)
    parser.add_argument("--prokaryotic", action="store_true", help="Compose the prokaryotic nf-core profile")

    parser.add_argument("--genome", default=None)
    parser.add_argument("--igenomes-base", default=None, help="Override iGenomes base path (S3 URI or local directory). Required when using --genome on HPC clusters with a local iGenomes mirror.")
    parser.add_argument("--fasta", default=None)
    parser.add_argument("--gtf", default=None)
    parser.add_argument("--gff", default=None)
    parser.add_argument("--gene-bed", default=None)
    parser.add_argument("--transcript-fasta", default=None)
    parser.add_argument("--additional-fasta", default=None)
    parser.add_argument("--splicesites", default=None)
    parser.add_argument("--star-index", default=None)
    parser.add_argument("--hisat2-index", default=None)
    parser.add_argument("--rsem-index", default=None)
    parser.add_argument("--salmon-index", default=None)
    parser.add_argument("--kallisto-index", default=None)
    parser.add_argument("--bowtie2-index", default=None)
    parser.add_argument("--gencode", action="store_true")

    parser.add_argument("--trimmer", default="trimgalore", choices=sorted(SUPPORTED_TRIMMERS))
    parser.add_argument("--extra-trimgalore-args", default=None)
    parser.add_argument("--extra-fastp-args", default=None)
    parser.add_argument("--min-trimmed-reads", type=int, default=None, help="Minimum number of reads a sample must retain after trimming to continue (pipeline default: 10000; must be ≥ 0).")
    parser.add_argument("--sortmerna-index", default=None)
    parser.add_argument("--ribo-database-manifest", default=None)
    parser.add_argument("--remove-ribo-rna", action="store_true")
    parser.add_argument("--ribo-removal-tool", default=None, choices=sorted(SUPPORTED_RIBO_TOOLS))
    parser.add_argument("--with-umi", action="store_true")
    parser.add_argument("--umi-dedup-tool", default=None, choices=sorted(SUPPORTED_UMI_TOOLS))
    parser.add_argument("--umitools-extract-method", default=None, choices=["string", "regex"])
    parser.add_argument("--umitools-bc-pattern", default=None)
    parser.add_argument("--umitools-bc-pattern2", default=None)
    parser.add_argument("--umitools-umi-separator", default=None)
    parser.add_argument("--umi-discard-read", type=int, default=None, choices=[1, 2])
    parser.add_argument(
        "--umitools-grouping-method",
        default=None,
        choices=["unique", "percentile", "cluster", "adjacency", "directional"],
    )
    parser.add_argument("--skip-umi-extract", action="store_true")
    parser.add_argument("--umitools-dedup-stats", action="store_true")
    parser.add_argument("--umitools-dedup-primary-only", action="store_true")

    parser.add_argument("--seq-center", default=None)
    parser.add_argument("--seq-platform", default=None)
    parser.add_argument("--min-mapped-reads", type=float, default=None)
    parser.add_argument("--star-ignore-sjdbgtf", action="store_true")
    parser.add_argument(
        "--salmon-quant-libtype",
        default=None,
        # Enum values from nf-core/rnaseq 3.26.0 nextflow_schema.json.
        choices=["A", "IS", "ISF", "ISR", "IU", "MS", "MSF", "MSR", "MU", "OS", "OSF", "OSR", "OU", "SF", "SR", "U"],
    )
    parser.add_argument("--extra-star-align-args", default=None)
    parser.add_argument("--extra-bowtie2-align-args", default=None)
    parser.add_argument("--extra-salmon-quant-args", default=None)
    parser.add_argument("--extra-kallisto-quant-args", default=None)
    parser.add_argument(
        "--kallisto-quant-fraglen",
        type=int,
        default=None,
        help="Mean fragment length for single-end Kallisto quantification (single-end only; pipeline default: 200).",
    )
    parser.add_argument(
        "--kallisto-quant-fraglen-sd",
        type=int,
        default=None,
        help="Fragment length standard deviation for single-end Kallisto quantification (single-end only; pipeline default: 200).",
    )
    parser.add_argument("--bam-csi-index", action="store_true")
    parser.add_argument("--stringtie-ignore-gtf", action="store_true")
    parser.add_argument("--stranded-threshold", type=float, default=None)
    parser.add_argument("--unstranded-threshold", type=float, default=None)

    parser.add_argument("--contaminant-screening", default=None, choices=["kraken2", "kraken2_bracken", "sylph"])
    parser.add_argument("--contaminant-screening-input", default=None, choices=["trimmed", "unmapped"])
    parser.add_argument("--kraken-db", default=None)
    parser.add_argument(
        "--bracken-precision",
        default=None,
        choices=["D", "P", "C", "O", "F", "G", "S"],
        help="Bracken taxonomic level for classification (D=domain P=phylum C=class O=order F=family G=genus S=species). Pipeline default: S.",
    )
    parser.add_argument("--sylph-db", default=None)
    parser.add_argument("--sylph-taxonomy", default=None)
    parser.add_argument("--bbsplit-fasta-list", default=None)
    parser.add_argument("--bbsplit-index", default=None)
    parser.add_argument("--skip-bbsplit", action="store_true", help="Skip BBSplit even when --bbsplit-fasta-list or --bbsplit-index is provided")
    parser.add_argument("--save-kraken-assignments", action="store_true")
    parser.add_argument("--save-kraken-unassigned", action="store_true")
    parser.add_argument("--save-bbsplit-reads", action="store_true")

    parser.add_argument("--hisat2-build-memory", default=None)
    parser.add_argument("--gffread-transcript-fasta", action="store_true")
    parser.add_argument("--arm", action="store_true", help="Compose arm64 into the Nextflow profile string (e.g. --profile docker --arm → -profile docker,arm64). Use on Apple M-series or AWS Graviton hosts.")
    parser.add_argument("--use-rustqc", action="store_true")
    parser.add_argument("--use-parabricks-star", action="store_true")
    parser.add_argument("--use-sentieon-star", action="store_true")
    parser.add_argument("--use-gpu-ribodetector", action="store_true")
    parser.add_argument("--gpu-container-options", default=None, help="GPU container flag override (e.g. '--gpus all')")
    parser.add_argument("--rapid-quant", action="store_true")
    parser.add_argument("--featurecounts-group-type", default=None)
    parser.add_argument("--featurecounts-feature-type", default=None)
    parser.add_argument("--gtf-extra-attributes", default=None)
    parser.add_argument("--gtf-group-features", default=None)
    parser.add_argument("--deseq2-vst", dest="deseq2_vst", action="store_true", default=None)
    parser.add_argument("--no-deseq2-vst", dest="deseq2_vst", action="store_false")
    parser.add_argument(
        "--rseqc-modules",
        default=None,
        help=(
            "Comma-separated RSeQC modules to run. "
            "Default set: bam_stat,inner_distance,infer_experiment,junction_annotation,"
            "junction_saturation,read_distribution,read_duplication. "
            "Add 'tin' for Transcript Integrity Number analysis (slow on large datasets)."
        ),
    )

    parser.add_argument("--extra-fqlint-args", default=None, help="Additional arguments for fq lint")
    parser.add_argument("--skip-linting", action="store_true")
    parser.add_argument("--skip-gtf-filter", action="store_true")
    parser.add_argument("--skip-gtf-transcript-filter", action="store_true")
    parser.add_argument("--skip-trimming", action="store_true")
    parser.add_argument("--skip-alignment", action="store_true")
    parser.add_argument("--skip-pseudo-alignment", action="store_true")
    parser.add_argument("--skip-quantification-merge", action="store_true")
    parser.add_argument("--skip-markduplicates", action="store_true")
    parser.add_argument("--skip-bigwig", action="store_true")
    parser.add_argument("--skip-stringtie", action="store_true")
    parser.add_argument("--skip-fastqc", action="store_true")
    parser.add_argument("--skip-dupradar", action="store_true")
    parser.add_argument("--skip-qualimap", action="store_true")
    parser.add_argument("--skip-rseqc", action="store_true")
    parser.add_argument("--skip-biotype-qc", action="store_true")
    parser.add_argument("--skip-deseq2-qc", action="store_true")
    parser.add_argument("--skip-multiqc", action="store_true")
    parser.add_argument("--skip-qc", action="store_true")
    parser.add_argument("--enable-preseq", action="store_true")

    parser.add_argument("--save-reference", action="store_true")
    parser.add_argument("--save-trimmed", action="store_true")
    parser.add_argument("--save-align-intermeds", action="store_true")
    parser.add_argument("--save-unaligned", action="store_true")
    parser.add_argument("--save-merged-fastq", action="store_true")
    parser.add_argument("--save-non-ribo-reads", action="store_true")
    parser.add_argument("--save-umi-intermeds", action="store_true")

    parser.add_argument(
        "--publish-dir-mode",
        default=None,
        choices=["symlink", "rellink", "link", "copy", "copyNoFollow", "move"],
        help="Nextflow publishDir mode. Use 'symlink' or 'link' to save disk space on HPC (pipeline default: copy).",
    )
    parser.add_argument("--email", default=None)
    parser.add_argument("--email-on-fail", default=None, help="Send failure notification to this address even when --email is not set.")
    parser.add_argument("--multiqc-title", default=None)
    parser.add_argument("--multiqc-config", default=None)
    parser.add_argument("--multiqc-logo", default=None)
    parser.add_argument("--multiqc-methods-description", default=None)
    parser.add_argument(
        "--rsem-extra-args",
        default=None,
        help=(
            "[No effect] nf-core/rnaseq 3.26.0 does not expose an extra_rsem_quant_args parameter. "
            "A preflight warning is emitted. To customise RSEM args use a Nextflow config: "
            "process { withName: 'RSEM_CALCULATEEXPRESSION' { ext.args = '...' } }"
        ),
    )
    parser.add_argument(
        "--nextflow-config",
        action="append",
        metavar="CONFIG",
        default=None,
        help=(
            "Additional Nextflow config file(s) passed as -c to Nextflow. "
            "Can be repeated: --nextflow-config hpc.config --nextflow-config rsem.config. "
            "Use this for institution-specific settings, RSEM ext.args, or any non-parametric "
            "configuration not exposed via --params-file."
        ),
    )
    parser.add_argument("--run-downstream", action="store_true", help="Write rnaseq-de handoff template when counts are available")
    parser.add_argument("--skip-downstream", action="store_true", help="Compatibility flag; prevents handoff template creation")
    parser.add_argument("--metadata", default=None, help="Metadata CSV/TSV passed to rnaseq-de when auto-handoff is enabled")
    parser.add_argument("--formula", default=None, help="DESeq2 formula passed to rnaseq-de when auto-handoff is enabled")
    parser.add_argument("--contrast", default=None, help="rnaseq-de contrast factor,numerator,denominator")
    parser.add_argument("--downstream-output", default=None, help="Optional rnaseq-de output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    output_dir = Path(args.output).expanduser().resolve()
    try:
        return _run_wrapper(args, output_dir)
    except SkillError as exc:
        return _handle_skill_error(output_dir, exc)
    except Exception as exc:
        return _handle_unexpected_error(output_dir, exc)


def _run_wrapper(args: argparse.Namespace, output_dir: Path) -> int:
    _apply_demo_overrides(args)
    _sync_profile_flags(args)
    _apply_prokaryotic_overrides(args)
    _apply_rapid_quant_overrides(args)
    _apply_aligner_default(args)
    if args.resume:
        with tempfile.TemporaryDirectory(prefix="clawbio-rnaseq-resume-") as staging:
            return _run_wrapper_with_staging(args, output_dir, staging_dir=Path(staging))
    return _run_wrapper_with_staging(args, output_dir, staging_dir=None)


# Reference / index flags that --demo must clear before they reach params.yaml.
# Why: the upstream `test` profile bundles test FASTQs paired with its own reference
# data. params-file values override profile values in Nextflow, so leaving e.g.
# args.fasta set would silently desynchronise the test samples from their reference
# genome and produce garbage counts. Clearing keeps the demo hermetic.
_DEMO_CLEARED_REFERENCE_FIELDS = (
    "genome",
    "igenomes_base",
    "fasta",
    "gtf",
    "gff",
    "transcript_fasta",
    "additional_fasta",
    "gene_bed",
    "splicesites",
    "star_index",
    "rsem_index",
    "hisat2_index",
    "salmon_index",
    "kallisto_index",
    "bowtie2_index",
    "sortmerna_index",
)


def _apply_demo_overrides(args: argparse.Namespace) -> None:
    """Coerce demo-incompatible flags before any validation runs.

    --demo runs the upstream `test` profile, which ships with a fixed
    samplesheet and STAR-Salmon-compatible test data. The wrapper enforces:

    * `--aligner` is forced to `star_salmon` (warn if the user requested another).
    * `--input` is dropped (the test profile provides its own samplesheet).
    * `--resume` is disabled (resume against a synthetic test run is not useful).
    * All reference/index flags are cleared (the test profile bundles its own refs;
      a partial override — e.g. only --fasta — would desync samples from refs).

    Centralising the override here keeps preflight, samplesheet preparation,
    and params construction consistent — every downstream stage sees the same
    coerced ``args``.
    """
    if not getattr(args, "demo", False):
        return
    requested_aligner = getattr(args, "aligner", None)
    if requested_aligner and requested_aligner != "star_salmon":
        print(
            f"WARNING: --demo forces --aligner star_salmon (requested: {requested_aligner!r}).",
            file=sys.stderr,
        )
    args.aligner = "star_salmon"
    if getattr(args, "input", None):
        print(
            "WARNING: --demo ignores --input; the upstream test profile provides its own samplesheet.",
            file=sys.stderr,
        )
        args.input = None
    if getattr(args, "resume", False):
        print(
            "WARNING: --demo disables --resume; demo runs cannot resume from a prior synthetic run.",
            file=sys.stderr,
        )
        args.resume = False
    cleared = [field for field in _DEMO_CLEARED_REFERENCE_FIELDS if getattr(args, field, None)]
    if cleared:
        flags = ", ".join("--" + field.replace("_", "-") for field in cleared)
        print(
            f"WARNING: --demo ignores reference flags ({flags}); "
            "the upstream test profile provides its own bundled references.",
            file=sys.stderr,
        )
        for field in cleared:
            setattr(args, field, None)


def _apply_prokaryotic_overrides(args: argparse.Namespace) -> None:
    """Coerce aligner to bowtie2_salmon when --prokaryotic is set and no aligner was specified.

    The nf-core/rnaseq prokaryotic profile (conf/prokaryotic.config) sets
    ``aligner = 'bowtie2_salmon'`` because STAR is a splice-aware eukaryotic
    aligner and is scientifically wrong for prokaryotic RNA-seq.  Nextflow
    params-file values override profile defaults, so writing ``aligner:
    star_salmon`` from the argparse default would silently defeat the profile.

    When the user explicitly passes ``--aligner <anything>`` (including
    ``star_salmon``), the sentinel value ``args.aligner`` is non-None and the
    user's choice is honoured without coercion.
    """
    if not getattr(args, "prokaryotic", False):
        return
    if getattr(args, "aligner", None) is None:
        print(
            "WARNING: --prokaryotic forces --aligner bowtie2_salmon "
            "(STAR is splice-aware and not suitable for prokaryotic RNA-seq).",
            file=sys.stderr,
        )
        args.aligner = "bowtie2_salmon"


_PROKARYOTIC_PROFILE_TOKENS = frozenset({"prokaryotic", "test_prokaryotic"})

# nf-core/rnaseq profiles that ship with params.input in their profile config.
# Running these without --input is valid upstream; the wrapper must not block them.
# NOTE: 'debug' is intentionally excluded — it only toggles debug logging flags
# (dumpHashes, cleanup=false) and carries no params.input or reference data.
_SELF_CONTAINED_TEST_PROFILES = frozenset({
    "test",
    "test_full",
    "test_prokaryotic",
    "test_full_aws",
    "test_full_gcp",
    "test_full_azure",
    "test_gpu",
})


def _sync_profile_flags(args: argparse.Namespace) -> None:
    """Detect modifier keywords in the --profile string and sync the corresponding args flags.

    Users may pass ``--profile prokaryotic,docker``, ``--profile test_prokaryotic``,
    or ``--profile rapid_quant`` instead of the dedicated ``--prokaryotic`` /
    ``--rapid-quant`` flags.  When a modifier keyword appears in the profile string,
    the corresponding flag is set to True so that ``_apply_prokaryotic_overrides`` and
    ``_apply_rapid_quant_overrides`` fire correctly — including their aligner coercion
    and params.yaml writes.

    ``test_prokaryotic`` is an official nf-core/rnaseq profile that includes
    ``conf/prokaryotic.config`` and sets ``aligner = 'bowtie2_salmon'``.
    ``arm64`` is detected so that ``params.yaml`` receives ``arm: true`` even when
    the user passes ``--profile docker,arm64`` instead of ``--arm``.

    Self-contained test profiles (test, test_full, test_prokaryotic, etc.) include
    ``params.input`` in their profile config and do not require a user samplesheet.
    When detected, ``args._noinput`` is set to True so that ``_prepare_samplesheet``
    and ``params_builder`` skip the input requirement.
    """
    profile_parts = {p.strip() for p in getattr(args, "profile", "").split(",") if p.strip()}
    if profile_parts & _PROKARYOTIC_PROFILE_TOKENS and not getattr(args, "prokaryotic", False):
        args.prokaryotic = True
    if "rapid_quant" in profile_parts and not getattr(args, "rapid_quant", False):
        args.rapid_quant = True
    if "arm64" in profile_parts and not getattr(args, "arm", False):
        args.arm = True
    if profile_parts & _SELF_CONTAINED_TEST_PROFILES and not getattr(args, "_noinput", False):
        args._noinput = True


def _apply_aligner_default(args: argparse.Namespace) -> None:
    """Apply the star_salmon default after all profile overrides have run.

    ``--aligner`` defaults to None (sentinel) so that ``_apply_prokaryotic_overrides``
    can distinguish "user did not pass --aligner" from "user explicitly passed
    --aligner star_salmon".  After all override functions have had a chance to
    set a non-None value (e.g. bowtie2_salmon for prokaryotic, star_salmon for demo),
    this function fills in the star_salmon default for any run that still has None.
    """
    if getattr(args, "aligner", None) is None:
        args.aligner = "star_salmon"


def _apply_rapid_quant_overrides(args: argparse.Namespace) -> None:
    """Mirror the rapid_quant profile's implied args so outputs_parser finds the right files.

    conf/rapid_quant.config sets skip_alignment=true, pseudo_aligner='salmon', and
    skip_quantification_merge=true.  Because Nextflow profile values are not visible to
    the Python wrapper, the outputs parser would otherwise look for star_salmon merged
    counts instead of per-sample salmon quant dirs.  Mirroring the profile settings
    into args also writes them explicitly to params.yaml, making the reproducibility
    bundle self-describing.
    """
    if not getattr(args, "rapid_quant", False):
        return
    if not getattr(args, "pseudo_aligner", None):
        args.pseudo_aligner = "salmon"
    if not getattr(args, "skip_alignment", False):
        args.skip_alignment = True
    if not getattr(args, "skip_quantification_merge", False):
        args.skip_quantification_merge = True


def _run_wrapper_with_staging(args: argparse.Namespace, output_dir: Path, *, staging_dir: Path | None) -> int:
    pipeline_source = resolve_pipeline_source(
        requested_version=args.pipeline_version,
        local_pipeline_dir=Path(args.pipeline_local).expanduser().resolve() if args.pipeline_local else None,
    )
    normalized_samplesheet, staged_samplesheet, samplesheet_summary = _prepare_samplesheet(
        args,
        output_dir,
        staging_dir=staging_dir,
    )
    preflight_result = run_preflight(args, pipeline_source=pipeline_source, samplesheet_summary=samplesheet_summary)
    if args.check:
        if staged_samplesheet != normalized_samplesheet:
            _commit_validated_samplesheet(staged_samplesheet, normalized_samplesheet)
        return _write_check_mode_result(output_dir, preflight_result=preflight_result, pipeline_source=pipeline_source)
    return _run_execution_mode(
        args,
        output_dir=output_dir,
        pipeline_source=pipeline_source,
        preflight_result=preflight_result,
        normalized_samplesheet=normalized_samplesheet,
        staged_samplesheet=staged_samplesheet,
        samplesheet_summary=samplesheet_summary,
    )


def _prepare_samplesheet(
    args: argparse.Namespace,
    output_dir: Path,
    *,
    staging_dir: Path | None,
) -> tuple[Path, Path, dict[str, object]]:
    if args.demo:
        return _prepare_demo_samplesheet(args, output_dir, staging_dir=staging_dir)
    if getattr(args, "_noinput", False):
        return _prepare_noinput_samplesheet(args, output_dir, staging_dir=staging_dir)
    return _prepare_user_samplesheet(args, output_dir, staging_dir=staging_dir)


def _prepare_demo_samplesheet(
    args: argparse.Namespace,
    output_dir: Path,
    *,
    staging_dir: Path | None,
) -> tuple[Path, Path, dict[str, object]]:
    # Demo overrides (aligner=star_salmon, input cleared, resume disabled) are
    # applied centrally in ``_apply_demo_overrides`` before this point.
    normalized_samplesheet = _final_samplesheet_path(output_dir, demo=True)
    staged_samplesheet = _staged_samplesheet_path(output_dir, staging_dir=staging_dir, demo=True)
    _write_demo_samplesheet(staged_samplesheet)
    return normalized_samplesheet, staged_samplesheet, {
        "normalized_path": normalized_samplesheet,
        "sample_count": 0,
        "sample_names": [],
        "fastq_paths": [],
        "bam_paths": [],
        "unknown_columns": [],
        "strandedness_counts": {},
    }


def _prepare_noinput_samplesheet(
    args: argparse.Namespace,
    output_dir: Path,
    *,
    staging_dir: Path | None,
) -> tuple[Path, Path, dict[str, object]]:
    """Write a provenance stub for self-contained nf-core test profiles.

    Profiles like test_full, test_prokaryotic, and test_full_aws ship with
    params.input in their own profile config.  The wrapper does not write an
    input key to params.yaml for these runs.  This stub (samplesheet.noinput.csv)
    lets auditors distinguish a test-profile run from a real --demo run.
    """
    normalized_samplesheet = _final_samplesheet_path(output_dir, noinput=True)
    staged_samplesheet = _staged_samplesheet_path(output_dir, staging_dir=staging_dir, noinput=True)
    _write_noinput_samplesheet_stub(staged_samplesheet)
    return normalized_samplesheet, staged_samplesheet, {
        "normalized_path": normalized_samplesheet,
        "sample_count": 0,
        "sample_names": [],
        "fastq_paths": [],
        "bam_paths": [],
        "unknown_columns": [],
        "strandedness_counts": {},
    }


def _prepare_user_samplesheet(
    args: argparse.Namespace,
    output_dir: Path,
    *,
    staging_dir: Path | None,
) -> tuple[Path, Path, dict[str, object]]:
    if not args.input:
        raise SkillError(
            stage="validation",
            error_code=ErrorCode.MISSING_INPUT,
            message="An input samplesheet is required unless --demo is used.",
            fix="Provide --input <samplesheet.csv> or run with --demo.",
            details={},
        )
    normalized_samplesheet = _final_samplesheet_path(output_dir)
    staged_samplesheet = _staged_samplesheet_path(output_dir, staging_dir=staging_dir)
    samplesheet_summary = validate_and_normalize_samplesheet(
        Path(args.input).expanduser().resolve(),
        staged_samplesheet,
        skip_alignment=getattr(args, "skip_alignment", False),
    )
    samplesheet_summary["normalized_path"] = normalized_samplesheet
    _warn_about_preserved_unknown_columns(samplesheet_summary)
    return normalized_samplesheet, staged_samplesheet, samplesheet_summary


def _write_demo_samplesheet(samplesheet_path: Path) -> None:
    samplesheet_path.parent.mkdir(parents=True, exist_ok=True)
    samplesheet_path.write_text("sample,fastq_1,fastq_2,strandedness\n", encoding="utf-8")


def _write_noinput_samplesheet_stub(samplesheet_path: Path) -> None:
    samplesheet_path.parent.mkdir(parents=True, exist_ok=True)
    samplesheet_path.write_text(
        "# Input provided by self-contained nf-core test profile (no --input required)\n",
        encoding="utf-8",
    )


def _final_samplesheet_path(output_dir: Path, *, demo: bool = False, noinput: bool = False) -> Path:
    if demo:
        filename = "samplesheet.demo.csv"
    elif noinput:
        filename = "samplesheet.noinput.csv"
    else:
        filename = "samplesheet.valid.csv"
    return output_dir / "reproducibility" / filename


def _staged_samplesheet_path(
    output_dir: Path, *, staging_dir: Path | None, demo: bool = False, noinput: bool = False
) -> Path:
    if staging_dir is not None:
        if demo:
            filename = "samplesheet.demo.csv"
        elif noinput:
            filename = "samplesheet.noinput.csv"
        else:
            filename = "samplesheet.valid.csv"
        return staging_dir / filename
    return _final_samplesheet_path(output_dir, demo=demo, noinput=noinput)


def _warn_about_preserved_unknown_columns(samplesheet_summary: dict[str, object]) -> None:
    unknown_columns = samplesheet_summary.get("unknown_columns", [])
    if unknown_columns:
        print(
            f"WARNING: samplesheet contains unrecognised columns that will be preserved: {unknown_columns}",
            file=sys.stderr,
        )


def _write_check_mode_result(
    output_dir: Path,
    *,
    preflight_result: dict[str, object],
    pipeline_source: dict[str, object],
) -> int:
    payload = {
        "ok": True,
        "skill": SKILL_NAME,
        "preflight": preflight_result,
        "pipeline_source": pipeline_source,
    }
    write_check_result(output_dir, payload)
    print(json.dumps(payload, indent=2))
    return 0


def _run_execution_mode(
    args: argparse.Namespace,
    *,
    output_dir: Path,
    pipeline_source: dict[str, object],
    preflight_result: dict[str, object],
    normalized_samplesheet: Path,
    staged_samplesheet: Path,
    samplesheet_summary: dict[str, object],
) -> int:
    params_payload = build_effective_params(
        args,
        normalized_samplesheet=normalized_samplesheet,
        output_dir=output_dir,
        gencode_autodetected=bool(preflight_result.get("gencode_autodetected", False)),
    )
    _check_resume_params_checksum(args, output_dir=output_dir, params_payload=params_payload)
    _check_resume_samplesheet_checksum(args, output_dir=output_dir, staged_samplesheet=staged_samplesheet)
    _commit_validated_samplesheet(staged_samplesheet, normalized_samplesheet)
    params_path = write_params_yaml(params_payload, output_dir=output_dir)
    command, command_str = _build_nextflow_invocation(args, output_dir, pipeline_source, params_path)
    nextflow_cwd = _nextflow_execution_cwd(output_dir)
    started = time.monotonic()
    execution_result = execute_nextflow(
        command,
        cwd=nextflow_cwd,
        output_dir=output_dir,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
    )
    duration_seconds = round(time.monotonic() - started, 3)
    parsed_outputs = _parse_outputs_with_effective_aligner(output_dir, args)
    if preflight_result.get("handoff_available") is False:
        parsed_outputs["handoff_available"] = False
    handoff_result = _run_downstream_handoff(args, parsed_outputs=parsed_outputs, output_dir=output_dir)
    _record_downstream_handoff_result(parsed_outputs, handoff_result)
    _write_success_outputs(
        output_dir,
        args=args,
        pipeline_source=pipeline_source,
        preflight_result=preflight_result,
        params_path=params_path,
        params_payload=params_payload,
        normalized_samplesheet=normalized_samplesheet,
        samplesheet_summary=samplesheet_summary,
        parsed_outputs=parsed_outputs,
        execution_result=execution_result,
        duration_seconds=duration_seconds,
        command_str=_nextflow_replay_command(command_str, nextflow_cwd),
    )
    print(f"Wrapper completed successfully. Output: {output_dir}")
    return 0


def _commit_validated_samplesheet(staged_samplesheet: Path, normalized_samplesheet: Path) -> None:
    if staged_samplesheet == normalized_samplesheet:
        return
    normalized_samplesheet.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_samplesheet, normalized_samplesheet)


def _check_resume_params_checksum(
    args: argparse.Namespace,
    *,
    output_dir: Path,
    params_payload: dict[str, object],
) -> None:
    if not getattr(args, "resume", False):
        return
    check_resume_params_checksum(params_payload, output_dir)


def _check_resume_samplesheet_checksum(
    args: argparse.Namespace,
    *,
    output_dir: Path,
    staged_samplesheet: Path,
) -> None:
    if not getattr(args, "resume", False):
        return
    check_resume_samplesheet_checksum(staged_samplesheet, output_dir)


def _build_nextflow_invocation(
    args: argparse.Namespace,
    output_dir: Path,
    pipeline_source: dict[str, object],
    params_path: Path,
) -> tuple[list[str], str]:
    return build_nextflow_command(
        pipeline_source=pipeline_source,
        profile=args.profile,
        params_path=params_path,
        resume=args.resume,
        work_dir=output_dir / "upstream" / "work",
        extra_configs=_build_extra_nextflow_configs(args, output_dir),
        demo=bool(getattr(args, "demo", False)),
        prokaryotic=bool(getattr(args, "prokaryotic", False)),
        rapid_quant=bool(getattr(args, "rapid_quant", False)),
        arm=bool(getattr(args, "arm", False)),
    )


def _build_extra_nextflow_configs(args: argparse.Namespace, output_dir: Path) -> list[Path]:
    configs: list[Path] = []
    profile_parts = {p.strip() for p in getattr(args, "profile", "").split(",") if p.strip()}
    arm = bool(getattr(args, "arm", False))
    if platform.system() == "Darwin" and "docker" in profile_parts:
        configs.append(_write_macos_docker_config(output_dir, arm=arm))
    for user_cfg in getattr(args, "nextflow_config", None) or []:
        # --nextflow-config accepts local paths only; Path.resolve() is intentional.
        # Nextflow's own -c flag also expects local file paths in typical use.
        configs.append(Path(user_cfg).expanduser().resolve())
    return configs


def _write_macos_docker_config(output_dir: Path, *, arm: bool = False) -> Path:
    config_path = output_dir / ".nextflow_macos_docker.config"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # --platform linux/amd64 forces qemu emulation on Apple Silicon; omit when using
    # ARM64-native containers (--arm / arm64 profile) so they run at native speed.
    platform_opts = "" if arm else "    containerOptions = '--platform linux/amd64'\n"
    docker_block = "" if arm else "docker {\n    runOptions = '--platform linux/amd64'\n}\n"
    # Autodetect CPU ceiling so users on multi-core Macs aren't capped at 4. Floor of
    # 4 preserves prior behaviour on tiny VMs. Memory/time stay conservative because
    # over-allocating memory can trigger OOM-kills (worse than throttling); users on
    # high-RAM hosts can override via --nextflow-config.
    cpus = max(4, os.cpu_count() or 4)
    config_path.write_text(
        "// macOS Docker compatibility for nf-core/rnaseq.\n"
        "process {\n"
        "    stageInMode = 'copy'\n"
        "    resourceLimits = [\n"
        f"        cpus: {cpus},\n"
        "        memory: '15.GB',\n"
        "        time: '12.h'\n"
        "    ]\n"
        + platform_opts
        + "}\n"
        + docker_block,
        encoding="utf-8",
    )
    return config_path


def _nextflow_execution_cwd(output_dir: Path) -> Path:
    return output_dir


def _nextflow_replay_command(command_str: str, cwd: Path) -> str:
    return f"cd {shlex.quote(cwd.as_posix())} && {command_str}"


def _parse_outputs_with_effective_aligner(output_dir: Path, args: argparse.Namespace) -> dict[str, object]:
    aligner = getattr(args, "aligner", "star_salmon")
    parsed = parse_outputs(
        output_dir,
        aligner=aligner,
        pseudo_aligner=getattr(args, "pseudo_aligner", None),
        skip_alignment=bool(getattr(args, "skip_alignment", False)),
        skip_quantification_merge=bool(getattr(args, "skip_quantification_merge", False)),
    )
    parsed["aligner_effective"] = aligner
    hisat2_no_quant = aligner == "hisat2" and not parsed.get("preferred_counts_tsv")
    parsed["hisat2_no_quant"] = hisat2_no_quant
    if hisat2_no_quant:
        parsed["handoff_available"] = False
    else:
        parsed.setdefault("handoff_available", bool(parsed.get("preferred_counts_tsv")))
    return parsed


def _write_success_outputs(
    output_dir: Path,
    *,
    args: argparse.Namespace,
    pipeline_source: dict[str, object],
    preflight_result: dict[str, object],
    params_path: Path,
    params_payload: dict[str, object],
    normalized_samplesheet: Path,
    samplesheet_summary: dict[str, object],
    parsed_outputs: dict[str, object],
    execution_result: dict[str, object],
    command_str: str,
    duration_seconds: float = 0,
) -> None:
    post_run_warnings: list[str] = []
    write_repro_commands(output_dir, args=args)
    try:
        write_provenance_bundle(
            output_dir,
            args=args,
            pipeline_source=pipeline_source,
            preflight_result=preflight_result,
            params_path=params_path,
            params_payload=params_payload,
            normalized_samplesheet=normalized_samplesheet,
            samplesheet_summary=samplesheet_summary,
            parsed_outputs=parsed_outputs,
            execution_result=execution_result,
            duration_seconds=duration_seconds,
            command_str=command_str,
        )
    except Exception as exc:
        post_run_warnings.append(
            f"Provenance bundle could not be written ({type(exc).__name__}: {exc}). "
            "Run --repair-bundle to regenerate missing files."
        )
    write_report(
        output_dir,
        args=args,
        pipeline_source=pipeline_source,
        preflight_result=preflight_result,
        parsed_outputs=parsed_outputs,
        command_str=command_str,
        post_run_warnings=post_run_warnings,
    )
    write_result(
        output_dir,
        args=args,
        pipeline_source=pipeline_source,
        parsed_outputs=parsed_outputs,
        command_str=command_str,
        post_run_warnings=post_run_warnings,
    )


def _run_downstream_handoff(
    args: argparse.Namespace,
    *,
    parsed_outputs: dict[str, object],
    output_dir: Path,
) -> dict[str, object] | None:
    if not getattr(args, "run_downstream", False) or getattr(args, "skip_downstream", False):
        return None
    counts = str(parsed_outputs.get("preferred_counts_tsv", "")).strip()
    if not counts or not parsed_outputs.get("handoff_available", bool(counts)):
        return None
    repro_dir = output_dir / "reproducibility"
    repro_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = repro_dir / "rnaseq_de_handoff.sh"
    handoff_path.write_text(
        "#!/usr/bin/env bash\n"
        "# Downstream rnaseq-de handoff — generated by nfcore-rnaseq-wrapper\n"
        "# Usage: CLAWBIO_REPO=/path/to/ClawBio bash rnaseq_de_handoff.sh\n"
        "set -euo pipefail\n\n"
        'if [[ -z "${CLAWBIO_REPO:-}" ]]; then\n'
        '  echo "ERROR: CLAWBIO_REPO is not set." >&2\n'
        '  echo "  CLAWBIO_REPO=/path/to/ClawBio bash ${BASH_SOURCE[0]}" >&2\n'
        "  exit 1\n"
        "fi\n\n"
        'python "${CLAWBIO_REPO}/clawbio.py" run rnaseq \\\n'
        f"  --counts {shlex.quote(counts)} \\\n"
        "  --metadata <your_metadata.csv> \\\n"
        '  --formula "~ batch + condition" \\\n'
        '  --contrast "condition,treated,control" \\\n'
        "  --output <dir>\n",
        encoding="utf-8",
    )
    if not _downstream_flags_complete(args):
        return _downstream_handoff_result(template_path=handoff_path, status="template_only")
    downstream_output = (
        Path(getattr(args, "downstream_output")).expanduser().resolve()
        if getattr(args, "downstream_output", None)
        else output_dir / "rnaseq_de"
    )
    clawbio_path = _PROJECT_ROOT / "clawbio.py"
    if not clawbio_path.exists():
        print(
            f"WARNING: clawbio.py not found at {clawbio_path}; downstream handoff skipped.",
            file=sys.stderr,
        )
        return _downstream_handoff_result(template_path=handoff_path, status="error")
    command = [
        sys.executable,
        str(clawbio_path),
        "run",
        "rnaseq",
        "--counts",
        counts,
        "--metadata",
        str(getattr(args, "metadata")),
        "--formula",
        str(getattr(args, "formula")),
        "--contrast",
        str(getattr(args, "contrast")),
        "--output",
        str(downstream_output),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=_DOWNSTREAM_HANDOFF_TIMEOUT_SECONDS,
            cwd=str(_PROJECT_ROOT),
        )
    except subprocess.TimeoutExpired:
        print(
            f"WARNING: rnaseq-de downstream handoff timed out after {_DOWNSTREAM_HANDOFF_TIMEOUT_SECONDS} seconds.",
            file=sys.stderr,
        )
        return _downstream_handoff_result(template_path=handoff_path, status="timeout")
    except OSError as exc:
        print(f"WARNING: rnaseq-de downstream handoff could not start: {exc}", file=sys.stderr)
        return _downstream_handoff_result(template_path=handoff_path, status="error")
    else:
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()
            suffix = f": {detail}" if detail else ""
            print(f"WARNING: rnaseq-de downstream handoff failed with exit code {result.returncode}{suffix}", file=sys.stderr)
            return _downstream_handoff_result(
                template_path=handoff_path,
                status="failed",
                returncode=result.returncode,
            )
    return _downstream_handoff_result(
        template_path=handoff_path,
        status="completed",
        output_dir=downstream_output,
        returncode=0,
    )


def _downstream_handoff_result(
    *,
    template_path: Path | None,
    status: str,
    output_dir: Path | None = None,
    returncode: int | None = None,
) -> dict[str, object]:
    return {
        "template_path": str(template_path) if template_path is not None else None,
        "downstream_output_dir": str(output_dir) if output_dir is not None else None,
        "downstream_status": status,
        "downstream_returncode": returncode,
    }


def _record_downstream_handoff_result(
    parsed_outputs: dict[str, object],
    handoff_result: dict[str, object] | None,
) -> None:
    if not handoff_result:
        return
    template_path = handoff_result.get("template_path")
    if template_path:
        parsed_outputs["rnaseq_de_handoff"] = str(template_path)
    status = handoff_result.get("downstream_status")
    if status:
        parsed_outputs["rnaseq_de_status"] = str(status)
    returncode = handoff_result.get("downstream_returncode")
    if returncode is not None:
        parsed_outputs["rnaseq_de_returncode"] = returncode
    output_dir = handoff_result.get("downstream_output_dir")
    if status == "completed" and output_dir:
        parsed_outputs["rnaseq_de_output_dir"] = str(output_dir)


def _downstream_flags_complete(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "metadata", None) and getattr(args, "formula", None) and getattr(args, "contrast", None))


def _write_error_result_if_safe(output_dir: Path, payload: dict[str, object]) -> None:
    error_code = payload.get("error_code")
    if error_code in {ErrorCode.OUTPUT_DIR_NOT_EMPTY, ErrorCode.OUTPUT_DIR_NOT_WRITABLE}:
        return
    if error_code == ErrorCode.INVALID_RESUME_STATE and (output_dir / "result.json").exists():
        return
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "result.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError:
        return


def _handle_skill_error(output_dir: Path, exc: SkillError) -> int:
    payload = exc.to_dict()
    _write_error_result_if_safe(output_dir, payload)
    print(json.dumps(payload, indent=2), file=sys.stderr)
    return 1


def _handle_unexpected_error(output_dir: Path, exc: Exception) -> int:
    payload = {
        "ok": False,
        "stage": "internal",
        "error_code": ErrorCode.UNEXPECTED_ERROR,
        "message": str(exc),
        "fix": "Report this as a bug. Include the traceback and command arguments.",
        "details": {
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
        },
    }
    _write_error_result_if_safe(output_dir, payload)
    print(json.dumps(payload, indent=2), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
