from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ciphertopology.utils import read_json


@dataclass(frozen=True)
class WorkflowContext:
    config_path: str
    python_executable: str
    parse_external: bool
    allow_fallback: bool
    build_manuscript: bool

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

    def run(self, context: WorkflowContext) -> None:
        if self.command is None:
            raise NotImplementedError(f"Stage has no command implementation: {self.name}")
        command = [item.format(**self._format_values(context)) for item in self.command]
        print(f"\n==> {self.name}: {self.description}")
        print("$ " + " ".join(command))
        subprocess.run(command, check=True)

    def _format_values(self, context: WorkflowContext) -> dict[str, str]:
        return {
            "python": context.python_executable,
            "config": context.config_path,
            "baseline": context.baseline_condition,
        }


class CleanGeneratedStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(
            name="clean",
            description="remove generated data, result, and external-test artifacts",
        )

    def run(self, context: WorkflowContext) -> None:
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
        for target in targets:
            if target.exists():
                shutil.rmtree(target)
            target.mkdir(parents=True, exist_ok=True)
        print("Cleaned generated artifact directories.")


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

    def run(self, context: WorkflowContext) -> None:
        if not context.parse_external:
            print(f"\n==> {self.name}: skipped; pass --parse-external to enable")
            return
        super().run(context)


class ConsistencyStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(
            name="consistency",
            description="validate backend summaries and baseline-aware distance artifacts",
        )

    def run(self, context: WorkflowContext) -> None:
        command = [
            context.python_executable,
            "scripts/09_validate_artifact_consistency.py",
            "--config",
            context.config_path,
        ]
        if context.allow_fallback:
            command.append("--allow-fallback")
        print(f"\n==> {self.name}: {self.description}")
        print("$ " + " ".join(command))
        subprocess.run(command, check=True)


class ManuscriptStage(WorkflowStage):
    def __init__(self) -> None:
        super().__init__(name="manuscript", description="build manuscript PDF with latexmk")

    def run(self, context: WorkflowContext) -> None:
        if not context.build_manuscript:
            print(f"\n==> {self.name}: skipped; pass --build-manuscript to enable")
            return
        command = ["latexmk", "-pdf", "main.tex"]
        print(f"\n==> {self.name}: {self.description}")
        print("$ cd manuscript && " + " ".join(command))
        subprocess.run(command, cwd="manuscript", check=True)


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

    def run(self, requested: list[str], context: WorkflowContext) -> None:
        stages = self.resolve(requested)
        print("Micro workflow config:")
        print(f"  config: {context.config_path}")
        print(f"  baseline: {context.baseline_condition}")
        print(f"  stages: {', '.join(stage.name for stage in stages)}")
        for stage in stages:
            stage.run(context)
        print("\nMicro workflow complete.")


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    context = WorkflowContext(
        config_path=args.config,
        python_executable=args.python,
        parse_external=args.parse_external,
        allow_fallback=args.allow_fallback,
        build_manuscript=args.build_manuscript,
    )
    build_workflow().run(args.stage, context)


if __name__ == "__main__":
    main()
