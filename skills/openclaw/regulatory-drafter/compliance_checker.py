# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import sys
import os
import json
from typing import Dict, Any, List, Optional

# Adjust path to find sibling modules
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

try:
    from Skills.Agentic_AI.Agent_Architectures.Self_Correction.self_correction_agent import SelfCorrectionAgent
except ImportError:
    # Fallback for relative imports
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Agentic_AI/Agent_Architectures/Self_Correction")))
    from self_correction_agent import SelfCorrectionAgent

class ComplianceCheckAgent:
    """
    Agent focused on auditing regulatory drafts for compliance violations.
    Uses 'Self-Correction' to iteratively refine the audit report.
    """

    def __init__(self):
        self.auditor = SelfCorrectionAgent()

    def audit_draft(self, 
                     draft_text: str,
                     regulation_code: str, 
                     risk_tolerance: str = "Low") -> Dict[str, Any]:
        """
        Audits a draft against a specific regulation.
        """
        
        # 1. Define the Task
        task = f"""
        Audit the following regulatory draft against Regulation {regulation_code}.
        
        Draft Content:
        "{draft_text}"        
        Risk Tolerance: {risk_tolerance}
        """
        
        task += "\n\nProvide a detailed compliance report listing any potential violations, missing citations, or promotional language."

        # 2. Define Success Criteria for the Critic
        criteria = [
            f"Identify at least one potential risk based on {regulation_code} (if applicable).",
            "Flag any promotional or non-objective language.",
            "Verify that claims are substantiable (simulated check).",
            "Output must be a structured list of findings."
        ]
        
        # 3. Execute Self-Correction Loop
        print(f"--- ComplianceCheckAgent: Auditing against {regulation_code} ---")
        result = self.auditor.run_cycle(task, criteria, max_iterations=2)
        
        return {
            "status": "success",
            "regulation": regulation_code,
            "final_report": result["final_output"],
            "iterations": result["iterations"],
            "history": result["history"]
        }

def _demo():
    agent = ComplianceCheckAgent()
    
    # Mock Data
    draft = """
    Our new drug, SuperCure, is the best treatment ever created for headaches. 
    It works instantly and has zero side effects. Everyone loves it!
    """
    reg = "FDA 21 CFR 202.1 (Promotional Labeling)"
    
    response = agent.audit_draft(
        draft_text=draft,
        regulation_code=reg,
        risk_tolerance="Zero"
    )
    
    print("=== COMPLIANCE AUDIT REPORT ===")
    print(response["final_report"])

if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
