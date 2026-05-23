from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

from ciphertopology.utils import ensure_dirs, sha256_file


def write_dieharder_script(out_dir: Path) -> None:
    script = out_dir / "run_dieharder.sh"
    script.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "mkdir -p ../results/dieharder\n"
        "for f in *.bin; do\n"
        "  base=${f%.bin}\n"
        "  dieharder -a -g 201 -f \"$f\" > \"../results/dieharder/${base}.txt\"\n"
        "done\n",
        encoding="utf-8",
    )


def write_nist_notes(out_dir: Path) -> None:
    notes = out_dir / "README_NIST_STS.md"
    notes.write_text(
        "# NIST SP 800-22 input files\n\n"
        "This directory contains binary stream exports for external randomness testing.\n\n"
        "NIST SP 800-22 execution depends on the locally compiled STS suite and its expected input path conventions. "
        "Record the STS version, compiler, operating system, bitstream length, and all selected tests before importing results.\n\n"
        "Do not treat SP 800-22 results as cryptographic proof. These outputs are conventional statistical diagnostics only.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/raw/stream_manifest.csv")
    parser.add_argument("--out-dir", default="external_tests/inputs")
    args = parser.parse_args()

    manifest = pd.read_csv(args.manifest)
    out_dir = Path(args.out_dir)
    ensure_dirs(out_dir, "external_tests/results/dieharder", "external_tests/results/nist_sts")

    rows = []
    for _, row in manifest.iterrows():
        source = Path(row["path"])
        target_name = f"{row['stream_id']}.bin"
        target = out_dir / target_name
        shutil.copyfile(source, target)
        rows.append(
            {
                "stream_id": row["stream_id"],
                "condition": row["condition"],
                "bytes": int(row["bytes"]),
                "export_path": str(target),
                "sha256": sha256_file(target),
            }
        )

    export_manifest = out_dir / "export_manifest.csv"
    pd.DataFrame(rows).to_csv(export_manifest, index=False)
    write_dieharder_script(out_dir)
    write_nist_notes(out_dir)
    print(f"Exported {len(rows)} files to {out_dir}")
    print(f"Wrote export manifest to {export_manifest}")


if __name__ == "__main__":
    main()
