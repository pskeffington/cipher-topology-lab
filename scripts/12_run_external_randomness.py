from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

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


@dataclass(frozen=True)
class ExternalTestTarget:
    condition: str
    replicate: int
    path: Path

    @property
    def stem(self) -> str:
        return self.path.stem


@dataclass(frozen=True)
class ExternalTestResult:
    target: ExternalTestTarget
    status: str
    command: str
    output_path: Path
    message: str


class DieharderRunner:
    def __init__(self, dieharder_bin: str, result_dir: Path, test_id: int) -> None:
        self.dieharder_bin = dieharder_bin
        self.result_dir = result_dir
        self.test_id = test_id

    def available(self) -> bool:
        return shutil.which(self.dieharder_bin) is not None

    def run_target(self, target: ExternalTestTarget) -> ExternalTestResult:
        ensure_dirs(self.result_dir)
        output_path = self.result_dir / f"{target.stem}_d{self.test_id}.txt"
        command = [self.dieharder_bin, "-d", str(self.test_id), "-g", "201", "-f", str(target.path)]
        command_text = " ".join(command)
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        output_text = completed.stdout + completed.stderr
        output_path.write_text(output_text, encoding="utf-8")
        if completed.returncode != 0:
            return ExternalTestResult(
                target=target,
                status="FAIL",
                command=command_text,
                output_path=output_path,
                message=f"dieharder returned {completed.returncode}",
            )
        if output_path.stat().st_size == 0:
            return ExternalTestResult(
                target=target,
                status="FAIL",
                command=command_text,
                output_path=output_path,
                message="dieharder produced an empty output file",
            )
        return ExternalTestResult(
            target=target,
            status="PASS",
            command=command_text,
            output_path=output_path,
            message="",
        )


def load_targets(manifest_path: Path, input_dir: Path, replicate: int) -> list[ExternalTestTarget]:
    manifest = pd.read_csv(manifest_path)
    targets: list[ExternalTestTarget] = []
    for _, row in manifest.iterrows():
        if int(row.get("replicate", -1)) != replicate:
            continue
        stream_id = str(row["stream_id"])
        condition = str(row["condition"])
        path = input_dir / f"{stream_id}.bin"
        if path.exists():
            targets.append(ExternalTestTarget(condition=condition, replicate=replicate, path=path))
    return targets


def write_empty_external_table(path: Path) -> None:
    ensure_dirs(path.parent)
    pd.DataFrame(columns=EXTERNAL_RESULT_COLUMNS).to_csv(path, index=False)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def write_status_report(
    path: Path,
    manifest_path: Path,
    input_dir: Path,
    result_dir: Path,
    parsed_output: Path,
    dieharder_bin: str,
    test_id: int,
    targets: list[ExternalTestTarget],
    results: list[ExternalTestResult],
    status: str,
    message: str,
) -> None:
    ensure_dirs(path.parent)
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    rows = [
        [
            result.target.condition,
            result.target.replicate,
            f"`{result.target.path}`",
            result.status,
            f"`{result.output_path}`",
            result.message,
        ]
        for result in results
    ]
    target_rows = [
        [target.condition, target.replicate, f"`{target.path}`", target.path.exists(), target.path.stat().st_size if target.path.exists() else 0]
        for target in targets
    ]
    content = f"""# External Randomness Test Status

Generated: `{generated_at}`
Status: `{status}`
Message: `{message}`

## Configuration

- Manifest: `{manifest_path}`
- Input directory: `{input_dir}`
- Result directory: `{result_dir}`
- Parsed output: `{parsed_output}`
- Dieharder executable: `{dieharder_bin}`
- Dieharder test id: `{test_id}`

## Selected targets

{markdown_table(['Condition', 'Replicate', 'Path', 'Exists', 'Bytes'], target_rows) if target_rows else 'No targets selected.'}

## Test results

{markdown_table(['Condition', 'Replicate', 'Input', 'Status', 'Output', 'Message'], rows) if rows else 'No external tests were run.'}

## Notes

This file is intentionally written even when Dieharder is unavailable or a test fails, so the evidence register can distinguish missing external infrastructure from absent analysis.
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/raw/stream_manifest.csv")
    parser.add_argument("--input-dir", default="external_tests/inputs")
    parser.add_argument("--result-dir", default="external_tests/results/dieharder")
    parser.add_argument("--parsed-output", default="data/processed/external_randomness_tests.csv")
    parser.add_argument("--status-report", default="results/logs/external_randomness_status.md")
    parser.add_argument("--dieharder-bin", default="dieharder")
    parser.add_argument("--test-id", type=int, default=0)
    parser.add_argument("--replicate", type=int, default=0)
    parser.add_argument("--allow-missing-dieharder", action="store_true")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    input_dir = Path(args.input_dir)
    result_dir = Path(args.result_dir)
    parsed_output = Path(args.parsed_output)
    status_report = Path(args.status_report)

    ensure_dirs(result_dir, parsed_output.parent, status_report.parent)
    write_empty_external_table(parsed_output)

    if not manifest_path.exists():
        write_status_report(
            status_report,
            manifest_path,
            input_dir,
            result_dir,
            parsed_output,
            args.dieharder_bin,
            args.test_id,
            [],
            [],
            "FAIL",
            f"Missing manifest: {manifest_path}",
        )
        raise SystemExit(f"Missing manifest: {manifest_path}")

    targets = load_targets(manifest_path, input_dir, args.replicate)
    runner = DieharderRunner(args.dieharder_bin, result_dir, args.test_id)

    if not runner.available():
        message = f"Dieharder executable not found on PATH: {args.dieharder_bin}"
        write_status_report(
            status_report,
            manifest_path,
            input_dir,
            result_dir,
            parsed_output,
            args.dieharder_bin,
            args.test_id,
            targets,
            [],
            "UNAVAILABLE",
            message,
        )
        print(message)
        if args.allow_missing_dieharder:
            return
        raise SystemExit(message)

    if not targets:
        message = f"No input files found for replicate {args.replicate} in {input_dir}"
        write_status_report(
            status_report,
            manifest_path,
            input_dir,
            result_dir,
            parsed_output,
            args.dieharder_bin,
            args.test_id,
            targets,
            [],
            "FAIL",
            message,
        )
        raise SystemExit(message)

    results = [runner.run_target(target) for target in targets]
    failed = [result for result in results if result.status != "PASS"]
    status = "FAIL" if failed else "PASS"
    message = f"{len(results) - len(failed)} passed, {len(failed)} failed."
    write_status_report(
        status_report,
        manifest_path,
        input_dir,
        result_dir,
        parsed_output,
        args.dieharder_bin,
        args.test_id,
        targets,
        results,
        status,
        message,
    )
    print(message)
    if failed:
        raise SystemExit(message)

    subprocess.run(
        [
            sys.executable,
            "scripts/06_parse_external_results.py",
            "--dieharder-dir",
            str(result_dir),
            "--out",
            str(parsed_output),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
