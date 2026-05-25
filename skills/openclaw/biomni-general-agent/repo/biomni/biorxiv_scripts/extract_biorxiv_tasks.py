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
"""Script to extract common tasks, databases, and software from bioRxiv papers
using the PaperTaskExtractor and existing metadata CSV.
"""

import argparse
import io
import json
import os
import random
import sys
import time
from typing import Any

import pandas as pd
import PyPDF2
import requests
from tqdm import tqdm

# Add the parent directory to the path so we can import the bioagentos package
sys.path.append("../../")
from biomni.agent.env_collection import PaperTaskExtractor


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Extract tasks from bioRxiv papers in a specific subject area.")
    parser.add_argument(
        "--subject",
        type=str,
        required=True,
        help='Subject area to search for papers (e.g., "neuroscience", "bioinformatics")',
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of papers to process (default: 10)",
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
        default=None,
        help="Directory to save results (default: ./biorxiv_results_{subject}_{limit})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-haiku-20240307",
        help="LLM model to use for extraction (default: claude-3-haiku-20240307)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=4000,
        help="Chunk size for text processing (default: 4000)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=400,
        help="Chunk overlap for text processing (default: 400)",
    )
    parser.add_argument(
        "--max-paper-length",
        type=int,
        default=200000,
        help="Maximum paper length in characters (default: 200000)",
    )
    parser.add_argument("--save-pdfs", action="store_true", help="Save downloaded PDFs (default: False)")
    parser.add_argument(
        "--random-sample",
        action="store_true",
        help="Randomly sample papers instead of taking the first N (default: False)",
    )
    return parser.parse_args()


def load_papers_from_csv(metadata_path: str, subject: str, limit: int, random_sample: bool) -> pd.DataFrame:
    """Load papers from bioRxiv metadata CSV file.

    Args:
        metadata_path: Path to the metadata CSV file
        subject: Subject area to filter by
        limit: Maximum number of papers to return
        random_sample: Whether to randomly sample papers

    Returns:
        DataFrame of filtered papers

    """
    try:
        # Load the metadata CSV
        df_biorxiv = pd.read_csv(metadata_path)

        # Filter published papers in the specified subject
        if subject.lower() == "all":
            filtered_df = df_biorxiv[df_biorxiv.published != "NA"]
        else:
            filtered_df = df_biorxiv[
                (df_biorxiv.published != "NA") & (df_biorxiv.category.str.lower() == subject.lower())
            ]

        # Sample papers
        if len(filtered_df) > limit:
            filtered_df = filtered_df.sample(limit, random_state=42) if random_sample else filtered_df.head(limit)

        print(f"Loaded {len(filtered_df)} papers in subject: {subject}")
        return filtered_df

    except Exception as e:
        print(f"Error loading papers from CSV: {e}")
        return pd.DataFrame()


def download_pdf(paper_doi: str, save_path: str | None = None) -> str | None:
    """Download PDF for a given paper DOI.

    Args:
        paper_doi: DOI of the paper
        save_path: Path to save the PDF (if None, won't save to disk)

    Returns:
        PDF text content or None if download failed

    """
    # Construct PDF URL from DOI
    pdf_url = f"https://www.biorxiv.org/content/{paper_doi}v1.full.pdf"

    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))

        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()

        # Save PDF if requested
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(io.BytesIO(response.content))
        return pdf_text

    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF for {paper_doi}: {e}")
        return None


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text content from a PDF file.

    Args:
        pdf_file: File-like object containing PDF data

    Returns:
        Extracted text content

    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to a maximum length while preserving complete sentences.

    Args:
        text: The text to truncate
        max_length: Maximum length in characters

    Returns:
        Truncated text

    """
    if len(text) <= max_length:
        return text

    # Find the last sentence boundary before max_length
    truncated = text[:max_length]
    last_period = truncated.rfind(".")
    last_question = truncated.rfind("?")
    last_exclamation = truncated.rfind("!")

    # Find the last sentence boundary
    last_boundary = max(last_period, last_question, last_exclamation)

    if last_boundary > 0:
        return text[: last_boundary + 1]
    else:
        # If no sentence boundary found, just truncate at max_length
        return truncated


def process_papers(papers_df: pd.DataFrame, args) -> list[dict[str, Any]]:
    """Process papers using PaperTaskExtractor.

    Args:
        papers_df: DataFrame of paper metadata
        args: Command line arguments

    Returns:
        List of papers with extracted tasks, databases, and software

    """
    # Initialize the task extractor
    extractor = PaperTaskExtractor(llm=args.model, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)

    results = []

    for _, paper in tqdm(papers_df.iterrows(), total=len(papers_df), desc="Processing papers"):
        paper_doi = paper.get("doi")
        if not paper_doi:
            continue

        print(f"\nProcessing paper: {paper.get('title')} (DOI: {paper_doi})")

        # Create paths
        pdf_path = None
        if args.save_pdfs:
            pdf_path = os.path.join(args.output_dir, "pdfs", f"{paper_doi.replace('/', '_')}.pdf")

        result_path = os.path.join(args.output_dir, "results", f"{paper_doi.replace('/', '_')}.json")

        # Skip if already processed
        if os.path.exists(result_path):
            print(f"Paper already processed, loading from {result_path}")
            with open(result_path) as f:
                paper_result = json.load(f)
                results.append(paper_result)
            continue

        # Download and process PDF
        pdf_text = download_pdf(paper_doi, pdf_path)
        if not pdf_text:
            print(f"Failed to download or extract text from {paper_doi}")
            continue

        # Truncate text if it exceeds max length
        if len(pdf_text) > args.max_paper_length:
            original_length = len(pdf_text)
            pdf_text = truncate_text(pdf_text, args.max_paper_length)
            print(f"Truncated paper from {original_length} to {len(pdf_text)} characters")

        # Extract tasks, databases, and software
        try:
            _, extraction_results = extractor.go(pdf_text)

            # Add paper metadata to results
            paper_result = {
                "metadata": {
                    "doi": paper.get("doi"),
                    "title": paper.get("title"),
                    "authors": paper.get("authors", ""),
                    "abstract": paper.get("abstract", ""),
                    "date": paper.get("date", ""),
                    "category": paper.get("category", ""),
                    "text_length": len(pdf_text),
                },
                "extraction": extraction_results,
            }

            # Save results
            os.makedirs(os.path.dirname(result_path), exist_ok=True)
            with open(result_path, "w") as f:
                json.dump(paper_result, f, indent=2)

            results.append(paper_result)

        except Exception as e:
            print(f"Error processing paper {paper_doi}: {e}")

    return results


def generate_summary(results: list[dict[str, Any]], output_dir: str):
    """Generate summary of extracted tasks, databases, and software.

    Args:
        results: List of papers with extraction results
        output_dir: Directory to save summary

    """
    # Collect all tasks, databases, and software
    all_tasks = []
    all_databases = []
    all_software = []

    for paper in results:
        extraction = paper.get("extraction", {})

        # Add paper metadata to each item
        paper_meta = paper.get("metadata", {})
        paper_id = f"{paper_meta.get('title')} ({paper_meta.get('doi')})"

        # Process tasks
        for task in extraction.get("tasks", []):
            task["paper"] = paper_id
            all_tasks.append(task)

        # Process databases
        for db in extraction.get("databases", []):
            db["paper"] = paper_id
            all_databases.append(db)

        # Process software
        for sw in extraction.get("software", []):
            sw["paper"] = paper_id
            all_software.append(sw)

    # Create summary dataframes
    if all_tasks:
        tasks_df = pd.DataFrame(all_tasks)
        tasks_df.to_csv(os.path.join(output_dir, "tasks_summary.csv"), index=False)

    if all_databases:
        db_df = pd.DataFrame(all_databases)
        db_df.to_csv(os.path.join(output_dir, "databases_summary.csv"), index=False)

    if all_software:
        sw_df = pd.DataFrame(all_software)
        sw_df.to_csv(os.path.join(output_dir, "software_summary.csv"), index=False)

    # Generate frequency counts
    task_counts = {}
    for task in all_tasks:
        task_name = task.get("task_name")
        if task_name:
            task_counts[task_name] = task_counts.get(task_name, 0) + 1

    db_counts = {}
    for db in all_databases:
        db_name = db.get("name")
        if db_name:
            db_counts[db_name] = db_counts.get(db_name, 0) + 1

    sw_counts = {}
    for sw in all_software:
        sw_name = sw.get("name")
        if sw_name:
            sw_counts[sw_name] = sw_counts.get(sw_name, 0) + 1

    # Save frequency counts
    with open(os.path.join(output_dir, "frequency_summary.json"), "w") as f:
        json.dump(
            {"tasks": task_counts, "databases": db_counts, "software": sw_counts},
            f,
            indent=2,
        )

    print(f"Summary files saved to {output_dir}")


def main():
    """Main function to run the script."""
    args = parse_arguments()

    # Set default output directory if not specified
    if args.output_dir is None:
        # Clean subject name for directory name (replace spaces with underscores, lowercase)
        clean_subject = args.subject.lower().replace(" ", "_").replace("/", "_")
        args.output_dir = f"./biorxiv_results_{clean_subject}_{args.limit}"

    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, "results"), exist_ok=True)
    if args.save_pdfs:
        os.makedirs(os.path.join(args.output_dir, "pdfs"), exist_ok=True)

    # Load papers from CSV
    print(f"Loading papers from {args.metadata_path} in subject area: {args.subject}")
    papers_df = load_papers_from_csv(args.metadata_path, args.subject, args.limit, args.random_sample)

    if len(papers_df) == 0:
        print(f"No papers found for subject: {args.subject}")
        return

    # Process papers
    results = process_papers(papers_df, args)

    # Generate summary
    generate_summary(results, args.output_dir)

    print("Done!")


if __name__ == "__main__":
    main()

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
