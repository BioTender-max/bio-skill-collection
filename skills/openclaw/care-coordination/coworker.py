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
Anthropic Health Stack - Care Coordination Coworker
----------------------------------------------------
Implements Claude's Care Coordination skill for patient message triage
and care team coordination.

Helps clinicians navigate large volumes of patient portal messages,
referrals, and handoffs to identify urgent matters.

Based on: https://www.anthropic.com/news/healthcare-life-sciences
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class UrgencyLevel(Enum):
    EMERGENT = "emergent"  # Requires immediate attention
    URGENT = "urgent"  # Same-day response needed
    ROUTINE = "routine"  # Standard response time (24-48 hours)
    LOW = "low"  # Can wait, informational


class MessageCategory(Enum):
    SYMPTOMS = "symptoms"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    RESULTS = "results"
    REFERRAL = "referral"
    BILLING = "billing"
    ADMINISTRATIVE = "administrative"
    MENTAL_HEALTH = "mental_health"


class CareCoordinationCoworker:
    """
    Claude-style coworker for patient message triage and care coordination.
    Produces structured triage decisions with reasoning traces.
    """

    def __init__(self) -> None:
        self.urgency_keywords = self._load_urgency_keywords()
        self.routing_rules = self._load_routing_rules()

    def _load_urgency_keywords(self) -> Dict[str, List[str]]:
        return {
            "emergent": [
                "chest pain", "difficulty breathing", "shortness of breath",
                "severe bleeding", "stroke symptoms", "suicidal", "overdose",
                "unresponsive", "seizure", "allergic reaction", "anaphylaxis",
            ],
            "urgent": [
                "fever over 101", "severe pain", "worsening symptoms",
                "new rash", "swelling", "dizziness", "fainting",
                "blood in urine", "blood in stool", "severe headache",
                "medication reaction", "can't keep food down",
            ],
            "routine": [
                "refill request", "lab results", "appointment",
                "follow-up", "chronic condition", "routine question",
            ],
        }

    def _load_routing_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            "symptoms": {
                "primary_route": "nursing_triage",
                "escalation": "provider_review",
            },
            "medication": {
                "primary_route": "pharmacy",
                "escalation": "provider_review",
            },
            "appointment": {
                "primary_route": "scheduling",
                "escalation": None,
            },
            "results": {
                "primary_route": "provider_review",
                "escalation": None,
            },
            "referral": {
                "primary_route": "care_coordinator",
                "escalation": "provider_review",
            },
            "mental_health": {
                "primary_route": "behavioral_health",
                "escalation": "crisis_team",
            },
            "billing": {
                "primary_route": "billing_dept",
                "escalation": None,
            },
        }

    def triage_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Triage a patient portal message with Claude-style reasoning.
        """
        trace = []

        # Step 1: Analyze message content
        content_analysis = self._analyze_content(message)
        trace.append(content_analysis["trace"])

        # Step 2: Assess urgency
        urgency = self._assess_urgency(message, content_analysis)
        trace.append(urgency["trace"])

        # Step 3: Categorize message
        category = self._categorize_message(message, content_analysis)
        trace.append(category["trace"])

        # Step 4: Determine routing
        routing = self._determine_routing(category, urgency)
        trace.append(routing["trace"])

        # Step 5: Generate response recommendation
        response = self._generate_response_recommendation(
            message, urgency, category
        )

        return {
            "message_id": message.get("message_id", "unknown"),
            "patient_id": message.get("patient_id", "unknown"),
            "urgency_level": urgency["level"],
            "urgency_score": urgency["score"],
            "category": category["primary"],
            "subcategories": category["secondary"],
            "routing": routing,
            "response_recommendation": response,
            "requires_provider_review": urgency["level"] in ["emergent", "urgent"],
            "suggested_response_time": self._get_response_time(urgency["level"]),
            "triaged_at": datetime.utcnow().isoformat(),
            "trace": "\n".join(trace),
        }

    def _analyze_content(self, message: Dict[str, Any]) -> Dict[str, Any]:
        content = message.get("content", "").lower()
        subject = message.get("subject", "").lower()

        # Extract key phrases
        key_phrases = []
        for urgency_level, keywords in self.urgency_keywords.items():
            for keyword in keywords:
                if keyword in content or keyword in subject:
                    key_phrases.append({"phrase": keyword, "urgency": urgency_level})

        return {
            "key_phrases": key_phrases,
            "word_count": len(content.split()),
            "has_question": "?" in content,
            "trace": (
                f"<thinking>Analyzing message from patient {message.get('patient_id')}. "
                f"Subject: '{message.get('subject', 'No subject')}'. "
                f"Identified {len(key_phrases)} clinically relevant phrases.</thinking>"
            ),
        }

    def _assess_urgency(
        self, message: Dict[str, Any], content_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        key_phrases = content_analysis.get("key_phrases", [])

        # Check for emergent keywords
        emergent_count = sum(1 for p in key_phrases if p["urgency"] == "emergent")
        urgent_count = sum(1 for p in key_phrases if p["urgency"] == "urgent")

        if emergent_count > 0:
            level = "emergent"
            score = 1.0
        elif urgent_count > 0:
            level = "urgent"
            score = 0.7
        elif len(key_phrases) > 0:
            level = "routine"
            score = 0.4
        else:
            level = "low"
            score = 0.2

        # Check patient history flags
        if message.get("patient_flags", {}).get("high_risk"):
            score = min(score + 0.2, 1.0)
            if level == "routine":
                level = "urgent"

        return {
            "level": level,
            "score": score,
            "emergent_indicators": emergent_count,
            "urgent_indicators": urgent_count,
            "trace": (
                f"<analysis>Urgency assessment: {level.upper()} (score: {score:.2f}). "
                f"Found {emergent_count} emergent and {urgent_count} urgent indicators. "
                f"Patient risk flags: {message.get('patient_flags', {})}</analysis>"
            ),
        }

    def _categorize_message(
        self, message: Dict[str, Any], content_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        content = message.get("content", "").lower()
        subject = message.get("subject", "").lower()

        categories = {
            "symptoms": ["pain", "fever", "cough", "tired", "nausea", "dizzy", "headache"],
            "medication": ["medication", "prescription", "refill", "dosage", "side effect"],
            "appointment": ["appointment", "schedule", "reschedule", "cancel", "availability"],
            "results": ["results", "lab", "test", "imaging", "biopsy"],
            "referral": ["referral", "specialist", "refer"],
            "mental_health": ["anxiety", "depression", "stress", "sleep", "mood"],
            "billing": ["bill", "payment", "insurance", "cost", "charge"],
        }

        matched = []
        for category, keywords in categories.items():
            matches = sum(1 for k in keywords if k in content or k in subject)
            if matches > 0:
                matched.append({"category": category, "matches": matches})

        matched.sort(key=lambda x: x["matches"], reverse=True)

        primary = matched[0]["category"] if matched else "administrative"
        secondary = [m["category"] for m in matched[1:3]]

        return {
            "primary": primary,
            "secondary": secondary,
            "trace": (
                f"<categorization>Primary category: {primary}. "
                f"Secondary categories: {', '.join(secondary) if secondary else 'None'}. "
                f"Based on keyword matching against {len(categories)} category definitions.</categorization>"
            ),
        }

    def _determine_routing(
        self, category: Dict[str, Any], urgency: Dict[str, Any]
    ) -> Dict[str, Any]:
        primary_cat = category.get("primary", "administrative")
        urgency_level = urgency.get("level", "routine")

        routing_config = self.routing_rules.get(
            primary_cat, {"primary_route": "general_inbox", "escalation": None}
        )

        if urgency_level == "emergent":
            route = "emergency_triage"
            escalate_to = "provider_stat"
        elif urgency_level == "urgent":
            route = routing_config.get("escalation") or routing_config["primary_route"]
            escalate_to = "provider_review"
        else:
            route = routing_config["primary_route"]
            escalate_to = routing_config.get("escalation")

        return {
            "primary_route": route,
            "escalation_path": escalate_to,
            "trace": (
                f"<routing>Routing to: {route}. "
                f"Escalation path: {escalate_to or 'None'}. "
                f"Based on {primary_cat} category and {urgency_level} urgency.</routing>"
            ),
        }

    def _generate_response_recommendation(
        self,
        message: Dict[str, Any],
        urgency: Dict[str, Any],
        category: Dict[str, Any],
    ) -> Dict[str, Any]:
        urgency_level = urgency.get("level", "routine")
        primary_cat = category.get("primary", "administrative")

        if urgency_level == "emergent":
            action = "CALL_PATIENT_IMMEDIATELY"
            template = (
                "This message indicates a potential emergency. "
                "Please call the patient immediately or advise them to call 911."
            )
        elif urgency_level == "urgent":
            action = "RESPOND_TODAY"
            template = (
                f"This {primary_cat} concern requires same-day attention. "
                "Please review and respond by end of business."
            )
        else:
            action = "STANDARD_RESPONSE"
            template = f"Standard {primary_cat} inquiry. Route to appropriate team."

        return {
            "action": action,
            "suggested_template": template,
            "auto_response_eligible": urgency_level in ["routine", "low"],
        }

    def _get_response_time(self, urgency_level: str) -> str:
        times = {
            "emergent": "IMMEDIATE",
            "urgent": "Within 4 hours",
            "routine": "Within 24-48 hours",
            "low": "Within 72 hours",
        }
        return times.get(urgency_level, "Within 48 hours")

    def batch_triage(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Triage multiple messages and return prioritized queue.
        """
        results = []
        for msg in messages:
            result = self.triage_message(msg)
            results.append(result)

        # Sort by urgency
        urgency_order = {"emergent": 0, "urgent": 1, "routine": 2, "low": 3}
        results.sort(key=lambda x: urgency_order.get(x["urgency_level"], 4))

        return {
            "total_messages": len(messages),
            "emergent_count": sum(1 for r in results if r["urgency_level"] == "emergent"),
            "urgent_count": sum(1 for r in results if r["urgency_level"] == "urgent"),
            "routine_count": sum(1 for r in results if r["urgency_level"] == "routine"),
            "prioritized_queue": results,
            "processed_at": datetime.utcnow().isoformat(),
        }


def _demo() -> None:
    coworker = CareCoordinationCoworker()

    messages = [
        {
            "message_id": "MSG-001",
            "patient_id": "PT-12345",
            "subject": "Chest pain since yesterday",
            "content": "I've been having chest pain and shortness of breath since yesterday afternoon. Should I be worried?",
            "patient_flags": {"high_risk": True, "cardiac_history": True},
        },
        {
            "message_id": "MSG-002",
            "patient_id": "PT-67890",
            "subject": "Medication refill",
            "content": "I need a refill on my blood pressure medication. I have about 5 days left.",
            "patient_flags": {},
        },
        {
            "message_id": "MSG-003",
            "patient_id": "PT-11111",
            "subject": "Lab results question",
            "content": "I got my lab results in the portal but I don't understand what they mean. Can someone explain?",
            "patient_flags": {},
        },
    ]

    print("=== Single Message Triage ===")
    result = coworker.triage_message(messages[0])
    print(json.dumps({k: v for k, v in result.items() if k != "trace"}, indent=2))
    print("\nTrace:")
    print(result["trace"])

    print("\n=== Batch Triage ===")
    batch_result = coworker.batch_triage(messages)
    print(f"Total: {batch_result['total_messages']}")
    print(f"Emergent: {batch_result['emergent_count']}")
    print(f"Urgent: {batch_result['urgent_count']}")
    print(f"Routine: {batch_result['routine_count']}")


if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
