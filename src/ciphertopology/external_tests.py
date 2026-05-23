from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def parse_dieharder_text(text: str, source_file: str | None = None) -> list[dict[str, Any]]:
    """Parse common Dieharder pipe-delimited result rows."""
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        if "|" not in line:
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 6:
            continue
        test_name, ntup, tsamples, psamples, p_value_raw, assessment = parts[:6]
        if test_name.lower().replace("#", "").strip() == "test_name":
            continue
        try:
            p_value = float(p_value_raw)
        except ValueError:
            continue
        rows.append(
            {
                "source_file": source_file,
                "suite": "dieharder",
                "test_name": test_name,
                "ntup": ntup,
                "tsamples": tsamples,
                "psamples": psamples,
                "p_value": p_value,
                "assessment": assessment,
            }
        )
    return rows


def parse_dieharder_directory(path: str | Path) -> pd.DataFrame:
    directory = Path(path)
    rows: list[dict[str, Any]] = []
    for result_file in sorted(directory.glob("*.txt")):
        rows.extend(parse_dieharder_text(result_file.read_text(encoding="utf-8"), str(result_file)))
    return pd.DataFrame(rows)
