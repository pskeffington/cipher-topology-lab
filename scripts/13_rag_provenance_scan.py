"""Run a cryptographic provenance scan for RAG-ready source assets."""

from __future__ import annotations

import argparse
from pathlib import Path

from ciphertopology.rag_provenance import build_manifest, write_manifest, write_markdown_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=".",
        help="Repository, data, or document root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--out-json",
        default="results/provenance/rag_provenance_manifest.json",
        help="Output path for the JSON provenance manifest.",
    )
    parser.add_argument(
        "--out-report",
        default="results/provenance/rag_provenance_report.md",
        help="Output path for the Markdown provenance report.",
    )
    parser.add_argument(
        "--include-extension",
        action="append",
        default=None,
        help="Restrict scan to an extension. May be repeated. Example: --include-extension .md",
    )
    parser.add_argument(
        "--lines-per-chunk",
        type=int,
        default=80,
        help="Line-window size for text chunk hashing.",
    )
    parser.add_argument(
        "--policy-name",
        default="default-rag-provenance-policy",
        help="Policy label written into the manifest.",
    )
    args = parser.parse_args()
    if args.lines_per_chunk <= 0:
        parser.error("--lines-per-chunk must be positive")
    return args


def main() -> int:
    args = parse_args()
    manifest = build_manifest(
        Path(args.root),
        include_extensions=args.include_extension,
        lines_per_chunk=args.lines_per_chunk,
        policy={
            "policy_name": args.policy_name,
            "purpose": "pre-ingestion source and chunk fingerprinting for RAG provenance control",
            "claim_boundary": "provenance evidence only; does not certify source truth or model safety",
        },
    )
    json_path = write_manifest(manifest, args.out_json)
    report_path = write_markdown_report(manifest, args.out_report)
    print(f"Wrote provenance manifest: {json_path}")
    print(f"Wrote provenance report: {report_path}")
    print(f"Assets scanned: {manifest.asset_count}")
    return 0


if __name__ == "__main__":
    main()
