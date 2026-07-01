"""Verifier for RAG answer citations against a provenance manifest.

This module checks whether an AI answer cites source files and chunks that are
present in a previously generated provenance manifest. It is designed as a
revenue-path control: a buyer-facing report can show which answer citations are
approved, missing, stale-looking, or not grounded in the manifest.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class CitationCheck:
    """Verification outcome for one cited source or chunk."""

    citation_id: str
    status: str
    path: str | None = None
    asset_id: str | None = None
    chunk_id: str | None = None
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AnswerVerificationReport:
    """Machine-readable verification report for a RAG answer object."""

    schema_version: str
    verifier: str
    generated_utc: str
    answer_id: str
    status: str
    citation_count: int
    approved_count: int
    rejected_count: int
    checks: list[CitationCheck]
    claim_boundary: str


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON file into a dictionary."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _assets_by_path(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("Manifest field 'assets' must be a list")
    indexed: dict[str, Mapping[str, Any]] = {}
    for asset in assets:
        if isinstance(asset, Mapping) and isinstance(asset.get("path"), str):
            indexed[asset["path"]] = asset
    return indexed


def _assets_by_id(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("Manifest field 'assets' must be a list")
    indexed: dict[str, Mapping[str, Any]] = {}
    for asset in assets:
        if isinstance(asset, Mapping) and isinstance(asset.get("asset_id"), str):
            indexed[asset["asset_id"]] = asset
    return indexed


def _chunks_by_id(asset: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    chunks = asset.get("chunks", [])
    if not isinstance(chunks, list):
        return {}
    indexed: dict[str, Mapping[str, Any]] = {}
    for chunk in chunks:
        if isinstance(chunk, Mapping) and isinstance(chunk.get("chunk_id"), str):
            indexed[chunk["chunk_id"]] = chunk
    return indexed


def _safe_str(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def verify_citation(citation: Mapping[str, Any], manifest: Mapping[str, Any]) -> CitationCheck:
    """Verify one citation against manifest file and chunk records.

    A citation may identify a source by `path` or `asset_id`. Chunk checks are
    optional but, when supplied, must match a chunk registered under the asset.
    Optional `asset_sha256` and `chunk_sha256` fields must also match when given.
    """

    citation_id = _safe_str(citation.get("citation_id")) or _safe_str(citation.get("id")) or "citation-unknown"
    path = _safe_str(citation.get("path"))
    asset_id = _safe_str(citation.get("asset_id"))
    chunk_id = _safe_str(citation.get("chunk_id"))
    asset_sha256 = _safe_str(citation.get("asset_sha256")) or _safe_str(citation.get("sha256"))
    chunk_sha256 = _safe_str(citation.get("chunk_sha256"))

    by_path = _assets_by_path(manifest)
    by_id = _assets_by_id(manifest)
    reasons: list[str] = []

    asset = by_id.get(asset_id) if asset_id else None
    if asset is None and path:
        asset = by_path.get(path)
    if asset is None:
        return CitationCheck(
            citation_id=citation_id,
            status="rejected",
            path=path,
            asset_id=asset_id,
            chunk_id=chunk_id,
            reasons=["asset_not_found_in_manifest"],
        )

    manifest_path = _safe_str(asset.get("path"))
    manifest_asset_id = _safe_str(asset.get("asset_id"))
    manifest_sha = _safe_str(asset.get("sha256"))
    trust_flags = asset.get("trust_flags", [])

    if path and manifest_path and path != manifest_path:
        reasons.append("path_asset_mismatch")
    if asset_id and manifest_asset_id and asset_id != manifest_asset_id:
        reasons.append("asset_id_mismatch")
    if asset_sha256 and manifest_sha and asset_sha256 != manifest_sha:
        reasons.append("asset_sha256_mismatch")
    if isinstance(trust_flags, list) and "possible_stale_or_archived_asset" in trust_flags:
        reasons.append("asset_has_stale_or_archived_flag")
    if isinstance(trust_flags, list) and "unknown_extension" in trust_flags:
        reasons.append("asset_has_unknown_extension_flag")

    if chunk_id:
        chunks = _chunks_by_id(asset)
        chunk = chunks.get(chunk_id)
        if chunk is None:
            reasons.append("chunk_not_found_under_asset")
        else:
            manifest_chunk_sha = _safe_str(chunk.get("sha256"))
            if chunk_sha256 and manifest_chunk_sha and chunk_sha256 != manifest_chunk_sha:
                reasons.append("chunk_sha256_mismatch")
    elif asset.get("chunks"):
        reasons.append("chunk_id_missing_for_chunked_asset")

    status = "approved" if not reasons else "rejected"
    return CitationCheck(
        citation_id=citation_id,
        status=status,
        path=manifest_path or path,
        asset_id=manifest_asset_id or asset_id,
        chunk_id=chunk_id,
        reasons=reasons,
    )


def verify_answer(answer: Mapping[str, Any], manifest: Mapping[str, Any]) -> AnswerVerificationReport:
    """Verify all citations in an answer object against a provenance manifest."""

    answer_id = _safe_str(answer.get("answer_id")) or _safe_str(answer.get("id")) or "answer-unknown"
    citations = answer.get("citations", [])
    if not isinstance(citations, list):
        raise ValueError("Answer field 'citations' must be a list")

    checks = [verify_citation(citation, manifest) for citation in citations if isinstance(citation, Mapping)]
    approved = sum(1 for check in checks if check.status == "approved")
    rejected = len(checks) - approved
    status = "approved" if checks and rejected == 0 else "rejected"
    if not checks:
        status = "rejected"

    return AnswerVerificationReport(
        schema_version="rag-answer-verification/v0.1",
        verifier="cipher-topology-lab.rag_verifier",
        generated_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        answer_id=answer_id,
        status=status,
        citation_count=len(checks),
        approved_count=approved,
        rejected_count=rejected,
        checks=checks,
        claim_boundary="citation provenance verification only; does not certify answer truth or model safety",
    )


def report_to_dict(report: AnswerVerificationReport) -> dict[str, Any]:
    """Convert a verification report into a JSON-serializable dictionary."""

    return asdict(report)


def write_verification_report(report: AnswerVerificationReport, out_path: str | Path) -> Path:
    """Write a JSON verification report."""

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report_to_dict(report), indent=2, sort_keys=True), encoding="utf-8")
    return out


def write_verification_markdown(report: AnswerVerificationReport, out_path: str | Path) -> Path:
    """Write a buyer-readable Markdown verification report."""

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RAG Answer Verification Report",
        "",
        f"Generated UTC: `{report.generated_utc}`",
        f"Answer ID: `{report.answer_id}`",
        f"Overall status: `{report.status}`",
        f"Citations checked: `{report.citation_count}`",
        f"Approved citations: `{report.approved_count}`",
        f"Rejected citations: `{report.rejected_count}`",
        "",
        "## Citation checks",
        "",
        "| Citation | Status | Path | Chunk | Reasons |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        reasons = ", ".join(check.reasons) if check.reasons else "none"
        lines.append(
            f"| `{check.citation_id}` | `{check.status}` | `{check.path or ''}` | `{check.chunk_id or ''}` | {reasons} |"
        )
    lines.extend([
        "",
        "## Claim boundary",
        "",
        report.claim_boundary,
        "",
    ])
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
