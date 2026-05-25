#!/usr/bin/env python3
import argparse
from pathlib import Path

from pymol import cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a clean protein structure image with PyMOL.")
    parser.add_argument("--input", required=True, help="PDB/mmCIF file path or 4-character PDB ID.")
    parser.add_argument("--output", required=True, help="Output image path.")
    parser.add_argument("--title", default="", help="Optional title stored in PyMOL scene name.")
    parser.add_argument("--highlight-selection", default="", help="Optional PyMOL selection to highlight.")
    parser.add_argument("--highlight-color", default="tv_orange", help="Color for highlight selection.")
    parser.add_argument("--width", type=int, default=1800, help="Output image width in pixels.")
    parser.add_argument("--height", type=int, default=1400, help="Output image height in pixels.")
    parser.add_argument("--style", choices=["cartoon", "surface"], default="cartoon", help="Main representation style.")
    return parser


def load_structure(input_value: str) -> None:
    input_path = Path(input_value)
    if input_path.exists():
        cmd.load(str(input_path), "structure")
    elif len(input_value) == 4 and input_value.isalnum():
        cmd.fetch(input_value, name="structure", type="pdb1")
    else:
        raise SystemExit(f"Input not found and does not look like a PDB ID: {input_value}")


def main() -> None:
    args = build_parser().parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd.reinitialize()
    load_structure(args.input)

    cmd.remove("solvent")
    cmd.hide("everything", "all")
    cmd.show(args.style, "polymer.protein")
    cmd.color("gray80", "polymer.protein")
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("ray_opaque_background", 0)
    cmd.bg_color("white")
    cmd.orient("all")
    cmd.zoom("all", buffer=3.0)

    if args.highlight_selection:
        cmd.show("sticks", args.highlight_selection)
        cmd.color(args.highlight_color, args.highlight_selection)

    if args.title:
        cmd.scene(args.title, "store")

    cmd.ray(args.width, args.height)
    cmd.png(str(output_path), width=args.width, height=args.height, dpi=300, ray=1)


if __name__ == "__main__":
    main()
