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
from typing import Dict, Any

# Adjust path to find platform module
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../platform")))

try:
    from optimizer.meta_prompter import PromptOptimizer, ModelTarget
except ImportError:
    # Fallback
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../platform")))
    from optimizer.meta_prompter import PromptOptimizer, ModelTarget

class OpentronsGenerator:
    """
    Generates executable Python code for Opentrons robots based on a structured JSON protocol.
    Uses LLMs to bridge the gap between high-level intent and low-level API calls.
    """

    def __init__(self):
        self.optimizer = PromptOptimizer()

    def generate_code(self, protocol_json: Dict[str, Any]) -> str:
        """
        Converts a JSON protocol definition into an Opentrons Python script.
        """
        
        # 1. Construct Prompt
        json_str = json.dumps(protocol_json, indent=2)
        
        raw_prompt = f"""
        Role: Lab Automation Engineer.
        Task: Write a complete Python script for the Opentrons OT-2 API v2.
        
        Input Protocol (JSON):
        {json_str}
        
        Requirements:
        - Use 'opentrons.protocol_api'.
        - Include a 'run(protocol: protocol_api.ProtocolContext)' function.
        - Load labware as specified in the 'labware' section.
        - Implement the 'steps' logic using p300_single_gen2 or similar pipettes.
        - Add comments explaining each step.
        - Return ONLY the Python code.
        """
        
        # 2. Optimize
        optimized_prompt = self.optimizer.optimize(raw_prompt, ModelTarget.CLAUDE)
        
        # 3. Simulate LLM Generation (Mocking for Demo)
        # In production: response = adapter.generate(optimized_prompt)
        print(f"--- OpentronsGenerator: Generating code for '{protocol_json.get('metadata', {}).get('name')}' ---")
        return self._mock_generation(protocol_json)

    def _mock_generation(self, protocol_json: Dict) -> str:
        """
        Mock logic to produce a valid-looking script for the demo without a real LLM.
        """
        name = protocol_json.get('metadata', {}).get('name', 'Protocol')
        steps = protocol_json.get('steps', [])
        
        code = f'''from opentrons import protocol_api

metadata = {{
    'protocolName': '{name}',
    'author': 'Opentrons Agent',
    'apiLevel': '2.13'
}}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    
    # Pipettes
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
    
    # Execution
    protocol.comment("Starting {name}")
'''
        
        for i, step in enumerate(steps):
            action = step.get('action')
            if action == 'transfer':
                vol = step.get('volume', 0)
                src = step.get('source', 'A1')
                dst = step.get('dest', 'B1')
                code += f'''
    # Step {i+1}: Transfer {vol}uL from {src} to {dst}
    p300.transfer({vol}, plate['{src}'], plate['{dst}'])
'''
            elif action == 'distribute_mastermix':
                vol = step.get('volume', 0)
                code += f'''
    # Step {i+1}: Distribute Mastermix
    p300.distribute({vol}, plate['A1'], plate.columns()[1])
'''
        
        return code

if __name__ == "__main__":
    # Test Integration with ExperimentDesigner output
    generator = OpentronsGenerator()
    
    mock_protocol = {
        "metadata": {"name": "Gradient Test", "robot": "OT2"},
        "labware": {"plate": "corning_96"},
        "steps": [
            {"action": "transfer", "source": "A1", "dest": "A2", "volume": 50},
            {"action": "transfer", "source": "A1", "dest": "A3", "volume": 100}
        ]
    }
    
    script = generator.generate_code(mock_protocol)
    print("\n>>> Generated Python Code:\n")
    print(script)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
