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
import numpy as np
from typing import Dict, Any, List

# Adjust path to find platform module
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
platform_dir = os.path.join(project_root, "platform")

if platform_dir not in sys.path:
    sys.path.append(platform_dir)

from adapters.runtime_adapter import llm

class ArrhythmiaDetector:
    """
    Simulates an intelligent ECG analysis agent.
    Combines 'signal processing' (numpy) with 'medical reasoning' (LLM).
    """

    def __init__(self):
        # Simulated classifier classes
        self.classes = {
            0: "Normal Sinus Rhythm",
            1: "Atrial Fibrillation",
            2: "Ventricular Tachycardia",
            3: "Noise/Artifact"
        }

    def analyze_ecg(self, ecg_signal: List[float], sampling_rate: int = 250) -> Dict[str, Any]:
        """
        Analyzes a raw ECG signal array.
        """
        # 1. Signal Processing (Mock Feature Extraction)
        # In real life: peaks, _ = scipy.signal.find_peaks(ecg_signal)
        # Here we just look at simple stats
        
        avg_voltage = np.mean(ecg_signal)
        max_voltage = np.max(ecg_signal)
        variance = np.var(ecg_signal)
        
        # Mock Classification Logic based on Variance
        # High variance -> likely Tachycardia or Artifact
        # Low/Steady -> Normal
        
        if variance > 2.0:
            predicted_class = 2 # VTach
        elif variance > 1.0:
            predicted_class = 1 # AFib
        else:
            predicted_class = 0 # Normal
            
        classification = self.classes[predicted_class]
        
        # 2. Semantic Analysis (LLM)
        # Generate a clinical report based on the "calculated" features.
        
        context = f"""
        ECG Analysis Results:
        - Classification: {classification}
        - Avg Voltage: {avg_voltage:.2f} mV
        - Max Voltage: {max_voltage:.2f} mV
        - Signal Variance: {variance:.2f}
        """
        
        prompt = f"""
        Act as a Cardiologist. 
        Context: {context}
        
        Task: Write a brief 1-sentence finding for the medical record and recommend next steps.
        """
        
        report = llm.complete("You are a cardiologist.", prompt)
        
        return {
            "status": "success",
            "classification": classification,
            "features": {
                "avg": float(avg_voltage),
                "max": float(max_voltage),
                "var": float(variance)
            },
            "clinical_report": report
        }

if __name__ == "__main__":
    detector = ArrhythmiaDetector()
    
    # 1. Normal Heartbeat Simulation (Sine wave)
    t = np.linspace(0, 10, 500)
    normal_ecg = np.sin(t)
    print("\n--- Test 1: Normal Rhythm ---")
    print(json.dumps(detector.analyze_ecg(normal_ecg.tolist()), indent=2))
    
    # 2. Arrhythmia Simulation (Random noise added)
    arrhythmia_ecg = np.sin(t) + np.random.normal(0, 1.5, 500)
    print("\n--- Test 2: Arrhythmia/Noise ---")
    print(json.dumps(detector.analyze_ecg(arrhythmia_ecg.tolist()), indent=2))

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
