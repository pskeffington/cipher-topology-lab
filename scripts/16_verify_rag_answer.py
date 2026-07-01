"""Verify a RAG answer citation object against a provenance manifest."""

from __future__ import annotations

import argparse

from ciphertopology.rag_verifier import (
    load_json,
    verify_answer,
    write_verification_markdown,
    write_verification_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default="results/provenance/rag_provenance_manifest.json",
        help="Path to a RAG provenance manifest JSON file.",
    )
    parser.add_argument(
        "--answer",
        required=True,
        help="Path to an answer citation JSON object.",
    )
    parser.add_argument(
        "--out-json",
        default="results/provenance/rag_answer_verification.json",
        help="Output path for machine-readable verification JSON.",
    )
    parser.add_argument(
        "--out-report",
        default="results/provenance/rag_answer_verification.md",
        help="Output path for buyer-readable verification Markdown.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_json(args.manifest)
    answer = load_json(args.answer)
    report = verify_answer(answer, manifest)
    write_verification_report(report, args.out_json)
    write_verification_markdown(report, args.out_report)
    print(f"Verification status: {report.status}")
    print(f"Approved citations: {report.approved_count}")
    print(f"Rejected citations: {report.rejected_count}")
    return 0 if report.status == "approved" else 1


if __name__ == "__main__":
    raise SystemExit(main())
