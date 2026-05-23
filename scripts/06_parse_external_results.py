from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ciphertopology.external_tests import parse_dieharder_directory
from ciphertopology.utils import ensure_dirs


EXTERNAL_RESULT_COLUMNS = [
    "source_file",
    "suite",
    "test_name",
    "ntup",
    "tsamples",
    "psamples",
    "p_value",
    "assessment",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dieharder-dir", default="external_tests/results/dieharder")
    parser.add_argument("--out", default="results/tables/external_randomness_tests.csv")
    args = parser.parse_args()

    ensure_dirs(Path(args.out).parent)
    dieharder = parse_dieharder_directory(args.dieharder_dir)
    if dieharder.empty:
        dieharder = pd.DataFrame(columns=EXTERNAL_RESULT_COLUMNS)
    else:
        dieharder = dieharder.reindex(columns=EXTERNAL_RESULT_COLUMNS)
    dieharder.to_csv(args.out, index=False)
    print(f"Wrote {len(dieharder)} external randomness-test rows to {args.out}")


if __name__ == "__main__":
    main()
