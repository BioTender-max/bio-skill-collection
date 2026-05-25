# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import json
import statistics
from typing import List, Dict, Any

# Consumer Health Copilot
# Focus: OpenAI "ChatGPT Health" Use Case
# Capabilities: Interprets JSON health dumps, finds trends, gives actionable advice.

class HealthCopilot:
    def __init__(self):
        self.alert_thresholds = {
            "resting_heart_rate_increase": 5, # bpm increase
            "sleep_score_decrease": 10        # percent decrease
        }

    def analyze_health_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingests user health JSON (e.g., from Apple Health export).
        Returns a structured insight report.
        """
        insights = []
        
        # 1. Heart Rate Analysis
        rhr_data = user_data.get("resting_heart_rate", [])
        if rhr_data:
            rhr_trend = self._analyze_trend(rhr_data)
            if rhr_trend["slope"] > 0 and rhr_trend["change"] > self.alert_thresholds["resting_heart_rate_increase"]:
                insights.append({
                    "type": "ALERT",
                    "metric": "Resting Heart Rate",
                    "message": f"Your RHR has increased by {rhr_trend['change']:.1f} bpm this week.",
                    "advice": "This can indicate stress, developing illness, or overtraining. Consider prioritizing sleep tonight."
                })
        
        # 2. Sleep Analysis
        sleep_data = user_data.get("sleep_quality_score", [])
        if sleep_data:
            sleep_trend = self._analyze_trend(sleep_data)
            if sleep_trend["slope"] < 0 and abs(sleep_trend["change"]) > self.alert_thresholds["sleep_score_decrease"]:
                insights.append({
                    "type": "WARNING",
                    "metric": "Sleep Quality",
                    "message": "Your sleep quality has dropped significantly.",
                    "advice": "Avoid caffeine after 2 PM and try to maintain a consistent bedtime."
                })

        return {
            "user_id": user_data.get("user_id"),
            "insights": insights,
            "summary": self._generate_summary(insights)
        }

    def _analyze_trend(self, data_points: List[float]) -> Dict[str, float]:
        """Simple linear regression slope to detect trend direction."""
        if len(data_points) < 2:
            return {"slope": 0, "change": 0}
        
        first_avg = statistics.mean(data_points[:3]) if len(data_points) >= 3 else data_points[0]
        last_avg = statistics.mean(data_points[-3:]) if len(data_points) >= 3 else data_points[-1]
        
        change = last_avg - first_avg
        slope = change / len(data_points)
        
        return {"slope": slope, "change": change}

    def _generate_summary(self, insights: List[Dict]) -> str:
        if not insights:
            return "Your health metrics look stable. Keep up the good work!"
        
        # OpenAI-style concise summary
        alert_count = len([i for i in insights if i["type"] == "ALERT"])
        return f"I found {len(insights)} potential issues in your recent data ({alert_count} Alerts). See details below."

if __name__ == "__main__":
    copilot = HealthCopilot()
    
    # Mock Data (Apple Health Style)
    mock_data = {
        "user_id": "user_123",
        "resting_heart_rate": [60, 61, 60, 62, 64, 65, 66], # Rising trend
        "sleep_quality_score": [85, 82, 80, 75, 70, 65, 60] # Falling trend
    }
    
    report = copilot.analyze_health_data(mock_data)
    print(json.dumps(report, indent=2))

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
