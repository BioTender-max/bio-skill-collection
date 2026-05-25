#!/usr/bin/env python3
import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a publication-style volcano plot.")
    parser.add_argument("--input", required=True, help="CSV/TSV file with gene, log2FC, and pvalue columns.")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    parser.add_argument("--title", default="Volcano Plot", help="Plot title.")
    parser.add_argument("--fc-col", default="log2FC", help="Fold-change column.")
    parser.add_argument("--p-col", default="pvalue", help="P-value column.")
    parser.add_argument("--label-col", default="gene", help="Label column.")
    parser.add_argument("--fc-threshold", type=float, default=1.0, help="Absolute log2 fold-change threshold.")
    parser.add_argument("--p-threshold", type=float, default=0.05, help="P-value significance threshold.")
    parser.add_argument("--top-labels", type=int, default=12, help="Maximum number of labels to annotate.")
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
    required = {args.fc_col, args.p_col, args.label_col}
    missing = required.difference(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df[[args.label_col, args.fc_col, args.p_col]].dropna().copy()
    df["neg_log10_p"] = -df[args.p_col].clip(lower=1e-300).map(math.log10)

    def classify(row: pd.Series) -> str:
        if row[args.p_col] < args.p_threshold and row[args.fc_col] >= args.fc_threshold:
            return "Upregulated"
        if row[args.p_col] < args.p_threshold and row[args.fc_col] <= -args.fc_threshold:
            return "Downregulated"
        return "Not significant"

    df["group"] = df.apply(classify, axis=1)

    palette = {
        "Upregulated": "#C0392B",
        "Downregulated": "#2E86C1",
        "Not significant": "#B3B6B7",
    }

    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x=args.fc_col,
        y="neg_log10_p",
        hue="group",
        palette=palette,
        s=24,
        linewidth=0,
        alpha=0.85,
        ax=ax,
    )

    ax.axvline(args.fc_threshold, color="#7F8C8D", linestyle="--", linewidth=1)
    ax.axvline(-args.fc_threshold, color="#7F8C8D", linestyle="--", linewidth=1)
    ax.axhline(-math.log10(args.p_threshold), color="#7F8C8D", linestyle="--", linewidth=1)

    label_candidates = df[df["group"] != "Not significant"].copy()
    label_candidates["label_score"] = label_candidates["neg_log10_p"] * label_candidates[args.fc_col].abs()
    label_candidates = label_candidates.nlargest(args.top_labels, "label_score")

    for _, row in label_candidates.iterrows():
        ax.text(
            row[args.fc_col],
            row["neg_log10_p"] + 0.08,
            str(row[args.label_col]),
            fontsize=9,
            ha="center",
            va="bottom",
        )

    ax.set_title(args.title, fontsize=16, weight="bold")
    ax.set_xlabel("log2 Fold Change", fontsize=13)
    ax.set_ylabel("-log10(p-value)", fontsize=13)
    ax.legend(title="", frameon=False, loc="upper right")
    sns.despine(ax=ax)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
