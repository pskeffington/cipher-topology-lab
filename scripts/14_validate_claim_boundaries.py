#!/usr/bin/env python3
"""Validate claim-boundary language for platform-facing files.

The checker is intentionally conservative. It scans public/reviewer-facing text
for prohibited overclaims and allows explicit boundary/negative language such as
"not cryptanalysis" or "does not claim to break AES".
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_PATHS = [
    "README.md",
    "docs/portfolio_status.md",
    "docs/platform_continuance.md",
    "docs/platform_walkthrough.md",
    "docs/productization_roadmap.md",
    "docs/productization_status.md",
    "docs/development_backlog.md",
    "manuscript/sections/discussion.tex",
    "manuscript/sections/conclusion.tex",
]

PROHIBITED_PATTERNS = [
    ("cipher_break", re.compile(r"\b(breaks?|broken|cracks?|cracked)\s+(aes|ascon|des|tdea|cipher|encryption)\b", re.IGNORECASE)),
    ("vulnerability_claim", re.compile(r"\b(aes|ascon|des|tdea|cipher|encryption)\s+(vulnerability|flaw|weakness|exploit)\b", re.IGNORECASE)),
    ("security_certification", re.compile(r"\b(certif(?:y|ies|ied|ication)|guarantee[sd]?)\s+(security|secure|randomness)\b", re.IGNORECASE)),
    ("proof_of_randomness", re.compile(r"\b(proves?|proved|proof)\s+(of\s+)?(randomness|security|cipher\s+security)\b", re.IGNORECASE)),
    ("cryptanalysis_result", re.compile(r"\bcryptanalysis\s+(result|breakthrough|finding|proof|success)\b", re.IGNORECASE)),
    ("unsupported_comparator_result", re.compile(r"\b(ascon|des|tdea)\s+(result|finding|evidence|separation|analysis)\b", re.IGNORECASE)),
]

NEGATION_HINTS = [
    "not ",
    "no ",
    "does not ",
    "do not ",
    "cannot ",
    "should not ",
    "avoid ",
    "without ",
    "until ",
    "unless ",
    "not treated as ",
    "not a ",
]


@dataclass(frozen=True)
class Finding:
    path: str
    line_number: int
    rule: str
    line: str


def is_boundary_context(line: str) -> bool:
    lower = line.lower()
    return any(hint in lower for hint in NEGATION_HINTS)


def scan_file(path: Path) -> list[Finding]:
    if not path.exists() or not path.is_file():
        return []
    findings: list[Finding] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        if is_boundary_context(line):
            continue
        for name, pattern in PROHIBITED_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(str(path.relative_to(ROOT)), idx, name, line.strip()))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate platform claim boundaries.")
    parser.add_argument("paths", nargs="*", default=DEFAULT_PATHS, help="Files to scan.")
    parser.add_argument("--report", default="results/logs/claim_boundary_report.md", help="Markdown report path.")
    args = parser.parse_args(argv)

    findings: list[Finding] = []
    scanned: list[str] = []
    for raw in args.paths:
        path = ROOT / raw
        if path.exists():
            scanned.append(raw)
            findings.extend(scan_file(path))

    report_path = ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Claim Boundary Validation Report",
        "",
        f"Files scanned: {len(scanned)}",
        f"Findings: {len(findings)}",
        "",
    ]
    if findings:
        lines.extend(["## Findings", "", "| File | Line | Rule | Text |", "|---|---:|---|---|"])
        for finding in findings:
            safe_line = finding.line.replace("|", "\\|")
            lines.append(f"| `{finding.path}` | {finding.line_number} | `{finding.rule}` | {safe_line} |")
    else:
        lines.append("No prohibited unbounded claims were detected in the scanned files.")
    lines.extend(["", "## Scanned Files", ""])
    lines.extend(f"- `{path}`" for path in scanned)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if findings:
        print(f"claim boundary check failed with {len(findings)} finding(s); see {args.report}")
        return 1
    print(f"claim boundary check passed; see {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
