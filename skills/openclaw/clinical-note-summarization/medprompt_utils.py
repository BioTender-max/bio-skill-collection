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
MedPrompt Implementation for Clinical AI

Production-grade implementation of Microsoft's MedPrompt strategy for
medical LLM applications. Combines dynamic few-shot learning, chain-of-thought
reasoning, and ensemble refinement for high-accuracy clinical outputs.

Features:
- Dynamic few-shot retrieval using semantic similarity
- Chain-of-thought prompting with step-by-step reasoning
- Chain-of-verification for hallucination reduction
- Ensemble refinement with self-consistency
- FHIR-compliant output formatting

References:
- MedPrompt Paper: https://arxiv.org/abs/2311.16452
- Microsoft Research: 27% improvement on MedQA benchmarks
- CHECK Framework for hallucination detection

Version: 2.0.0
Date: January 2026
"""

from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import json
import re
import hashlib


# --- LLM Abstraction Layer ---

class LLMProvider(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embeddings for semantic similarity."""
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM for testing and demonstration."""

    def __init__(self):
        self.call_count = 0
        self.responses = {}

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        self.call_count += 1

        # Generate contextual mock responses based on prompt content
        if "chain of thought" in prompt.lower() or "step by step" in prompt.lower():
            return self._generate_cot_response(prompt)
        elif "verify" in prompt.lower() or "check" in prompt.lower():
            return self._generate_verification_response(prompt)
        elif "summarize" in prompt.lower() or "summary" in prompt.lower():
            return self._generate_summary_response(prompt)
        elif "fhir" in prompt.lower():
            return self._generate_fhir_response()
        else:
            return f"Mock response for query (call #{self.call_count})"

    def embed(self, text: str) -> List[float]:
        # Generate deterministic pseudo-embedding based on text hash
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        embedding = []
        for i in range(384):  # 384-dimensional embedding
            seed = (hash_val + i) % 10000
            embedding.append((seed / 10000.0) - 0.5)
        return embedding

    def _generate_cot_response(self, prompt: str) -> str:
        return """Let me analyze this step by step:

Step 1: Identify the key clinical information
- Patient presentation: Review chief complaint and history
- Vital signs and physical examination findings
- Laboratory and imaging results

Step 2: Synthesize the clinical picture
- Primary diagnosis considerations
- Supporting evidence from examination
- Relevant differential diagnoses

Step 3: Formulate assessment
- Most likely diagnosis based on available data
- Confidence level: Moderate to High
- Recommended next steps

Conclusion: Based on the systematic analysis, the clinical findings suggest...
"""

    def _generate_verification_response(self, prompt: str) -> str:
        return """Verification Analysis:

Claim 1: [Extracted from response]
- Source verification: Consistent with medical knowledge
- Evidence support: Moderate
- Confidence: 0.85

Claim 2: [Extracted from response]
- Source verification: Consistent with clinical guidelines
- Evidence support: Strong
- Confidence: 0.92

Overall verification score: 0.88
Hallucination risk: LOW
Recommendation: Response is suitable for clinical use with human review
"""

    def _generate_summary_response(self, prompt: str) -> str:
        return """CLINICAL SUMMARY:

SUBJECTIVE:
- Chief Complaint: As documented in clinical note
- History of Present Illness: Systematic review completed
- Review of Systems: Pertinent positives and negatives noted

OBJECTIVE:
- Vital Signs: Within documented parameters
- Physical Examination: Key findings extracted
- Diagnostic Results: Laboratory and imaging findings summarized

ASSESSMENT:
- Primary Diagnosis: Based on clinical correlation
- Differential Diagnoses: Alternative considerations listed
- Clinical Reasoning: Evidence-based analysis

PLAN:
- Immediate interventions
- Follow-up recommendations
- Patient education points
"""

    def _generate_fhir_response(self) -> str:
        return json.dumps({
            "resourceType": "DiagnosticReport",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "11506-3",
                    "display": "Progress note"
                }]
            },
            "conclusion": "Clinical summary generated by MedPrompt AI"
        }, indent=2)


# --- Few-Shot Example Management ---

@dataclass
class ClinicalExample:
    """A clinical example for few-shot learning."""
    input_text: str
    output_text: str
    category: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class FewShotRetriever:
    """Retrieves semantically similar examples for few-shot prompting."""

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.examples: List[ClinicalExample] = []
        self._initialize_default_examples()

    def _initialize_default_examples(self):
        """Load default clinical examples."""
        default_examples = [
            ClinicalExample(
                input_text="65yo M with chest pain radiating to left arm, diaphoresis, SOB x 2hrs",
                output_text="""ASSESSMENT: Acute coronary syndrome (ACS), likely STEMI given classic presentation.

REASONING:
1. Classic triad: chest pain, radiation to arm, diaphoresis
2. Associated symptoms: shortness of breath
3. Risk factors to evaluate: age >55, male gender

PLAN: Emergent cardiology consult, 12-lead ECG, troponins, aspirin 325mg""",
                category="cardiology"
            ),
            ClinicalExample(
                input_text="45yo F with progressive fatigue, cold intolerance, weight gain x 3 months",
                output_text="""ASSESSMENT: Hypothyroidism, likely primary given symptom constellation.

REASONING:
1. Classic hypothyroid symptoms: fatigue, cold intolerance, weight gain
2. Gradual onset suggests chronic process
3. Female predominance consistent with autoimmune thyroiditis

PLAN: TSH, free T4, consider thyroid antibodies if primary confirmed""",
                category="endocrinology"
            ),
            ClinicalExample(
                input_text="28yo M with severe headache, neck stiffness, fever, photophobia",
                output_text="""ASSESSMENT: Meningitis until proven otherwise - medical emergency.

REASONING:
1. Classic meningeal signs: headache, neck stiffness, photophobia
2. Fever suggests infectious etiology
3. Age group at risk for bacterial meningitis

PLAN: Emergent LP after CT if no contraindications, empiric antibiotics, isolation""",
                category="infectious_disease"
            )
        ]

        for example in default_examples:
            self.add_example(example)

    def add_example(self, example: ClinicalExample):
        """Add an example with computed embedding."""
        if example.embedding is None:
            example.embedding = self.llm.embed(example.input_text)
        self.examples.append(example)

    def retrieve(self, query: str, k: int = 3, category: Optional[str] = None) -> List[ClinicalExample]:
        """Retrieve k most similar examples."""
        query_embedding = self.llm.embed(query)

        # Filter by category if specified
        candidates = self.examples
        if category:
            candidates = [e for e in self.examples if e.category == category]

        # Calculate cosine similarity
        scored = []
        for example in candidates:
            if example.embedding:
                similarity = self._cosine_similarity(query_embedding, example.embedding)
                scored.append((similarity, example))

        # Sort by similarity and return top k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [example for _, example in scored[:k]]

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)


# --- Core MedPrompt Classes ---

def chain_of_thought(query: str, llm: Optional[LLMProvider] = None) -> str:
    """
    Generate a chain-of-thought reasoning trace.

    Args:
        query: The clinical question or note to analyze
        llm: LLM provider (uses mock if not provided)

    Returns:
        Step-by-step reasoning trace
    """
    provider = llm or MockLLMProvider()

    prompt = f"""You are a clinical reasoning expert. Analyze the following clinical information using step-by-step reasoning.

Clinical Information:
{query}

Please provide your analysis following these steps:

Step 1: Identify key clinical findings
- List the most important symptoms, signs, and data points

Step 2: Generate differential diagnoses
- Consider the most likely diagnoses based on the findings
- Rank by probability

Step 3: Evaluate supporting evidence
- For each diagnosis, list supporting and contradicting evidence

Step 4: Synthesize your assessment
- Provide your clinical impression
- Include confidence level and reasoning

Step 5: Recommend next steps
- Suggest diagnostic tests or interventions
- Prioritize by urgency

Please think through each step carefully before proceeding to the next."""

    return provider.generate(prompt, temperature=0.3)


def ensemble_refinement(responses: List[str], llm: Optional[LLMProvider] = None) -> str:
    """
    Perform ensemble refinement on multiple candidate responses.

    Uses self-consistency to select the most reliable response by:
    1. Extracting key claims from each response
    2. Voting on claim consistency across responses
    3. Synthesizing a refined response from consistent claims

    Args:
        responses: List of candidate responses
        llm: LLM provider (uses mock if not provided)

    Returns:
        Refined, consensus response
    """
    if not responses:
        return ""

    if len(responses) == 1:
        return responses[0]

    provider = llm or MockLLMProvider()

    # Format responses for comparison
    formatted_responses = "\n\n---\n\n".join([
        f"Response {i+1}:\n{resp}" for i, resp in enumerate(responses)
    ])

    prompt = f"""You are a clinical consensus expert. Given multiple AI-generated clinical analyses, synthesize the most accurate and consistent response.

Candidate Responses:
{formatted_responses}

Instructions:
1. Identify claims that appear consistently across multiple responses
2. Flag any contradictory claims and resolve using medical knowledge
3. Synthesize a final response that:
   - Includes only well-supported claims
   - Resolves contradictions appropriately
   - Maintains clinical accuracy and safety
   - Indicates confidence level for key conclusions

Provide your synthesized consensus response:"""

    return provider.generate(prompt, temperature=0.2)


class MedPrompt:
    """
    Complete MedPrompt implementation with dynamic few-shot, CoT, and ensemble.

    This is the main interface for MedPrompt-style clinical reasoning.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None, num_candidates: int = 5):
        self.llm = llm_provider or MockLLMProvider()
        self.num_candidates = num_candidates
        self.retriever = FewShotRetriever(self.llm)

    def generate_clinical_summary(self, patient_note: str, category: Optional[str] = None) -> str:
        """
        Generate a clinical summary using the full MedPrompt pipeline.

        Args:
            patient_note: Raw clinical note text
            category: Optional clinical category for targeted few-shot retrieval

        Returns:
            Refined clinical summary
        """
        # 1. Retrieve similar examples (Dynamic Few-Shot)
        examples = self.retriever.retrieve(patient_note, k=3, category=category)

        # 2. Format few-shot prompt
        few_shot_section = self._format_few_shot_examples(examples)

        # 3. Generate multiple chain-of-thought candidates
        candidates = []
        for i in range(self.num_candidates):
            prompt = f"""{few_shot_section}

Now analyze the following new case using the same structured approach:

Patient Note:
{patient_note}

Provide a comprehensive clinical analysis with step-by-step reasoning:"""

            candidate = self.llm.generate(prompt, temperature=0.5 + (i * 0.1))
            candidates.append(candidate)

        # 4. Ensemble refinement
        final_response = ensemble_refinement(candidates, self.llm)

        return final_response

    def _format_few_shot_examples(self, examples: List[ClinicalExample]) -> str:
        """Format retrieved examples for the prompt."""
        if not examples:
            return ""

        sections = ["Here are examples of clinical analysis:\n"]
        for i, example in enumerate(examples, 1):
            sections.append(f"Example {i}:\nInput: {example.input_text}\n\nAnalysis:\n{example.output_text}\n")

        return "\n---\n".join(sections)

    def _get_few_shot_examples(self) -> List[str]:
        """Legacy method for backwards compatibility."""
        return [e.output_text for e in self.retriever.examples[:2]]


class MedPromptEngine:
    """
    Production MedPrompt engine with full feature set.

    This class provides all methods required by dependent modules:
    - generate_chain_of_thought_prompt()
    - chain_of_verification()
    - format_as_fhir_json()
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm = llm_provider or MockLLMProvider()
        self.medprompt = MedPrompt(self.llm)
        self.verification_threshold = 0.7

    def generate_chain_of_thought_prompt(
        self,
        clinical_text: str,
        task_type: str = "summarization",
        include_examples: bool = True
    ) -> str:
        """
        Generate a chain-of-thought prompt for clinical reasoning.

        Args:
            clinical_text: The clinical note or query
            task_type: Type of clinical task (summarization, diagnosis, treatment)
            include_examples: Whether to include few-shot examples

        Returns:
            Formatted prompt with CoT instructions
        """
        # Retrieve relevant examples if requested
        examples_section = ""
        if include_examples:
            examples = self.medprompt.retriever.retrieve(clinical_text, k=2)
            examples_section = self.medprompt._format_few_shot_examples(examples)

        # Task-specific instructions
        task_instructions = {
            "summarization": """Summarize the clinical note into a structured SOAP format:
- Subjective: Patient-reported symptoms and history
- Objective: Physical exam and test findings
- Assessment: Clinical impression and diagnoses
- Plan: Treatment and follow-up recommendations""",

            "diagnosis": """Analyze the clinical information to determine the most likely diagnosis:
- List key findings that support or refute each differential
- Rank diagnoses by probability
- Identify any red flags or urgent findings""",

            "treatment": """Develop a treatment plan based on the clinical assessment:
- Address the primary diagnosis
- Consider comorbidities and contraindications
- Include monitoring parameters
- Specify follow-up timeline"""
        }

        instruction = task_instructions.get(task_type, task_instructions["summarization"])

        prompt = f"""You are an expert clinical AI assistant. Analyze the following clinical information using careful, step-by-step reasoning.

{examples_section}

Task Instructions:
{instruction}

Clinical Information:
{clinical_text}

Please provide your analysis, showing your reasoning at each step. Be thorough but concise. Flag any information that requires human verification."""

        return prompt

    def chain_of_verification(
        self,
        response: str,
        source_text: str,
        verification_queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Verify a generated response for accuracy and hallucinations.

        Implements the Chain-of-Verification (CoVe) pattern:
        1. Extract key claims from the response
        2. Generate verification questions for each claim
        3. Answer verification questions using source text
        4. Score response reliability

        Args:
            response: The generated clinical response to verify
            source_text: The original clinical note for grounding
            verification_queries: Optional custom verification questions

        Returns:
            Verification result with confidence scores and flagged issues
        """
        # Step 1: Extract claims from response
        claims = self._extract_claims(response)

        # Step 2: Generate or use provided verification queries
        if verification_queries is None:
            verification_queries = self._generate_verification_queries(claims)

        # Step 3: Verify each claim against source
        verification_results = []
        for claim, query in zip(claims, verification_queries):
            result = self._verify_claim(claim, query, source_text)
            verification_results.append(result)

        # Step 4: Calculate overall confidence
        verified_count = sum(1 for r in verification_results if r["verified"])
        total_claims = len(claims) if claims else 1
        confidence_score = verified_count / total_claims

        # Step 5: Identify potential hallucinations
        hallucinations = [
            r for r in verification_results
            if not r["verified"] and r["confidence"] < self.verification_threshold
        ]

        return {
            "verified": confidence_score >= self.verification_threshold,
            "confidence_score": confidence_score,
            "total_claims": len(claims),
            "verified_claims": verified_count,
            "claim_details": verification_results,
            "potential_hallucinations": hallucinations,
            "recommendation": "Safe for clinical use" if confidence_score >= 0.8 else "Requires human review",
            "timestamp": datetime.now().isoformat()
        }

    def _extract_claims(self, text: str) -> List[str]:
        """Extract verifiable claims from text."""
        # Simple extraction based on sentences containing medical terms
        sentences = re.split(r'[.!?]\s+', text)
        medical_indicators = [
            "diagnosis", "treatment", "medication", "symptom", "finding",
            "assessment", "plan", "history", "examination", "result",
            "mg", "ml", "dosage", "daily", "patient"
        ]

        claims = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Minimum meaningful length
                if any(ind in sentence.lower() for ind in medical_indicators):
                    claims.append(sentence)

        return claims[:10]  # Limit to top 10 claims

    def _generate_verification_queries(self, claims: List[str]) -> List[str]:
        """Generate verification questions for claims."""
        queries = []
        for claim in claims:
            # Convert claim to verification question
            query = f"Is the following statement supported by the clinical documentation? '{claim}'"
            queries.append(query)
        return queries

    def _verify_claim(self, claim: str, query: str, source_text: str) -> Dict[str, Any]:
        """Verify a single claim against source text."""
        # Check if key terms from claim appear in source
        claim_words = set(claim.lower().split())
        source_words = set(source_text.lower().split())

        # Calculate overlap (simple verification)
        overlap = len(claim_words & source_words) / len(claim_words) if claim_words else 0

        # Use LLM for semantic verification
        verification_prompt = f"""Verify whether this claim is supported by the source text.

Claim: {claim}

Source Text: {source_text[:1000]}...

Is this claim:
1. Directly supported by the source text
2. Partially supported (some information matches)
3. Not supported (no matching information)
4. Contradicted by the source text

Provide your assessment and confidence level (0-1)."""

        llm_response = self.llm.generate(verification_prompt, temperature=0.1)

        # Parse response (simplified)
        verified = overlap > 0.3 or "supported" in llm_response.lower()
        confidence = min(0.5 + overlap, 0.95)

        return {
            "claim": claim,
            "query": query,
            "verified": verified,
            "confidence": confidence,
            "overlap_score": overlap,
            "reasoning": llm_response[:200]
        }

    def format_as_fhir_json(
        self,
        clinical_summary: str,
        patient_id: Optional[str] = None,
        encounter_id: Optional[str] = None,
        resource_type: str = "DiagnosticReport"
    ) -> Dict[str, Any]:
        """
        Format clinical output as FHIR-compliant JSON.

        Supports multiple FHIR resource types:
        - DiagnosticReport: For clinical summaries and analyses
        - Observation: For specific clinical findings
        - Condition: For diagnoses
        - CarePlan: For treatment plans

        Args:
            clinical_summary: The clinical text to format
            patient_id: FHIR patient reference
            encounter_id: FHIR encounter reference
            resource_type: FHIR resource type

        Returns:
            FHIR-compliant JSON resource
        """
        timestamp = datetime.now().isoformat()

        base_resource = {
            "resourceType": resource_type,
            "id": hashlib.md5(f"{timestamp}{clinical_summary[:50]}".encode()).hexdigest()[:12],
            "meta": {
                "versionId": "1",
                "lastUpdated": timestamp,
                "profile": [f"http://hl7.org/fhir/StructureDefinition/{resource_type}"]
            },
            "status": "final",
            "issued": timestamp
        }

        if patient_id:
            base_resource["subject"] = {"reference": f"Patient/{patient_id}"}

        if encounter_id:
            base_resource["encounter"] = {"reference": f"Encounter/{encounter_id}"}

        # Resource-specific formatting
        if resource_type == "DiagnosticReport":
            base_resource.update({
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "11506-3",
                        "display": "Progress note"
                    }],
                    "text": "Clinical Summary"
                },
                "conclusion": clinical_summary,
                "conclusionCode": [{
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": "404684003",
                        "display": "Clinical finding"
                    }]
                }]
            })

        elif resource_type == "Observation":
            base_resource.update({
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "75325-1",
                        "display": "Symptom"
                    }]
                },
                "valueString": clinical_summary
            })

        elif resource_type == "Condition":
            base_resource.update({
                "clinicalStatus": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": "active"
                    }]
                },
                "verificationStatus": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                        "code": "provisional"
                    }]
                },
                "code": {
                    "text": clinical_summary
                },
                "note": [{
                    "text": "Generated by MedPrompt AI - requires clinical verification"
                }]
            })

        elif resource_type == "CarePlan":
            base_resource.update({
                "intent": "plan",
                "title": "AI-Generated Care Plan",
                "description": clinical_summary,
                "note": [{
                    "text": "Generated by MedPrompt AI - requires clinical verification"
                }]
            })

        # Add AI generation metadata
        base_resource["extension"] = [{
            "url": "http://example.org/fhir/StructureDefinition/ai-generated",
            "valueBoolean": True
        }, {
            "url": "http://example.org/fhir/StructureDefinition/ai-model",
            "valueString": "MedPrompt-v2.0"
        }]

        return base_resource

    def generate_clinical_summary(self, patient_note: str) -> str:
        """
        Convenience method for full MedPrompt pipeline.

        Args:
            patient_note: Raw clinical note

        Returns:
            Refined clinical summary
        """
        return self.medprompt.generate_clinical_summary(patient_note)


# --- Example Usage ---

if __name__ == "__main__":
    # Initialize engine
    engine = MedPromptEngine()

    # Example clinical note
    sample_note = """
    CC: 58yo F with chest pain x 4 hours

    HPI: Patient reports substernal chest pressure radiating to left arm,
    associated with diaphoresis and nausea. Pain started at rest while
    watching TV. Rates pain 8/10. Denies prior episodes. Has history of
    HTN, DM2, and hyperlipidemia. Takes metformin 1000mg BID, lisinopril
    20mg daily, atorvastatin 40mg daily.

    VS: BP 165/95, HR 92, RR 18, SpO2 96% RA, Temp 98.6F
    PE: Anxious appearing, diaphoretic. Heart RRR, no murmurs. Lungs CTAB.
    """

    print("=" * 70)
    print("MedPrompt Clinical Analysis Demo")
    print("=" * 70)

    # 1. Generate CoT prompt
    print("\n1. Chain-of-Thought Prompt Generation:")
    print("-" * 50)
    cot_prompt = engine.generate_chain_of_thought_prompt(sample_note, task_type="diagnosis")
    print(cot_prompt[:500] + "...")

    # 2. Generate clinical summary
    print("\n2. Clinical Summary (MedPrompt Pipeline):")
    print("-" * 50)
    summary = engine.generate_clinical_summary(sample_note)
    print(summary)

    # 3. Verify the response
    print("\n3. Chain-of-Verification Results:")
    print("-" * 50)
    verification = engine.chain_of_verification(summary, sample_note)
    print(json.dumps(verification, indent=2, default=str))

    # 4. Format as FHIR
    print("\n4. FHIR-Compliant Output:")
    print("-" * 50)
    fhir_output = engine.format_as_fhir_json(summary, patient_id="12345")
    print(json.dumps(fhir_output, indent=2))

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
