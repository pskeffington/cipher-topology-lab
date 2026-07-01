#!/usr/bin/env python3
"""Build a portfolio-readable platform report for cipher-topology-lab.

The report summarizes current supported evidence, claim boundaries, platform
lanes, and packaging gaps without expanding the scientific claim. It is designed
for technical reviewers, portfolio valuation tools, and sponsor/foundation
review workflows.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = ROOT / "results" / "platform" / "platform_report.md"
DEFAULT_OBJECT_PATH = ROOT / "results" / "platform" / "platform_object.json"

CLAIM_BOUNDARIES = [
    "diagnostic and reproducibility infrastructure only",
    "not cryptanalysis",
    "not vulnerability discovery",
    "not security certification",
    "not proof of randomness",
    "no Ascon, DES, or TDEA empirical claims until implemented and registered",
]

SUPPORTED_CLAIM = (
    "Registered persistent-homology summaries reproducibly distinguish deliberately structured "
    "weak-control byte streams from a SHA-256 seeded deterministic baseline under configured "
    "byte-pair and sliding-window embeddings. AES-CTR, OS CSPRNG, and xorshift32 do not show "
    "comparable top-ranked separation under the currently registered internal summaries."
)


@dataclass(frozen=True)
class EvidenceItem:
    name: str
    status: str
    source: str
    summary: str


@dataclass(frozen=True)
class PlatformObject:
    schema: str
    repo_full_name: str
    platform_name: str
    generated_at_utc: str
    market_segment: str
    evidence_level: str
    demo_status: str
    current_claim: str
    claim_boundaries: list[str]
    platform_lanes: list[str]
    evidence_items: list[EvidenceItem]
    packaging_gaps: list[str]
    next_milestone: str
    recommended_next_commands: list[str] = field(default_factory=list)


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def evidence_items() -> list[EvidenceItem]:
    items = [
        EvidenceItem(
            name="Primary 64-replicate internal TDA run",
            status="registered" if exists("docs/evidence_register.md") else "expected",
            source="docs/evidence_register.md",
            summary="Six-condition run with AES-CTR, SHA-256 baseline, OS CSPRNG, and weak-generator controls.",
        ),
        EvidenceItem(
            name="Weak-control sensitivity extension",
            status="registered" if exists("docs/evidence_register_weak_controls.md") else "expected",
            source="docs/evidence_register_weak_controls.md",
            summary="Eight-condition extension with deliberately periodic and biased byte-stream controls.",
        ),
        EvidenceItem(
            name="Alternate-seed robustness check",
            status="registered" if exists("docs/evidence_register_weak_controls_seed_robustness.md") else "expected",
            source="docs/evidence_register_weak_controls_seed_robustness.md",
            summary="Re-run under alternate deterministic master seed to test weak-control pattern stability.",
        ),
        EvidenceItem(
            name="Experiment expansion ladder",
            status="planned" if exists("docs/experiment_expansion_plan.md") else "missing",
            source="docs/experiment_expansion_plan.md",
            summary="Seed sweep, 128-replicate scale check, embedding sensitivity, and external randomness decision.",
        ),
        EvidenceItem(
            name="Platform continuance plan",
            status="active" if exists("docs/platform_continuance.md") else "missing",
            source="docs/platform_continuance.md",
            summary="Platform lanes, milestones, operating rules, and claim-control posture.",
        ),
    ]
    return items


def platform_object() -> PlatformObject:
    return PlatformObject(
        schema="cipher-topology-platform/v0.1",
        repo_full_name="pskeffington/cipher-topology-lab",
        platform_name="Cipher Topology Lab",
        generated_at_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        market_segment="security_ai_platform",
        evidence_level="registered_internal_evidence_with_planned_expansion",
        demo_status="platform_report_available; deterministic_demo_next",
        current_claim=SUPPORTED_CLAIM,
        claim_boundaries=CLAIM_BOUNDARIES,
        platform_lanes=[
            "research-grade diagnostic platform",
            "security/AI methods platform",
            "productizable evidence-register engine",
        ],
        evidence_items=evidence_items(),
        packaging_gaps=[
            "deterministic platform demo target not yet complete",
            "buyer/sponsor walkthrough needs first public-safe version",
            "claim-boundary validator should be added before external promotion",
            "external randomness completion decision remains open",
        ],
        next_milestone="Milestone 1: demo hardening and platform report integration",
        recommended_next_commands=[
            "make platform-report",
            "make segmented-smoke",
            "make external-randomness",
        ],
    )


def bullet_list(values: Iterable[str]) -> list[str]:
    return [f"- {value}" for value in values]


def write_object(obj: PlatformObject, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(obj), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(obj: PlatformObject, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# Cipher Topology Lab Platform Report",
        "",
        f"Generated: {obj.generated_at_utc}",
        f"Repository: `{obj.repo_full_name}`",
        f"Schema: `{obj.schema}`",
        "",
        "## Platform Position",
        "",
        "`cipher-topology-lab` is a reproducible diagnostic platform for generated byte-stream analysis using topological summaries, conventional randomness diagnostics, validation logs, and evidence-register controls.",
        "",
        "## Current Supported Claim",
        "",
        obj.current_claim,
        "",
        "## Claim Boundaries",
        "",
        *bullet_list(obj.claim_boundaries),
        "",
        "## Platform Lanes",
        "",
        *bullet_list(obj.platform_lanes),
        "",
        "## Evidence State",
        "",
        "| Evidence item | Status | Source | Summary |",
        "|---|---|---|---|",
    ]
    for item in obj.evidence_items:
        lines.append(f"| {item.name} | `{item.status}` | `{item.source}` | {item.summary} |")
    lines.extend([
        "",
        "## Packaging Gaps",
        "",
        *bullet_list(obj.packaging_gaps),
        "",
        "## Next Milestone",
        "",
        obj.next_milestone,
        "",
        "## Recommended Commands",
        "",
        "```bash",
        *obj.recommended_next_commands,
        "```",
        "",
        "## Reviewer Note",
        "",
        "This report is intentionally conservative. It makes the platform reviewable without expanding the underlying scientific claim. New empirical claims should only be added after a corresponding configuration, artifact set, and evidence register exist.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build platform report and object for cipher-topology-lab.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH), help="Markdown report output path.")
    parser.add_argument("--object", default=str(DEFAULT_OBJECT_PATH), help="JSON platform object output path.")
    args = parser.parse_args(argv)

    obj = platform_object()
    write_report(obj, ROOT / args.report if not Path(args.report).is_absolute() else Path(args.report))
    write_object(obj, ROOT / args.object if not Path(args.object).is_absolute() else Path(args.object))
    print(f"wrote {args.report}")
    print(f"wrote {args.object}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
