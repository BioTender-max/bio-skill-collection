#!/usr/bin/env python3
"""Validate sample annotations against ontology schema constraints."""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional


def _load_summary(ontology: Optional[str] = None,
                  summary_file: Optional[str] = None) -> Dict:
    """Load a summary JSON by ontology name or direct file path."""
    if summary_file:
        path = summary_file
    elif ontology:
        explorer_ref = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "ontology-explorer", "references",
            "ontology_registry.json",
        )
        if not os.path.isfile(explorer_ref):
            raise ValueError(f"Ontology registry not found at {explorer_ref}")
        with open(explorer_ref, encoding="utf-8") as f:
            registry = json.load(f)
        key = ontology.lower()
        if key not in registry:
            available = ", ".join(sorted(registry.keys()))
            raise ValueError(
                f"Ontology '{ontology}' not in registry. Available: {available}"
            )
        ref_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "ontology-explorer", "references",
        )
        path = os.path.join(ref_dir, registry[key]["summary_file"])
    else:
        raise ValueError("Provide --ontology or --summary-file")

    if not os.path.isfile(path):
        raise ValueError(f"Summary file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_constraints(ontology: Optional[str] = None,
                      constraints_file: Optional[str] = None) -> Dict:
    """Load constraints JSON."""
    if constraints_file:
        path = constraints_file
    elif ontology:
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "references", f"{ontology.lower()}_constraints.json",
        )
    else:
        return {}

    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_schema(
    summary: Dict,
    constraints: Dict,
    annotation: Dict,
) -> Dict:
    """Validate an annotation against ontology schema.

    Parameters
    ----------
    summary : dict
        Ontology summary.
    constraints : dict
        Validation constraints (required/recommended per class).
    annotation : dict
        Annotation to validate. Expected structure:
        {"class": "ClassName", "properties": {"propName": value, ...}}
        or a list of such dicts.

    Returns
    -------
    dict
        valid, errors, warnings, class_valid, properties_valid.

    Raises
    ------
    ValueError
        If annotation format is invalid.
    """
    if not isinstance(annotation, dict):
        raise ValueError("Annotation must be a dict")

    # Handle single annotation or list
    annotations = annotation.get("annotations", [annotation])
    if not isinstance(annotations, list):
        annotations = [annotations]

    classes = summary.get("classes", {})
    obj_props = summary.get("object_properties", {})
    data_props = summary.get("data_properties", {})
    all_props = {}
    all_props.update(obj_props)
    all_props.update(data_props)

    errors: List[Dict] = []
    warnings: List[Dict] = []
    class_results: Dict[str, bool] = {}
    property_results: Dict[str, bool] = {}

    for ann in annotations:
        if not isinstance(ann, dict):
            continue

        # Skip warning-type annotations
        if ann.get("type") == "warning":
            continue

        cls_name = ann.get("class") or ann.get("subclass")
        if not cls_name:
            continue

        # Validate class
        if cls_name in classes:
            class_results[cls_name] = True
        else:
            # Try case-insensitive match
            found = False
            for c in classes:
                if c.lower() == cls_name.lower():
                    class_results[cls_name] = True
                    found = True
                    break
            if not found:
                class_results[cls_name] = False
                errors.append({
                    "field": cls_name,
                    "error_type": "unknown_class",
                    "message": f"Class '{cls_name}' not found in ontology",
                })

        # Validate properties
        props = ann.get("properties", {})
        if isinstance(props, dict):
            for prop_name, value in props.items():
                if prop_name in all_props:
                    property_results[prop_name] = True
                    # Check domain compatibility
                    prop_info = all_props[prop_name]
                    domain = prop_info.get("domain", "")
                    if domain and cls_name and cls_name not in domain:
                        # Check case-insensitive
                        if cls_name.lower() not in domain.lower():
                            warnings.append({
                                "field": prop_name,
                                "warning_type": "domain_mismatch",
                                "message": (
                                    f"Property '{prop_name}' has domain "
                                    f"'{domain}', but applied to '{cls_name}'"
                                ),
                            })
                else:
                    # Try case-insensitive
                    found = False
                    for p in all_props:
                        if p.lower() == prop_name.lower():
                            property_results[prop_name] = True
                            found = True
                            break
                    if not found:
                        property_results[prop_name] = False
                        errors.append({
                            "field": prop_name,
                            "error_type": "unknown_property",
                            "message": f"Property '{prop_name}' not found in ontology",
                        })

        # Validate single property in annotation dict
        prop_name = ann.get("property")
        if prop_name:
            if prop_name in all_props:
                property_results[prop_name] = True
            else:
                found = False
                for p in all_props:
                    if p.lower() == prop_name.lower():
                        property_results[prop_name] = True
                        found = True
                        break
                if not found:
                    property_results[prop_name] = False
                    errors.append({
                        "field": prop_name,
                        "error_type": "unknown_property",
                        "message": f"Property '{prop_name}' not found in ontology",
                    })

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "class_valid": class_results,
        "properties_valid": property_results,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate annotations against ontology schema.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ontology", help="Ontology name (e.g., cmso)")
    group.add_argument("--summary-file", help="Path to summary JSON file")
    parser.add_argument("--annotation", help="JSON string of annotation to validate")
    parser.add_argument("--annotation-file", help="Path to annotation JSON file")
    parser.add_argument("--constraints-file", help="Path to constraints JSON file")
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
        constraints = _load_constraints(
            ontology=args.ontology,
            constraints_file=args.constraints_file,
        )
        if args.annotation_file:
            with open(args.annotation_file, encoding="utf-8") as f:
                annotation = json.load(f)
        elif args.annotation:
            annotation = json.loads(args.annotation)
        else:
            raise ValueError("Provide --annotation or --annotation-file")

        result = check_schema(
            summary=summary,
            constraints=constraints,
            annotation=annotation,
        )
    except (ValueError, json.JSONDecodeError) as exc:
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
        },
        "results": result,
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        print()
    else:
        status = "VALID" if result["valid"] else "INVALID"
        print(f"Validation: {status}")
        for e in result["errors"]:
            print(f"  ERROR: [{e['error_type']}] {e['message']}")
        for w in result["warnings"]:
            print(f"  WARNING: [{w['warning_type']}] {w['message']}")


if __name__ == "__main__":
    main()
