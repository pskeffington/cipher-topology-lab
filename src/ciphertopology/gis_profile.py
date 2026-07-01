"""GIS and infrastructure provenance profile helpers.

This module turns a generic RAG provenance manifest into a civic/infrastructure
readiness view. It is intentionally conservative: it infers layer sectors from
paths and names, flags missing sectors, and produces a buyer-readable summary
without claiming data completeness or operational readiness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_INFRASTRUCTURE_SECTORS: dict[str, tuple[str, ...]] = {
    "roads_transportation": ("road", "roads", "street", "streets", "transport", "bridge", "highway"),
    "parcels_property": ("parcel", "parcels", "property", "assessor", "lot"),
    "water": ("water", "hydrant", "main", "drinking"),
    "sewer_wastewater": ("sewer", "wastewater", "stormwater", "drain"),
    "electric_energy": ("electric", "energy", "grid", "substation", "power"),
    "telecom": ("telecom", "fiber", "broadband", "cell", "tower"),
    "public_safety": ("police", "fire", "ems", "public_safety", "safety"),
    "emergency_management": ("emergency", "shelter", "evacuation", "hazard", "incident"),
    "healthcare_public_health": ("health", "hospital", "clinic", "public_health"),
    "schools_civic": ("school", "library", "town_hall", "municipal", "civic"),
    "flood_environment": ("flood", "wetland", "watershed", "environment", "fema"),
    "zoning_land_use": ("zoning", "land_use", "landuse", "planning"),
}

GIS_EXTENSIONS = {".geojson", ".gpkg", ".shp", ".tif", ".tiff", ".kml", ".kmz"}


@dataclass(frozen=True)
class SectorFinding:
    """Profile result for one expected civic/infrastructure sector."""

    sector: str
    status: str
    matched_assets: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GISProfileReport:
    """Machine-readable GIS provenance profile report."""

    schema_version: str
    profiler: str
    generated_utc: str
    manifest_asset_count: int
    gis_candidate_count: int
    covered_sector_count: int
    missing_sector_count: int
    findings: list[SectorFinding]
    claim_boundary: str


def load_manifest(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected manifest object at {path}")
    return payload


def _asset_path(asset: Mapping[str, Any]) -> str:
    value = asset.get("path")
    return value if isinstance(value, str) else ""


def _asset_flags(asset: Mapping[str, Any]) -> list[str]:
    flags = asset.get("trust_flags", [])
    return [flag for flag in flags if isinstance(flag, str)] if isinstance(flags, list) else []


def is_gis_candidate(asset: Mapping[str, Any]) -> bool:
    path = _asset_path(asset).lower()
    extension = asset.get("extension")
    source_type = asset.get("source_type")
    flags = _asset_flags(asset)
    return (
        source_type == "gis_layer"
        or extension in GIS_EXTENSIONS
        or any(path.endswith(ext) for ext in GIS_EXTENSIONS)
        or "gis_layer_candidate" in flags
    )


def infer_asset_sector(asset: Mapping[str, Any]) -> str | None:
    """Infer a sector from a manifest asset path/name using conservative keywords."""

    path = _asset_path(asset).lower().replace("-", "_").replace("/", "_")
    for sector, keywords in REQUIRED_INFRASTRUCTURE_SECTORS.items():
        if any(keyword in path for keyword in keywords):
            return sector
    return None


def build_gis_profile(manifest: Mapping[str, Any]) -> GISProfileReport:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("Manifest field 'assets' must be a list")

    gis_assets = [asset for asset in assets if isinstance(asset, Mapping) and is_gis_candidate(asset)]
    sector_matches: dict[str, list[str]] = {sector: [] for sector in REQUIRED_INFRASTRUCTURE_SECTORS}

    for asset in gis_assets:
        sector = infer_asset_sector(asset)
        if sector:
            sector_matches[sector].append(_asset_path(asset))

    findings: list[SectorFinding] = []
    for sector in REQUIRED_INFRASTRUCTURE_SECTORS:
        matched = sorted(sector_matches[sector])
        if matched:
            findings.append(
                SectorFinding(
                    sector=sector,
                    status="covered_candidate",
                    matched_assets=matched,
                    notes=["sector inferred from GIS candidate asset naming"],
                )
            )
        else:
            findings.append(
                SectorFinding(
                    sector=sector,
                    status="missing_candidate",
                    matched_assets=[],
                    notes=["no GIS candidate asset matched this sector keyword profile"],
                )
            )

    missing = sum(1 for finding in findings if finding.status == "missing_candidate")
    covered = len(findings) - missing
    return GISProfileReport(
        schema_version="gis-provenance-profile/v0.1",
        profiler="cipher-topology-lab.gis_profile",
        generated_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        manifest_asset_count=len(assets),
        gis_candidate_count=len(gis_assets),
        covered_sector_count=covered,
        missing_sector_count=missing,
        findings=findings,
        claim_boundary="GIS provenance profile only; does not certify map completeness, asset accuracy, public safety readiness, or infrastructure security",
    )


def report_to_dict(report: GISProfileReport) -> dict[str, Any]:
    return asdict(report)


def write_gis_profile_json(report: GISProfileReport, out_path: str | Path) -> Path:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report_to_dict(report), indent=2, sort_keys=True), encoding="utf-8")
    return out


def write_gis_profile_markdown(report: GISProfileReport, out_path: str | Path) -> Path:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# GIS Provenance Profile Report",
        "",
        f"Generated UTC: `{report.generated_utc}`",
        f"Manifest assets: `{report.manifest_asset_count}`",
        f"GIS candidates: `{report.gis_candidate_count}`",
        f"Covered sectors: `{report.covered_sector_count}`",
        f"Missing sectors: `{report.missing_sector_count}`",
        "",
        "## Sector findings",
        "",
        "| Sector | Status | Matched assets | Notes |",
        "|---|---|---|---|",
    ]
    for finding in report.findings:
        assets = "<br>".join(f"`{path}`" for path in finding.matched_assets) if finding.matched_assets else ""
        notes = "; ".join(finding.notes)
        lines.append(f"| {finding.sector} | `{finding.status}` | {assets} | {notes} |")
    lines.extend([
        "",
        "## Claim boundary",
        "",
        report.claim_boundary,
        "",
    ])
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
