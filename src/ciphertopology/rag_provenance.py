"""Cryptographic provenance scanner for retrieval-augmented generation assets.

The scanner is intentionally dependency-light so it can run inside the existing
research repository without changing the cipher/TDA experiment pipeline. It
creates a deterministic manifest for source files that may later feed a RAG
index, GIS layer registry, evidence report, or platform object.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

DEFAULT_TEXT_EXTENSIONS = {
    ".csv",
    ".geojson",
    ".json",
    ".md",
    ".py",
    ".rst",
    ".txt",
    ".yaml",
    ".yml",
}

DEFAULT_BINARY_EXTENSIONS = {
    ".db",
    ".docx",
    ".gpkg",
    ".gz",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".shp",
    ".sqlite",
    ".tif",
    ".tiff",
    ".xlsx",
    ".zip",
}

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}


@dataclass(frozen=True)
class ProvenanceChunk:
    """Deterministic chunk-level fingerprint for text-like source material."""

    chunk_id: str
    start_line: int
    end_line: int
    sha256: str
    bytes: int


@dataclass(frozen=True)
class ProvenanceAsset:
    """File-level provenance record for a source that may enter a RAG pipeline."""

    asset_id: str
    path: str
    source_type: str
    extension: str
    bytes: int
    sha256: str
    modified_utc: str
    trust_flags: list[str] = field(default_factory=list)
    chunks: list[ProvenanceChunk] = field(default_factory=list)


@dataclass(frozen=True)
class ProvenanceManifest:
    """Top-level manifest object written by the scanner."""

    schema_version: str
    scanner: str
    generated_utc: str
    root: str
    asset_count: int
    total_bytes: int
    assets: list[ProvenanceAsset]
    policy: dict[str, object]


def sha256_bytes(data: bytes) -> str:
    """Return a lowercase SHA-256 hex digest for bytes."""

    return sha256(data).hexdigest()


def sha256_file(path: Path, block_size: int = 1024 * 1024) -> str:
    """Hash a file without loading the whole file into memory."""

    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_timestamp(ts: float) -> str:
    """Convert a POSIX timestamp to a stable UTC string."""

    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def infer_source_type(path: Path) -> str:
    """Infer an operational source class from extension and naming conventions."""

    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix in {".geojson", ".gpkg", ".shp", ".tif", ".tiff"}:
        return "gis_layer"
    if suffix in {".pdf", ".docx", ".md", ".rst", ".txt"}:
        return "document"
    if suffix in {".csv", ".json", ".xlsx", ".sqlite", ".db"}:
        return "dataset"
    if suffix in {".py", ".yaml", ".yml"} or "config" in name:
        return "code_or_config"
    return "unknown"


def should_exclude(path: Path, exclude_dirs: Iterable[str]) -> bool:
    """Return true when any path part belongs to an excluded directory."""

    excluded = set(exclude_dirs)
    return any(part in excluded for part in path.parts)


def trust_flags_for(path: Path, *, text_extensions: set[str], binary_extensions: set[str]) -> list[str]:
    """Generate conservative trust flags for a provenance asset."""

    flags: list[str] = []
    suffix = path.suffix.lower()
    if suffix in text_extensions:
        flags.append("chunk_hashable")
    elif suffix in binary_extensions:
        flags.append("file_hash_only")
    else:
        flags.append("unknown_extension")

    if "draft" in path.name.lower():
        flags.append("draft_named_asset")
    if "deprecated" in path.name.lower() or "archive" in path.parts:
        flags.append("possible_stale_or_archived_asset")
    if infer_source_type(path) == "gis_layer":
        flags.append("gis_layer_candidate")
    return flags


def chunk_text_lines(text: str, *, lines_per_chunk: int = 80) -> list[ProvenanceChunk]:
    """Create deterministic line-window chunks for text sources."""

    if lines_per_chunk <= 0:
        raise ValueError("lines_per_chunk must be positive")

    lines = text.splitlines()
    chunks: list[ProvenanceChunk] = []
    for start in range(0, len(lines), lines_per_chunk):
        window = lines[start : start + lines_per_chunk]
        payload = "\n".join(window).encode("utf-8", errors="replace")
        start_line = start + 1
        end_line = start + len(window)
        chunk_hash = sha256_bytes(payload)
        chunks.append(
            ProvenanceChunk(
                chunk_id=f"lines-{start_line:06d}-{end_line:06d}-{chunk_hash[:12]}",
                start_line=start_line,
                end_line=end_line,
                sha256=chunk_hash,
                bytes=len(payload),
            )
        )
    return chunks


def scan_file(
    path: Path,
    *,
    root: Path,
    text_extensions: set[str] | None = None,
    binary_extensions: set[str] | None = None,
    lines_per_chunk: int = 80,
) -> ProvenanceAsset:
    """Scan one file into a file-level and optional chunk-level provenance record."""

    text_extensions = text_extensions or DEFAULT_TEXT_EXTENSIONS
    binary_extensions = binary_extensions or DEFAULT_BINARY_EXTENSIONS
    rel = path.relative_to(root).as_posix()
    stat = path.stat()
    file_hash = sha256_file(path)
    chunks: list[ProvenanceChunk] = []

    if path.suffix.lower() in text_extensions:
        try:
            text = path.read_text(encoding="utf-8")
            chunks = chunk_text_lines(text, lines_per_chunk=lines_per_chunk)
        except UnicodeDecodeError:
            chunks = []

    return ProvenanceAsset(
        asset_id=f"asset-{file_hash[:16]}",
        path=rel,
        source_type=infer_source_type(path),
        extension=path.suffix.lower() or "",
        bytes=stat.st_size,
        sha256=file_hash,
        modified_utc=utc_timestamp(stat.st_mtime),
        trust_flags=trust_flags_for(
            path,
            text_extensions=text_extensions,
            binary_extensions=binary_extensions,
        ),
        chunks=chunks,
    )


def iter_candidate_files(root: Path, *, exclude_dirs: Iterable[str] = DEFAULT_EXCLUDE_DIRS) -> Iterable[Path]:
    """Yield regular files under root in deterministic order."""

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if should_exclude(path.relative_to(root), exclude_dirs):
            continue
        yield path


def build_manifest(
    root: str | Path,
    *,
    include_extensions: Sequence[str] | None = None,
    exclude_dirs: Iterable[str] = DEFAULT_EXCLUDE_DIRS,
    lines_per_chunk: int = 80,
    policy: Mapping[str, object] | None = None,
) -> ProvenanceManifest:
    """Build a deterministic provenance manifest for a repository or data root."""

    root_path = Path(root).expanduser().resolve()
    if not root_path.exists():
        raise FileNotFoundError(root_path)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    allowed = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in include_extensions or []}
    assets: list[ProvenanceAsset] = []
    for path in iter_candidate_files(root_path, exclude_dirs=exclude_dirs):
        if allowed and path.suffix.lower() not in allowed:
            continue
        assets.append(scan_file(path, root=root_path, lines_per_chunk=lines_per_chunk))

    return ProvenanceManifest(
        schema_version="rag-provenance-manifest/v0.1",
        scanner="cipher-topology-lab.rag_provenance",
        generated_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        root=root_path.as_posix(),
        asset_count=len(assets),
        total_bytes=sum(asset.bytes for asset in assets),
        assets=assets,
        policy=dict(policy or {}),
    )


def manifest_to_dict(manifest: ProvenanceManifest) -> dict[str, object]:
    """Convert dataclass manifest to a plain JSON-serializable dictionary."""

    return asdict(manifest)


def write_manifest(manifest: ProvenanceManifest, out_path: str | Path) -> Path:
    """Write a manifest JSON file with stable key ordering and indentation."""

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest_to_dict(manifest), indent=2, sort_keys=True), encoding="utf-8")
    return out


def write_markdown_report(manifest: ProvenanceManifest, out_path: str | Path) -> Path:
    """Write a compact human-readable provenance report."""

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    by_type: dict[str, int] = {}
    flagged: list[ProvenanceAsset] = []
    for asset in manifest.assets:
        by_type[asset.source_type] = by_type.get(asset.source_type, 0) + 1
        if any(flag in asset.trust_flags for flag in {"unknown_extension", "possible_stale_or_archived_asset"}):
            flagged.append(asset)

    lines = [
        "# RAG Provenance Scan Report",
        "",
        f"Generated UTC: `{manifest.generated_utc}`",
        f"Root: `{manifest.root}`",
        f"Assets scanned: `{manifest.asset_count}`",
        f"Total bytes: `{manifest.total_bytes}`",
        "",
        "## Asset classes",
        "",
        "| Source type | Count |",
        "|---|---:|",
    ]
    for source_type, count in sorted(by_type.items()):
        lines.append(f"| {source_type} | {count} |")

    lines.extend([
        "",
        "## Review flags",
        "",
        "| Path | Flags | SHA-256 |",
        "|---|---|---|",
    ])
    for asset in flagged[:100]:
        lines.append(f"| `{asset.path}` | {', '.join(asset.trust_flags)} | `{asset.sha256}` |")
    if not flagged:
        lines.append("| None | No review flags generated |  |")

    lines.extend([
        "",
        "## Intended use",
        "",
        "This report is a provenance-control artifact for RAG, GIS, document, and dataset ingestion. It records source fingerprints and chunk fingerprints where text extraction is available. It does not certify truth, completeness, safety, or cryptographic security of the scanned content.",
        "",
    ])
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
