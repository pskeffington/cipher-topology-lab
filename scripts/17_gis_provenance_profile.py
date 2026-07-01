"""Build a GIS/infrastructure provenance profile from a RAG provenance manifest."""

from __future__ import annotations

import argparse

from ciphertopology.gis_profile import (
    build_gis_profile,
    load_manifest,
    write_gis_profile_json,
    write_gis_profile_markdown,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="results/provenance/rag_provenance_manifest.json",
        help="Path to a RAG provenance manifest JSON file.",
    )
    parser.add_argument(
        "--out-json",
        default="results/provenance/gis_provenance_profile.json",
        help="Output path for machine-readable GIS profile JSON.",
    )
    parser.add_argument(
        "--out-report",
        default="results/provenance/gis_provenance_profile.md",
        help="Output path for buyer-readable GIS profile Markdown.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    report = build_gis_profile(manifest)
    write_gis_profile_json(report, args.out_json)
    write_gis_profile_markdown(report, args.out_report)
    print(f"GIS candidates: {report.gis_candidate_count}")
    print(f"Covered sectors: {report.covered_sector_count}")
    print(f"Missing sectors: {report.missing_sector_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
