from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ciphertopology.utils import ensure_dirs, read_json


@dataclass(frozen=True)
class StageResult:
    name: str
    status: str
    returncode: int | None
    command: str
    message: str

    @property
    def failed(self) -> bool:
        return self.status == "FAIL"


@dataclass(frozen=True)
class WorkflowContext:
    config_path: str
    python_executable: str
    parse_external: bool
    allow_fallback: bool
    build_manuscript: bool
    continue_on_failure: bool
    report_path: Path

    @property
    def baseline_condition(self) -> str:
        config = read_json(self.config_path)
        baseline = config.get("baseline_condition")
        if not baseline:
            raise SystemExit(f"Config has no baseline_condition: {self.config_path}")
        return str(baseline)


@dataclass(frozen=True)
class WorkflowStage:
    name: str
    description: str
    command: list[str] | None = None

    def run(self, context: WorkflowContext) -> StageResult:
        if self.command is None:
            raise NotImplementedError(f"Stage has no command implementation: {self.name}")
        command = [item.format(**self._format_values(context)) for item in self.command]
        return run_command_stage(self.name, self.description, command)

    def _format_values(self, context: WorkflowContext) -> dict[str, str]:
        return {
            "python": context.python_executable,
            "config": context.config_path,
            "baseline": context.baseline_condition,
        }


def command_string(command: list[str]) -> str:
    return " ".join(command)


def run_command_stage(
    name: str,
    description: str,
    command: list[str],
    cwd: str | None = None,
) -> StageResult:
    print(f"\n==> {name}: {description}")
    prefix = f"cd {cwd} && " if cwd else ""
    print("$ " + prefix + command_string(command))
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode == 0:
        print(f"PASS: {name}")
        return StageResult(name, "PASS", completed.returncode, prefix + command_string(command), "")
    message = f"Stage failed with return code {completed.returncode}."
    print(f"FAIL: {name}: {message}")
    return StageResult(name, "FAIL", completed.returncode, prefix + command_string(command), message)


class CleanGeneratedStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(
            name="clean",
            description="remove generated data, result, and external-test artifacts",
        )

    def run(self, context: WorkflowContext) -> StageResult:
        print(f"\n==> {self.name}: {self.description}")
        targets = [
            Path("data/raw"),
            Path("data/interim"),
            Path("data/processed"),
            Path("results/figures"),
            Path("results/tables"),
            Path("results/logs"),
            Path("external_tests/inputs"),
            Path("external_tests/results"),
        ]
        try:
            for target in targets:
                if target.exists():
                    shutil.rmtree(target)
                target.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            message = f"Clean failed: {exc}"
            print(f"FAIL: {self.name}: {message}")
            return StageResult(self.name, "FAIL", None, "clean generated directories", message)
        print("PASS: cleaned generated artifact directories.")
        return StageResult(self.name, "PASS", 0, "clean generated directories", "")


class OptionalExternalParseStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(
            name="external-parse",
            description="parse external randomness-test outputs when available",
            command=[
                "{python}",
                "scripts/06_parse_external_results.py",
                "--dieharder-dir",
                "external_tests/results/dieharder",
                "--out",
                "data/processed/external_randomness_tests.csv",
            ],
        )

    def run(self, context: WorkflowContext) -> StageResult:
        if not context.parse_external:
            message = "Skipped; pass --parse-external to enable."
            print(f"\n==> {self.name}: {message}")
            return StageResult(self.name, "SKIP", 0, "", message)
        return super().run(context)


class ConsistencyStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(
            name="consistency",
            description="validate backend summaries and baseline-aware distance artifacts",
        )

    def run(self, context: WorkflowContext) -> StageResult:
        command = [
            context.python_executable,
            "scripts/09_validate_artifact_consistency.py",
            "--config",
            context.config_path,
        ]
        if context.allow_fallback:
            command.append("--allow-fallback")
        return run_command_stage(self.name, self.description, command)


class ManuscriptStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(name="manuscript", description="build manuscript PDF with latexmk")

    def run(self, context: WorkflowContext) -> StageResult:
        if not context.build_manuscript:
            message = "Skipped; pass --build-manuscript to enable."
            print(f"\n==> {self.name}: {message}")
            return StageResult(self.name, "SKIP", 0, "", message)
        return run_command_stage(self.name, self.description, ["latexmk", "-pdf", "main.tex"], cwd="manuscript")


class MicroWorkflow:
    def __init__(self, stages: list[WorkflowStage]) -> None:
        self.stages = {stage.name: stage for stage in stages}

    @property
    def ordered_stage_names(self) -> list[str]:
        return list(self.stages.keys())

    def resolve(self, requested: list[str]) -> list[WorkflowStage]:
        if not requested or requested == ["all"]:
            requested = self.ordered_stage_names
        unknown = [name for name in requested if name not in self.stages]
        if unknown:
            raise SystemExit(
                "Unknown stage(s): "
                + ", ".join(unknown)
                + "\nAvailable stages: "
                + ", ".join(self.ordered_stage_names)
            )
        return [self.stages[name] for name in requested]

    def run(self, requested: list[str], context: WorkflowContext) -> list[StageResult]:
        stages = self.resolve(requested)
        print("Micro workflow config:")
        print(f"  config: {context.config_path}")
        print(f"  baseline: {context.baseline_condition}")
        print(f"  stages: {', '.join(stage.name for stage in stages)}")
        print(f"  continue_on_failure: {context.continue_on_failure}")
        results: list[StageResult] = []
        for stage in stages:
            result = stage.run(context)
            results.append(result)
            write_run_report(context, results, final=False)
            if result.failed and not context.continue_on_failure:
                break
        write_run_report(context, results, final=True)
        failed = [result.name for result in results if result.failed]
        if failed:
            print("\nMicro workflow completed with failures: " + ", ".join(failed))
            print(f"Report: {context.report_path}")
            if not context.continue_on_failure:
                raise SystemExit(1)
            return results
        print("\nMicro workflow complete.")
        print(f"Report: {context.report_path}")
        return results


def artifact_status_rows() -> list[tuple[str, str, str]]:
    paths = [
        "data/raw/stream_manifest.csv",
        "data/interim/embedding_manifest.csv",
        "data/processed/tda_features.csv",
        "data/processed/randomness_tests_internal.csv",
        "data/processed/external_randomness_tests.csv",
        "results/tables/tda_backend_summary.csv",
        "results/tables/tda_feature_summary.csv",
        "results/tables/tda_persistence_entropy_effects.csv",
        "results/tables/tda_distance_effects.csv",
        "results/tables/tda_effects_combined.csv",
        "docs/evidence_register.md",
    ]
    rows = []
    for item in paths:
        path = Path(item)
        if path.exists():
            rows.append((item, "present", str(path.stat().st_size)))
        else:
            rows.append((item, "missing", "0"))
    for directory in ["results/figures", "results/logs", "external_tests/inputs"]:
        path = Path(directory)
        count = len([item for item in path.glob("*") if item.is_file()]) if path.exists() else 0
        rows.append((directory, "present" if path.exists() else "missing", f"{count} files"))
    return rows


def markdown_table(headers: list[str], rows: list[list[str] | tuple[str, ...]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def write_run_report(context: WorkflowContext, results: list[StageResult], final: bool) -> None:
    ensure_dirs(context.report_path.parent)
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    status = "final" if final else "partial"
    result_rows = [
        [result.name, result.status, "" if result.returncode is None else result.returncode, result.command, result.message]
        for result in results
    ]
    content = f"""# Segmented Run Report

Generated: `{generated_at}`
Status: `{status}`
Config: `{context.config_path}`
Baseline condition: `{context.baseline_condition}`
Continue on failure: `{context.continue_on_failure}`

## Stage results

{markdown_table(['Stage', 'Status', 'Return code', 'Command', 'Message'], result_rows) if result_rows else 'No stages have run.'}

## Artifact availability

{markdown_table(['Artifact', 'Status', 'Size or count'], artifact_status_rows())}

## Notes

This report is written after every stage, so a failed segmented run should still leave partial diagnostics and artifact availability information for debugging.
"""
    context.report_path.write_text(content, encoding="utf-8")


def build_workflow() -> MicroWorkflow:
    return MicroWorkflow(
        [
            CleanGeneratedStage(),
            WorkflowStage(
                name="generate",
                description="generate reproducible stream artifacts and manifest",
                command=["{python}", "scripts/00_generate_streams.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="embed",
                description="convert generated streams into configured embeddings",
                command=["{python}", "scripts/01_embed_ciphertext.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="features",
                description="compute persistent-homology feature tables",
                command=["{python}", "scripts/02_compute_tda_features.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="randomness",
                description="run internal randomness diagnostics",
                command=["{python}", "scripts/03_randomness_tests.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="analysis",
                description="build summaries, distance tables, figures, and logs",
                command=["{python}", "scripts/04_analyze_results.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="export",
                description="export streams for external randomness-test suites",
                command=[
                    "{python}",
                    "scripts/05_export_randomness_inputs.py",
                    "--manifest",
                    "data/raw/stream_manifest.csv",
                ],
            ),
            OptionalExternalParseStage(),
            WorkflowStage(
                name="coherence",
                description="validate artifact counts, categories, and config coherence",
                command=["{python}", "scripts/08_validate_artifact_coherence.py", "--config", "{config}"],
            ),
            ConsistencyStage(),
            WorkflowStage(
                name="effects",
                description="build baseline-aware effect-size tables",
                command=["{python}", "scripts/10_effect_size_tables.py", "--config", "{config}"],
            ),
            WorkflowStage(
                name="evidence",
                description="build evidence register for claim traceability",
                command=[
                    "{python}",
                    "scripts/09_build_evidence_register.py",
                    "--config",
                    "{config}",
                    "--output",
                    "docs/evidence_register.md",
                ],
            ),
            ManuscriptStage(),
        ]
    )


def parse_args() -> argparse.Namespace:
    workflow = build_workflow()
    parser = argparse.ArgumentParser(
        description="Run object-oriented micro-stages for the cipher-topology-lab analysis pipeline."
    )
    parser.add_argument(
        "--config",
        default="configs/experiment_v0.json",
        help="Analysis config to use. Use configs/smoke_test.json for a quick validation run.",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable used to run stage scripts. Defaults to the current interpreter.",
    )
    parser.add_argument(
        "--stage",
        nargs="+",
        default=["all"],
        help="Stage(s) to run. Use 'all' or any ordered subset: "
        + ", ".join(workflow.ordered_stage_names),
    )
    parser.add_argument(
        "--parse-external",
        action="store_true",
        help="Parse external randomness-test outputs after export when results are present.",
    )
    parser.add_argument(
        "--allow-fallback",
        action="store_true",
        help="Allow fallback TDA backends during artifact consistency validation.",
    )
    parser.add_argument(
        "--build-manuscript",
        action="store_true",
        help="Run latexmk after evidence generation.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first failed stage. By default, the workflow continues and reports partial artifacts.",
    )
    parser.add_argument(
        "--report-path",
        default="results/logs/segmented_run_report.md",
        help="Markdown report path written after every stage.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    context = WorkflowContext(
        config_path=args.config,
        python_executable=args.python,
        parse_external=args.parse_external,
        allow_fallback=args.allow_fallback,
        build_manuscript=args.build_manuscript,
        continue_on_failure=not args.fail_fast,
        report_path=Path(args.report_path),
    )
    results = build_workflow().run(args.stage, context)
    failed = [result for result in results if result.failed]
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
