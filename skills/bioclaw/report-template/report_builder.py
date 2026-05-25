#!/usr/bin/env python3
"""
BioClaw Report Builder
Generates publication-quality PDF reports using Typst templates.

Architecture:
  - scientific_report.typ defines styling and reusable components
  - This builder generates a .typ file that imports the template
  - Typst compiles the generated .typ → PDF

Usage:
    from report_builder import ReportBuilder, T

    report = ReportBuilder(
        title="SEC Analysis Report",
        subtitle="De Novo Designed Protein Oligomers",
    )
    report.heading(1, "Background")
    report.text("This report presents...")
    report.heading(1, "Results")
    report.callout("Important finding", title="Key", kind="success")
    report.table(["Col A", "Col B"], [["1", "2"]], caption="Table 1")
    report.image("plots/fig1.png", caption="Figure 1. Overview")
    report.compile("output/report.pdf")
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Typst markup helpers (T namespace for convenience)
# ---------------------------------------------------------------------------

class T:
    """Static helpers that return raw Typst markup strings."""

    @staticmethod
    def table(headers: list[str], rows: list[list[str]],
              caption: Optional[str] = None) -> str:
        h = ", ".join(f'"{h}"' for h in headers)
        r_parts = []
        for row in rows:
            cells = ", ".join(f'"{_esc(c)}"' for c in row)
            r_parts.append(f"    ({cells}),")
        rows_str = "\n".join(r_parts)
        cap = f", caption-text: [{caption}]" if caption else ""
        return f"#data-table(\n  ({h}),\n  (\n{r_parts and rows_str}\n  ){cap},\n)"

    @staticmethod
    def callout(text: str, title: str = "Note",
                kind: str = "note") -> str:
        return f'#callout(title: "{title}", kind: "{kind}")[{text}]'

    @staticmethod
    def image(path: str, caption: Optional[str] = None,
              width: str = "100%") -> str:
        img = f'image("{path}", width: {width})'
        if caption:
            return f"#figure({img}, caption: [{caption}])"
        return f"#{img}"

    @staticmethod
    def metadata_block(pairs: list[tuple[str, str]]) -> str:
        items = ", ".join(f'("{_esc(k)}", "{_esc(v)}")' for k, v in pairs)
        return f"#metadata-block(({items}))"

    @staticmethod
    def metric_cards(metrics: list[dict]) -> str:
        items = ", ".join(
            f'(label: "{_esc(m["label"])}", value: "{_esc(m["value"])}")'
            for m in metrics
        )
        return f"#metric-cards(({items}))"

    @staticmethod
    def pagebreak() -> str:
        return "#pagebreak()"

    @staticmethod
    def vspace(size: str = "12pt") -> str:
        return f"#v({size})"

    @staticmethod
    def text(content: str) -> str:
        return content

    @staticmethod
    def bold(content: str) -> str:
        return f"*{content}*"

    @staticmethod
    def italic(content: str) -> str:
        return f"_{content}_"

    @staticmethod
    def list(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    @staticmethod
    def enum(items: list[str]) -> str:
        return "\n".join(f"+ {item}" for item in items)


def _esc(s: str) -> str:
    """Escape special characters for Typst string literals."""
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


# ---------------------------------------------------------------------------
# ReportBuilder
# ---------------------------------------------------------------------------

@dataclass
class ReportBuilder:
    """Builds a scientific PDF report using the BioClaw Typst template."""

    title: str = "Analysis Report"
    subtitle: str = ""
    author: str = "BioClaw"
    date: str = ""
    project: str = ""
    confidential: str = "Confidential"
    header_left: str = ""

    _parts: list[str] = field(default_factory=list, repr=False)
    _image_dir: Optional[Path] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%B %Y")
        if not self.header_left:
            self.header_left = self.title

    # ── Content Methods ──

    def heading(self, level: int, text: str):
        """Add a heading."""
        prefix = "=" * level
        self._parts.append(f"\n{prefix} {text}\n")

    def text(self, content: str):
        """Add a paragraph."""
        self._parts.append(f"\n{content}\n")

    def raw(self, typst_markup: str):
        """Add raw Typst markup."""
        self._parts.append(f"\n{typst_markup}\n")

    def callout(self, text: str, title: str = "Note", kind: str = "note"):
        """Add a callout box."""
        self._parts.append(f'\n#callout(title: "{title}", kind: "{kind}")[{text}]\n')

    def table(self, headers: list[str], rows: list[list[str]],
              caption: Optional[str] = None):
        """Add a styled table."""
        self._parts.append(f"\n{T.table(headers, rows, caption)}\n")

    def image(self, path: str, caption: Optional[str] = None,
              width: str = "100%"):
        """Add an image/figure."""
        self._parts.append(f"\n{T.image(path, caption, width)}\n")

    def metadata_block(self, pairs: list[tuple[str, str]]):
        """Add a key-value metadata block."""
        self._parts.append(f"\n{T.metadata_block(pairs)}\n")

    def metric_cards(self, metrics: list[dict]):
        """Add metric cards row."""
        self._parts.append(f"\n{T.metric_cards(metrics)}\n")

    def pagebreak(self):
        """Insert a page break."""
        self._parts.append("\n#pagebreak()\n")

    def vspace(self, size: str = "12pt"):
        """Insert vertical space."""
        self._parts.append(f"\n#v({size})\n")

    # ── Build & Compile ──

    def _find_template(self) -> Path:
        """Locate the Typst template library."""
        here = Path(__file__).resolve().parent
        candidates = [
            here / "templates" / "scientific_report.typ",
            Path("/home/node/.claude/skills/report-template/templates"
                 "/scientific_report.typ"),
        ]
        for c in candidates:
            if c.exists():
                return c
        raise FileNotFoundError(
            f"Typst template not found. Searched: {candidates}"
        )

    def _generate_typ(self, template_rel_path: str) -> str:
        """Generate the complete .typ source file."""
        lines = [
            f'#import "{template_rel_path}": *',
            "",
            "#show: report-setup.with(",
            f'  title: "{_esc(self.title)}",',
            f'  subtitle: "{_esc(self.subtitle)}",',
            f'  date: "{_esc(self.date)}",',
            f'  author: "{_esc(self.author)}",',
            f'  project: "{_esc(self.project)}",',
            f'  confidential: "{_esc(self.confidential)}",',
            f'  header-left: "{_esc(self.header_left)}",',
            ")",
            "",
        ]
        lines.extend(self._parts)
        return "\n".join(lines)

    def set_image_dir(self, path: str | Path):
        """Set the directory containing images referenced in the report."""
        self._image_dir = Path(path)

    def compile(self, output_path: str | Path,
                template_path: Optional[str | Path] = None) -> Path:
        """Compile the report to PDF."""
        typst_mod = None
        try:
            import typst as typst_mod  # type: ignore[assignment]
        except ImportError:
            typst_mod = None

        output = Path(output_path).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)

        template = Path(template_path).resolve() if template_path \
            else self._find_template()

        # Work in a temp directory with template and images
        with tempfile.TemporaryDirectory(prefix="bioclaw_report_") as tmpdir:
            tmp = Path(tmpdir)

            # Copy template library
            tmpl_name = "template_lib.typ"
            shutil.copy2(template, tmp / tmpl_name)

            # Copy images if image_dir is explicitly set
            if self._image_dir and self._image_dir.exists():
                for ext in ("*.png", "*.jpg", "*.jpeg", "*.svg"):
                    for img_file in self._image_dir.glob(ext):
                        shutil.copy2(img_file, tmp / img_file.name)
                    for img_file in self._image_dir.rglob(ext):
                        rel = img_file.relative_to(self._image_dir)
                        if len(rel.parts) > 1:  # only subdirs
                            dest = tmp / rel
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(img_file, dest)

            # Generate .typ source
            typ_source = self._generate_typ(tmpl_name)
            typ_file = tmp / "report.typ"
            typ_file.write_text(typ_source, encoding="utf-8")

            # Compile
            if typst_mod is not None:
                typst_mod.compile(
                    str(typ_file),
                    output=str(output),
                    root=str(tmp),
                )
            else:
                typst_bin = shutil.which("typst")
                if not typst_bin:
                    raise ImportError(
                        "Typst compiler unavailable. Install either the "
                        'Python package (`pip install typst`) or the `typst` CLI.'
                    )
                subprocess.run(
                    [
                        typst_bin,
                        "compile",
                        str(typ_file),
                        str(output),
                        "--root",
                        str(tmp),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

        return output

    def compile_to_bytes(self,
                         template_path: Optional[str | Path] = None) -> bytes:
        """Compile the report and return PDF bytes."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            tmp_path = f.name
        try:
            self.compile(tmp_path, template_path)
            return Path(tmp_path).read_bytes()
        finally:
            os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def build_report(title: str, output_path: str, **kwargs) -> ReportBuilder:
    """Create a ReportBuilder with common defaults."""
    return ReportBuilder(title=title, **kwargs)


# ---------------------------------------------------------------------------
# Demo / self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    report = ReportBuilder(
        title="BioClaw Template Demo",
        subtitle="Publication-Quality Report System",
        author="BioClaw",
        project="Template Development",
    )

    # Metadata
    report.metadata_block([
        ("Constructs analysed", "6"),
        ("Detection", "UV 280 nm"),
        ("Report generated", datetime.now().strftime("%Y-%m-%d")),
        ("Analysis", "Automated (Python / Typst)"),
    ])

    # Section 1
    report.heading(1, "1. Background")
    report.text(
        "This report demonstrates the BioClaw report template system. "
        "It produces publication-quality PDF reports with professional "
        "styling inspired by leading biotech platforms."
    )
    report.callout(
        "All measurements were taken under standard conditions (25 C, pH 7.4). "
        "No absolute molecular weight calibration was applied.",
        title="Note", kind="note",
    )

    # Section 2
    report.heading(1, "2. Results")

    report.heading(2, "2.1 Summary Metrics")
    report.metric_cards([
        {"label": "Constructs", "value": "6"},
        {"label": "Success Rate", "value": "67%"},
        {"label": "Best pLDDT", "value": "94.7"},
        {"label": "Quality", "value": "A+"},
    ])

    report.vspace("12pt")

    report.heading(2, "2.2 Detailed Results")
    report.table(
        ["Construct", "Peak (mL)", "Classification", "Quality"],
        [
            ["Ring_Design_01", "10.0", "Oligomer (ring)", "Excellent"],
            ["Ring_Design_11", "9.8", "Oligomer (ring)", "Very Good"],
            ["Dimer_Variant_03", "13.5", "Dimer", "Good"],
            ["Monomer_Only_09", "15.5", "Monomer", "Excellent"],
            ["Aggregator_05", "8.0", "Aggregate", "Poor"],
            ["Mixed_Assembly_07", "9.6", "Heterogeneous", "Poor"],
        ],
        caption="Table 1. Summary of all constructs analysed.",
    )

    report.callout(
        "Ring_Design_01 and Ring_Design_11 are the top candidates for "
        "structural validation by cryo-EM or SEC-MALS.",
        title="Key Finding", kind="success",
    )

    # Section 3
    report.heading(1, "3. Discussion")
    report.text(
        "The results demonstrate that the ring design strategy successfully "
        "produces higher-order oligomeric assemblies. Two out of six constructs "
        "show clear evidence of ring formation based on their early elution "
        "volumes and monodisperse SEC profiles."
    )

    report.callout(
        "Aggregator_05 shows significant void-volume signal indicating "
        "non-specific aggregation. Redesign of the interface is recommended.",
        title="Warning", kind="warning",
    )

    # Section 4
    report.heading(1, "4. Conclusions and Recommendations")
    report.text("Based on the SEC analysis, we recommend:")
    report.raw(T.enum([
        "*Ring_Design_01*: Proceed to cryo-EM and SEC-MALS",
        "*Ring_Design_11*: Proceed to SEC-MALS, minor optimization needed",
        "*Dimer_Variant_03*: Use as positive control",
        "*Aggregator_05*: Redesign interface residues",
        "*Mixed_Assembly_07*: Buffer screen to improve homogeneity",
    ]))

    pdf_path = report.compile("/tmp/bioclaw_demo_report.pdf")
    print(f"Report generated: {pdf_path} "
          f"({pdf_path.stat().st_size / 1024:.0f} KB)")
