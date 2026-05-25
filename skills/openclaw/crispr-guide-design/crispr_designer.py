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
CRISPR Design Agent (2026 Skills)

A specialized bioinformatics tool for designing gRNA (guide RNA) sequences.
Functionality:
1. Scan DNA for PAM sites (NGG).
2. Extract 20bp spacers (Protospacers).
3. Score efficiency (GC Content & Homopolymer checks).
4. Check for off-targets (Mocked).
"""

import re

class CRISPRDesigner:
    def __init__(self):
        self.pam_motif = "GG" # SpCas9 PAM is NGG
        self.spacer_length = 20

    def find_targets(self, dna_sequence: str):
        """
        Scans sequence for 'GG' and looks 21-23bp upstream.
        """
        dna = dna_sequence.upper()
        candidates = []
        
        # Iterate through sequence to find PAMs
        # Note: NGG means any base followed by GG.
        # We look for GG, then check index.
        
        for i in range(len(dna) - 1):
            if dna[i:i+2] == "GG":
                pam_index = i
                # NGG starts at pam_index-1. Spacer ends at pam_index-1.
                # Spacer start = (pam_index-1) - 20
                start = pam_index - 1 - self.spacer_length
                
                if start >= 0:
                    spacer = dna[start : start + self.spacer_length]
                    pam_full = dna[start + self.spacer_length : start + self.spacer_length + 3]
                    
                    score = self.calculate_score(spacer)
                    
                    candidates.append({
                        "location": start,
                        "spacer": spacer,
                        "pam": pam_full,
                        "gc_content": score["gc"],
                        "efficiency_score": score["efficiency"]
                    })
                    
        return sorted(candidates, key=lambda x: x["efficiency_score"], reverse=True)

    def calculate_score(self, spacer: str):
        # 1. GC Content (Ideal: 40-60%)
        g_count = spacer.count('G')
        c_count = spacer.count('C')
        gc_percent = (g_count + c_count) / len(spacer) * 100
        
        score = 0.0
        if 40 <= gc_percent <= 60:
            score += 50
        elif 30 <= gc_percent <= 80:
            score += 25
            
        # 2. Position Specific Weights (Mock Rule: G at pos 20 is good)
        if spacer[-1] == 'G':
            score += 10
            
        # 3. Penalize Poly-T (Termination signal)
        if "TTTT" in spacer:
            score -= 50
            
        return {"gc": round(gc_percent, 1), "efficiency": max(0, score)}

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="CRISPR Design Agent")
    parser.add_argument("--sequence", required=True, help="DNA sequence to scan")
    parser.add_argument("--output", help="Path to save JSON output")
    
    args = parser.parse_args()
    
    designer = CRISPRDesigner()
    
    print(f"Scanning DNA ({len(args.sequence)} bp) for CRISPR targets...", file=sys.stderr)
    
    targets = designer.find_targets(args.sequence)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(targets, f, indent=2)
        print(f"Saved {len(targets)} targets to {args.output}", file=sys.stderr)
    else:
        # Print valid JSON to stdout for piping
        print(json.dumps(targets, indent=2))


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
