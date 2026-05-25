# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

"Enhanced (Jan 2026) with AI-generated Clinical Reports."

import argparse
import json
import sys
import os

# Path adjustment for platform modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
platform_dir = os.path.join(project_root, "platform")

if platform_dir not in sys.path:
    sys.path.append(platform_dir)

try:
    from adapters.runtime_adapter import llm
except ImportError:
    print("Warning: RuntimeLLMAdapter not found. Reports will be basic.")
    llm = None

try:
    from optimizer.meta_prompter import PromptOptimizer, ModelTarget
except ImportError:
    PromptOptimizer = None

class ACMGClassifier:
    def __init__(self):
        # Weights for Pathogenicity
        self.p_weights = {
            "PVS1": 8,  # Very Strong
            "PS1": 4, "PS2": 4, "PS3": 4, "PS4": 4, # Strong
            "PM1": 2, "PM2": 2, "PM3": 2, "PM4": 2, "PM5": 2, "PM6": 2, # Moderate
            "PP1": 1, "PP2": 1, "PP3": 1, "PP4": 1, "PP5": 1 # Supporting
        }
        
        # Weights for Benign
        self.b_weights = {
            "BA1": 8, # Stand-alone
            "BS1": 4, "BS2": 4, "BS3": 4, "BS4": 4, # Strong
            "BP1": 1, "BP2": 1, "BP3": 1, "BP4": 1, "BP5": 1, "BP6": 1 # Supporting
        }

    def classify(self, evidence_codes: list):
        p_score = 0
        b_score = 0
        
        applied_codes = []
        
        for code in evidence_codes:
            code = code.upper().strip()
            if code in self.p_weights:
                p_score += self.p_weights[code]
                applied_codes.append({"code": code, "type": "Pathogenic", "weight": self.p_weights[code]})
            elif code in self.b_weights:
                b_score += self.b_weights[code]
                applied_codes.append({"code": code, "type": "Benign", "weight": self.b_weights[code]})
            else:
                print(f"Warning: Unknown code {code}", file=sys.stderr)

        # Simplified Scoring Logic
        verdict = "Uncertain Significance (VUS)"
        
        # Pathogenic logic (Approximation)
        if "PVS1" in evidence_codes:
            if p_score >= 10: verdict = "Pathogenic"
            elif p_score >= 9: verdict = "Likely Pathogenic"
        elif p_score >= 12: # e.g. 3 Strong
            verdict = "Pathogenic"
        elif p_score >= 6:
            verdict = "Likely Pathogenic"
            
        # Benign logic
        if "BA1" in evidence_codes:
            verdict = "Benign"
        elif b_score >= 8: # 2 Strong
            verdict = "Benign"
        elif b_score >= 4:
            verdict = "Likely Benign"
            
        return {
            "verdict": verdict,
            "pathogenicity_score": p_score,
            "benign_score": b_score,
            "evidence_applied": applied_codes
        }

    def generate_report(self, variant_name: str, classification_result: dict) -> str:
        """
        Generates a clinical report draft using RuntimeLLMAdapter.
        """
        if not llm:
            return "AI Report Generation unavailable."

        context = json.dumps(classification_result, indent=2)
        
        # Use Meta-Prompter logic if we wanted, but let's keep it simple for RuntimeAdapter
        prompt = f"""
        Task: Write a clinical genetic report section for variant {variant_name}.
        
        Classification Result:
        {context}
        
        Requirements:
        - State the final verdict clearly.
        - Explain the evidence codes used (e.g., PVS1 means null variant...). 
        - Provide a recommendation for genetic counseling.
        - Professional clinical tone.
        """
        
        return llm.complete("You are a clinical geneticist.", prompt)

    def _format_evidence_text(self, evidence_list):
        return "\n".join([f"- {item['code']} ({item['type']})" for item in evidence_list])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACMG Variant Classifier")
    parser.add_argument("--evidence", required=True, help="Comma-separated list of codes (e.g., PVS1,PM2)")
    parser.add_argument("--variant", default="Unknown Variant", help="Name of the variant (e.g., BRCA1 c.123G>A)")
    parser.add_argument("--output", help="Path to save JSON output")
    parser.add_argument("--report", action="store_true", help="Generate text report")
    
    args = parser.parse_args()
    
    codes = args.evidence.split(",")
    classifier = ACMGClassifier()
    result = classifier.classify(codes)
    
    if args.report:
        print(classifier.generate_report(args.variant, result))
    else:
        print(json.dumps(result, indent=2))
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
