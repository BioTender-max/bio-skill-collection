#!/usr/bin/env python3
"""Look up ontology properties by name, class, or search term."""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional


def _load_summary(ontology: Optional[str] = None,
                  summary_file: Optional[str] = None) -> Dict:
    """Load a summary JSON by ontology name or direct file path."""
    if summary_file:
        path = summary_file
    elif ontology:
        registry_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "references", "ontology_registry.json",
        )
        if not os.path.isfile(registry_path):
            raise ValueError(f"Ontology registry not found at {registry_path}")
        with open(registry_path, encoding="utf-8") as f:
            registry = json.load(f)
        key = ontology.lower()
        if key not in registry:
            available = ", ".join(sorted(registry.keys()))
            raise ValueError(
                f"Ontology '{ontology}' not in registry. Available: {available}"
            )
        ref_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "references",
        )
        path = os.path.join(ref_dir, registry[key]["summary_file"])
    else:
        raise ValueError("Provide --ontology or --summary-file")

    if not os.path.isfile(path):
        raise ValueError(f"Summary file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def lookup_property(
    summary: Dict,
    property_name: Optional[str] = None,
    class_name: Optional[str] = None,
    prop_type: str = "all",
    search: Optional[str] = None,
) -> Dict:
    """Look up ontology properties.

    Parameters
    ----------
    summary : dict
        Ontology summary (as produced by ontology_summarizer.py).
    property_name : str, optional
        Name of a specific property to look up.
    class_name : str, optional
        Class name to find all properties for (where class is domain).
    prop_type : str
        Filter: "object", "data", or "all".
    search : str, optional
        Search term to match against property labels.

    Returns
    -------
    dict
        Query results with property_info, class_properties, or search_results.

    Raises
    ------
    ValueError
        If no valid query mode is specified or property not found.
    """
    if not property_name and not class_name and not search:
        raise ValueError(
            "Provide --property, --class, or --search"
        )

    obj_props = summary.get("object_properties", {})
    data_props = summary.get("data_properties", {})
    result: Dict = {}

    if property_name:
        # Search in both object and data properties
        found = None
        found_type = None
        for name, info in obj_props.items():
            if name.lower() == property_name.lower():
                found = {"name": name, "type": "object", **info}
                found_type = "object"
                break
        if not found:
            for name, info in data_props.items():
                if name.lower() == property_name.lower():
                    found = {"name": name, "type": "data", **info}
                    found_type = "data"
                    break
        if not found:
            # Try partial match
            for name, info in obj_props.items():
                if property_name.lower() in name.lower():
                    found = {"name": name, "type": "object", **info}
                    found_type = "object"
                    break
            if not found:
                for name, info in data_props.items():
                    if property_name.lower() in name.lower():
                        found = {"name": name, "type": "data", **info}
                        found_type = "data"
                        break
        if not found:
            all_names = sorted(list(obj_props.keys()) + list(data_props.keys()))
            raise ValueError(
                f"Property '{property_name}' not found. "
                f"Available: {', '.join(all_names[:20])}"
                + ("..." if len(all_names) > 20 else "")
            )
        result["property_info"] = found

    if class_name:
        class_props: List[Dict] = []
        if prop_type in ("all", "object"):
            for name, info in obj_props.items():
                domain = info.get("domain", "")
                if domain and (
                    class_name in domain
                    or class_name.replace(" ", "") in domain
                    or class_name.lower() in domain.lower()
                ):
                    class_props.append({
                        "name": name,
                        "type": "object",
                        "domain": info.get("domain"),
                        "range": info.get("range"),
                        "description": info.get("description"),
                    })
        if prop_type in ("all", "data"):
            for name, info in data_props.items():
                domain = info.get("domain", "")
                if domain and (
                    class_name in domain
                    or class_name.replace(" ", "") in domain
                    or class_name.lower() in domain.lower()
                ):
                    class_props.append({
                        "name": name,
                        "type": "data",
                        "domain": info.get("domain"),
                        "range_type": info.get("range_type"),
                        "description": info.get("description"),
                    })
        class_props.sort(key=lambda p: (p["type"], p["name"]))
        result["class_properties"] = class_props
        result["class_name"] = class_name

    if search:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        matches: List[Dict] = []
        if prop_type in ("all", "object"):
            for name, info in obj_props.items():
                if pattern.search(name) or (
                    info.get("description") and pattern.search(info["description"])
                ):
                    matches.append({
                        "name": name,
                        "type": "object",
                        "domain": info.get("domain"),
                        "range": info.get("range"),
                        "description": info.get("description"),
                    })
        if prop_type in ("all", "data"):
            for name, info in data_props.items():
                if pattern.search(name) or (
                    info.get("description") and pattern.search(info["description"])
                ):
                    matches.append({
                        "name": name,
                        "type": "data",
                        "domain": info.get("domain"),
                        "range_type": info.get("range_type"),
                        "description": info.get("description"),
                    })
        matches.sort(key=lambda m: (m["type"], m["name"]))
        result["search_results"] = matches

    return result


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Look up ontology properties by name, class, or search.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--property", dest="property_name",
                        help="Property name to look up")
    parser.add_argument("--class", dest="class_name",
                        help="Class name to find properties for")
    parser.add_argument("--search", help="Search term for property labels")
    parser.add_argument("--type", dest="prop_type", default="all",
                        choices=["object", "data", "all"],
                        help="Filter by property type")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    try:
        summary = _load_summary(
            ontology=args.ontology,
            summary_file=args.summary_file,
        )
        result = lookup_property(
            summary=summary,
            property_name=args.property_name,
            class_name=args.class_name,
            prop_type=args.prop_type,
            search=args.search,
        )
    except ValueError as exc:
        if args.json:
            json.dump({"error": str(exc)}, sys.stdout)
            print()
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "ontology": args.ontology,
            "summary_file": args.summary_file,
            "property": args.property_name,
            "class": args.class_name,
            "search": args.search,
            "type": args.prop_type,
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        if "property_info" in result:
            p = result["property_info"]
            print(f"Property: {p['name']} ({p['type']})")
            if p.get("domain"):
                print(f"  Domain: {p['domain']}")
            if p.get("range"):
                print(f"  Range: {p['range']}")
            if p.get("range_type"):
                print(f"  Range type: {p['range_type']}")
            if p.get("description"):
                print(f"  Description: {p['description']}")
        if "class_properties" in result:
            print(f"Properties for class '{result['class_name']}':")
            for p in result["class_properties"]:
                target = p.get("range") or p.get("range_type", "?")
                print(f"  {p['name']} ({p['type']}) -> {target}")
        if "search_results" in result:
            print(f"Search results for '{args.search}':")
            for p in result["search_results"]:
                target = p.get("range") or p.get("range_type", "?")
                print(f"  {p['name']} ({p['type']}) -> {target}")


if __name__ == "__main__":
    main()
