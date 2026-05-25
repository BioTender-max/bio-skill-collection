#!/bin/bash
# ============================================================
#  SEC Report Skill — End-to-End Test Script
# ============================================================
#
#  Usage:
#    cd BioClaw/container/skills/sec-report/tests
#    bash run_test.sh
#
#  What it does:
#    1. Install dependencies (fpdf2)
#    2. Generate synthetic SEC data (6 constructs + images)
#    3. Run pipeline on individual files (directory mode)
#    4. Run pipeline on ZIP file (ZIP mode)
#    5. Verify all outputs exist
#    6. Print summary
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEST_DIR="$SCRIPT_DIR/workspace"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  SEC Report Skill — End-to-End Test${NC}"
echo -e "${BLUE}============================================================${NC}"

# Clean previous test runs
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# ── Step 1: Check dependencies ──────────────────────────────
echo -e "\n${BLUE}[1/5] Checking dependencies...${NC}"
python -c "import fpdf" 2>/dev/null || {
    echo "  Installing fpdf2..."
    pip install fpdf2 -q
}
python -c "import scipy, matplotlib, pandas, numpy; print('  All dependencies OK')"

# ── Step 2: Generate test data ──────────────────────────────
echo -e "\n${BLUE}[2/5] Generating synthetic SEC data...${NC}"
python "$SCRIPT_DIR/generate_test_data.py" \
    --output-dir "$TEST_DIR/test_dataset"

# ── Step 3: Test directory mode ─────────────────────────────
echo -e "\n${BLUE}[3/5] Testing directory input mode...${NC}"
python "$SKILL_DIR/sec_pipeline.py" \
    --input "$TEST_DIR/test_dataset" \
    --output "$TEST_DIR/output_dir_mode" \
    --renderer auto \
    --report-profile full

# ── Step 4: Test ZIP mode ───────────────────────────────────
echo -e "\n${BLUE}[4/5] Testing ZIP input mode...${NC}"
python "$SKILL_DIR/sec_pipeline.py" \
    --input "$TEST_DIR/test_dataset/SEC_test_dataset.zip" \
    --output "$TEST_DIR/output_zip_mode" \
    --renderer auto \
    --report-profile compact

# ── Step 5: Verify outputs ──────────────────────────────────
echo -e "\n${BLUE}[5/5] Verifying outputs...${NC}"

PASS=0
FAIL=0

check_file() {
    local path="$1"
    local desc="$2"
    if [ -f "$path" ] && [ -s "$path" ]; then
        echo -e "  ${GREEN}PASS${NC}  $desc"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}  $desc  (missing or empty: $path)"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "  Directory mode outputs:"
check_file "$TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf" "PDF report (dir mode)"
check_file "$TEST_DIR/output_dir_mode/analysis_summary.json" "JSON summary (dir mode)"
check_file "$TEST_DIR/output_dir_mode/figures/comparison_overlay.png" "Comparison overlay"
check_file "$TEST_DIR/output_dir_mode/figures/ranking_summary.png" "Ranking chart"

for name in Ring_Design_01 Dimer_Variant_03 Aggregator_05 Mixed_Assembly_07 Monomer_Only_09 Ring_Design_11; do
    check_file "$TEST_DIR/output_dir_mode/figures/${name}_annotated.png" "Annotated: $name"
done

echo ""
echo "  ZIP mode outputs:"
check_file "$TEST_DIR/output_zip_mode/SEC_Analysis_Report.pdf" "PDF report (ZIP mode)"
check_file "$TEST_DIR/output_zip_mode/analysis_summary.json" "JSON summary (ZIP mode)"

echo ""
echo "  Metadata checks:"
TEST_DIR="$TEST_DIR" python - <<'PY'
import json
import os
from pathlib import Path

checks = [
    Path(os.environ["TEST_DIR"]) / "output_dir_mode" / "analysis_summary.json",
    Path(os.environ["TEST_DIR"]) / "output_zip_mode" / "analysis_summary.json",
]

required_keys = [
    "renderer",
    "requested_renderer",
    "report_profile",
    "fallback_used",
]

for path in checks:
    data = json.loads(path.read_text())
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise SystemExit(f"Missing metadata keys in {path}: {missing}")
    print(f"  PASS  metadata present in {path.name}: renderer={data['renderer']}, profile={data['report_profile']}")
PY

echo ""
echo "  Compact/full page-count check:"
if command -v pdfinfo >/dev/null 2>&1; then
    FULL_PAGES=$(pdfinfo "$TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf" | awk '/^Pages:/ {print $2}')
    COMPACT_PAGES=$(pdfinfo "$TEST_DIR/output_zip_mode/SEC_Analysis_Report.pdf" | awk '/^Pages:/ {print $2}')
    FULL_SIZE=$(pdfinfo "$TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf" | awk -F': *' '/^Page size:/ {print $2}')
    COMPACT_SIZE=$(pdfinfo "$TEST_DIR/output_zip_mode/SEC_Analysis_Report.pdf" | awk -F': *' '/^Page size:/ {print $2}')
    echo "  full pages:    $FULL_PAGES"
    echo "  compact pages: $COMPACT_PAGES"
    if [ "$COMPACT_PAGES" -le "$FULL_PAGES" ]; then
        echo -e "  ${GREEN}PASS${NC}  compact report is not longer than full report"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC}  compact report should not exceed full report length"
        FAIL=$((FAIL + 1))
    fi
    echo "  full page size:    $FULL_SIZE"
    echo "  compact page size: $COMPACT_SIZE"
    case "$FULL_SIZE $COMPACT_SIZE" in
        *A4* )
            echo -e "  ${GREEN}PASS${NC}  reports are generated in A4"
            PASS=$((PASS + 1))
            ;;
        * )
            echo -e "  ${RED}FAIL${NC}  expected A4 page size in generated reports"
            FAIL=$((FAIL + 1))
            ;;
    esac
else
    echo "  SKIP  pdfinfo not available; page-count comparison skipped"
fi

# ── Summary ─────────────────────────────────────────────────
echo ""
echo -e "${BLUE}============================================================${NC}"
PDF_SIZE=$(du -h "$TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf" 2>/dev/null | cut -f1)
echo -e "  PDF size: ${PDF_SIZE}"
echo -e "  Results:  ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"

if [ $FAIL -eq 0 ]; then
    echo -e "  ${GREEN}ALL TESTS PASSED${NC}"
else
    echo -e "  ${RED}SOME TESTS FAILED${NC}"
fi
echo -e "${BLUE}============================================================${NC}"

echo ""
echo "  Output files:"
echo "    PDF:  $TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf"
echo "    JSON: $TEST_DIR/output_dir_mode/analysis_summary.json"
echo "    Figs: $TEST_DIR/output_dir_mode/figures/"
echo ""
echo "  To view the PDF:"
echo "    # On local machine, copy it out:"
echo "    scp <server>:$TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf ."
echo "    # Or open in browser (if X11/VNC available):"
echo "    xdg-open $TEST_DIR/output_dir_mode/SEC_Analysis_Report.pdf"
