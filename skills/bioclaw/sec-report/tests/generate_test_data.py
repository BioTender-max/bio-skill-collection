#!/usr/bin/env python3
"""
Generate realistic synthetic SEC test data for pipeline validation.
Creates a ZIP file with multiple constructs simulating different outcomes.

Usage:
    python generate_test_data.py [--output-dir /path/to/dir]
"""

import os
import sys
import zipfile
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def gaussian(x, mu, sigma, amplitude):
    """Generate a Gaussian peak."""
    return amplitude * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def make_sec_trace(volumes, peaks_spec, noise_level=0.3):
    """
    Generate a simulated SEC trace.

    peaks_spec: list of (center_mL, sigma_mL, amplitude_mAU)
    """
    signal = np.zeros_like(volumes)
    for mu, sigma, amp in peaks_spec:
        signal += gaussian(volumes, mu, sigma, amp)
    # Add realistic noise
    noise = np.random.normal(0, noise_level, len(volumes))
    signal = np.maximum(signal + noise, 0)
    return signal


def save_csv(filepath, volumes, absorbance, detector="UV 280nm (mAU)"):
    """Save as SEC CSV data file."""
    with open(filepath, 'w') as f:
        f.write(f"Volume (mL),{detector}\n")
        for v, a in zip(volumes, absorbance):
            f.write(f"{v:.3f},{a:.2f}\n")


def plot_chromatogram(filepath, volumes, absorbance, title):
    """Generate a mock SEC chromatogram image (simulating instrument output)."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(volumes, absorbance, 'b-', linewidth=0.8)
    ax.fill_between(volumes, absorbance, alpha=0.1, color='blue')
    ax.set_xlabel('Elution Volume (mL)')
    ax.set_ylabel('UV 280nm (mAU)')
    ax.set_title(title)
    ax.axvline(x=8.0, color='gray', linestyle=':', alpha=0.5, linewidth=0.5)
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)


def generate_test_data(output_dir: str):
    """Generate a complete test dataset with 6 constructs."""

    os.makedirs(output_dir, exist_ok=True)
    volumes = np.arange(0, 25, 0.05)  # 0-25 mL, 0.05 mL resolution

    constructs = {
        # ── Construct 1: Ideal ring candidate ──────────────────────────
        # Single sharp peak at ~10 mL (large oligomer region)
        # Minimal aggregation, no monomer
        "Ring_Design_01": {
            "peaks": [(10.0, 0.6, 120)],
            "noise": 0.2,
            "description": "Ideal ring assembly - single sharp oligomer peak",
        },

        # ── Construct 2: Good dimer with some oligomer ─────────────────
        # Main peak at ~13.5 mL (dimer), minor oligomer at ~10.5 mL
        "Dimer_Variant_03": {
            "peaks": [(13.5, 0.7, 80), (10.5, 0.5, 25)],
            "noise": 0.3,
            "description": "Clean dimer with minor oligomer shoulder",
        },

        # ── Construct 3: Aggregation-prone design ──────────────────────
        # Large void volume peak, smaller oligomer and monomer
        "Aggregator_05": {
            "peaks": [(8.0, 0.4, 90), (11.5, 0.8, 30), (15.0, 0.6, 20)],
            "noise": 0.5,
            "description": "Aggregation-dominated profile",
        },

        # ── Construct 4: Mixed oligomeric states ───────────────────────
        # Multiple peaks of similar height - polydisperse
        "Mixed_Assembly_07": {
            "peaks": [(9.5, 0.5, 45), (11.0, 0.6, 50), (13.0, 0.7, 40), (15.5, 0.5, 30)],
            "noise": 0.4,
            "description": "Polydisperse - multiple oligomeric states",
        },

        # ── Construct 5: Clean monomer (design failed to assemble) ─────
        # Single peak in monomer region
        "Monomer_Only_09": {
            "peaks": [(15.5, 0.7, 95)],
            "noise": 0.2,
            "description": "Only monomer - assembly failed",
        },

        # ── Construct 6: Promising ring with minor monomer ─────────────
        # Dominant large oligomer peak + small monomer peak
        "Ring_Design_11": {
            "peaks": [(9.8, 0.55, 100), (15.0, 0.6, 15)],
            "noise": 0.25,
            "description": "Strong ring candidate with minor monomer leak",
        },
    }

    # Generate data and images
    for name, spec in constructs.items():
        print(f"  Generating: {name}")

        absorbance = make_sec_trace(volumes, spec["peaks"], spec["noise"])

        # Save CSV
        csv_path = os.path.join(output_dir, f"{name}.csv")
        save_csv(csv_path, volumes, absorbance)

        # Save simulated instrument image
        img_path = os.path.join(output_dir, f"{name}_instrument.png")
        plot_chromatogram(img_path, volumes, absorbance, f"SEC: {name}")

    # Create ZIP archive
    zip_path = os.path.join(output_dir, "SEC_test_dataset.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for name in constructs:
            zf.write(os.path.join(output_dir, f"{name}.csv"), f"{name}.csv")
            zf.write(os.path.join(output_dir, f"{name}_instrument.png"),
                     f"{name}_instrument.png")

    print(f"\n  ZIP archive: {zip_path}")
    print(f"  Contains {len(constructs)} constructs x 2 files = {len(constructs)*2} files")
    return zip_path


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Generate synthetic SEC test data')
    ap.add_argument('--output-dir', '-o', default='./test_dataset',
                    help='Output directory (default: ./test_dataset)')
    args = ap.parse_args()

    print("Generating synthetic SEC test dataset...")
    zip_path = generate_test_data(args.output_dir)
    print(f"\nDone! Test ZIP: {zip_path}")
