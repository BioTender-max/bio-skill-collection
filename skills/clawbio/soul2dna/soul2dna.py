#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClawBio Soul2DNA Compiler
Compile SOUL.md character profiles into synthetic diploid genomes.

Usage:
    python soul2dna.py          # Compile all souls
    python soul2dna.py --demo   # Run demo (summary only)
"""

import argparse
import sys
from pathlib import Path

# Import the core compiler from GENOMEBOOK/PYTHON/
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_GENOMEBOOK_PYTHON = _PROJECT_ROOT / "GENOMEBOOK" / "PYTHON"

if str(_GENOMEBOOK_PYTHON) not in sys.path:
    sys.path.insert(0, str(_GENOMEBOOK_PYTHON))

# We need to add project root too for any shared imports
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def _import_soul2dna():
    """Import the core soul2dna module."""
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location(
        "soul2dna_core",
        _GENOMEBOOK_PYTHON / "01-soul2dna.py"
    )
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_demo():
    """Run a demo compilation showing summary output."""
    core = _import_soul2dna()
    registry = core.load_trait_registry()
    soul_files = sorted(core.SOULS_DIR.glob("*.soul.md"))

    if not soul_files:
        print("ERROR: No .soul.md files found.")
        sys.exit(1)

    print("=" * 70)
    print("SOUL2DNA COMPILER - DEMO MODE")
    print("=" * 70)
    print(f"Souls directory: {core.SOULS_DIR}")
    print(f"Trait registry:  {core.TRAIT_REGISTRY}")
    print(f"Traits defined:  {len(registry['traits'])}")
    print(f"Soul files:      {len(soul_files)}")
    print()

    males, females = [], []
    print(f"{'ID':>20s} | {'Sex':>6s} | Loci | Name")
    print("-" * 70)

    for sf in soul_files:
        agent_id = sf.stem.replace(".soul", "")
        soul_data = core.parse_soul(sf)
        genome = core.compile_genome(soul_data, registry)
        genome["id"] = f"{agent_id}-g0"

        sex = soul_data["sex"]
        if sex == "Male":
            males.append(agent_id)
        else:
            females.append(agent_id)

        print(f"{genome['id']:>20s} | {sex:>6s} | {len(genome['loci']):>4d} | {soul_data['name']}")

    print()
    print(f"Total: {len(soul_files)} genomes ({len(males)}M / {len(females)}F)")
    print(f"Males:   {', '.join(males)}")
    print(f"Females: {', '.join(females)}")
    print()
    print("[DEMO] No files written. Run without --demo to compile.")


def run_compile():
    """Run full compilation."""
    core = _import_soul2dna()
    print("=" * 70)
    print("SOUL2DNA COMPILER")
    print("=" * 70)
    core.main()
    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(
        description="Soul2DNA: Compile SOUL.md profiles into synthetic genomes"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Run demo mode (show summary, don't write files)"
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_compile()


if __name__ == "__main__":
    main()
