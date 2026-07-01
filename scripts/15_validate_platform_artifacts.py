#!/usr/bin/env python3
"""Validate generated platform report artifacts.

This checker verifies the existence and minimal schema of platform outputs created
by scripts/13_build_platform_report.py. It is intentionally lightweight so it can
run in local development and CI without additional dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_OBJECT_FIELDS = [
    "schema",
    "repo_full_name",
    "platform_name",
    "market_segment",
    "evidence_level",
    "demo_status",
    "current_claim",
    "claim_boundaries",
    "platform_lanes",
    "evidence_items",
    "packaging_gaps",
    "next_milestone",
    "recommended_next_commands",
]

REQUIRED_REPORT_SECTIONS = [
    "# Cipher Topology Lab Platform Report",
    "## Platform Position",
    "## Current Supported Claim",
    "## Claim Boundaries",
    "## Platform Lanes",
    "## Evidence State",
    "## Packaging Gaps",
    "## Next Milestone",
    "## Recommended Commands",
    "## Reviewer Note",
]


def validate_object(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing platform object: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON in {path}: {exc}"]

    for field in REQUIRED_OBJECT_FIELDS:
        if field not in payload:
            errors.append(f"missing required object field: {field}")
    if payload.get("schema") != "cipher-topology-platform/v0.1":
        errors.append("unexpected schema; expected cipher-topology-platform/v0.1")
    if payload.get("repo_full_name") != "pskeffington/cipher-topology-lab":
        errors.append("unexpected repo_full_name")
    for list_field in ["claim_boundaries", "platform_lanes", "evidence_items", "packaging_gaps", "recommended_next_commands"]:
        if list_field in payload and not isinstance(payload[list_field], list):
            errors.append(f"expected list field: {list_field}")
        elif list_field in payload and not payload[list_field]:
            errors.append(f"empty required list field: {list_field}")
    return errors


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing platform report: {path}"]
    text = path.read_text(encoding="utf-8", errors="ignore")
    for section in REQUIRED_REPORT_SECTIONS:
        if section not in text:
            errors.append(f"missing report section: {section}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate generated platform report artifacts.")
    parser.add_argument("--report", default="results/platform/platform_report.md", help="Platform report path.")
    parser.add_argument("--object", default="results/platform/platform_object.json", help="Platform object path.")
    parser.add_argument("--out", default="results/logs/platform_artifact_validation.md", help="Validation report path.")
    args = parser.parse_args(argv)

    report_path = ROOT / args.report
    object_path = ROOT / args.object
    errors = validate_report(report_path) + validate_object(object_path)

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Platform Artifact Validation",
        "",
        f"Report: `{args.report}`",
        f"Object: `{args.object}`",
        f"Errors: {len(errors)}",
        "",
    ]
    if errors:
        lines.append("## Errors")
        lines.append("")
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("Platform artifacts passed validation.")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        print(f"platform artifact validation failed with {len(errors)} error(s); see {args.out}")
        return 1
    print(f"platform artifact validation passed; see {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
