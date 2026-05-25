from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import requests

SKILL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_DIR.parent.parent

sys.path.insert(0, str(SKILL_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

import illumina_bridge  # noqa: E402
from illumina_bundle import (  # noqa: E402
    discover_bundle_artifacts,
    is_recognizable_illumina_bundle,
    parse_qc_metrics,
    parse_sample_sheet,
    summarize_sample_sheet,
)
from illumina_providers import ICAMetadataProvider  # noqa: E402

ORCHESTRATOR_DIR = PROJECT_ROOT / "skills" / "bio-orchestrator"
sys.path.insert(0, str(ORCHESTRATOR_DIR))
import orchestrator  # noqa: E402

_RUNNER_SPEC = importlib.util.spec_from_file_location("clawbio_runner", PROJECT_ROOT / "clawbio.py")
clawbio_runner = importlib.util.module_from_spec(_RUNNER_SPEC)
assert _RUNNER_SPEC.loader is not None
_RUNNER_SPEC.loader.exec_module(clawbio_runner)


DEMO_BUNDLE = SKILL_DIR / "demo_bundle"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses=None):
        self.headers = {}
        self.responses = list(responses or [])
        self.calls = []

    def get(self, url, timeout, headers=None):
        self.calls.append(
            {
                "url": url,
                "timeout": timeout,
                "headers": dict(headers or {}),
            }
        )
        if not self.responses:
            raise AssertionError(f"Unexpected GET request: {url}")
        return self.responses.pop(0)

BASESPACE_SAMPLE_SHEET = """[Header],
FileFormatVersion,2
RunName,Demo_Run
InstrumentPlatform,NovaSeq
AnalysisLocation,Cloud

[BCLConvert_Data]
Sample_ID,Index,Index2
TumorA_dna,AAAACCCC,GGGGTTTT
TumorB_rna,CCCCAAAA,TTTTGGGG

[Cloud_TSO500S_Data]
Sample_ID,Sample_Type,Pair_ID,Sample_Feature,Index_ID,Index,Index2
TumorA_dna,DNA,TumorA,HRD,UDP0001,AAAACCCC,GGGGTTTT
TumorB_rna,RNA,TumorB,,UDP0002,CCCCAAAA,TTTTGGGG

[Cloud_Data]
Sample_ID,ProjectName,LibraryName,LibraryPrepKitName,IndexAdapterKitName
TumorA_dna,DemoProject,TumorA_dna_AAAACCCC_GGGGTTTT,TSO500_v2,TSO500v2_ForwardOrientation
TumorB_rna,DemoProject,TumorB_rna_CCCCAAAA_TTTTGGGG,TSO500_v2,TSO500v2_ForwardOrientation
"""

METRICS_OUTPUT_TSV = """DRAGEN TruSight Oncology 500 v2.6.2 Analysis Software - Metrics Output

[Header]
Output Date\t2025-11-25
Output Time\t10:24:49
Workflow Version\t2.6.2.4

[Run QC Metrics]
Metric (UOM)\tLSL Guideline\tUSL Guideline\tValue
PCT_PF_READS (%)\t55.0\tNA\t77.5
PCT_Q30_R1 (%)\t80.0\tNA\t92.8
PCT_Q30_R2 (%)\t80.0\tNA\t92.3

[Analysis Status]
\tTumorA_dna\tTumorB_rna
COMPLETED_ALL_STEPS\tTRUE\tTRUE
FAILED_STEPS\tNA\tNA
STEPS_NOT_EXECUTED\tNA\tNA
"""


@pytest.fixture
def copied_bundle(tmp_path):
    dest = tmp_path / "bundle"
    shutil.copytree(DEMO_BUNDLE, dest)
    return dest


def test_discover_bundle_artifacts_success(copied_bundle):
    artifacts = discover_bundle_artifacts(copied_bundle)
    assert artifacts.sample_sheet_path.name == "SampleSheet.csv"
    assert artifacts.vcf_path.name == "demo.vcf"
    assert artifacts.qc_path.name == "qc_metrics.json"


def test_discover_bundle_artifacts_explicit_override_precedence(copied_bundle, tmp_path):
    alt_vcf = tmp_path / "manual.vcf"
    alt_vcf.write_text("##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    artifacts = discover_bundle_artifacts(copied_bundle, vcf_override=alt_vcf)
    assert artifacts.vcf_path == alt_vcf.resolve()


def test_discover_bundle_missing_sample_sheet_fails(copied_bundle):
    (copied_bundle / "SampleSheet.csv").unlink()
    with pytest.raises(FileNotFoundError):
        discover_bundle_artifacts(copied_bundle)


def test_discover_bundle_missing_vcf_fails(copied_bundle):
    (copied_bundle / "demo.vcf").unlink()
    with pytest.raises(FileNotFoundError):
        discover_bundle_artifacts(copied_bundle)


def test_parse_sample_sheet_extracts_rows():
    rows = parse_sample_sheet(DEMO_BUNDLE / "SampleSheet.csv")
    assert len(rows) == 2
    assert rows[0]["sample_id"] == "DEMO_SAMPLE_01"
    assert rows[1]["sample_project"] == "ClawBioDemo"


def test_parse_sample_sheet_merges_basespace_sections(tmp_path):
    sample_sheet = tmp_path / "samplesheet.csv"
    sample_sheet.write_text(BASESPACE_SAMPLE_SHEET, encoding="utf-8")
    rows = parse_sample_sheet(sample_sheet)
    assert len(rows) == 2
    assert rows[0]["sample_id"] == "TumorA_dna"
    assert rows[0]["sample_name"] == "TumorA"
    assert rows[0]["sample_type"] == "DNA"
    assert rows[0]["sample_feature"] == "HRD"
    assert rows[0]["library_name"] == "TumorA_dna_AAAACCCC_GGGGTTTT"
    assert rows[1]["sample_type"] == "RNA"
    assert rows[1]["sample_project"] == "DemoProject"


def test_parse_qc_metrics_json_normalizes_fixture():
    qc = parse_qc_metrics(DEMO_BUNDLE / "qc_metrics.json")
    assert qc["run_id"] == "demo-run-001"
    assert qc["percent_q30"] == 92.7
    assert qc["instrument"] == "NovaSeq X Plus"


def test_parse_qc_metrics_tsv_normalizes_metrics_output(tmp_path):
    metrics_tsv = tmp_path / "MetricsOutput.tsv"
    metrics_tsv.write_text(METRICS_OUTPUT_TSV, encoding="utf-8")
    qc = parse_qc_metrics(metrics_tsv)
    assert qc["analysis_software"] == "DRAGEN TruSight Oncology 500 v2.6.2 Analysis Software - Metrics Output"
    assert qc["workflow_version"] == "2.6.2.4"
    assert qc["percent_pf_reads"] == 77.5
    assert qc["percent_q30"] == 92.55
    assert qc["completed_samples"] == 2
    assert qc["reported_sample_count"] == 2


def test_parse_qc_metrics_malformed_json_raises(tmp_path):
    bad_qc = tmp_path / "bad_qc.json"
    bad_qc.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(ValueError):
        parse_qc_metrics(bad_qc)


def test_discover_bundle_prefers_primary_result_vcf(tmp_path):
    bundle = tmp_path / "bundle"
    (bundle / "Results" / "TumorA" / "TumorA_dna").mkdir(parents=True)
    (bundle / "Logs_Intermediates" / "TumorA" / "TumorA_dna").mkdir(parents=True)
    (bundle / "samplesheet.csv").write_text(BASESPACE_SAMPLE_SHEET, encoding="utf-8")
    (bundle / "MetricsOutput.tsv").write_text(METRICS_OUTPUT_TSV, encoding="utf-8")
    preferred_vcf = bundle / "Results" / "TumorA" / "TumorA_dna" / "TumorA_dna.hard-filtered.vcf"
    preferred_vcf.write_text("##fileformat=VCFv4.2\n", encoding="utf-8")
    (bundle / "Results" / "TumorA" / "TumorA_dna" / "TumorA_dna.cnv.vcf").write_text(
        "##fileformat=VCFv4.2\n",
        encoding="utf-8",
    )
    (bundle / "Logs_Intermediates" / "TumorA" / "TumorA_dna" / "TumorA_dna.hard-filtered.vcf.gz").write_text(
        "placeholder",
        encoding="utf-8",
    )

    artifacts = discover_bundle_artifacts(bundle)
    assert artifacts.vcf_path == preferred_vcf.resolve()


def test_build_summary_and_data_is_deterministic(copied_bundle):
    artifacts = discover_bundle_artifacts(copied_bundle)
    sample_rows = parse_sample_sheet(artifacts.sample_sheet_path)
    sample_summary = summarize_sample_sheet(sample_rows)
    qc_summary = parse_qc_metrics(artifacts.qc_path)
    provider = ICAMetadataProvider(api_key="")
    metadata = provider.enrich(
        bundle_dir=copied_bundle,
        project_id="ica-project-demo",
        run_id="ica-run-demo",
        allow_mock=True,
    )
    merged_rows, merge = illumina_bridge.merge_sample_metadata(sample_rows, metadata)
    hints = illumina_bridge.build_downstream_routing_hints(
        vcf_path=artifacts.vcf_path,
        sample_count=sample_summary["sample_count"],
    )
    summary1, data1 = illumina_bridge.build_summary_and_data(
        bundle=artifacts,
        sample_rows=merged_rows,
        sample_summary=sample_summary,
        qc_summary=qc_summary,
        metadata_result=metadata,
        metadata_merge=merge,
        downstream_hints=hints,
    )
    summary2, data2 = illumina_bridge.build_summary_and_data(
        bundle=artifacts,
        sample_rows=merged_rows,
        sample_summary=sample_summary,
        qc_summary=qc_summary,
        metadata_result=metadata,
        metadata_merge=merge,
        downstream_hints=hints,
    )
    assert summary1 == summary2
    assert data1 == data2


def test_ica_provider_merges_project_run_and_sample_metadata(copied_bundle):
    provider = ICAMetadataProvider(api_key="")
    result = provider.enrich(
        bundle_dir=copied_bundle,
        project_id="ica-project-demo",
        run_id="ica-run-demo",
        allow_mock=True,
    )
    rows = parse_sample_sheet(copied_bundle / "SampleSheet.csv")
    merged_rows, merge = illumina_bridge.merge_sample_metadata(rows, result)
    assert result.status == "mocked-demo"
    assert result.project["name"] == "Demo ICA Project"
    assert result.run["status"] == "SUCCEEDED"
    assert merge["samples_enriched"] == 2
    assert merged_rows[0]["ica_sample_id"] == "ica-sample-001"


def test_ica_provider_missing_api_key_yields_warning(copied_bundle):
    provider = ICAMetadataProvider(api_key="")
    assert provider.api_key is None
    result = provider.enrich(
        bundle_dir=copied_bundle,
        project_id="ica-project-demo",
        run_id="ica-run-demo",
        allow_mock=False,
    )
    assert result.status == "warning"
    assert "ILLUMINA_ICA_API_KEY" in result.warnings[0]


def test_ica_provider_network_failure_yields_warning(copied_bundle, monkeypatch):
    provider = ICAMetadataProvider(api_key="test-key")

    def raise_request_error(endpoint: str):
        raise requests.RequestException("network down")

    monkeypatch.setattr(provider, "_fetch_json", raise_request_error)
    result = provider.enrich(
        bundle_dir=copied_bundle,
        project_id="ica-project-demo",
        run_id="ica-run-demo",
    )
    assert result.status == "warning"
    assert "network down" in result.warnings[0]


def test_ica_provider_does_not_store_api_key_in_session_headers():
    session = FakeSession()
    provider = ICAMetadataProvider(api_key="super-secret-key", session=session)
    assert provider.api_key == "super-secret-key"
    assert session.headers["Accept"] == "application/vnd.illumina.v3+json"
    assert "X-API-Key" not in session.headers


def test_ica_provider_fetch_json_sends_api_key_per_request():
    session = FakeSession([FakeResponse({"id": "project-1"})])
    provider = ICAMetadataProvider(api_key="super-secret-key", session=session)
    payload = provider._fetch_json("/api/projects/project-1")
    assert payload["id"] == "project-1"
    assert session.calls[0]["headers"]["X-API-Key"] == "super-secret-key"


def test_ica_provider_repr_redacts_api_key():
    provider = ICAMetadataProvider(api_key="super-secret-key")
    rendered = repr(provider)
    assert "super-secret-key" not in rendered
    assert "has_api_key=True" in rendered


def test_ica_provider_invalid_base_url_falls_back_with_warning(copied_bundle):
    session = FakeSession(
        [
            FakeResponse({"id": "project-1", "name": "Demo Project", "status": "READY"}),
            FakeResponse({"id": "run-1", "name": "Demo Run", "status": "SUCCEEDED", "samples": []}),
        ]
    )
    provider = ICAMetadataProvider(
        api_key="test-key",
        base_url="http://example.com/ica/rest",
        session=session,
    )
    assert provider.base_url == "https://ica.illumina.com/ica/rest"
    result = provider.enrich(
        bundle_dir=copied_bundle,
        project_id="project-1",
        run_id="run-1",
    )
    assert result.status == "enriched"
    assert any("ILLUMINA_ICA_BASE_URL" in warning for warning in result.warnings)


def test_ica_provider_accepts_trusted_illumina_base_url():
    session = FakeSession()
    provider = ICAMetadataProvider(
        api_key="test-key",
        base_url="https://tenant.illumina.com/ica/rest",
        session=session,
    )
    assert provider.base_url == "https://tenant.illumina.com/ica/rest"
    assert provider._initialization_warnings == []


def test_import_bundle_demo_creates_standard_outputs(tmp_path):
    output_dir = tmp_path / "demo_output"
    result = illumina_bridge.import_bundle(
        bundle_dir=DEMO_BUNDLE,
        output_dir=output_dir,
        metadata_provider_name="none",
        allow_mock_metadata=True,
    )
    assert result["summary"]["platform"] == "illumina"
    assert (output_dir / "report.md").exists()
    assert (output_dir / "result.json").exists()
    assert (output_dir / "tables" / "sample_manifest.csv").exists()
    assert (output_dir / "reproducibility" / "commands.sh").exists()


def test_import_bundle_with_basespace_style_inputs_creates_standard_outputs(tmp_path):
    bundle = tmp_path / "basespace_bundle"
    (bundle / "Results" / "TumorA" / "TumorA_dna").mkdir(parents=True)
    (bundle / "samplesheet.csv").write_text(BASESPACE_SAMPLE_SHEET, encoding="utf-8")
    (bundle / "MetricsOutput.tsv").write_text(METRICS_OUTPUT_TSV, encoding="utf-8")
    (bundle / "Results" / "TumorA" / "TumorA_dna" / "TumorA_dna.hard-filtered.vcf").write_text(
        "##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "basespace_output"
    result = illumina_bridge.import_bundle(
        bundle_dir=bundle,
        output_dir=output_dir,
        metadata_provider_name="none",
        allow_mock_metadata=False,
    )
    assert result["summary"]["platform"] == "illumina"
    assert result["summary"]["sample_count"] == 2
    assert (output_dir / "report.md").exists()
    manifest_rows = list(csv.DictReader((output_dir / "tables" / "sample_manifest.csv").open(encoding="utf-8")))
    assert manifest_rows[0]["sample_type"] == "DNA"
    assert manifest_rows[0]["library_name"] == "TumorA_dna_AAAACCCC_GGGGTTTT"


def test_clawbio_run_illumina_input_bundle_completes(tmp_path):
    output_dir = tmp_path / "cli_output"
    proc = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "clawbio.py"),
            "run",
            "illumina",
            "--input",
            str(DEMO_BUNDLE),
            "--output",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (output_dir / "report.md").exists()
    payload = json.loads((output_dir / "result.json").read_text())
    assert payload["data"]["platform"] == "illumina"


def test_orchestrator_routes_illumina_keywords():
    skill, _ = orchestrator.detect_skill_with_hint_from_query(
        "Import this Illumina DRAGEN sample sheet bundle and add ICA metadata"
    )
    assert skill == "illumina-bridge"


def test_orchestrator_routes_illumina_bundle_directory():
    assert is_recognizable_illumina_bundle(DEMO_BUNDLE)
    assert orchestrator.detect_skill_from_file(DEMO_BUNDLE) == "illumina-bridge"


def test_security_filter_rejects_unsupported_flags_for_illumina(tmp_path):
    output_dir = tmp_path / "secure_output"
    result = clawbio_runner.run_skill(
        skill_name="illumina",
        demo=True,
        output_dir=str(output_dir),
        extra_args=["--bogus", "nope", "--metadata-provider", "none"],
    )
    assert result["success"] is True
    assert (output_dir / "result.json").exists()


def test_sample_manifest_csv_contains_expected_columns(tmp_path):
    output_dir = tmp_path / "manifest_output"
    illumina_bridge.import_bundle(
        bundle_dir=DEMO_BUNDLE,
        output_dir=output_dir,
        metadata_provider_name="ica",
        ica_project_id="ica-project-demo",
        ica_run_id="ica-run-demo",
        allow_mock_metadata=True,
    )
    manifest = output_dir / "tables" / "sample_manifest.csv"
    with manifest.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["sample_id"] == "DEMO_SAMPLE_01"
    assert rows[0]["ica_sample_id"] == "ica-sample-001"
