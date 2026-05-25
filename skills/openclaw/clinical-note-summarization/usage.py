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
Clinical Note Summarization Demo (2026 Update)

Demonstrates the use of 'MedPrompt' patterns (Chain-of-Thought, Verification)
to summarize clinical text safely.
"""

import sys
import os

# Ensure we can import the utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from medprompt_utils import MedPromptEngine
    HAS_UTILS = True
except ImportError:
    HAS_UTILS = False

def run_demo():
    if not HAS_UTILS:
        print("Error: medprompt_utils.py not found.")
        return

    engine = MedPromptEngine()
    
    # Input Note
    clinical_note = """
    HISTORY OF PRESENT ILLNESS:
    Patient is a 65-year-old female presenting with 3 days of worsening shortness of breath.
    She has a history of COPD and HFpEF. Denies chest pain. 
    
    PHYSICAL EXAM:
    Lungs: Wheezing bilaterally.
    Heart: Regular rate and rhythm. 2+ pitting edema in lower extremities.
    
    PLAN:
    1. Lasix 40mg IV.
    2. Duonebs q4h.
    3. Admit to Medicine.
    """
    
    print("=== Clinical Note Summarization Pipeline ===\n")
    
    # Step 1: Generate Reasoning Prompt
    print("--- Step 1: Generating Chain-of-Thought Prompt ---")
    cot_prompt = engine.generate_chain_of_thought_prompt(
        task="Summarize admission reason and plan.",
        clinical_text=clinical_note
    )
    print(cot_prompt)
    
    # Simulate LLM Response (Mock)
    mock_cot_response = """
    [Reasoning]
    Patient has SOB, history of HFpEF, and edema. 
    Lasix is for heart failure. Duonebs for COPD/wheezing.
    Admission is for exacerbation of both.
    
    [Final Output]
    65F admitted for COPD/HF exacerbation. Plan: IV Diuretics and Bronchodilators.
    """
    print("\n[Simulated LLM Output]:")
    print(mock_cot_response)
    
    # Step 2: Verification
    print("\n--- Step 2: Generating Verification Prompt ---")
    verify_prompt = engine.chain_of_verification(
        initial_response=mock_cot_response,
        clinical_text=clinical_note
    )
    print(verify_prompt)
    
    # Step 3: FHIR Formatting
    print("\n--- Step 3: FHIR Structured Output ---")
    fhir_json = engine.format_as_fhir_json({
        "patient_age": 65,
        "diagnosis": "COPD/HF Exacerbation"
    })
    print(fhir_json)

if __name__ == "__main__":
    run_demo()
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
