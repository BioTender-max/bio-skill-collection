# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import argparse
import json
from typing import List, Dict, Tuple, Any

class DrugInteractionChecker:
    """
    Checks for drug-drug interactions using a local knowledge base.
    """
    
    def __init__(self):
        # Mock DDI Database
        # Key: tuple(sorted(drug_pair)), Value: Interaction Details
        self.ddi_db = {
            ("aspirin", "warfarin"): {
                "severity": "Major",
                "mechanism": "Pharmacodynamic synergism",
                "effect": "Increased risk of bleeding.",
                "recommendation": "Avoid concurrent use or monitor INR closely."
            },
            ("lisinopril", "potassium chloride"): {
                "severity": "Major",
                "mechanism": "Additive hyperkalemic effect",
                "effect": "Risk of severe hyperkalemia.",
                "recommendation": "Monitor serum potassium."
            },
            ("atorvastatin", "clarithromycin"): {
                "severity": "Major",
                "mechanism": "CYP3A4 inhibition",
                "effect": "Increased risk of myopathy/rhabdomyolysis.",
                "recommendation": "Avoid combination or limit statin dose."
            },
            ("sildenafil", "nitroglycerin"): {
                "severity": "Severe/Contraindicated",
                "mechanism": "Vasodilation synergism",
                "effect": "Profound hypotension.",
                "recommendation": "Contraindicated."
            }
        }

    def check(self, drugs: List[str]) -> Dict[str, Any]:
        drugs = [d.lower().strip() for d in drugs]
        interactions = []
        
        # Check all pairs
        for i in range(len(drugs)):
            for j in range(i + 1, len(drugs)):
                pair = tuple(sorted((drugs[i], drugs[j])))
                
                if pair in self.ddi_db:
                    info = self.ddi_db[pair]
                    interactions.append({
                        "drug_1": pair[0],
                        "drug_2": pair[1],
                        "severity": info["severity"],
                        "effect": info["effect"],
                        "recommendation": info["recommendation"]
                    })
        
        return {
            "input_drugs": drugs,
            "interaction_count": len(interactions),
            "interactions": interactions,
            "status": "Safe" if len(interactions) == 0 else "Alert"
        }

def main():
    parser = argparse.ArgumentParser(description="Drug Interaction Checker")
    parser.add_argument("--drugs", type=str, required=True, help="Comma-separated list of drugs (e.g. 'Warfarin, Aspirin')")
    
    args = parser.parse_args()
    
    drug_list = args.drugs.split(",")
    checker = DrugInteractionChecker()
    result = checker.check(drug_list)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
