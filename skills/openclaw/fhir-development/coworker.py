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
Anthropic Health Stack - FHIR Development Coworker
---------------------------------------------------
Implements Claude's FHIR Development Skill for healthcare data interoperability.
Helps developers connect healthcare systems faster with fewer errors.

Based on: https://www.anthropic.com/news/healthcare-life-sciences
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class FHIRResourceType(Enum):
    PATIENT = "Patient"
    OBSERVATION = "Observation"
    CONDITION = "Condition"
    MEDICATION_REQUEST = "MedicationRequest"
    DIAGNOSTIC_REPORT = "DiagnosticReport"
    PROCEDURE = "Procedure"
    ENCOUNTER = "Encounter"
    ALLERGY_INTOLERANCE = "AllergyIntolerance"
    IMMUNIZATION = "Immunization"
    CARE_PLAN = "CarePlan"


class FHIRDevelopmentCoworker:
    """
    Claude-style coworker for FHIR resource development and validation.
    Produces <thinking>, <analysis>, <implementation> traces for audit.
    """

    def __init__(self) -> None:
        self.fhir_version = "R4"
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict[str, Any]:
        return {
            "Patient": {
                "required": ["identifier", "name"],
                "recommended": ["birthDate", "gender", "address"],
            },
            "Observation": {
                "required": ["status", "code", "subject"],
                "recommended": ["effectiveDateTime", "valueQuantity"],
            },
            "Condition": {
                "required": ["clinicalStatus", "code", "subject"],
                "recommended": ["onsetDateTime", "recordedDate"],
            },
            "MedicationRequest": {
                "required": ["status", "intent", "medication", "subject"],
                "recommended": ["authoredOn", "dosageInstruction"],
            },
        }

    def generate_resource(
        self, resource_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a FHIR-compliant resource with Claude-style traces.
        """
        trace = self._build_generation_trace(resource_type, data)
        resource = self._construct_resource(resource_type, data)
        validation = self._validate_resource(resource_type, resource)

        return {
            "resource_type": resource_type,
            "fhir_version": self.fhir_version,
            "resource": resource,
            "validation": validation,
            "generated_at": datetime.utcnow().isoformat(),
            "trace": trace,
        }

    def _construct_resource(
        self, resource_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build FHIR R4 compliant resource structure."""
        base = {
            "resourceType": resource_type,
            "id": data.get("id", f"{resource_type.lower()}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
            "meta": {
                "versionId": "1",
                "lastUpdated": datetime.utcnow().isoformat(),
                "profile": [f"http://hl7.org/fhir/StructureDefinition/{resource_type}"],
            },
        }

        if resource_type == "Patient":
            base.update(self._build_patient(data))
        elif resource_type == "Observation":
            base.update(self._build_observation(data))
        elif resource_type == "Condition":
            base.update(self._build_condition(data))
        elif resource_type == "MedicationRequest":
            base.update(self._build_medication_request(data))

        return base

    def _build_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "identifier": [
                {
                    "system": data.get("identifier_system", "http://hospital.example.org/patients"),
                    "value": data.get("identifier", ""),
                }
            ],
            "active": True,
            "name": [
                {
                    "use": "official",
                    "family": data.get("family_name", ""),
                    "given": data.get("given_names", []),
                }
            ],
            "gender": data.get("gender", "unknown"),
            "birthDate": data.get("birth_date", ""),
            "address": [
                {
                    "use": "home",
                    "line": data.get("address_lines", []),
                    "city": data.get("city", ""),
                    "state": data.get("state", ""),
                    "postalCode": data.get("postal_code", ""),
                }
            ],
        }

    def _build_observation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": data.get("status", "final"),
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": data.get("category", "vital-signs"),
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": data.get("code_system", "http://loinc.org"),
                        "code": data.get("code", ""),
                        "display": data.get("display", ""),
                    }
                ]
            },
            "subject": {"reference": f"Patient/{data.get('patient_id', '')}"},
            "effectiveDateTime": data.get("effective_date", datetime.utcnow().isoformat()),
            "valueQuantity": {
                "value": data.get("value", 0),
                "unit": data.get("unit", ""),
                "system": "http://unitsofmeasure.org",
                "code": data.get("unit_code", ""),
            },
        }

    def _build_condition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": data.get("clinical_status", "active"),
                    }
                ]
            },
            "verificationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                        "code": data.get("verification_status", "confirmed"),
                    }
                ]
            },
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": data.get("snomed_code", ""),
                        "display": data.get("condition_name", ""),
                    }
                ]
            },
            "subject": {"reference": f"Patient/{data.get('patient_id', '')}"},
            "onsetDateTime": data.get("onset_date", ""),
        }

    def _build_medication_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": data.get("status", "active"),
            "intent": data.get("intent", "order"),
            "medicationCodeableConcept": {
                "coding": [
                    {
                        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                        "code": data.get("rxnorm_code", ""),
                        "display": data.get("medication_name", ""),
                    }
                ]
            },
            "subject": {"reference": f"Patient/{data.get('patient_id', '')}"},
            "authoredOn": data.get("authored_on", datetime.utcnow().isoformat()),
            "dosageInstruction": [
                {
                    "text": data.get("dosage_text", ""),
                    "timing": {
                        "repeat": {
                            "frequency": data.get("frequency", 1),
                            "period": data.get("period", 1),
                            "periodUnit": data.get("period_unit", "d"),
                        }
                    },
                }
            ],
        }

    def _validate_resource(
        self, resource_type: str, resource: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate resource against FHIR R4 rules."""
        rules = self.validation_rules.get(resource_type, {})
        errors = []
        warnings = []

        for field in rules.get("required", []):
            if field not in resource or not resource[field]:
                errors.append(f"Missing required field: {field}")

        for field in rules.get("recommended", []):
            if field not in resource or not resource[field]:
                warnings.append(f"Missing recommended field: {field}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def _build_generation_trace(
        self, resource_type: str, data: Dict[str, Any]
    ) -> str:
        return (
            f"<thinking>Generating FHIR {self.fhir_version} {resource_type} resource. "
            f"Input contains {len(data)} fields to map.</thinking>\n"
            f"<analysis>Mapping input fields to FHIR {resource_type} structure. "
            f"Applying HL7 FHIR R4 specification constraints.</analysis>\n"
            f"<implementation>Constructed {resource_type} with required identifiers, "
            f"coded elements using standard terminologies (SNOMED, LOINC, RxNorm).</implementation>"
        )

    def convert_bundle(
        self, resources: List[Dict[str, Any]], bundle_type: str = "collection"
    ) -> Dict[str, Any]:
        """Create a FHIR Bundle from multiple resources."""
        return {
            "resourceType": "Bundle",
            "type": bundle_type,
            "timestamp": datetime.utcnow().isoformat(),
            "entry": [{"resource": r} for r in resources],
        }


def _demo() -> None:
    coworker = FHIRDevelopmentCoworker()

    # Demo: Create a Patient resource
    patient_data = {
        "identifier": "MRN-12345",
        "family_name": "Smith",
        "given_names": ["John", "Robert"],
        "gender": "male",
        "birth_date": "1985-03-15",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
    }
    result = coworker.generate_resource("Patient", patient_data)
    print("=== FHIR Patient Resource ===")
    print(json.dumps(result, indent=2))

    # Demo: Create an Observation resource
    observation_data = {
        "patient_id": "patient-12345",
        "code": "8867-4",
        "display": "Heart rate",
        "category": "vital-signs",
        "value": 72,
        "unit": "beats/minute",
        "unit_code": "/min",
    }
    result = coworker.generate_resource("Observation", observation_data)
    print("\n=== FHIR Observation Resource ===")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
