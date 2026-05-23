from __future__ import annotations

import argparse
from pathlib import Path

from ciphertopology.external_tests import parse_dieharder_directory
from ciphertopology.utils import ensure_dirs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dieharder-dir", default="external_tests/results/dieharder")
    parser.add_argument("--out", default="results/tables/external_randomness_tests.csv")
    args = parser.parse_args()

    ensure_dirs(Path(args.out).parent)
    dieharder = parse_dieharder_directory(args.dieharder_dir)
    dieharder.to_csv(args.out, index=False)
    print(f"Wrote {len(dieharder)} external randomness-test rows to {args.out}")


if __name__ == "__main__":
    main()
