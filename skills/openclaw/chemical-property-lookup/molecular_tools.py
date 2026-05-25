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
Utility functions for lightweight cheminformatics calculations using RDKit.
Designed for use inside LLM toolchains where we need deterministic, short
responses with basic drug-likeness heuristics.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, QED
except ImportError as exc:
    raise ImportError(
        "RDKit is required. Install via 'conda install -c conda-forge rdkit' "
        "or 'pip install rdkit-pypi'."
    ) from exc


def _load_molecule(smiles: str) -> Tuple[Any, str | None]:
    """Return an RDKit Mol object or an error string."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Error: Invalid SMILES string."
    return mol, None


def calculate_molecular_weight(smiles: str) -> str:
    """Return a formatted molecular weight string."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    weight = Descriptors.ExactMolWt(mol)
    return f"Molecular weight: {weight:.2f} Da"


def get_mol_block(smiles: str) -> str:
    """Return an SDF/MolBlock representation for visualization."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    return Chem.MolToMolBlock(mol)


def calculate_logp(smiles: str) -> str:
    """Return the Crippen cLogP value."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    logp = Crippen.MolLogP(mol)
    return f"LogP: {logp:.2f}"


def calculate_tpsa(smiles: str) -> str:
    """Return the topological polar surface area (Å²)."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    return f"TPSA: {tpsa:.2f} Å²"


def count_hbd_hba(smiles: str) -> str:
    """Return hydrogen bond donor/acceptor counts."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    donors = Descriptors.NumHDonors(mol)
    acceptors = Descriptors.NumHAcceptors(mol)
    return f"HBD: {donors}; HBA: {acceptors}"


def calculate_qed(smiles: str) -> str:
    """Return Quantitative Estimate of Drug-likeness."""
    mol, error = _load_molecule(smiles)
    if error:
        return error
    score = QED.qed(mol)
    return f"QED: {score:.2f}"


def _lipinski_metrics(mol: Any) -> Tuple[Dict[str, float], list[str]]:
    """Compute standard Lipinski metrics and violations."""
    metrics = {
        "mol_weight": Descriptors.MolWt(mol),
        "logp": Crippen.MolLogP(mol),
        "hbd": float(Descriptors.NumHDonors(mol)),
        "hba": float(Descriptors.NumHAcceptors(mol)),
        "tpsa": rdMolDescriptors.CalcTPSA(mol),
    }

    violations = []
    if metrics["mol_weight"] > 500:
        violations.append("MW>500")
    if metrics["logp"] > 5:
        violations.append("LogP>5")
    if metrics["hbd"] > 5:
        violations.append("HBD>5")
    if metrics["hba"] > 10:
        violations.append("HBA>10")

    return metrics, violations


def check_lipinski(smiles: str) -> str:
    """Return a Lipinski Rule-of-Five assessment."""
    mol, error = _load_molecule(smiles)
    if error:
        return error

    metrics, violations = _lipinski_metrics(mol)
    status = "Pass" if not violations else f"Fail ({', '.join(violations)})"
    return (
        f"Lipinski assessment: {status}. "
        f"MW={metrics['mol_weight']:.1f} Da, "
        f"LogP={metrics['logp']:.2f}, "
        f"HBD={metrics['hbd']:.0f}, "
        f"HBA={metrics['hba']:.0f}, "
        f"TPSA={metrics['tpsa']:.1f} Å²"
    )


def summarize_properties(smiles: str) -> Dict[str, Any]:
    """
    Return a dictionary with the most useful cheminformatics descriptors.
    Suitable for a single agent tool call.
    """
    mol, error = _load_molecule(smiles)
    if error:
        return {"smiles": smiles, "error": error}

    metrics, violations = _lipinski_metrics(mol)
    qed_score = QED.qed(mol)
    molblock = Chem.MolToMolBlock(mol)

    return {
        "smiles": smiles,
        "molecular_weight": round(metrics["mol_weight"], 2),
        "logp": round(metrics["logp"], 2),
        "tpsa": round(metrics["tpsa"], 2),
        "hbd": int(metrics["hbd"]),
        "hba": int(metrics["hba"]),
        "qed": round(qed_score, 2),
        "lipinski_pass": not violations,
        "lipinski_violations": violations,
        "molblock": molblock,
    }


if __name__ == "__main__":
    aspirin_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
    print("Testing RDKit utilities with Aspirin:")
    print(calculate_molecular_weight(aspirin_smiles))
    print(calculate_logp(aspirin_smiles))
    print(calculate_tpsa(aspirin_smiles))
    print(count_hbd_hba(aspirin_smiles))
    print(calculate_qed(aspirin_smiles))
    print(check_lipinski(aspirin_smiles))
    print(summarize_properties(aspirin_smiles))

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
