from __future__ import annotations

import json
import shlex
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from clawbio.common.portable_commands import write_portable_commands_sh
from clawbio.common.report import generate_report_footer, generate_report_header, write_result_json

_SKILL_DIR = Path(__file__).resolve().parent
if str(_SKILL_DIR) in sys.path:
    sys.path.remove(str(_SKILL_DIR))
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_bare_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and _SKILL_DIR not in module_file.parents and module_file != _SKILL_DIR / f"{name}.py":
            sys.modules.pop(name, None)


_purge_foreign_bare_modules("schemas")

from schemas import SKILL_ALIAS, SKILL_DIR, SKILL_NAME, SKILL_VERSION

_REPRO_PATH_FLAGS = (
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
    "bowtie2_index",
    "salmon_index",
    "kallisto_index",
    "sortmerna_index",
    "multiqc_config",
    "multiqc_logo",
    "multiqc_methods_description",
    "ribo_database_manifest",
    "kraken_db",
    "sylph_db",
    "sylph_taxonomy",
    "bbsplit_fasta_list",
    "bbsplit_index",
    "igenomes_base",
)
_OPTIONAL_VALUE_FLAGS = (
    "pseudo_aligner",
    "trimmer",
    "genome",
    "ribo_removal_tool",
    "umi_dedup_tool",
    "umitools_bc_pattern",
    "umitools_bc_pattern2",
    "umitools_umi_separator",
    "umitools_extract_method",
    "umi_discard_read",
    "umitools_grouping_method",
    "stranded_threshold",
    "unstranded_threshold",
    "min_mapped_reads",
    "pseudo_aligner_kmer_size",
    "extra_trimgalore_args",
    "extra_fastp_args",
    "extra_fqlint_args",
    "extra_salmon_quant_args",
    "extra_kallisto_quant_args",
    "min_trimmed_reads",
    "seq_center",
    "seq_platform",
    "salmon_quant_libtype",
    "kallisto_quant_fraglen",
    "kallisto_quant_fraglen_sd",
    "featurecounts_feature_type",
    "featurecounts_group_type",
    "gtf_extra_attributes",
    "gtf_group_features",
    "rseqc_modules",
    "extra_star_align_args",
    "extra_bowtie2_align_args",
    "hisat2_build_memory",
    "gpu_container_options",
    "email",
    "multiqc_title",
    "contaminant_screening",
    "contaminant_screening_input",
    "bracken_precision",
    "rsem_extra_args",
    "metadata",
    "formula",
    "contrast",
    "downstream_output",
    "publish_dir_mode",
    "email_on_fail",
)
_BOOLEAN_FLAGS = (
    "skip_quantification_merge",
    "skip_trimming",
    "skip_alignment",
    "skip_pseudo_alignment",
    "skip_markduplicates",
    "skip_bigwig",
    "skip_stringtie",
    "skip_fastqc",
    "skip_dupradar",
    "skip_qualimap",
    "skip_rseqc",
    "skip_biotype_qc",
    "skip_deseq2_qc",
    "skip_multiqc",
    "skip_qc",
    "skip_linting",
    "skip_gtf_filter",
    "skip_gtf_transcript_filter",
    "save_reference",
    "save_trimmed",
    "save_align_intermeds",
    "save_unaligned",
    "save_merged_fastq",
    "save_non_ribo_reads",
    "save_umi_intermeds",
    "save_bbsplit_reads",
    "remove_ribo_rna",
    "with_umi",
    "skip_umi_extract",
    "umitools_dedup_stats",
    "umitools_dedup_primary_only",
    "gencode",
    "star_ignore_sjdbgtf",
    "bam_csi_index",
    "stringtie_ignore_gtf",
    "gffread_transcript_fasta",
    "arm",
    "prokaryotic",
    "rapid_quant",
    "enable_preseq",
    "save_kraken_assignments",
    "save_kraken_unassigned",
    "use_rustqc",
    "use_parabricks_star",
    "use_sentieon_star",
    "use_gpu_ribodetector",
    "run_downstream",
    "skip_downstream",
    "skip_bbsplit",
)

_PORTABILITY_NOTICE = """\

# ── Portability notice ────────────────────────────────────────────────────────
# Input paths in samplesheet.valid.csv are absolute (required by Nextflow).
# This covers FASTQ paths for fresh runs and BAM paths for reprocessing runs.
# Before replaying on a different machine:
#
#   1. Remap FASTQ paths:
#        python reproducibility/remap_paths.py --old /original/prefix --new /new/prefix
#
#   2. Update the --output path above if the output directory changed:
#        python reproducibility/remap_paths.py --output-dir /new/output/dir
#
#   3. Verify everything:
#        python reproducibility/remap_paths.py --verify
#
# If ClawBio is installed at a non-standard path on this machine:
#   CLAWBIO_REPO=/path/to/ClawBio bash reproducibility/commands.sh
"""

_CLAWBIO_REPO_FALLBACK = (
    'if [[ ! -d "$REPO_ROOT/skills" ]]; then\n'
    '  echo "ERROR: Could not locate repo root (no skills/ directory found)" >&2\n'
    '  exit 1\n'
    'fi'
)
_CLAWBIO_REPO_FALLBACK_PATCHED = (
    'if [[ ! -d "$REPO_ROOT/skills" ]]; then\n'
    '  if [[ -n "${CLAWBIO_REPO:-}" && -d "${CLAWBIO_REPO}/skills" ]]; then\n'
    '    REPO_ROOT="$CLAWBIO_REPO"\n'
    '  else\n'
    '    echo "ERROR: Could not locate repo root (no skills/ directory found)" >&2\n'
    '    echo "If ClawBio is installed elsewhere, set CLAWBIO_REPO:" >&2\n'
    '    echo "  CLAWBIO_REPO=/path/to/ClawBio bash commands.sh" >&2\n'
    '    exit 1\n'
    '  fi\n'
    'fi'
)


def write_report(
    output_dir: Path,
    *,
    args,
    pipeline_source: dict[str, object],
    preflight_result: dict[str, object],
    parsed_outputs: dict[str, object],
    command_str: str,
    post_run_warnings: list[str] | None = None,
) -> Path:
    lines = build_report_lines(
        output_dir,
        args=args,
        pipeline_source=pipeline_source,
        preflight_result=preflight_result,
        parsed_outputs=parsed_outputs,
        command_str=command_str,
        post_run_warnings=post_run_warnings,
    )
    report_path = output_dir / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def build_report_lines(
    output_dir: Path,
    *,
    args,
    pipeline_source: dict[str, object],
    preflight_result: dict[str, object],
    parsed_outputs: dict[str, object],
    command_str: str,
    post_run_warnings: list[str] | None = None,
) -> list[str]:
    header = generate_report_header(
        "nf-core/rnaseq Wrapper Report",
        SKILL_NAME,
        extra_metadata={
            "Aligner": str(getattr(args, "aligner", "")),
            "Profile": str(getattr(args, "profile", "")),
            "Pipeline source": str(pipeline_source.get("source_kind", "")),
            "Pipeline ref": str(pipeline_source.get("resolved_version", "")),
        },
    )
    warnings = preflight_result.get("warnings", [])
    warning_text = "none" if not warnings else ", ".join(str(w) for w in warnings)
    commands_sh = output_dir / "reproducibility" / "commands.sh"
    lines: list[str] = [
        header,
        "## Summary",
        "",
        f"- Aligner: `{getattr(args, 'aligner', '')}`",
        f"- Pseudo-aligner: `{getattr(args, 'pseudo_aligner', None) or 'none'}`",
        f"- Trimmer: `{getattr(args, 'trimmer', '')}`",
        f"- Samples: `{parsed_outputs.get('samples_detected', 0)}`",
        f"- Strandedness mode: `{_strandedness_summary(preflight_result)}`",
        "",
        "## Preflight",
        "",
        f"- Java: `{preflight_result.get('java', {}).get('version', '')}`",
        f"- Nextflow: `{preflight_result.get('nextflow', {}).get('version', '')}`",
        f"- Backend profile: `{getattr(args, 'profile', '')}`",
        f"- Warnings: {warning_text}",
        "",
        "## Outputs",
        "",
        f"- Preferred counts TSV: `{_value_or(parsed_outputs.get('preferred_counts_tsv', ''), 'not available')}`",
        f"- SummarizedExperiment RDS: `{_value_or(parsed_outputs.get('rds_file', ''), 'not available')}`",
        f"- TPM TSV: `{_value_or(parsed_outputs.get('tpm_tsv', ''), 'not available')}`",
        f"- MultiQC report: `{_value_or(parsed_outputs.get('multiqc_report', ''), 'not found')}`",
        f"- Pipeline info: `{_value_or(parsed_outputs.get('pipeline_info_dir', ''), 'not found')}`",
        f"- Per-sample mode: `{str(bool(parsed_outputs.get('skip_quantification_merge', False))).lower()}`",
        f"- HISAT2 no-quant mode: `{str(bool(parsed_outputs.get('hisat2_no_quant', False))).lower()}`",
        "",
        "## Reproducibility",
        "",
        f"- Command: `{command_str}`",
        f"- Repro bundle: `{output_dir / 'reproducibility'}`",
        f"- Replay: `CLAWBIO_REPO=<repo_root> bash {shlex.quote(str(commands_sh))}`",
        "",
        *_build_handoff_lines(parsed_outputs, args=args),
    ]
    if post_run_warnings:
        lines += [
            "## Post-run Warnings",
            "",
            *[f"- {w}" for w in post_run_warnings],
            "",
        ]
    lines.append(generate_report_footer())
    return lines


def _build_handoff_lines(parsed_outputs: dict[str, object] | str, *, args=None) -> list[str]:
    if isinstance(parsed_outputs, str):
        parsed_outputs = {"preferred_counts_tsv": parsed_outputs, "handoff_available": bool(parsed_outputs)}
    counts = str(parsed_outputs.get("preferred_counts_tsv", ""))
    if parsed_outputs.get("handoff_available") and counts:
        quoted_counts = shlex.quote(counts)
        metadata = getattr(args, "metadata", None) if args is not None else None
        formula = getattr(args, "formula", None) if args is not None else None
        contrast = getattr(args, "contrast", None) if args is not None else None
        downstream_output = getattr(args, "downstream_output", None) if args is not None else None
        metadata_arg = shlex.quote(str(metadata)) if metadata else "<your_metadata.csv>"
        formula_arg = shlex.quote(str(formula)) if formula else '"~ batch + condition"'
        contrast_arg = shlex.quote(str(contrast)) if contrast else '"condition,treated,control"'
        output_arg = shlex.quote(str(downstream_output)) if downstream_output else "<dir>"
        return [
            "## Next Steps",
            "",
            "```bash",
            '"${CLAWBIO_REPO}/clawbio.py" run rnaseq \\',
            f"  --counts {quoted_counts} \\",
            f"  --metadata {metadata_arg} \\",
            f"  --formula {formula_arg} \\",
            f"  --contrast {contrast_arg} \\",
            f"  --output {output_arg}",
            "```",
            "",
        ]
    if parsed_outputs.get("hisat2_no_quant"):
        detail = "HISAT2 mode does not produce merged quantification counts for rnaseq downstream analysis."
    elif parsed_outputs.get("skip_quantification_merge"):
        detail = "Per-sample quantification mode does not produce the merged count matrix required by rnaseq downstream analysis."
    else:
        detail = "No preferred merged count matrix was found for rnaseq downstream analysis."
    return ["## Next Steps", "", f"- {detail}", ""]


def write_repro_commands(output_dir: Path, *, args) -> None:
    repro_dir = output_dir / "reproducibility"
    command_args = build_repro_command_args(output_dir, args=args)
    write_portable_commands_sh(
        repro_dir,
        skill_name=SKILL_NAME,
        # Phase 4 owns creating this orchestrator entrypoint; Phase 3 records
        # the planned replay target so generated bundles remain stable.
        script_name="nfcore_rnaseq_wrapper.py",
        args=command_args,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    commands_sh = repro_dir / "commands.sh"
    _patch_commands_sh_repo_fallback(commands_sh)
    if not getattr(args, "demo", False):
        with commands_sh.open("a", encoding="utf-8") as fh:
            fh.write(_PORTABILITY_NOTICE)
    _write_remap_script(repro_dir)


def build_repro_command_args(output_dir: Path, *, args) -> dict[str, str | None]:
    command_args: dict[str, str | None] = {
        "--output": output_dir.as_posix(),
        "--aligner": getattr(args, "aligner", ""),
        "--profile": getattr(args, "profile", ""),
        "--pipeline-version": getattr(args, "pipeline_version", ""),
    }
    if getattr(args, "pipeline_local", None):
        command_args["--pipeline-local"] = Path(getattr(args, "pipeline_local")).expanduser().resolve().as_posix()
    if getattr(args, "demo", False):
        command_args["--demo"] = None
    elif not getattr(args, "_noinput", False):
        # _noinput: self-contained test profile supplies params.input; write neither --input nor --demo.
        # For normal runs, reference the bundled samplesheet copy so the replay command is
        # portable: commands.sh lives in reproducibility/ and ${SCRIPT_DIR} resolves to it.
        command_args["--input"] = "${SCRIPT_DIR}/samplesheet.valid.csv"
    for field in _OPTIONAL_VALUE_FLAGS:
        value = getattr(args, field, None)
        if value is not None and value != "":
            command_args[f"--{field.replace('_', '-')}"] = str(value)
    for field in _BOOLEAN_FLAGS:
        if getattr(args, field, False):
            command_args[f"--{field.replace('_', '-')}"] = None
    if getattr(args, "resume", False):
        command_args["--resume"] = None
    _deseq2_vst = getattr(args, "deseq2_vst", None)
    if _deseq2_vst is False:
        command_args["--no-deseq2-vst"] = None
    elif _deseq2_vst is True:
        command_args["--deseq2-vst"] = None
    for field in _REPRO_PATH_FLAGS:
        value = getattr(args, field, None)
        if value:
            if "://" in str(value):
                command_args[f"--{field.replace('_', '-')}"] = str(value)
            else:
                command_args[f"--{field.replace('_', '-')}"] = Path(value).expanduser().resolve().as_posix()
    user_configs = getattr(args, "nextflow_config", None) or []
    if user_configs:
        command_args["--nextflow-config"] = [Path(c).expanduser().resolve().as_posix() for c in user_configs]
    return command_args


def write_result(
    output_dir: Path,
    *,
    args,
    pipeline_source: dict[str, object],
    parsed_outputs: dict[str, object],
    command_str: str,
    post_run_warnings: list[str] | None = None,
) -> Path:
    output_artifacts = build_output_artifacts(parsed_outputs)
    return write_result_json(
        output_dir,
        skill=SKILL_ALIAS,
        version=SKILL_VERSION,
        summary=build_result_summary(
            args=args,
            pipeline_source=pipeline_source,
            parsed_outputs=parsed_outputs,
            output_artifacts=output_artifacts,
            post_run_warnings=post_run_warnings,
        ),
        data=build_result_data(parsed_outputs=parsed_outputs, output_artifacts=output_artifacts, command_str=command_str),
    )


def build_output_artifacts(parsed_outputs: dict[str, object]) -> dict[str, object]:
    return dict(parsed_outputs)


def build_result_summary(
    *,
    args,
    pipeline_source: dict[str, object],
    parsed_outputs: dict[str, object],
    output_artifacts: dict[str, object],
    post_run_warnings: list[str] | None = None,
) -> dict[str, object]:
    return {
        "aligner": getattr(args, "aligner", ""),
        "aligner_effective": parsed_outputs.get("aligner_effective", ""),
        "pseudo_aligner": getattr(args, "pseudo_aligner", None),
        "pipeline_source_kind": pipeline_source.get("source_kind", ""),
        "pipeline_version_or_commit": pipeline_source.get("resolved_version", ""),
        "profile": getattr(args, "profile", ""),
        "resume_used": bool(getattr(args, "resume", False)),
        "preferred_counts_tsv": parsed_outputs.get("preferred_counts_tsv", ""),
        "rds_file": parsed_outputs.get("rds_file", ""),
        "multiqc_report": parsed_outputs.get("multiqc_report", ""),
        "handoff_available": parsed_outputs.get("handoff_available", False),
        "samples_detected": parsed_outputs.get("samples_detected", 0),
        "skip_quantification_merge": parsed_outputs.get("skip_quantification_merge", False),
        "hisat2_no_quant": parsed_outputs.get("hisat2_no_quant", False),
        "output_artifacts": output_artifacts,
        "post_run_warnings": list(post_run_warnings) if post_run_warnings else [],
    }


def build_result_data(
    *,
    parsed_outputs: dict[str, object],
    output_artifacts: dict[str, object],
    command_str: str,
) -> dict[str, object]:
    return {
        "canonical_skill_name": SKILL_NAME,
        "cli_alias": SKILL_ALIAS,
        "command": command_str,
        "output_artifacts": output_artifacts,
        "outputs": parsed_outputs,
    }


def write_check_result(output_dir: Path, payload: dict[str, object]) -> Path:
    path = output_dir / "check_result.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _patch_commands_sh_repo_fallback(commands_sh: Path) -> None:
    if not commands_sh.exists():
        return
    content = commands_sh.read_text(encoding="utf-8")
    if _CLAWBIO_REPO_FALLBACK not in content:
        return
    commands_sh.write_text(content.replace(_CLAWBIO_REPO_FALLBACK, _CLAWBIO_REPO_FALLBACK_PATCHED), encoding="utf-8")


def _write_remap_script(repro_dir: Path) -> None:
    repro_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SKILL_DIR / "remap_paths.py", repro_dir / "remap_paths.py")


def _value_or(value: object, fallback: str) -> str:
    return str(value) if value else fallback


def _strandedness_summary(preflight_result: dict[str, object]) -> str:
    samplesheet = preflight_result.get("samplesheet", {})
    counts = samplesheet.get("strandedness_counts", {}) if isinstance(samplesheet, dict) else {}
    if not counts:
        return "not recorded"
    return ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
