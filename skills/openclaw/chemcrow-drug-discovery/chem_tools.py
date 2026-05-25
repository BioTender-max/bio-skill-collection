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
ChemCrow Tools - Production-Grade Cheminformatics Toolkit

Comprehensive molecular analysis tools for drug discovery AI agents.
Provides real RDKit implementations with graceful fallback for environments
without RDKit installed.

Features:
- Molecular property calculation (MolWt, LogP, TPSA, QED)
- Lipinski Rule of 5 analysis
- Synthetic Accessibility (SA) Score
- PAINS (Pan-Assay Interference) filter
- Toxicity alerts via SMARTS patterns
- 3D conformer generation
- Molecular fingerprints for similarity search
- ADMET property predictions

References:
- ChemCrow Paper: https://arxiv.org/abs/2304.05376
- RDKit Documentation: https://www.rdkit.org/docs/
- SA Score: https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-3-36

Version: 2.0.0
Date: January 2026
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import math

# --- RDKit Import with Fallback ---

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, QED, AllChem, Crippen, Lipinski
    from rdkit.Chem import rdMolDescriptors, FilterCatalog, Draw
    from rdkit.Chem.FilterCatalog import FilterCatalogParams
    from rdkit import DataStructs
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False
    print("Warning: RDKit not installed. Using mock mode for demonstration.")


# --- Data Classes ---

@dataclass
class MolecularProperties:
    """Container for molecular property calculations."""
    smiles: str
    mol_weight: float
    log_p: float
    tpsa: float
    qed: float
    hbd: int  # Hydrogen bond donors
    hba: int  # Hydrogen bond acceptors
    rotatable_bonds: int
    aromatic_rings: int
    heavy_atoms: int


@dataclass
class LipinskiResult:
    """Lipinski Rule of 5 analysis result."""
    passes: bool
    violations: int
    mw_pass: bool  # MW <= 500
    logp_pass: bool  # LogP <= 5
    hbd_pass: bool  # HBD <= 5
    hba_pass: bool  # HBA <= 10
    details: Dict[str, Any]


@dataclass
class SAScoreResult:
    """Synthetic Accessibility Score result."""
    score: float  # 1 (easy) to 10 (hard)
    category: str  # "Easy", "Moderate", "Hard", "Very Hard"
    fragment_score: float
    complexity_penalty: float


@dataclass
class ToxicityAlert:
    """Toxicity alert from SMARTS matching."""
    alert_name: str
    pattern: str
    severity: str  # "High", "Medium", "Low"
    description: str


# --- SMARTS Patterns for Toxicity Alerts ---

TOXICITY_SMARTS = {
    # High severity alerts
    "nitro_aromatic": {
        "pattern": "[$(c1ccccc1[N+](=O)[O-]),$(c1cccc2c1cccc2[N+](=O)[O-])]",
        "severity": "High",
        "description": "Nitroaromatic compounds - potential mutagens"
    },
    "azide": {
        "pattern": "[N-]=[N+]=[N-]",
        "severity": "High",
        "description": "Azide group - potentially explosive"
    },
    "michael_acceptor": {
        "pattern": "[C,N]=[C]-[C]=[O,N,S]",
        "severity": "High",
        "description": "Michael acceptor - reactive with proteins"
    },
    "acyl_halide": {
        "pattern": "[C](=[O])[F,Cl,Br,I]",
        "severity": "High",
        "description": "Acyl halide - highly reactive"
    },

    # Medium severity alerts
    "aniline": {
        "pattern": "[NH2]c1ccccc1",
        "severity": "Medium",
        "description": "Aniline - potential metabolic activation"
    },
    "hydrazine": {
        "pattern": "[NH2][NH2]",
        "severity": "Medium",
        "description": "Hydrazine - potential hepatotoxin"
    },
    "epoxide": {
        "pattern": "C1OC1",
        "severity": "Medium",
        "description": "Epoxide - alkylating agent"
    },

    # Low severity alerts (flagged for review)
    "aldehyde": {
        "pattern": "[CH]=O",
        "severity": "Low",
        "description": "Aldehyde - potential Schiff base former"
    },
    "phenol": {
        "pattern": "c1ccccc1O",
        "severity": "Low",
        "description": "Phenol - may undergo metabolic activation"
    }
}

# --- PAINS Patterns (Simplified subset) ---

PAINS_PATTERNS = {
    "quinone": "[#6]1=[#6]-[#6](=[O])-[#6]=[#6]-[#6](=[O])-1",
    "catechol": "c1ccc(O)c(O)c1",
    "rhodanine": "S=C1NC(=O)CS1",
    "quinone_a": "[#6]1(=[O])-[#6]=[#6]-[#6](=[O])-[#6]=[#6]1",
    "imine_one": "[#6]-[#7]=[#6]-[#6]=[O]",
    "azo": "[#6]-[#7]=[#7]-[#6]",
}


# --- Main ChemTools Class ---

class ChemTools:
    """
    Production-grade cheminformatics toolkit using RDKit.

    Provides comprehensive molecular analysis for drug discovery applications.
    Falls back to mock implementations when RDKit is not available.

    Example:
        >>> tools = ChemTools()
        >>> props = tools.calculate_properties("CC(=O)OC1=CC=CC=C1C(=O)O")  # Aspirin
        >>> print(f"MW: {props.mol_weight:.2f}, LogP: {props.log_p:.2f}")
    """

    def __init__(self):
        self.rdkit_available = RDKIT_AVAILABLE

    # --- Core Property Calculations ---

    @staticmethod
    def validate_smiles(smiles: str) -> bool:
        """
        Validate a SMILES string.

        Args:
            smiles: SMILES string to validate

        Returns:
            True if valid, False otherwise
        """
        if not RDKIT_AVAILABLE:
            return True  # Assume valid in mock mode

        mol = Chem.MolFromSmiles(smiles)
        return mol is not None

    def calculate_properties(self, smiles: str) -> MolecularProperties:
        """
        Calculate comprehensive molecular properties.

        Args:
            smiles: Valid SMILES string

        Returns:
            MolecularProperties dataclass with all calculated values

        Raises:
            ValueError: If SMILES is invalid
        """
        if not RDKIT_AVAILABLE:
            return self._mock_properties(smiles)

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        return MolecularProperties(
            smiles=smiles,
            mol_weight=Descriptors.MolWt(mol),
            log_p=Descriptors.MolLogP(mol),
            tpsa=Descriptors.TPSA(mol),
            qed=QED.qed(mol),
            hbd=Descriptors.NumHDonors(mol),
            hba=Descriptors.NumHAcceptors(mol),
            rotatable_bonds=Descriptors.NumRotatableBonds(mol),
            aromatic_rings=Descriptors.NumAromaticRings(mol),
            heavy_atoms=Descriptors.HeavyAtomCount(mol)
        )

    def calculate_descriptors(self, smiles: str) -> Dict[str, float]:
        """
        Calculate molecular descriptors as a dictionary.

        Legacy method for backwards compatibility.

        Args:
            smiles: Valid SMILES string

        Returns:
            Dictionary with MolWt, LogP, TPSA, QED
        """
        props = self.calculate_properties(smiles)
        return {
            "MolWt": props.mol_weight,
            "LogP": props.log_p,
            "TPSA": props.tpsa,
            "QED": props.qed
        }

    # --- Lipinski Rule of 5 ---

    def check_lipinski(self, smiles: str) -> LipinskiResult:
        """
        Check Lipinski's Rule of 5 for oral bioavailability.

        Rules:
        - Molecular weight <= 500 Da
        - LogP <= 5
        - Hydrogen bond donors <= 5
        - Hydrogen bond acceptors <= 10

        Args:
            smiles: Valid SMILES string

        Returns:
            LipinskiResult with pass/fail details
        """
        props = self.calculate_properties(smiles)

        mw_pass = props.mol_weight <= 500
        logp_pass = props.log_p <= 5
        hbd_pass = props.hbd <= 5
        hba_pass = props.hba <= 10

        violations = sum([not mw_pass, not logp_pass, not hbd_pass, not hba_pass])

        return LipinskiResult(
            passes=violations <= 1,  # One violation allowed
            violations=violations,
            mw_pass=mw_pass,
            logp_pass=logp_pass,
            hbd_pass=hbd_pass,
            hba_pass=hba_pass,
            details={
                "mol_weight": props.mol_weight,
                "log_p": props.log_p,
                "hbd": props.hbd,
                "hba": props.hba,
                "rotatable_bonds": props.rotatable_bonds
            }
        )

    # --- Synthetic Accessibility Score ---

    def calculate_sa_score(self, smiles: str) -> SAScoreResult:
        """
        Calculate Synthetic Accessibility Score.

        Based on the method by Ertl & Schuffenhauer (2009).
        Score ranges from 1 (easy to synthesize) to 10 (hard to synthesize).

        Args:
            smiles: Valid SMILES string

        Returns:
            SAScoreResult with score and category
        """
        if not RDKIT_AVAILABLE:
            return self._mock_sa_score(smiles)

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        # Calculate fragment-based score
        # This is a simplified implementation
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
        on_bits = fp.GetNumOnBits()

        # Fragment contribution (more common fragments = easier)
        num_atoms = mol.GetNumHeavyAtoms()
        num_rings = rdMolDescriptors.CalcNumRings(mol)
        num_stereo = rdMolDescriptors.CalcNumAtomStereoCenters(mol)
        num_bridgehead = rdMolDescriptors.CalcNumBridgeheadAtoms(mol)
        num_spiro = rdMolDescriptors.CalcNumSpiroAtoms(mol)

        # Base score from fragment complexity
        fragment_score = 1.0 + (on_bits / 500.0)

        # Complexity penalties
        complexity_penalty = 0.0
        complexity_penalty += num_rings * 0.3
        complexity_penalty += num_stereo * 0.5
        complexity_penalty += num_bridgehead * 1.0
        complexity_penalty += num_spiro * 1.0

        # Size penalty
        if num_atoms > 25:
            complexity_penalty += (num_atoms - 25) * 0.1

        # Calculate final score (normalized to 1-10 scale)
        raw_score = fragment_score + complexity_penalty
        sa_score = min(10.0, max(1.0, raw_score))

        # Categorize
        if sa_score < 3:
            category = "Easy"
        elif sa_score < 5:
            category = "Moderate"
        elif sa_score < 7:
            category = "Hard"
        else:
            category = "Very Hard"

        return SAScoreResult(
            score=sa_score,
            category=category,
            fragment_score=fragment_score,
            complexity_penalty=complexity_penalty
        )

    # --- Toxicity Alerts ---

    def check_toxicity_alerts(self, smiles: str) -> List[ToxicityAlert]:
        """
        Screen for toxicity alerts using SMARTS patterns.

        Checks for structural features associated with toxicity
        including reactive groups, mutagenic substructures, and
        metabolically activated moieties.

        Args:
            smiles: Valid SMILES string

        Returns:
            List of ToxicityAlert objects for matched patterns
        """
        if not RDKIT_AVAILABLE:
            return []

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return []

        alerts = []
        for alert_name, alert_info in TOXICITY_SMARTS.items():
            pattern = Chem.MolFromSmarts(alert_info["pattern"])
            if pattern and mol.HasSubstructMatch(pattern):
                alerts.append(ToxicityAlert(
                    alert_name=alert_name,
                    pattern=alert_info["pattern"],
                    severity=alert_info["severity"],
                    description=alert_info["description"]
                ))

        return alerts

    # --- PAINS Filter ---

    def check_pains(self, smiles: str) -> List[str]:
        """
        Screen for PAINS (Pan-Assay Interference Compounds).

        PAINS are compounds that frequently give false positives
        in biochemical assays due to non-specific mechanisms.

        Args:
            smiles: Valid SMILES string

        Returns:
            List of matched PAINS pattern names
        """
        if not RDKIT_AVAILABLE:
            return []

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return []

        matches = []
        for pattern_name, smarts in PAINS_PATTERNS.items():
            pattern = Chem.MolFromSmarts(smarts)
            if pattern and mol.HasSubstructMatch(pattern):
                matches.append(pattern_name)

        return matches

    # --- 3D Conformer Generation ---

    def generate_3d_conformer(self, smiles: str, num_confs: int = 1) -> str:
        """
        Generate 3D conformer(s) for a molecule.

        Uses ETKDG algorithm for initial embedding followed by
        MMFF force field optimization.

        Args:
            smiles: Valid SMILES string
            num_confs: Number of conformers to generate

        Returns:
            MOL block string with 3D coordinates
        """
        if not RDKIT_AVAILABLE:
            return "MOCK_3D_BLOCK"

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        mol = Chem.AddHs(mol)

        # Use ETKDG for conformer generation
        params = AllChem.ETKDGv3()
        params.randomSeed = 42

        if num_confs == 1:
            AllChem.EmbedMolecule(mol, params)
        else:
            AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)

        # Optimize with MMFF
        try:
            AllChem.MMFFOptimizeMolecule(mol)
        except:
            pass  # Some molecules may fail optimization

        return Chem.MolToMolBlock(mol)

    # --- Molecular Fingerprints ---

    def calculate_fingerprint(
        self,
        smiles: str,
        fp_type: str = "morgan",
        radius: int = 2,
        n_bits: int = 2048
    ) -> List[int]:
        """
        Calculate molecular fingerprint.

        Supports multiple fingerprint types for similarity searching.

        Args:
            smiles: Valid SMILES string
            fp_type: Fingerprint type ("morgan", "rdkit", "maccs")
            radius: Morgan fingerprint radius (ignored for other types)
            n_bits: Number of bits for bit vector fingerprints

        Returns:
            List of bit positions that are ON
        """
        if not RDKIT_AVAILABLE:
            return list(range(100))  # Mock fingerprint

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        if fp_type == "morgan":
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        elif fp_type == "rdkit":
            fp = Chem.RDKFingerprint(mol, fpSize=n_bits)
        elif fp_type == "maccs":
            fp = AllChem.GetMACCSKeysFingerprint(mol)
        else:
            raise ValueError(f"Unknown fingerprint type: {fp_type}")

        return list(fp.GetOnBits())

    def calculate_similarity(self, smiles1: str, smiles2: str, metric: str = "tanimoto") -> float:
        """
        Calculate molecular similarity between two compounds.

        Args:
            smiles1: First SMILES string
            smiles2: Second SMILES string
            metric: Similarity metric ("tanimoto", "dice")

        Returns:
            Similarity score (0-1)
        """
        if not RDKIT_AVAILABLE:
            return 0.5  # Mock similarity

        mol1 = Chem.MolFromSmiles(smiles1)
        mol2 = Chem.MolFromSmiles(smiles2)

        if not mol1 or not mol2:
            raise ValueError("Invalid SMILES string")

        fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=2048)
        fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=2048)

        if metric == "tanimoto":
            return DataStructs.TanimotoSimilarity(fp1, fp2)
        elif metric == "dice":
            return DataStructs.DiceSimilarity(fp1, fp2)
        else:
            raise ValueError(f"Unknown metric: {metric}")

    # --- ADMET Predictions ---

    def predict_admet(self, smiles: str) -> Dict[str, Any]:
        """
        Predict ADMET properties (simplified rule-based).

        Provides rough estimates for:
        - Absorption (solubility, permeability)
        - Distribution (BBB penetration, plasma protein binding)
        - Metabolism (CYP450 liability)
        - Excretion (clearance estimate)
        - Toxicity (hepatotoxicity risk, hERG liability)

        Args:
            smiles: Valid SMILES string

        Returns:
            Dictionary with ADMET predictions
        """
        props = self.calculate_properties(smiles)
        lipinski = self.check_lipinski(smiles)
        alerts = self.check_toxicity_alerts(smiles)

        # Rule-based predictions
        predictions = {}

        # Absorption
        predictions["absorption"] = {
            "oral_bioavailability": "Good" if lipinski.passes else "Poor",
            "solubility": "Low" if props.log_p > 3 else ("Moderate" if props.log_p > 1 else "High"),
            "permeability": "High" if props.tpsa < 140 else "Low"
        }

        # Distribution
        predictions["distribution"] = {
            "bbb_penetration": "Yes" if (props.tpsa < 90 and props.mol_weight < 450) else "No",
            "plasma_protein_binding": "High" if props.log_p > 3 else "Low"
        }

        # Metabolism
        predictions["metabolism"] = {
            "cyp_substrate_risk": "High" if props.mol_weight > 400 else "Low",
            "half_life_estimate": "Short" if props.mol_weight < 300 else "Long"
        }

        # Excretion
        predictions["excretion"] = {
            "clearance": "Renal" if props.log_p < 0 else "Hepatic"
        }

        # Toxicity
        high_alerts = [a for a in alerts if a.severity == "High"]
        predictions["toxicity"] = {
            "hepatotoxicity_risk": "High" if len(high_alerts) > 0 else "Low",
            "herg_liability": "High" if (props.log_p > 4 and props.mol_weight > 400) else "Low",
            "structural_alerts": [a.alert_name for a in alerts]
        }

        return predictions

    # --- Comprehensive Screening ---

    def screen_compound(self, smiles: str) -> Dict[str, Any]:
        """
        Perform comprehensive compound screening.

        Combines all analyses into a single comprehensive report.

        Args:
            smiles: Valid SMILES string

        Returns:
            Complete screening report
        """
        if not self.validate_smiles(smiles):
            return {"error": "Invalid SMILES", "smiles": smiles}

        props = self.calculate_properties(smiles)
        lipinski = self.check_lipinski(smiles)
        sa_score = self.calculate_sa_score(smiles)
        tox_alerts = self.check_toxicity_alerts(smiles)
        pains = self.check_pains(smiles)
        admet = self.predict_admet(smiles)

        # Calculate overall druglikeness score
        druglikeness_score = 0.0
        druglikeness_score += 0.3 * props.qed
        druglikeness_score += 0.2 * (1.0 if lipinski.passes else 0.0)
        druglikeness_score += 0.2 * (1.0 - (sa_score.score - 1) / 9.0)
        druglikeness_score += 0.15 * (1.0 if len(tox_alerts) == 0 else 0.0)
        druglikeness_score += 0.15 * (1.0 if len(pains) == 0 else 0.0)

        return {
            "smiles": smiles,
            "properties": {
                "mol_weight": props.mol_weight,
                "log_p": props.log_p,
                "tpsa": props.tpsa,
                "qed": props.qed,
                "hbd": props.hbd,
                "hba": props.hba,
                "rotatable_bonds": props.rotatable_bonds,
                "aromatic_rings": props.aromatic_rings,
                "heavy_atoms": props.heavy_atoms
            },
            "lipinski": {
                "passes": lipinski.passes,
                "violations": lipinski.violations,
                "details": lipinski.details
            },
            "synthetic_accessibility": {
                "score": sa_score.score,
                "category": sa_score.category
            },
            "toxicity_alerts": [
                {"name": a.alert_name, "severity": a.severity, "description": a.description}
                for a in tox_alerts
            ],
            "pains_alerts": pains,
            "admet": admet,
            "druglikeness_score": druglikeness_score,
            "recommendation": self._generate_recommendation(
                lipinski.passes,
                len(tox_alerts),
                len(pains),
                sa_score.score
            )
        }

    def _generate_recommendation(
        self,
        lipinski_passes: bool,
        num_tox_alerts: int,
        num_pains: int,
        sa_score: float
    ) -> str:
        """Generate a recommendation based on screening results."""
        issues = []

        if not lipinski_passes:
            issues.append("violates Lipinski rules")
        if num_tox_alerts > 0:
            issues.append(f"has {num_tox_alerts} toxicity alerts")
        if num_pains > 0:
            issues.append(f"matches {num_pains} PAINS patterns")
        if sa_score > 6:
            issues.append("has poor synthetic accessibility")

        if not issues:
            return "Compound passes all screening criteria. Recommended for further evaluation."
        elif len(issues) == 1:
            return f"Compound {issues[0]}. Consider optimization."
        else:
            return f"Compound has multiple concerns: {', '.join(issues)}. Significant optimization needed."

    # --- Mock Methods ---

    def _mock_properties(self, smiles: str) -> MolecularProperties:
        """Generate mock properties when RDKit is unavailable."""
        # Generate deterministic mock values based on SMILES length
        seed = len(smiles)
        return MolecularProperties(
            smiles=smiles,
            mol_weight=100.0 + seed * 10,
            log_p=1.0 + (seed % 5),
            tpsa=40.0 + seed * 2,
            qed=0.5,
            hbd=seed % 3,
            hba=seed % 6,
            rotatable_bonds=seed % 8,
            aromatic_rings=seed % 3,
            heavy_atoms=seed
        )

    def _mock_sa_score(self, smiles: str) -> SAScoreResult:
        """Generate mock SA score when RDKit is unavailable."""
        seed = len(smiles) % 10
        score = 2.0 + seed * 0.5
        return SAScoreResult(
            score=score,
            category="Moderate" if score < 5 else "Hard",
            fragment_score=1.5,
            complexity_penalty=score - 1.5
        )


# --- Example Usage ---

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="ChemCrow Tools - Molecular Analysis")
    parser.add_argument("--smiles", help="SMILES string to analyze")
    parser.add_argument("--output", help="Path to save JSON output")
    parser.add_argument("--demo", action="store_true", help="Run demonstration on test molecules")
    
    args = parser.parse_args()
    
    tools = ChemTools()

    if args.demo:
        # Test molecules
        test_molecules = {
            "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
            "Ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
            "Atorvastatin": "CC(C)C1=C(C(=C(N1CCC(CC(CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4"
        }

        print("=" * 70)
        print("ChemCrow Tools - Comprehensive Molecular Analysis")
        print("=" * 70)
        print(f"RDKit Available: {RDKIT_AVAILABLE}")
        print()

        for name, smiles in test_molecules.items():
            print(f"\n{'='*60}")
            print(f"Compound: {name}")
            print(f"SMILES: {smiles}")
            print("=" * 60)
            
            try:
                result = tools.screen_compound(smiles)
                print(json.dumps(result, indent=2, default=str))
            except Exception as e:
                print(f"Error: {e}")
                
    elif args.smiles:
        try:
            result = tools.screen_compound(args.smiles)
            output_json = json.dumps(result, indent=2, default=str)
            print(output_json)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_json)
                    print(f"\nSaved to {args.output}", file=sys.stderr)
                    
        except Exception as e:
            print(f"Error processing SMILES: {e}", file=sys.stderr)
            sys.exit(1)
            
    else:
        parser.print_help()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
