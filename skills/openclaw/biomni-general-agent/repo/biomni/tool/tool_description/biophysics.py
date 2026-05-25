# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

description = [
    {
        "description": "Predicts intrinsically disordered regions (IDRs) in a protein sequence using IUPred2A.",
        "name": "predict_protein_disorder_regions",
        "optional_parameters": [
            {
                "default": 0.5,
                "description": "The disorder score threshold above which a residue is considered disordered",
                "name": "threshold",
                "type": "float",
            },
            {
                "default": "disorder_prediction_results.csv",
                "description": "Filename to save the per-residue disorder scores",
                "name": "output_file",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "The amino acid sequence of the protein to analyze",
                "name": "protein_sequence",
                "type": "str",
            }
        ],
    },
    {
        "description": "Quantifies cell morphology and cytoskeletal organization from fluorescence microscopy images.",
        "name": "analyze_cell_morphology_and_cytoskeleton",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "Directory to save output files",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "otsu",
                "description": "Method for cell segmentation ('otsu', 'adaptive', or 'manual')",
                "name": "threshold_method",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to the fluorescence microscopy image file",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "Quantify tissue deformation and flow dynamics from microscopy image sequence.",
        "name": "analyze_tissue_deformation_flow",
        "optional_parameters": [
            {
                "default": "results",
                "description": "Directory to save results",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 1.0,
                "description": "Physical scale of pixels (e.g., μm/pixel) for proper scaling of metrics",
                "name": "pixel_scale",
                "type": "float",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Sequence of microscopy images "
                "(either a list of file paths or a "
                "3D numpy array [time, height, "
                "width])",
                "name": "image_sequence",
                "type": "list or numpy.ndarray",
            }
        ],
    },
]

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
