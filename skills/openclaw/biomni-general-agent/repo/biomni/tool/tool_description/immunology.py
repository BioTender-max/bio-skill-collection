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
        "description": "Perform ATAC-seq peak calling and differential accessibility analysis using MACS2.",
        "name": "analyze_atac_seq_differential_accessibility",
        "optional_parameters": [
            {
                "default": "./atac_results",
                "description": "Directory to save output files",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "hs",
                "description": "Genome size parameter for MACS2",
                "name": "genome_size",
                "type": "str",
            },
            {
                "default": 0.05,
                "description": "q-value cutoff for peak detection",
                "name": "q_value",
                "type": "float",
            },
            {
                "default": "atac",
                "description": "Prefix for output file names",
                "name": "name_prefix",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to the treatment condition BAM file with aligned ATAC-seq reads",
                "name": "treatment_bam",
                "type": "str",
            },
            {
                "default": None,
                "description": "Path to the control condition BAM file with aligned ATAC-seq reads",
                "name": "control_bam",
                "type": "str",
            },
        ],
    },
    {
        "description": "Analyzes bacterial growth curve data to determine growth "
        "parameters such as doubling time, growth rate, and lag "
        "phase.",
        "name": "analyze_bacterial_growth_curve",
        "optional_parameters": [
            {
                "default": ".",
                "description": "Directory where output files will be saved",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Time points of measurements in hours",
                "name": "time_points",
                "type": "List or numpy.ndarray",
            },
            {
                "default": None,
                "description": "Optical density measurements corresponding to each time point",
                "name": "od_values",
                "type": "List or numpy.ndarray",
            },
            {
                "default": None,
                "description": "Name of the bacterial strain being analyzed",
                "name": "strain_name",
                "type": "str",
            },
        ],
    },
    {
        "description": "Simulates the isolation and purification of immune cells from tissue samples.",
        "name": "isolate_purify_immune_cells",
        "optional_parameters": [
            {
                "default": "collagenase",
                "description": "The enzyme used for tissue digestion",
                "name": "enzyme_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "Specific antibody for magnetic-assisted cell sorting",
                "name": "macs_antibody",
                "type": "str",
            },
            {
                "default": 45,
                "description": "Digestion time in minutes",
                "name": "digestion_time_min",
                "type": "int",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "The type of tissue sample (e.g., 'adipose', 'kidney', 'liver', 'lung', 'spleen')",
                "name": "tissue_type",
                "type": "str",
            },
            {
                "default": None,
                "description": "The immune cell population to isolate (e.g., 'macrophages', 'leukocytes', 'T cells')",
                "name": "target_cell_type",
                "type": "str",
            },
        ],
    },
    {
        "description": "Estimate cell cycle phase durations using dual-nucleoside "
        "pulse labeling data and mathematical modeling.",
        "name": "estimate_cell_cycle_phase_durations",
        "optional_parameters": [],
        "required_parameters": [
            {
                "default": None,
                "description": "Dictionary containing experimental "
                "data from flow cytometry with EdU "
                "and BrdU labeling, including time "
                "points and percentages of labeled "
                "cells",
                "name": "flow_cytometry_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "Initial estimates for cell cycle phase durations and death rates",
                "name": "initial_estimates",
                "type": "dict",
            },
        ],
    },
    {
        "description": "Track immune cells under flow conditions and classify their behaviors.",
        "name": "track_immune_cells_under_flow",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "Directory to save output files",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": 1.0,
                "description": "Pixel size in micrometers",
                "name": "pixel_size_um",
                "type": "float",
            },
            {
                "default": 1.0,
                "description": "Time interval between frames in seconds",
                "name": "time_interval_sec",
                "type": "float",
            },
            {
                "default": "right",
                "description": "Direction of flow ('right', 'left', 'up', 'down')",
                "name": "flow_direction",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to image sequence directory or video file",
                "name": "image_sequence_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "Analyze CFSE-labeled cell samples to quantify cell division and proliferation.",
        "name": "analyze_cfse_cell_proliferation",
        "optional_parameters": [
            {
                "default": "FL1-A",
                "description": "Name of the channel containing CFSE fluorescence data",
                "name": "cfse_channel",
                "type": "str",
            },
            {
                "default": None,
                "description": "Tuple of (min_fsc, max_fsc, min_ssc, max_ssc) for lymphocyte gating",
                "name": "lymphocyte_gate",
                "type": "tuple or None",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to the FCS file containing flow cytometry data from CFSE-labeled cells",
                "name": "fcs_file_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "Analyze cytokine production (IFN-γ, IL-17) in CD4+ T cells after antigen stimulation.",
        "name": "analyze_cytokine_production_in_cd4_tcells",
        "optional_parameters": [
            {
                "default": "./results",
                "description": "Directory to save the results file",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Dictionary mapping stimulation "
                "conditions to FCS file paths. "
                "Expected keys: 'unstimulated', "
                "'Mtb300', 'CMV', 'SEB'",
                "name": "fcs_files_dict",
                "type": "dict",
            }
        ],
    },
    {
        "description": "Analyze ELISA data to quantify EBV antibody titers in plasma/serum samples.",
        "name": "analyze_ebv_antibody_titers",
        "optional_parameters": [
            {
                "default": "./",
                "description": "Directory to save output files.",
                "name": "output_dir",
                "type": "str",
            }
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Dictionary containing optical "
                "density (OD) readings for each "
                "sample. Format: {sample_id: "
                "{'VCA_IgG': float, 'VCA_IgM': "
                "float, 'EA_IgG': float, 'EA_IgM': "
                "float, 'EBNA1_IgG': float, "
                "'EBNA1_IgM': float}}",
                "name": "raw_od_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "Dictionary containing standard "
                "curve data for each antibody type. "
                "Format: {antibody_type: "
                "[(concentration, OD), ...]}",
                "name": "standard_curve_data",
                "type": "dict",
            },
            {
                "default": None,
                "description": "Dictionary containing metadata for "
                "each sample. Format: {sample_id: "
                "{'group': str, 'collection_date': "
                "str}}",
                "name": "sample_metadata",
                "type": "dict",
            },
        ],
    },
    {
        "description": "Analyzes histological images of CNS lesions to quantify "
        "immune cell infiltration, demyelination, and tissue damage.",
        "name": "analyze_cns_lesion_histology",
        "optional_parameters": [
            {
                "default": "./output",
                "description": "Directory to save output files",
                "name": "output_dir",
                "type": "str",
            },
            {
                "default": "H&E",
                "description": 'Type of histological stain used (options: "H&E", "LFB", "IHC")',
                "name": "stain_type",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to the microscopy image file of brain or spinal cord tissue section",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
    {
        "description": "Analyzes immunohistochemistry images to quantify protein expression and spatial distribution.",
        "name": "analyze_immunohistochemistry_image",
        "optional_parameters": [
            {
                "default": "Unknown",
                "description": "Name of the protein being analyzed",
                "name": "protein_name",
                "type": "str",
            },
            {
                "default": "./ihc_results/",
                "description": "Directory to save output files",
                "name": "output_dir",
                "type": "str",
            },
        ],
        "required_parameters": [
            {
                "default": None,
                "description": "Path to the microscopy image of tissue section stained with antibodies",
                "name": "image_path",
                "type": "str",
            }
        ],
    },
]

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
