"""Build a buyer-facing Resilient Provenance pilot report."""

from __future__ import annotations

import argparse

from ciphertopology.pilot_report import write_pilot_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="results/provenance/rag_provenance_manifest.json",
        help="Path to the provenance manifest JSON.",
    )
    parser.add_argument(
        "--verification",
        default="results/provenance/rag_answer_verification.json",
        help="Optional path to RAG answer verification JSON.",
    )
    parser.add_argument(
        "--gis-profile",
        default="results/provenance/gis_provenance_profile.json",
        help="Optional path to GIS profile JSON.",
    )
    parser.add_argument(
        "--out-report",
        default="results/provenance/pilot_report.md",
        help="Output path for the buyer-facing pilot report.",
    )
    parser.add_argument(
        "--client-name",
        default="Pilot Client",
        help="Client or pilot label to include in the report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = write_pilot_report(
        manifest_path=args.manifest,
        verification_path=args.verification,
        gis_profile_path=args.gis_profile,
        out_path=args.out_report,
        client_name=args.client_name,
    )
    print(f"Wrote pilot report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
