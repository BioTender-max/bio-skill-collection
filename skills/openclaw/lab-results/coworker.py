# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"""
Anthropic Health Stack - Lab Results Interpretation Coworker
-------------------------------------------------------------
Implements Claude's lab results interpretation capability for
patient-facing explanations and clinical decision support.

Based on: https://www.anthropic.com/news/healthcare-life-sciences
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


class ResultStatus(Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"


class LabCategory(Enum):
    CBC = "complete_blood_count"
    BMP = "basic_metabolic_panel"
    CMP = "comprehensive_metabolic_panel"
    LIPID = "lipid_panel"
    THYROID = "thyroid_panel"
    LFT = "liver_function"
    CARDIAC = "cardiac_markers"
    COAGULATION = "coagulation"
    URINALYSIS = "urinalysis"


class LabResultsCoworker:
    """
    Claude-style coworker for lab results interpretation.
    Provides patient-friendly explanations with clinical context.
    """

    def __init__(self) -> None:
        self.reference_ranges = self._load_reference_ranges()
        self.clinical_context = self._load_clinical_context()

    def _load_reference_ranges(self) -> Dict[str, Dict[str, Any]]:
        """Load standard reference ranges for common lab tests."""
        return {
            # CBC
            "WBC": {"low": 4.5, "high": 11.0, "unit": "K/uL", "critical_low": 2.0, "critical_high": 30.0},
            "RBC": {"low": 4.5, "high": 5.5, "unit": "M/uL", "critical_low": 2.5, "critical_high": 7.0},
            "Hemoglobin": {"low": 12.0, "high": 17.5, "unit": "g/dL", "critical_low": 7.0, "critical_high": 20.0},
            "Hematocrit": {"low": 36.0, "high": 50.0, "unit": "%", "critical_low": 20.0, "critical_high": 60.0},
            "Platelets": {"low": 150, "high": 400, "unit": "K/uL", "critical_low": 50, "critical_high": 1000},

            # BMP
            "Glucose": {"low": 70, "high": 100, "unit": "mg/dL", "critical_low": 40, "critical_high": 500},
            "BUN": {"low": 7, "high": 20, "unit": "mg/dL", "critical_low": None, "critical_high": 100},
            "Creatinine": {"low": 0.7, "high": 1.3, "unit": "mg/dL", "critical_low": None, "critical_high": 10.0},
            "Sodium": {"low": 136, "high": 145, "unit": "mEq/L", "critical_low": 120, "critical_high": 160},
            "Potassium": {"low": 3.5, "high": 5.0, "unit": "mEq/L", "critical_low": 2.5, "critical_high": 6.5},

            # Lipid Panel
            "Total Cholesterol": {"low": 0, "high": 200, "unit": "mg/dL", "critical_low": None, "critical_high": 400},
            "LDL": {"low": 0, "high": 100, "unit": "mg/dL", "critical_low": None, "critical_high": None},
            "HDL": {"low": 40, "high": 999, "unit": "mg/dL", "critical_low": None, "critical_high": None},
            "Triglycerides": {"low": 0, "high": 150, "unit": "mg/dL", "critical_low": None, "critical_high": 1000},

            # Thyroid
            "TSH": {"low": 0.4, "high": 4.0, "unit": "mIU/L", "critical_low": 0.01, "critical_high": 100},
            "Free T4": {"low": 0.8, "high": 1.8, "unit": "ng/dL", "critical_low": None, "critical_high": None},

            # LFT
            "AST": {"low": 0, "high": 40, "unit": "U/L", "critical_low": None, "critical_high": 1000},
            "ALT": {"low": 0, "high": 56, "unit": "U/L", "critical_low": None, "critical_high": 1000},
            "Alkaline Phosphatase": {"low": 44, "high": 147, "unit": "U/L", "critical_low": None, "critical_high": None},
            "Total Bilirubin": {"low": 0.1, "high": 1.2, "unit": "mg/dL", "critical_low": None, "critical_high": 15.0},

            # Cardiac
            "Troponin I": {"low": 0, "high": 0.04, "unit": "ng/mL", "critical_low": None, "critical_high": 0.4},
            "BNP": {"low": 0, "high": 100, "unit": "pg/mL", "critical_low": None, "critical_high": 1000},

            # HbA1c
            "HbA1c": {"low": 4.0, "high": 5.7, "unit": "%", "critical_low": None, "critical_high": 14.0},
        }

    def _load_clinical_context(self) -> Dict[str, Dict[str, str]]:
        """Load clinical context for result interpretation."""
        return {
            "WBC": {
                "high": "May indicate infection, inflammation, or stress response",
                "low": "May indicate bone marrow issues or immunosuppression",
                "description": "White blood cells help fight infection",
            },
            "Hemoglobin": {
                "high": "May indicate dehydration or polycythemia",
                "low": "May indicate anemia; discuss with your doctor",
                "description": "Carries oxygen throughout your body",
            },
            "Glucose": {
                "high": "May indicate diabetes or prediabetes; fasting affects results",
                "low": "May cause symptoms like shakiness; eat if symptomatic",
                "description": "Blood sugar level; important for diabetes monitoring",
            },
            "Creatinine": {
                "high": "May indicate reduced kidney function",
                "low": "Usually not clinically significant",
                "description": "Measures how well your kidneys filter waste",
            },
            "Potassium": {
                "high": "Can affect heart rhythm; may need dietary changes",
                "low": "Can cause muscle weakness; may need supplements",
                "description": "Important for heart and muscle function",
            },
            "TSH": {
                "high": "May indicate underactive thyroid (hypothyroidism)",
                "low": "May indicate overactive thyroid (hyperthyroidism)",
                "description": "Reflects thyroid gland function",
            },
            "LDL": {
                "high": "Increased cardiovascular risk; lifestyle changes may help",
                "low": "Generally favorable for heart health",
                "description": "'Bad' cholesterol that can build up in arteries",
            },
            "HDL": {
                "high": "Protective for heart health",
                "low": "Increased cardiovascular risk; exercise can help",
                "description": "'Good' cholesterol that removes other cholesterol",
            },
            "HbA1c": {
                "high": "Indicates elevated average blood sugar over 2-3 months",
                "low": "Normal or well-controlled blood sugar",
                "description": "3-month average of blood sugar control",
            },
            "Troponin I": {
                "high": "May indicate heart muscle damage; requires immediate evaluation",
                "low": "Normal heart muscle",
                "description": "Protein released when heart muscle is damaged",
            },
        }

    def interpret_results(
        self, lab_results: List[Dict[str, Any]], patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Interpret lab results with Claude-style reasoning traces.
        """
        trace = []
        interpretations = []

        # Step 1: Categorize and evaluate each result
        for result in lab_results:
            interpretation = self._evaluate_single_result(result, patient_context)
            interpretations.append(interpretation)
            trace.append(interpretation["trace"])

        # Step 2: Identify patterns
        patterns = self._identify_patterns(interpretations)
        trace.append(patterns["trace"])

        # Step 3: Generate patient-friendly summary
        summary = self._generate_patient_summary(interpretations, patterns)
        trace.append(summary["trace"])

        # Step 4: Generate clinical recommendations
        recommendations = self._generate_recommendations(interpretations, patterns)

        return {
            "results_count": len(lab_results),
            "interpretations": interpretations,
            "patterns": patterns["findings"],
            "patient_summary": summary["text"],
            "clinical_recommendations": recommendations,
            "critical_values": [i for i in interpretations if i["status"] in ["critical_low", "critical_high"]],
            "abnormal_count": sum(1 for i in interpretations if i["status"] != "normal"),
            "interpreted_at": datetime.utcnow().isoformat(),
            "trace": "\n".join(trace),
        }

    def _evaluate_single_result(
        self, result: Dict[str, Any], patient_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Evaluate a single lab result against reference ranges."""
        test_name = result.get("test_name", "Unknown")
        value = result.get("value", 0)

        ranges = self.reference_ranges.get(test_name, {})
        context = self.clinical_context.get(test_name, {})

        # Determine status
        status = "normal"
        if ranges:
            if ranges.get("critical_low") and value <= ranges["critical_low"]:
                status = "critical_low"
            elif ranges.get("critical_high") and value >= ranges["critical_high"]:
                status = "critical_high"
            elif value < ranges.get("low", float("-inf")):
                status = "low"
            elif value > ranges.get("high", float("inf")):
                status = "high"

        # Get interpretation
        interpretation_text = context.get(status.replace("critical_", ""), "")
        description = context.get("description", "")

        return {
            "test_name": test_name,
            "value": value,
            "unit": result.get("unit", ranges.get("unit", "")),
            "reference_range": f"{ranges.get('low', 'N/A')} - {ranges.get('high', 'N/A')}",
            "status": status,
            "interpretation": interpretation_text,
            "description": description,
            "trace": (
                f"<thinking>{test_name}: {value} {ranges.get('unit', '')}. "
                f"Reference: {ranges.get('low')}-{ranges.get('high')}. "
                f"Status: {status.upper()}.</thinking>"
            ),
        }

    def _identify_patterns(self, interpretations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify clinical patterns across multiple results."""
        findings = []

        # Check for anemia pattern
        hgb = next((i for i in interpretations if i["test_name"] == "Hemoglobin"), None)
        rbc = next((i for i in interpretations if i["test_name"] == "RBC"), None)
        if hgb and hgb["status"] == "low":
            findings.append({
                "pattern": "Anemia",
                "supporting_results": ["Hemoglobin", "RBC"],
                "recommendation": "Follow up with your doctor about anemia evaluation",
            })

        # Check for kidney function
        creat = next((i for i in interpretations if i["test_name"] == "Creatinine"), None)
        bun = next((i for i in interpretations if i["test_name"] == "BUN"), None)
        if creat and creat["status"] == "high":
            findings.append({
                "pattern": "Elevated kidney markers",
                "supporting_results": ["Creatinine", "BUN"],
                "recommendation": "May need further kidney function evaluation",
            })

        # Check for diabetes/prediabetes
        glucose = next((i for i in interpretations if i["test_name"] == "Glucose"), None)
        a1c = next((i for i in interpretations if i["test_name"] == "HbA1c"), None)
        if (glucose and glucose["status"] == "high") or (a1c and a1c["status"] == "high"):
            findings.append({
                "pattern": "Elevated glucose markers",
                "supporting_results": ["Glucose", "HbA1c"],
                "recommendation": "Discuss blood sugar management with your doctor",
            })

        # Check for thyroid issues
        tsh = next((i for i in interpretations if i["test_name"] == "TSH"), None)
        if tsh and tsh["status"] in ["high", "low"]:
            findings.append({
                "pattern": f"{'Underactive' if tsh['status'] == 'high' else 'Overactive'} thyroid markers",
                "supporting_results": ["TSH", "Free T4"],
                "recommendation": "May need thyroid function follow-up",
            })

        return {
            "findings": findings,
            "trace": (
                f"<analysis>Pattern analysis complete. Identified {len(findings)} "
                f"clinical patterns across {len(interpretations)} lab values.</analysis>"
            ),
        }

    def _generate_patient_summary(
        self, interpretations: List[Dict[str, Any]], patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate patient-friendly summary."""
        normal_count = sum(1 for i in interpretations if i["status"] == "normal")
        abnormal_count = len(interpretations) - normal_count
        critical_count = sum(1 for i in interpretations if "critical" in i["status"])

        if critical_count > 0:
            summary = (
                f"IMPORTANT: You have {critical_count} critical value(s) that may "
                "require immediate attention. Please contact your healthcare provider right away."
            )
        elif abnormal_count == 0:
            summary = (
                f"Good news! All {len(interpretations)} of your lab results are "
                "within normal ranges."
            )
        else:
            summary = (
                f"Out of {len(interpretations)} tests, {normal_count} are normal "
                f"and {abnormal_count} are outside the typical range. "
                "Your doctor will discuss any needed follow-up."
            )

        return {
            "text": summary,
            "trace": (
                f"<summary>Generated patient summary: {normal_count} normal, "
                f"{abnormal_count} abnormal, {critical_count} critical.</summary>"
            ),
        }

    def _generate_recommendations(
        self, interpretations: List[Dict[str, Any]], patterns: Dict[str, Any]
    ) -> List[str]:
        """Generate clinical recommendations."""
        recommendations = []

        # Check for critical values
        critical = [i for i in interpretations if "critical" in i["status"]]
        if critical:
            recommendations.append(
                "URGENT: Critical values detected. Contact healthcare provider immediately."
            )

        # Add pattern-based recommendations
        for finding in patterns.get("findings", []):
            recommendations.append(finding.get("recommendation", ""))

        # General recommendations
        if not recommendations:
            recommendations.append(
                "All results within expected ranges. Continue routine follow-up as scheduled."
            )

        return recommendations


def _demo() -> None:
    coworker = LabResultsCoworker()

    # Sample lab results
    lab_results = [
        {"test_name": "Hemoglobin", "value": 10.5, "unit": "g/dL"},
        {"test_name": "WBC", "value": 7.2, "unit": "K/uL"},
        {"test_name": "Glucose", "value": 142, "unit": "mg/dL"},
        {"test_name": "HbA1c", "value": 7.2, "unit": "%"},
        {"test_name": "Creatinine", "value": 0.9, "unit": "mg/dL"},
        {"test_name": "TSH", "value": 2.5, "unit": "mIU/L"},
        {"test_name": "LDL", "value": 145, "unit": "mg/dL"},
        {"test_name": "HDL", "value": 52, "unit": "mg/dL"},
    ]

    print("=== Lab Results Interpretation ===")
    result = coworker.interpret_results(lab_results)

    print(f"\nTotal Results: {result['results_count']}")
    print(f"Abnormal: {result['abnormal_count']}")
    print(f"Critical: {len(result['critical_values'])}")

    print("\n=== Patient Summary ===")
    print(result["patient_summary"])

    print("\n=== Patterns Identified ===")
    for pattern in result["patterns"]:
        print(f"- {pattern['pattern']}: {pattern['recommendation']}")

    print("\n=== Individual Results ===")
    for interp in result["interpretations"]:
        status_icon = {"normal": "OK", "high": "HIGH", "low": "LOW", "critical_high": "CRIT!", "critical_low": "CRIT!"}
        print(f"  {interp['test_name']}: {interp['value']} {interp['unit']} [{status_icon.get(interp['status'], '?')}]")


if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
