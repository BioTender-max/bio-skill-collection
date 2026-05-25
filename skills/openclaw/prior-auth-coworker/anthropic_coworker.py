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
Anthropic Health Stack – Prior Authorization Coworker
----------------------------------------------------
Produces Claude-style coworker traces (<thinking> + JSON decision payload)
so the Event Bus can replay determinations for auditors.
"""

from __future__ import annotations

import json
import sys
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# --- Import Resolution ---
# We want to be able to import from 'platform' and 'Skills' regardless of where this script is run.
# Strategy: Find the project root by looking for 'platform' or 'Skills' in parent directories.

def _setup_paths():
    current = os.path.dirname(os.path.abspath(__file__))
    # Walk up until we find 'platform' directory
    while current != "/":
        if os.path.exists(os.path.join(current, "platform")):
            if current not in sys.path:
                sys.path.append(current)
            # Also add platform explicitly if needed
            if os.path.join(current, "platform") not in sys.path:
                sys.path.append(os.path.join(current, "platform"))
            return
        current = os.path.dirname(current)

_setup_paths()

try:
    from optimizer.meta_prompter import PromptOptimizer, ModelTarget
except ImportError:
    # Fallback mock if environment is strictly isolated
    class PromptOptimizer:
        def optimize(self, p, t): return p
    class ModelTarget:
        CLAUDE = "claude"

class PriorAuthCoworker:
    def __init__(self, policy_path: Optional[str] = None) -> None:
        self.optimizer = PromptOptimizer()
        self._load_policies(policy_path)

    def _load_policies(self, path: Optional[str]) -> None:
        # Default to policies.json in the same directory
        if not path:
            path = os.path.join(os.path.dirname(__file__), "policies.json")
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.policy_db = json.load(f)
        else:
            print(f"Warning: Policy file {path} not found. Using minimal fallback.")
            self.policy_db = {
                "MRI-L-SPINE": {
                    "version": "FALLBACK-01",
                    "criteria": ["Pain > 6 weeks", "Failed PT"]
                }
            }

    def review(self, casefile: Dict[str, str]) -> Dict[str, Any]:
        """
        Returns Anthropic-style trace plus structured JSON output.
        """
        procedure_code = casefile.get("procedure_code")
        policy = self.policy_db.get(procedure_code)
        
        if not policy:
             return {
                "case_id": casefile.get("case_id", "unknown"),
                "error": f"No policy found for {procedure_code}"
            }

        reasoning = self._evaluate(casefile.get("clinical_note", ""), policy)
        # Decision logic: All criteria must be met (simplified)
        # In reality, it might be "ANY red flag OR (Pain AND Therapy)"
        # Here we assume a simple "ALL" for the demo unless it's a red flag list
        
        # improved logic: check if any red flag is met, OR if standard conservative therapy criteria are met
        # For this demo, let's keep it simple: count how many criteria are met.
        
        met_count = sum(1 for item in reasoning if item["met"])
        decision = met_count == len(reasoning) # Strict approval
        
        trace = self._build_trace(casefile, policy, reasoning, decision)
        
        payload = {
            "case_id": casefile.get("case_id", "unknown"),
            "procedure_code": procedure_code,
            "policy_version": policy["version"],
            "decision": "APPROVED" if decision else "DENIED",
            "reasoning": reasoning,
            "generated_at": datetime.utcnow().isoformat(),
            "trace": trace,
        }
        return payload

    def _evaluate(self, note: str, policy: Dict[str, Any]) -> List[Dict[str, Any]]:
        note_lower = note.lower()
        checks = []
        for criterion in policy["criteria"]:
            if criterion.startswith("Persistent"):
                checks.append({"criterion": criterion, "met": "week" in note_lower})
            elif "conservative" in criterion:
                checks.append({"criterion": criterion, "met": "therapy" in note_lower})
            else:
                checks.append({"criterion": criterion, "met": "red flag" in note_lower or "trauma" in note_lower})
        return checks

    def _build_trace(self, casefile: Dict[str, str], policy: Dict[str, Any], reasoning: List[Dict[str, Any]], decision: bool) -> str:
        # Use Meta-Prompter to format the "system" thinking
        # In a real agent, this would be the PROMPT sent to the model to generate the trace.
        # Here, we are constructing the trace retrospectively to match the format.
        
        # However, to demonstrate the Optimizer, let's pretend we are asking Claude to explain the decision.
        explanation_prompt = f"""
        Explain the decision for Case {casefile.get('case_id')}.
        Policy: {policy['version']}
        Criteria Met: {json.dumps(reasoning)}
        Final Decision: {'Approved' if decision else 'Denied'}
        """
        
        # We simulate the structure the model WOULD produce given an Optimized Prompt
        # <thinking>...</thinking><analysis>...</analysis><decision>...</decision>
        
        trace = (
            f"<thinking>Reviewing case {casefile.get('case_id')} for {casefile['procedure_code']} "
            f"against policy v{policy['version']}. Checking specific criteria against extracted entities.</thinking>\n"
            f"<analysis>Extracted clinical entities: duration, conservative therapy, and red-flag indicators.\n"
            f"Criteria Evaluation:\n"
        )
        for r in reasoning:
            trace += f"- {r['criterion']}: {'MET' if r['met'] else 'NOT MET'}\n"
        
        trace += f"</analysis>\n<decision>The request is { 'APPROVED' if decision else 'DENIED'} based on policy criteria.</decision>"
        
        return trace


def _demo() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run Prior Auth Review")
    parser.add_argument("--note", type=str, help="Clinical note text")
    parser.add_argument("--code", type=str, help="Procedure code (e.g., MRI-L-SPINE)")
    args = parser.parse_args()

    coworker = PriorAuthCoworker()

    if args.note and args.code:
        case = {
            "case_id": "CLI-CASE-001",
            "procedure_code": args.code,
            "clinical_note": args.note,
        }
        payload = coworker.review(case)
        print(json.dumps(payload, indent=2))
    else:
        # Default Demo
        case = {
            "case_id": "PA-1001",
            "procedure_code": "MRI-L-SPINE",
            "clinical_note": "Chronic back pain for 8 weeks with failed PT and NSAIDs. No trauma.",
        }
        payload = coworker.review(case)
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
