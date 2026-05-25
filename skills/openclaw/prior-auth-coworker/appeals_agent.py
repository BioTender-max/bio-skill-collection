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

class PriorAuthAppealsAgent:
    """
    Agent focused on overturning Prior Authorization denials.
    Uses 'Self-Correction' to iteratively refine the legal/clinical argument.
    """

    def __init__(self):
        self.corrector = SelfCorrectionAgent()

    def draft_appeal(self, 
                     patient_id: str,
                     denial_reason: str, 
                     clinical_context: str, 
                     payer_policy: Optional[str] = None) -> Dict[str, Any]:
        """
        Drafts a formal appeal letter.
        """
        
        # 1. Define the Task
        task = f"""
        Draft a Prior Authorization Appeal Letter for Patient {patient_id}.
        
        The denial reason was: "{denial_reason}"
        
        The patient's clinical context is:
        {clinical_context}
        """
        
        if payer_policy:
            task += f"\n\nRelevant Payer Policy: {payer_policy}"
            
        task += "\n\nThe letter must be professional, firm, and cite specific clinical evidence."

        # 2. Define Success Criteria for the Critic
        criteria = [
            "Address the specific denial reason directly.",
            "Cite clinical values (e.g., HbA1c, ejection fraction) from context.",
            "Maintain a professional tone.",
            "Include a clear 'Call to Action' (e.g., 'Please reverse this decision')."
        ]
        
        if payer_policy:
            criteria.append("Reference the specific Payer Policy section.")

        # 3. Execute Self-Correction Loop
        print(f"--- PriorAuthAppealsAgent: Processing Appeal for {patient_id} ---")
        result = self.corrector.run_cycle(task, criteria, max_iterations=2)
        
        return {
            "status": "success",
            "patient_id": patient_id,
            "final_draft": result["final_output"],
            "iterations": result["iterations"],
            "history": result["history"]
        }

def _demo():
    agent = PriorAuthAppealsAgent()
    
    # Mock Data
    denial = "Medical necessity not established. Patient has not tried and failed Metformin."
    context = """
    Patient: John Doe (DOB: 01/01/1980)
    Diagnosis: Type 2 Diabetes
    Current Meds: None.
    History: 
    - Diagnosed 2023.
    - CKD Stage 4 (eGFR 25).
    - Contraindication: Metformin is contraindicated due to renal impairment.
    """
    policy = "Policy 101: GLP-1 agonists require step therapy with Metformin, unless contraindicated."
    
    response = agent.draft_appeal(
        patient_id="PT-12345",
        denial_reason=denial,
        clinical_context=context,
        payer_policy=policy
    )
    
    print("=== FINAL APPEAL DRAFT ===")
    print(response["final_draft"])
    print("\n=== DEBUG: REVISION HISTORY ===")
    print(json.dumps(response["history"], indent=2))

if __name__ == "__main__":
    _demo()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
