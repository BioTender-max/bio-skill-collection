#!/usr/bin/env python3
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DEFAULT_COLUMNS = [
    "total_reads",
    "q30_pct",
    "gc_pct",
    "duplication_pct",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a compact QC summary plot from a CSV/TSV table.")
    parser.add_argument("--input", required=True, help="QC summary table in CSV/TSV format.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    parser.add_argument("--title", default="QC Summary", help="Plot title.")
    parser.add_argument("--sample-col", default="sample", help="Sample column name.")
    parser.add_argument(
        "--metrics",
        nargs="*",
        default=DEFAULT_COLUMNS,
        help="Metric columns to visualize. Missing columns are skipped.",
    )
    return parser


def read_table(input_path: Path) -> pd.DataFrame:
    suffix = input_path.suffix.lower()
    sep = "\t" if suffix in {".tsv", ".txt"} else ","
    return pd.read_csv(input_path, sep=sep)


def main() -> None:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = read_table(input_path).copy()
    if args.sample_col not in df.columns:
        raise SystemExit(f"Missing sample column: {args.sample_col}")

    metrics = [metric for metric in args.metrics if metric in df.columns]
    if not metrics:
        raise SystemExit(
            f"None of the requested metrics were found. Available columns: {', '.join(df.columns)}"
        )

    sns.set_theme(style="whitegrid", context="talk")
    rows = 2 if len(metrics) > 2 else 1
    cols = 2 if len(metrics) > 1 else 1
    fig, axes = plt.subplots(rows, cols, figsize=(12, 6 if rows == 1 else 8), dpi=300)
    axes_list = axes.flatten() if hasattr(axes, "flatten") else [axes]
    palette = sns.color_palette("Blues_r", n_colors=max(len(df), 3))

    for index, metric in enumerate(metrics):
        ax = axes_list[index]
        metric_df = df.sort_values(metric, ascending=False)
        sns.barplot(
            data=metric_df,
            x=args.sample_col,
            y=metric,
            palette=palette,
            ax=ax,
        )
        ax.set_title(metric.replace("_", " ").title(), fontsize=13, weight="bold")
        ax.set_xlabel("")
        ax.set_ylabel(metric.replace("_", " ").title(), fontsize=11)
        ax.tick_params(axis="x", rotation=35, labelsize=9)
        ax.tick_params(axis="y", labelsize=9)

    for index in range(len(metrics), len(axes_list)):
        axes_list[index].axis("off")

    fig.suptitle(args.title, fontsize=17, weight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
