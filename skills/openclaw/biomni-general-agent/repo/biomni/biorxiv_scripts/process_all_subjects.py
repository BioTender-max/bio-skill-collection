# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

#!/usr/bin/env python3
"""Script to process all bioRxiv subjects and extract computational tasks from the top 100 papers in each."""

import argparse
import os
import subprocess
import sys
import time

import pandas as pd
from tqdm import tqdm

# Add the parent directory to the path so we can import the bioagentos package
sys.path.append("/dfs/user/kexinh/BioAgentOS/")

# List of all bioRxiv subjects
BIORXIV_SUBJECTS = [
    "evolutionary biology",
    "ecology",
    "neuroscience",
    "developmental biology",
    "plant biology",
    "microbiology",
    "cancer biology",
    "immunology",
    "cell biology",
    "biochemistry",
    "genetics",
    "bioinformatics",
    "animal behavior and cognition",
    "biophysics",
    "genomics",
    "systems biology",
    "bioengineering",
    "molecular biology",
    "physiology",
    "zoology",
    "scientific communication and education",
    "pathology",
    "synthetic biology",
    "paleontology",
    "pharmacology and toxicology",
]


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process all bioRxiv subjects and extract tasks from papers.")
    parser.add_argument(
        "--papers-per-subject",
        type=int,
        default=100,
        help="Number of papers to process per subject (default: 100)",
    )
    parser.add_argument(
        "--metadata-path",
        type=str,
        default="/dfs/user/kexinh/BioAgentOS/data/biorxiv_metadata.csv",
        help="Path to bioRxiv metadata CSV file (default: data/biorxiv_metadata.csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./biorxiv_all_subjects",
        help="Base directory to save results (default: ./biorxiv_all_subjects)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-haiku-20240307",
        help="LLM model to use for extraction (default: claude-3-haiku-20240307)",
    )
    parser.add_argument(
        "--max-paper-length",
        type=int,
        default=200000,
        help="Maximum paper length in characters (default: 200000)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=10000,
        help="Chunk size for text processing (default: 10000)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=400,
        help="Chunk overlap for text processing (default: 400)",
    )
    parser.add_argument("--save-pdfs", action="store_true", help="Save downloaded PDFs (default: False)")
    parser.add_argument(
        "--random-sample",
        action="store_true",
        help="Randomly sample papers instead of taking the first N (default: False)",
    )
    parser.add_argument(
        "--subjects",
        type=str,
        nargs="+",
        help="Specific subjects to process (default: all subjects)",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=60,
        help="Delay in seconds between processing subjects (default: 60)",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only generate the combined summary (default: False)",
    )
    return parser.parse_args()


def check_subject_availability(metadata_path, subjects):
    """Check which subjects have papers available in the metadata.

    Args:
        metadata_path: Path to the metadata CSV file
        subjects: List of subjects to check

    Returns:
        List of subjects with available papers

    """
    try:
        df_biorxiv = pd.read_csv(metadata_path)
        available_subjects = []

        for subject in subjects:
            count = len(
                df_biorxiv[(df_biorxiv.published != "NA") & (df_biorxiv.category.str.lower() == subject.lower())]
            )
            if count > 0:
                available_subjects.append((subject, count))
                print(f"Subject '{subject}' has {count} papers available")
            else:
                print(f"Subject '{subject}' has no papers available")

        return available_subjects
    except Exception as e:
        print(f"Error checking subject availability: {e}")
        return []


def process_subject(subject, args):
    """Process a single subject by calling the extract_biorxiv_tasks.py script.

    Args:
        subject: Subject to process
        args: Command line arguments

    """
    # Clean subject name for command line
    subject.replace(" ", "\\ ")

    # Build command
    cmd = [
        "python",
        "BioAgentOS/bioagentos/scripts/extract_biorxiv_tasks.py",
        "--subject",
        f'"{subject}"',
        "--limit",
        str(args.papers_per_subject),
        "--metadata-path",
        args.metadata_path,
        "--model",
        args.model,
        "--max-paper-length",
        str(args.max_paper_length),
        "--chunk-size",
        str(args.chunk_size),
        "--chunk-overlap",
        str(args.chunk_overlap),
    ]

    # Add optional arguments
    if args.save_pdfs:
        cmd.append("--save-pdfs")
    if args.random_sample:
        cmd.append("--random-sample")

    # Convert command list to string
    cmd_str = " ".join(cmd)

    print(f"\n{'=' * 80}\nProcessing subject: {subject}\n{'=' * 80}")
    print(f"Running command: {cmd_str}")

    # Execute command
    try:
        subprocess.run(cmd_str, shell=True, check=True)
        print(f"Successfully processed subject: {subject}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing subject '{subject}': {e}")


def combine_summaries(base_dir, subjects, papers_per_subject):
    """Combine frequency summaries from all subjects into a single summary.

    Args:
        base_dir: Base directory containing subject results
        subjects: List of subjects that were processed
        papers_per_subject: Number of papers processed per subject

    """
    all_tasks = {}
    all_databases = {}
    all_software = {}

    for subject, _ in subjects:
        # Clean subject name for directory name
        clean_subject = subject.lower().replace(" ", "_").replace("/", "_")
        subject_dir = f"biorxiv_results_{clean_subject}_{papers_per_subject}"
        summary_path = os.path.join(subject_dir, "frequency_summary.json")

        try:
            if os.path.exists(summary_path):
                with open(summary_path) as f:
                    summary = json.load(f)

                    # Merge tasks
                    for task, count in summary.get("tasks", {}).items():
                        if task in all_tasks:
                            all_tasks[task] += count
                        else:
                            all_tasks[task] = count

                    # Merge databases
                    for db, count in summary.get("databases", {}).items():
                        if db in all_databases:
                            all_databases[db] += count
                        else:
                            all_databases[db] = count

                    # Merge software
                    for sw, count in summary.get("software", {}).items():
                        if sw in all_software:
                            all_software[sw] += count
                        else:
                            all_software[sw] = count
            else:
                print(f"Warning: Summary file not found for subject '{subject}'")
        except Exception as e:
            print(f"Error processing summary for subject '{subject}': {e}")

    # Sort by frequency (descending)
    all_tasks = dict(sorted(all_tasks.items(), key=lambda item: item[1], reverse=True))
    all_databases = dict(sorted(all_databases.items(), key=lambda item: item[1], reverse=True))
    all_software = dict(sorted(all_software.items(), key=lambda item: item[1], reverse=True))

    # Create combined summary
    combined_summary = {
        "tasks": all_tasks,
        "databases": all_databases,
        "software": all_software,
    }

    # Save combined summary
    combined_path = os.path.join(base_dir, "combined_summary.json")
    os.makedirs(base_dir, exist_ok=True)

    with open(combined_path, "w") as f:
        json.dump(combined_summary, f, indent=2)

    print(f"Combined summary saved to {combined_path}")

    # Create CSV files for each category
    tasks_df = pd.DataFrame(list(all_tasks.items()), columns=["Task", "Frequency"])
    tasks_df.to_csv(os.path.join(base_dir, "tasks_frequency.csv"), index=False)

    db_df = pd.DataFrame(list(all_databases.items()), columns=["Database", "Frequency"])
    db_df.to_csv(os.path.join(base_dir, "databases_frequency.csv"), index=False)

    sw_df = pd.DataFrame(list(all_software.items()), columns=["Software", "Frequency"])
    sw_df.to_csv(os.path.join(base_dir, "software_frequency.csv"), index=False)

    print(f"CSV summaries saved to {base_dir}")


def main():
    """Main function to run the script."""
    args = parse_arguments()

    # Determine which subjects to process
    subjects_to_process = args.subjects if args.subjects else BIORXIV_SUBJECTS

    # Check which subjects have papers available
    available_subjects = check_subject_availability(args.metadata_path, subjects_to_process)

    if not available_subjects:
        print("No subjects with available papers found. Exiting.")
        return

    if not args.summary_only:
        # Process each subject
        for subject, _count in tqdm(available_subjects, desc="Processing subjects"):
            process_subject(subject, args)

            # Add delay between subjects to avoid rate limiting
            if args.delay > 0:
                print(f"Waiting {args.delay} seconds before processing the next subject...")
                time.sleep(args.delay)

    # Combine summaries from all subjects
    combine_summaries(args.output_dir, available_subjects, args.papers_per_subject)

    print("All subjects processed successfully!")


if __name__ == "__main__":
    import json  # Import here to avoid circular import with the main script

    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
