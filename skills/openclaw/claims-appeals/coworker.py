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
Anthropic Health Stack - Claims Appeals Coworker
-------------------------------------------------
Implements Claude's Claims Appeals Support skill for healthcare payers.
Combines patient records, coverage policies, clinical guidelines, and prior
documentation to strengthen appeal submissions.

Based on: https://www.anthropic.com/news/healthcare-life-sciences
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class AppealType(Enum):
    FIRST_LEVEL = "first_level"
    SECOND_LEVEL = "second_level"
    EXTERNAL_REVIEW = "external_review"
    EXPEDITED = "expedited"


class DenialReason(Enum):
    MEDICAL_NECESSITY = "medical_necessity"
    EXPERIMENTAL = "experimental_investigational"
    OUT_OF_NETWORK = "out_of_network"
    PRIOR_AUTH_MISSING = "prior_authorization_missing"
    CODING_ERROR = "coding_error"
    BENEFIT_EXCLUSION = "benefit_exclusion"
    TIMELY_FILING = "timely_filing"


class ClaimsAppealsCoworker:
    """
    Claude-style coworker for insurance claims appeal processing.
    Produces structured reasoning traces with evidence synthesis.
    """

    def __init__(self) -> None:
        self.guideline_db = self._load_clinical_guidelines()
        self.policy_db = self._load_coverage_policies()

    def _load_clinical_guidelines(self) -> Dict[str, Any]:
        return {
            "MRI-LUMBAR": {
                "source": "ACR Appropriateness Criteria",
                "indications": [
                    "Radiculopathy with motor deficit",
                    "Cauda equina syndrome suspected",
                    "Failed conservative therapy > 6 weeks",
                    "Post-surgical evaluation",
                ],
                "evidence_level": "Usually Appropriate",
            },
            "BIOLOGICS-RA": {
                "source": "ACR/AAFP Guidelines 2021",
                "indications": [
                    "Moderate-to-high disease activity despite csDMARD",
                    "Poor prognostic factors present",
                    "Contraindication to methotrexate",
                ],
                "evidence_level": "Strong Recommendation",
            },
            "GENETIC-TESTING-BRCA": {
                "source": "NCCN Guidelines v3.2024",
                "indications": [
                    "Personal history of breast cancer < 50",
                    "Family history meeting criteria",
                    "Ashkenazi Jewish ancestry with breast/ovarian cancer",
                    "Male breast cancer",
                ],
                "evidence_level": "Category 1",
            },
        }

    def _load_coverage_policies(self) -> Dict[str, Any]:
        return {
            "CMS-LCD-L35050": {
                "title": "MRI of the Spine",
                "criteria": [
                    "Documentation of failed conservative therapy",
                    "Neurological examination findings",
                    "Specific clinical indication documented",
                ],
            },
            "CMS-NCD-110.21": {
                "title": "Genetic Testing for BRCA",
                "criteria": [
                    "Family history assessment completed",
                    "Risk assessment tool utilized",
                    "Genetic counseling provided",
                ],
            },
        }

    def process_appeal(
        self,
        claim: Dict[str, Any],
        denial_reason: str,
        clinical_records: List[Dict[str, Any]],
        appeal_type: str = "first_level",
    ) -> Dict[str, Any]:
        """
        Process a claims appeal with Claude-style extended thinking.
        """
        trace = []

        # Step 1: Analyze denial reason
        trace.append(self._analyze_denial(denial_reason, claim))

        # Step 2: Extract clinical evidence
        evidence = self._extract_clinical_evidence(clinical_records, claim)
        trace.append(evidence["trace"])

        # Step 3: Match to guidelines
        guideline_support = self._match_guidelines(claim, evidence["findings"])
        trace.append(guideline_support["trace"])

        # Step 4: Check coverage policy
        policy_analysis = self._analyze_coverage_policy(claim, evidence["findings"])
        trace.append(policy_analysis["trace"])

        # Step 5: Generate appeal letter
        appeal_letter = self._generate_appeal_letter(
            claim, denial_reason, evidence, guideline_support, policy_analysis
        )

        return {
            "claim_id": claim.get("claim_id", "unknown"),
            "appeal_type": appeal_type,
            "denial_reason": denial_reason,
            "recommendation": self._determine_recommendation(
                evidence, guideline_support, policy_analysis
            ),
            "evidence_strength": self._calculate_evidence_strength(
                evidence, guideline_support
            ),
            "appeal_letter": appeal_letter,
            "supporting_documents": self._list_required_documents(denial_reason),
            "generated_at": datetime.utcnow().isoformat(),
            "trace": "\n".join(trace),
        }

    def _analyze_denial(self, denial_reason: str, claim: Dict[str, Any]) -> str:
        return (
            f"<thinking>Analyzing denial for claim {claim.get('claim_id')}. "
            f"Denial reason: {denial_reason}. This requires demonstrating "
            f"medical necessity through clinical documentation and guideline alignment.</thinking>"
        )

    def _extract_clinical_evidence(
        self, records: List[Dict[str, Any]], claim: Dict[str, Any]
    ) -> Dict[str, Any]:
        findings = []
        for record in records:
            if record.get("type") == "clinical_note":
                findings.append({
                    "source": record.get("provider", "Unknown"),
                    "date": record.get("date", ""),
                    "key_findings": record.get("findings", []),
                    "supports_necessity": True,
                })
            elif record.get("type") == "lab_result":
                findings.append({
                    "source": "Laboratory",
                    "date": record.get("date", ""),
                    "key_findings": [f"{record.get('test')}: {record.get('result')}"],
                    "supports_necessity": record.get("abnormal", False),
                })

        return {
            "findings": findings,
            "trace": (
                f"<analysis>Extracted {len(findings)} relevant clinical findings from "
                f"{len(records)} source documents. Key evidence includes diagnostic "
                f"results, treatment history, and specialist assessments.</analysis>"
            ),
        }

    def _match_guidelines(
        self, claim: Dict[str, Any], findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        procedure = claim.get("procedure_code", "")
        guideline = None

        for key, value in self.guideline_db.items():
            if key in procedure or procedure in key:
                guideline = value
                break

        if guideline:
            matched_indications = []
            for indication in guideline.get("indications", []):
                for finding in findings:
                    if any(
                        indication.lower() in f.lower()
                        for f in finding.get("key_findings", [])
                    ):
                        matched_indications.append(indication)
                        break

            return {
                "guideline_source": guideline.get("source"),
                "evidence_level": guideline.get("evidence_level"),
                "matched_indications": matched_indications,
                "coverage_supported": len(matched_indications) > 0,
                "trace": (
                    f"<evidence>Matched {len(matched_indications)} indications from "
                    f"{guideline.get('source')}. Evidence level: {guideline.get('evidence_level')}. "
                    f"Clinical documentation supports guideline criteria.</evidence>"
                ),
            }

        return {
            "guideline_source": None,
            "matched_indications": [],
            "coverage_supported": False,
            "trace": "<evidence>No specific guideline match found. Will rely on clinical documentation.</evidence>",
        }

    def _analyze_coverage_policy(
        self, claim: Dict[str, Any], findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        met_criteria = []
        unmet_criteria = []

        # Check against CMS policies
        for policy_id, policy in self.policy_db.items():
            for criterion in policy.get("criteria", []):
                criterion_met = any(
                    criterion.lower() in str(f).lower() for f in findings
                )
                if criterion_met:
                    met_criteria.append(criterion)
                else:
                    unmet_criteria.append(criterion)

        return {
            "met_criteria": met_criteria,
            "unmet_criteria": unmet_criteria,
            "policy_compliance": len(met_criteria) / max(len(met_criteria) + len(unmet_criteria), 1),
            "trace": (
                f"<policy>Coverage policy analysis: {len(met_criteria)} criteria met, "
                f"{len(unmet_criteria)} require additional documentation. "
                f"Compliance score: {len(met_criteria) / max(len(met_criteria) + len(unmet_criteria), 1):.0%}</policy>"
            ),
        }

    def _determine_recommendation(
        self,
        evidence: Dict[str, Any],
        guideline_support: Dict[str, Any],
        policy_analysis: Dict[str, Any],
    ) -> str:
        score = 0
        if len(evidence.get("findings", [])) >= 2:
            score += 1
        if guideline_support.get("coverage_supported"):
            score += 2
        if policy_analysis.get("policy_compliance", 0) >= 0.5:
            score += 1

        if score >= 3:
            return "STRONG_APPEAL"
        elif score >= 2:
            return "MODERATE_APPEAL"
        else:
            return "WEAK_APPEAL"

    def _calculate_evidence_strength(
        self, evidence: Dict[str, Any], guideline_support: Dict[str, Any]
    ) -> str:
        if guideline_support.get("evidence_level") in ["Category 1", "Strong Recommendation"]:
            return "HIGH"
        elif len(evidence.get("findings", [])) >= 3:
            return "MODERATE"
        else:
            return "LOW"

    def _generate_appeal_letter(
        self,
        claim: Dict[str, Any],
        denial_reason: str,
        evidence: Dict[str, Any],
        guideline_support: Dict[str, Any],
        policy_analysis: Dict[str, Any],
    ) -> str:
        return f"""
APPEAL FOR CLAIM {claim.get('claim_id')}

RE: Request for Reconsideration - {claim.get('procedure_name', 'Medical Service')}
Patient: {claim.get('patient_name', '[Patient Name]')}
Date of Service: {claim.get('service_date', '[Date]')}
Denial Reason: {denial_reason}

Dear Claims Review Committee,

We are writing to appeal the denial of the above-referenced claim. Based on our
review of the clinical documentation and applicable guidelines, we believe this
service meets medical necessity criteria.

CLINICAL EVIDENCE:
{self._format_evidence(evidence)}

GUIDELINE SUPPORT:
{self._format_guideline_support(guideline_support)}

COVERAGE POLICY COMPLIANCE:
{self._format_policy_compliance(policy_analysis)}

Based on the above evidence, we respectfully request that this claim be
reconsidered and approved for payment.

Sincerely,
[Provider Name]
"""

    def _format_evidence(self, evidence: Dict[str, Any]) -> str:
        lines = []
        for finding in evidence.get("findings", []):
            lines.append(f"- {finding.get('source')} ({finding.get('date')}): {', '.join(finding.get('key_findings', []))}")
        return "\n".join(lines) if lines else "See attached clinical documentation."

    def _format_guideline_support(self, guideline_support: Dict[str, Any]) -> str:
        if guideline_support.get("coverage_supported"):
            return f"Per {guideline_support.get('guideline_source')}, this service meets criteria with {guideline_support.get('evidence_level')} recommendation."
        return "Clinical documentation supports medical necessity."

    def _format_policy_compliance(self, policy_analysis: Dict[str, Any]) -> str:
        return f"Coverage criteria compliance: {policy_analysis.get('policy_compliance', 0):.0%}"

    def _list_required_documents(self, denial_reason: str) -> List[str]:
        base_docs = [
            "Clinical notes from treating physician",
            "Relevant diagnostic test results",
            "Prior authorization documentation (if applicable)",
        ]

        if denial_reason == "medical_necessity":
            base_docs.extend([
                "Letter of medical necessity",
                "Peer-reviewed literature supporting treatment",
            ])
        elif denial_reason == "experimental_investigational":
            base_docs.extend([
                "FDA approval documentation",
                "Clinical trial results",
                "Compendia citations",
            ])

        return base_docs


def _demo() -> None:
    coworker = ClaimsAppealsCoworker()

    claim = {
        "claim_id": "CLM-2026-001234",
        "patient_name": "Jane Doe",
        "procedure_code": "MRI-LUMBAR",
        "procedure_name": "MRI Lumbar Spine without Contrast",
        "service_date": "2026-01-10",
    }

    clinical_records = [
        {
            "type": "clinical_note",
            "provider": "Dr. Smith, Orthopedics",
            "date": "2026-01-05",
            "findings": [
                "Failed conservative therapy > 6 weeks",
                "Persistent radiculopathy with motor deficit",
                "Physical therapy x 8 sessions without improvement",
            ],
        },
        {
            "type": "lab_result",
            "test": "EMG/NCS",
            "result": "Abnormal - L5 radiculopathy",
            "date": "2026-01-03",
            "abnormal": True,
        },
    ]

    result = coworker.process_appeal(
        claim=claim,
        denial_reason="medical_necessity",
        clinical_records=clinical_records,
        appeal_type="first_level",
    )

    print("=== Claims Appeal Analysis ===")
    print(json.dumps({k: v for k, v in result.items() if k != "appeal_letter"}, indent=2))
    print("\n=== Generated Appeal Letter ===")
    print(result["appeal_letter"])


if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
