"""Buyer-facing pilot report builder for Resilient Provenance.

The report builder combines provenance scan output, optional RAG answer
verification output, and optional GIS profile output into a single pilot report
that can support a paid source-trust readiness engagement.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping


def load_optional_json(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {candidate}")
    return payload


def _count_review_flagged_assets(manifest: Mapping[str, Any]) -> int:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return 0
    risk_flags = {"unknown_extension", "possible_stale_or_archived_asset", "draft_named_asset"}
    count = 0
    for asset in assets:
        if not isinstance(asset, Mapping):
            continue
        flags = asset.get("trust_flags", [])
        if isinstance(flags, list) and any(flag in risk_flags for flag in flags):
            count += 1
    return count


def _source_type_counts(manifest: Mapping[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return counts
    for asset in assets:
        if not isinstance(asset, Mapping):
            continue
        source_type = asset.get("source_type")
        label = source_type if isinstance(source_type, str) and source_type else "unknown"
        counts[label] = counts.get(label, 0) + 1
    return counts


def build_pilot_report_markdown(
    *,
    manifest: Mapping[str, Any],
    verification: Mapping[str, Any] | None = None,
    gis_profile: Mapping[str, Any] | None = None,
    client_name: str = "Pilot Client",
    product_name: str = "Resilient Provenance",
) -> str:
    generated = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    asset_count = manifest.get("asset_count", 0)
    total_bytes = manifest.get("total_bytes", 0)
    flagged_count = _count_review_flagged_assets(manifest)
    source_counts = _source_type_counts(manifest)

    lines = [
        f"# {product_name} Pilot Report",
        "",
        f"Client: **{client_name}**",
        f"Generated UTC: `{generated}`",
        "",
        "## Executive summary",
        "",
        "This pilot report summarizes source-provenance readiness for AI retrieval workflows. It combines source fingerprinting, conservative asset classification, review-risk flags, and optional answer-citation and GIS/infrastructure profile checks.",
        "",
        "## Source provenance summary",
        "",
        f"- Assets scanned: `{asset_count}`",
        f"- Total bytes scanned: `{total_bytes}`",
        f"- Review-flagged assets: `{flagged_count}`",
        "",
        "### Source type counts",
        "",
        "| Source type | Count |",
        "|---|---:|",
    ]
    for source_type, count in sorted(source_counts.items()):
        lines.append(f"| {source_type} | {count} |")

    if verification:
        lines.extend([
            "",
            "## RAG answer verification summary",
            "",
            f"- Answer ID: `{verification.get('answer_id', 'unknown')}`",
            f"- Overall status: `{verification.get('status', 'unknown')}`",
            f"- Citations checked: `{verification.get('citation_count', 0)}`",
            f"- Approved citations: `{verification.get('approved_count', 0)}`",
            f"- Rejected citations: `{verification.get('rejected_count', 0)}`",
        ])
    else:
        lines.extend([
            "",
            "## RAG answer verification summary",
            "",
            "No answer verification file was provided for this report. The next pilot step should verify at least one representative answer citation object against the manifest.",
        ])

    if gis_profile:
        lines.extend([
            "",
            "## GIS/infrastructure profile summary",
            "",
            f"- GIS candidates: `{gis_profile.get('gis_candidate_count', 0)}`",
            f"- Covered sectors: `{gis_profile.get('covered_sector_count', 0)}`",
            f"- Missing sectors: `{gis_profile.get('missing_sector_count', 0)}`",
        ])
    else:
        lines.extend([
            "",
            "## GIS/infrastructure profile summary",
            "",
            "No GIS profile was provided. For municipal, public-works, emergency-management, or infrastructure buyers, run the GIS provenance profile before final delivery.",
        ])

    lines.extend([
        "",
        "## Recommended remediation backlog",
        "",
        "1. Resolve assets with unknown, stale, archived, or draft-related flags.",
        "2. Require chunk-level citations for text assets entering RAG workflows.",
        "3. Verify representative AI answers before expanding retrieval scope.",
        "4. Add owner, source-system, permission, and approval metadata to manifest records.",
        "5. For GIS clients, resolve missing civic/infrastructure sectors or document why they are out of scope.",
        "6. Add manifest signing before using this workflow for chain-of-custody-sensitive operations.",
        "",
        "## Claim boundary",
        "",
        "This report provides source-provenance evidence, review flags, citation verification status, and GIS candidate-sector coverage. It does not certify source truth, answer correctness, regulatory compliance, privacy compliance, cybersecurity sufficiency, public safety readiness, infrastructure security, or model safety.",
        "",
    ])
    return "\n".join(lines)


def write_pilot_report(
    *,
    manifest_path: str | Path,
    out_path: str | Path,
    verification_path: str | Path | None = None,
    gis_profile_path: str | Path | None = None,
    client_name: str = "Pilot Client",
    product_name: str = "Resilient Provenance",
) -> Path:
    manifest = load_optional_json(manifest_path)
    if manifest is None:
        raise FileNotFoundError(manifest_path)
    verification = load_optional_json(verification_path)
    gis_profile = load_optional_json(gis_profile_path)
    markdown = build_pilot_report_markdown(
        manifest=manifest,
        verification=verification,
        gis_profile=gis_profile,
        client_name=client_name,
        product_name=product_name,
    )
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    return out
