#!/usr/bin/env python3
"""
SEC Analysis PDF Report Builder
================================
Generates a structured, publication-quality PDF report from SEC analysis results.
Uses fpdf2 with Unicode TTF fonts (DejaVu Sans from matplotlib bundle).

Install:  pip install fpdf2
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

import matplotlib
from fpdf import FPDF

from sec_report_common import select_representative_constructs


# ─── Constants ──────────────────────────────────────────────────────────────────

CHAIN_A_MW = 52.9   # kDa
CHAIN_B_MW = 26.7   # kDa
HETERODIMER_MW = CHAIN_A_MW + CHAIN_B_MW

HDR = (41, 65, 122)     # dark blue
ACC = (52, 152, 219)    # accent blue
TXT = (40, 40, 40)      # body text
SUB = (100, 100, 100)   # subtle text
WHT = (255, 255, 255)

# DejaVu Sans TTF fonts shipped with matplotlib
_MPL_FONT_DIR = os.path.join(matplotlib.get_data_path(), 'fonts', 'ttf')


# ─── PDF Builder ────────────────────────────────────────────────────────────────

class SECReportPDF(FPDF):
    """Custom PDF report class for SEC analysis (Unicode-safe)."""

    FONT = 'DejaVu'  # alias registered below

    def __init__(self, void_volume: float = 8.0, report_profile: str = "full"):
        super().__init__()
        self.v0 = void_volume
        self.report_profile = report_profile
        self.set_auto_page_break(auto=True, margin=22)
        self._register_fonts()

    def _register_fonts(self):
        """Register DejaVu Sans as a Unicode TTF font family."""
        self.add_font(self.FONT, '',  os.path.join(_MPL_FONT_DIR, 'DejaVuSans.ttf'))
        self.add_font(self.FONT, 'B', os.path.join(_MPL_FONT_DIR, 'DejaVuSans-Bold.ttf'))
        self.add_font(self.FONT, 'I', os.path.join(_MPL_FONT_DIR, 'DejaVuSans-Oblique.ttf'))
        self.add_font(self.FONT, 'BI', os.path.join(_MPL_FONT_DIR, 'DejaVuSans-BoldOblique.ttf'))

    # ── chrome ──────────────────────────────────────────────────────────────

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.FONT, 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 8, 'SEC Analysis Report  |  De Novo Protein Oligomers', align='L')
            self.set_draw_color(*ACC)
            self.set_line_width(0.3)
            self.line(15, 11, self.w - 15, 11)
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.FONT, 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    # ── primitives ──────────────────────────────────────────────────────────

    def section(self, title: str, level: int = 1):
        if level == 1:
            self.ln(4)
            self.set_font(self.FONT, 'B', 16)
            self.set_text_color(*HDR)
            self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(*ACC)
            self.set_line_width(0.4)
            self.line(15, self.get_y(), self.w - 15, self.get_y())
            self.ln(3)
        elif level == 2:
            self.ln(3)
            self.set_font(self.FONT, 'B', 13)
            self.set_text_color(55, 55, 55)
            self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)
        else:
            self.set_font(self.FONT, 'BI', 11)
            self.set_text_color(80, 80, 80)
            self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")

    def body(self, text: str):
        self.set_font(self.FONT, '', 10)
        self.set_text_color(*TXT)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def _interpretation_text(self, result) -> str:
        dom = result.dominant_species.replace('_', ' ')
        hom = result.homogeneity.replace('_', ' ')
        txt = f'Dominant species: {dom}. Sample homogeneity: {hom}. '
        if result.has_aggregation:
            txt += (
                f'Aggregation is present ({result.aggregation_pct:.0f}% of total area), '
                f'indicating potential stability or solubility issues. '
            )
        if result.quality_score >= 7:
            txt += (
                'This construct displays a well-behaved SEC profile with high '
                'monodispersity, suitable for downstream biophysical characterization.'
            )
        elif result.quality_score >= 4:
            txt += (
                'This construct shows a moderate SEC profile. Buffer or construct '
                'optimization may improve homogeneity.'
            )
        else:
            txt += (
                'This construct shows a poor SEC profile, suggesting significant '
                'heterogeneity or instability. Redesign may be necessary.'
            )
        return txt

    def bullet(self, text: str, indent: float = 8):
        self.set_font(self.FONT, '', 10)
        self.set_text_color(*TXT)
        left = self.l_margin + indent
        self.set_x(left)
        self.cell(5, 5.5, '-')
        self.set_font(self.FONT, '', 10)
        self.multi_cell(self.w - left - 5 - self.r_margin, 5.5, text)

    def figure(self, path: str, caption: str, w: int = 170):
        if not path or not os.path.exists(path):
            return
        if self.get_y() > 190:
            self.add_page()
        try:
            img_w = min(w, self.w - 34)
            self.image(path, x=15 + (self.w - 30 - img_w) / 2, w=img_w)
        except Exception:
            self.body(f"[Could not embed: {Path(path).name}]")
            return
        self.ln(2)
        self.set_font(self.FONT, 'I', 9)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 4.5, caption)
        self.ln(3)

    def table(self, headers: List[str], rows: List[List[str]],
              widths: Optional[List[float]] = None):
        if not widths:
            avail = self.w - 30
            widths = [avail / len(headers)] * len(headers)
        # header row
        self.set_font(self.FONT, 'B', 9)
        self.set_fill_color(*HDR)
        self.set_text_color(*WHT)
        for i, h in enumerate(headers):
            self.cell(widths[i], 7, h, border=1, fill=True, align='C')
        self.ln()
        # data
        self.set_font(self.FONT, '', 9)
        self.set_text_color(*TXT)
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(240, 245, 250)
            else:
                self.set_fill_color(*WHT)
            for i, cell in enumerate(row):
                self.cell(widths[i], 6.5, str(cell)[:30], border=1, fill=True, align='C')
            self.ln()
        self.ln(3)

    # ── pages ───────────────────────────────────────────────────────────────

    def _title_page(self):
        self.add_page()
        self.ln(45)
        self.set_font(self.FONT, 'B', 26)
        self.set_text_color(*HDR)
        self.multi_cell(0, 13, 'SEC Analysis of De Novo\nDesigned Protein Oligomers', align='C')
        self.ln(8)
        self.set_font(self.FONT, '', 14)
        self.set_text_color(*SUB)
        self.cell(0, 8, 'Comprehensive Technical Report', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(18)
        self.set_font(self.FONT, '', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 7, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, 'Pipeline: BioClaw SEC Analysis v1.0',
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, f'Chain A: ~481 aa (~{CHAIN_A_MW:.1f} kDa)  |  '
                        f'Chain B: ~243 aa (~{CHAIN_B_MW:.1f} kDa)',
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, f'Void volume (V\u2080): {self.v0:.1f} mL',
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(25)
        self.set_draw_color(*ACC)
        self.set_line_width(0.5)
        self.line(15, self.get_y(), self.w - 15, self.get_y())
        self.ln(5)
        self.set_font(self.FONT, 'I', 9)
        self.set_text_color(120, 120, 120)
        self.multi_cell(0, 5,
            'Disclaimer: Peak classifications are approximate and based on relative elution '
            'behavior. Without a column-specific calibration curve, exact molecular weights '
            'cannot be assigned. All interpretations should be validated with orthogonal '
            'biophysical methods (SEC-MALS, AUC, nsEM, native MS).')

    def _exec_summary(self, results):
        self.add_page()
        self.section('Executive Summary')
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        n = len(results)
        ng = sum(1 for r in results if r.quality_score >= 7)
        nm = sum(1 for r in results if 4 <= r.quality_score < 7)
        np_ = sum(1 for r in results if r.quality_score < 4)

        self.body(
            f'This report presents SEC analysis of {n} protein construct(s) from a de novo '
            f'protein assembly project targeting oligomeric ring-like structures. '
            f'Results: {ng} high-quality (\u22657/10), {nm} moderate (4\u20137/10), '
            f'{np_} poor (<4/10).')

        if ng > 0:
            top_names = [r.name for r in sr if r.quality_score >= 7]
            if len(top_names) > 5:
                tops = ', '.join(top_names[:5]) + f', and {len(top_names) - 5} more'
            else:
                tops = ', '.join(top_names)
            self.body(f'Top candidate(s): {tops}')

        self.section('Construct Overview', 2)
        hdrs = ['Construct', 'Score', 'Dominant', 'Homogeneity', 'Agg.', 'Peaks']
        rows = []
        for r in sr:
            rows.append([
                r.name[:22],
                f'{r.quality_score:.1f}',
                r.dominant_species.replace('_', ' ').title()[:16],
                r.homogeneity.replace('_', ' ').title()[:18],
                f'{r.aggregation_pct:.0f}%' if r.has_aggregation else 'No',
                str(len(r.peaks)),
            ])
        self.table(hdrs, rows, [38, 16, 32, 36, 16, 16])

    def _background(self):
        self.add_page()
        self.section('1. Background')
        self.body(
            'This project involves de novo designed protein assemblies targeting distinct '
            'oligomeric states: monomers, dimers, higher-order oligomers, and ring-like '
            'architectures. Size-exclusion chromatography (SEC) serves as the primary '
            'screening tool to evaluate whether designed proteins assemble into their '
            'intended quaternary structures.')
        self.body(
            f'The constructs consist of two polypeptide chains: Chain A (~481 amino acids, '
            f'~{CHAIN_A_MW:.1f} kDa) and Chain B (~243 amino acids, ~{CHAIN_B_MW:.1f} kDa). '
            f'The minimal functional unit is a heterodimer with an expected molecular weight '
            f'of ~{HETERODIMER_MW:.1f} kDa. Successful ring assembly would yield species '
            f'with apparent molecular weights that are integer multiples of the heterodimer '
            f'(e.g., hexameric ring ~{HETERODIMER_MW * 3:.0f} kDa, octameric ring '
            f'~{HETERODIMER_MW * 4:.0f} kDa).')
        self.body(
            'In SEC, larger assemblies elute earlier (lower elution volume) due to reduced '
            'partitioning into the column matrix pores. The void volume (V\u2080) represents the '
            'exclusion limit beyond which species are too large for size-based separation, '
            'and peaks at V\u2080 typically indicate aggregation.')

    def _methods(self):
        self.section('2. Methods')
        self.body('SEC data were analyzed by an automated computational pipeline:')
        self.bullet('Data parsing: auto-detection of elution volume and absorbance columns '
                    'from CSV/TSV/XLSX files')
        self.bullet('Signal smoothing: Savitzky\u2013Golay filter (window 15, polynomial order 3)')
        self.bullet('Peak detection: scipy.signal.find_peaks with adaptive height, distance, '
                    'and prominence thresholds')
        self.bullet('Peak width: full width at half-maximum (FWHM) via scipy.signal.peak_widths')
        self.bullet('Peak area: trapezoidal integration with extended boundaries')
        self.bullet('Classification: relative to void volume (V\u2080) \u2014 see classification table')
        self.ln(2)

        self.section('Classification Scheme', 3)
        cls_hdrs = ['Elution Region', 'Classification', 'Interpretation']
        cls_rows = [
            ['\u2264 V\u2080 + 0.5 mL', 'Aggregate', 'Excluded; non-specific'],
            ['V\u2080 + 0.5\u20132.5 mL', 'Large Oligomer', 'High-MW assemblies, rings'],
            ['V\u2080 + 2.5\u20134.5 mL', 'Oligomer', 'Trimers, tetramers'],
            ['V\u2080 + 4.5\u20136.5 mL', 'Dimer', 'Heterodimer range'],
            ['V\u2080 + 6.5\u20139.0 mL', 'Monomer', 'Individual chains'],
            ['> V\u2080 + 9.0 mL', 'Small Molecule', 'Buffer, degradation'],
        ]
        self.table(cls_hdrs, cls_rows, [42, 35, 78])

        self.body(
            'Note: classifications are approximate. Without a molecular weight calibration '
            'curve for the specific column and running conditions, exact molecular weights '
            'cannot be determined. Non-globular or elongated proteins may elute at '
            'anomalously early volumes.')

    def _results(self, results, figs_dir):
        if self.report_profile == 'compact':
            self._results_compact(results)
            return

        self.add_page()
        self.section('3. Results')
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)

        for idx, r in enumerate(sr):
            if idx > 0:
                self.add_page()
            self.section(f'3.{idx + 1}  {r.name}', 2)

            # peak table
            if r.peaks:
                self.section('Detected Peaks', 3)
                ph = ['#', 'Ve (mL)', 'Height', 'FWHM (mL)', 'Area %', 'Class']
                pr = [[str(p.peak_number),
                       f'{p.elution_volume:.2f}',
                       f'{p.height:.1f}',
                       f'{p.fwhm:.2f}',
                       f'{p.relative_area_pct:.1f}',
                       p.classification.replace('_', ' ').title()[:16]]
                      for p in r.peaks]
                self.table(ph, pr, [10, 24, 24, 24, 22, 42])

            # interpretation
            self.section('Interpretation', 3)
            self.body(self._interpretation_text(r))

            for note in r.notes:
                self.bullet(note)

            # annotated chromatogram
            if r.figure_path:
                self.figure(r.figure_path,
                            f'Figure {idx + 2}. Annotated SEC chromatogram of {r.name}. '
                            f'Peaks labeled with classification, elution volume, and '
                            f'relative area percentage.')

            # original user image
            if r.original_image_path:
                self.figure(r.original_image_path,
                            f'Original SEC chromatogram for {r.name} (user-provided).',
                            w=150)

    def _results_compact(self, results):
        self.add_page()
        self.section('3. Results')
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        primary_sr = [r for r in sr if getattr(r, 'cohort', 'primary') == 'primary']
        selected = select_representative_constructs(primary_sr or sr, max_items=6)

        self.body(
            f'This compact report highlights {len(selected)} representative constructs '
            f'out of {len(sr)} total. The exhaustive per-construct chromatogram set is '
            f'reserved for the full report and supporting outputs.'
        )

        self.section('Selected Construct Summary', 2)
        headers = ['Construct', 'Score', 'Dominant', 'Homogeneity', 'Agg.']
        rows = []
        for r in selected:
            rows.append([
                r.name[:28],
                f'{r.quality_score:.1f}',
                r.dominant_species.replace('_', ' ').title()[:16],
                r.homogeneity.replace('_', ' ').title()[:18],
                f'{r.aggregation_pct:.0f}%' if r.has_aggregation else '0%',
            ])
        self.table(headers, rows, [52, 16, 30, 48, 16])

        self.section('Selected Construct Highlights', 2)
        for r in selected:
            self.section(r.name[:48], 3)
            self.body(self._interpretation_text(r))
            for note in r.notes[:2]:
                self.bullet(note)

        # Historical context
        context = [r for r in sr if getattr(r, 'cohort', 'primary') == 'context']
        if context:
            years = sorted({str(getattr(r, 'cohort_year', '')) for r in context} - {''})
            self.section('Historical Context', 2)
            self.body(
                f'{len(context)} constructs from earlier experiment(s) '
                f'({", ".join(years)}) are included for reference only.'
            )
            hdrs = ['Construct', 'Score', 'Dominant', 'Classification']
            rows = [[r.name[:28], f'{r.quality_score:.1f}',
                     r.dominant_species.replace('_', ' ').title()[:16],
                     r.homogeneity.replace('_', ' ').title()[:18]]
                    for r in context]
            self.table(hdrs, rows, [52, 16, 48, 46])

    def _comparison(self, results, figs_dir):
        if len(results) < 2:
            return
        self.add_page()
        self.section('4. Comparative Analysis')

        comp = os.path.join(figs_dir, 'comparison_overlay.png')
        self.figure(comp,
                    'Normalized SEC profile overlay. Earlier elution corresponds to '
                    'larger apparent molecular size.')

        zone = os.path.join(figs_dir, 'zone_fractions.png')
        if self.report_profile == 'compact':
            self.figure(zone,
                        'Zone-fraction summary across constructs. Stacked fractions show '
                        'how signal is distributed across SEC elution regions.')

        rank = os.path.join(figs_dir, 'ranking_summary.png')
        self.figure(rank,
                    'Construct quality ranking based on SEC profile characteristics.')

        self.section('Ranking', 2)
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        for i, r in enumerate(sr):
            dom = r.dominant_species.replace('_', ' ')
            hom = r.homogeneity.replace('_', ' ')
            self.bullet(f'{i + 1}. {r.name} -- Q={r.quality_score:.1f}/10 | '
                        f'{dom} | {hom}')

    def _discussion(self, results):
        self.add_page()
        sec_n = '5' if len(results) > 1 else '4'
        self.section(f'{sec_n}. Discussion')

        self.section('Oligomerization Behavior', 2)
        counts = {}
        for r in results:
            s = r.dominant_species.replace('_', ' ')
            counts[s] = counts.get(s, 0) + 1
        dist = ', '.join(f'{k} ({v})' for k, v in counts.items())
        self.body(f'Dominant species distribution across constructs: {dist}.')

        good = [r for r in results if r.quality_score >= 7]
        poor = [r for r in results if r.quality_score < 4]
        mid = [r for r in results if 4 <= r.quality_score < 7]

        if good:
            self.section('Successful Designs', 2)
            for r in good:
                self.bullet(
                    f'{r.name}: sharp {r.dominant_species.replace("_", " ")} peak, '
                    f'{r.homogeneity.replace("_", " ")} profile (Q={r.quality_score:.1f})')
        if poor:
            self.section('Failed Designs', 2)
            for r in poor:
                reasons = '; '.join(r.notes) if r.notes else 'poor overall profile'
                self.bullet(f'{r.name}: {reasons} (Q={r.quality_score:.1f})')
        if mid:
            self.section('Ambiguous Cases', 2)
            for r in mid:
                self.bullet(
                    f'{r.name}: moderate profile, dominant '
                    f'{r.dominant_species.replace("_", " ")} (Q={r.quality_score:.1f})')

        self.section('Design Patterns', 2)
        ring_candidates = [r for r in results
                           if r.dominant_species in ('large_oligomer', 'oligomer')
                           and r.quality_score >= 5]
        if ring_candidates:
            self.body(
                'The following constructs show dominant higher-order oligomeric species '
                'consistent with ring-like assembly: '
                + ', '.join(r.name for r in ring_candidates) + '. '
                'These are priority candidates for structural validation by electron '
                'microscopy.')
        else:
            self.body(
                'No constructs show strong evidence of ring-like assembly based on SEC '
                'profiles alone. This may indicate that the designs favor lower-order '
                'oligomeric states, or that ring formation requires specific conditions '
                'not captured in the current SEC experiments.')

    def _conclusion(self, results):
        self.add_page()
        sec_n = '6' if len(results) > 1 else '5'
        self.section(f'{sec_n}. Conclusion & Recommendations')

        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        good = [r for r in sr if r.quality_score >= 7]

        self.section('Top Candidates', 2)
        if good:
            self.body('The following constructs are recommended for advancement '
                      'to structural and functional characterization:')
            for r in good:
                dom = r.dominant_species.replace('_', ' ')
                hom = r.homogeneity.replace('_', ' ')
                self.bullet(f'{r.name} (Q={r.quality_score:.1f}) -- {dom}, {hom}')
        else:
            self.body(
                f'No constructs scored above 7.0/10. The best available candidate is '
                f'{sr[0].name} (Q={sr[0].quality_score:.1f}). Consider optimization '
                f'before proceeding to downstream assays.')

        self.section('Recommended Next Steps', 2)
        steps = [
            'SEC-MALS (multi-angle light scattering): determine absolute molecular '
            'weight and confirm oligomeric state without calibration assumptions',
            'Analytical ultracentrifugation (AUC): orthogonal validation of '
            'molecular weight and stoichiometry in solution',
            'Negative-stain electron microscopy (nsEM): directly visualize '
            'ring-like architecture and particle homogeneity',
            'Differential scanning fluorimetry (nanoDSF): assess thermal stability '
            'of top candidates',
            'Native mass spectrometry: confirm subunit stoichiometry and identify '
            'proteoforms',
            'Cross-linking mass spectrometry (XL-MS): map inter-subunit interfaces '
            'and validate assembly topology',
            'Buffer optimization for ambiguous constructs: screen pH (6.0-8.5), '
            'NaCl (50-500 mM), and additives (glycerol, arginine)',
        ]
        for s in steps:
            self.bullet(s)

        self.ln(5)
        self.section('Caveats', 2)
        self.body(
            'This analysis is based on SEC elution profiles and carries inherent '
            'limitations: (1) SEC measures apparent hydrodynamic radius, not true '
            'molecular weight -- non-globular proteins may elute anomalously; '
            '(2) peak classifications rely on relative elution position without '
            'column-specific calibration; (3) SEC cannot distinguish conformational '
            'variants with similar size; (4) low-abundance species may be below '
            'detection limits. Orthogonal biophysical methods are essential for '
            'definitive characterization of oligomeric state and assembly architecture.')

    # ── public API ──────────────────────────────────────────────────────────

    def build(self, results, image_files, figs_dir, output_path):
        """Assemble and write the complete PDF report."""
        self.alias_nb_pages()
        self._title_page()
        self._exec_summary(results)
        self._background()
        self._methods()
        self._results(results, figs_dir)
        self._comparison(results, figs_dir)
        self._discussion(results)
        self._conclusion(results)
        self.output(output_path)
        return output_path

    def build_appendix(self, results, image_files, figs_dir, output_path):
        """Generate appendix PDF with all per-construct chromatograms and tables."""
        self.alias_nb_pages()

        # Title page
        self.add_page()
        self.ln(45)
        self.set_font(self.FONT, 'B', 22)
        self.set_text_color(*HDR)
        self.multi_cell(0, 11, 'SEC Analysis\nSupporting Material', align='C')
        self.ln(8)
        self.set_font(self.FONT, '', 12)
        self.set_text_color(*SUB)
        self.cell(0, 8, 'Per-Construct Chromatograms and Peak Tables',
                  align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(12)
        self.set_font(self.FONT, '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 7, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                  new_x="LMARGIN", new_y="NEXT")

        # Individual grid
        grid_path = os.path.join(figs_dir, 'individual_grid.png')
        if os.path.exists(grid_path):
            self.add_page()
            self.section('A. Individual Chromatogram Grid')
            self.figure(grid_path,
                        'Individual SEC chromatograms for all constructs.')

        # Per-construct details
        sr = sorted(results, key=lambda r: r.quality_score, reverse=True)
        self.add_page()
        self.section('B. Per-Construct Analysis')

        for idx, r in enumerate(sr):
            if idx > 0:
                self.add_page()
            self.section(f'{r.name}', 2)

            if r.peaks:
                self.section('Detected Peaks', 3)
                ph = ['#', 'Ve (mL)', 'Height', 'FWHM (mL)', 'Area %', 'Class']
                pr = [[str(p.peak_number),
                       f'{p.elution_volume:.2f}',
                       f'{p.height:.1f}',
                       f'{p.fwhm:.2f}',
                       f'{p.relative_area_pct:.1f}',
                       p.classification.replace('_', ' ').title()[:16]]
                      for p in r.peaks]
                self.table(ph, pr, [10, 24, 24, 24, 22, 42])

            self.section('Interpretation', 3)
            self.body(self._interpretation_text(r))

            for note in r.notes:
                self.bullet(note)

            if r.figure_path:
                self.figure(r.figure_path,
                            f'Annotated SEC chromatogram of {r.name}.')

            if r.original_image_path:
                self.figure(r.original_image_path,
                            f'Original chromatogram for {r.name} (user-provided).',
                            w=150)

        self.output(output_path)
        return output_path
