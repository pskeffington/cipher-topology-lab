#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "${ROOT_DIR}"

CONFIG="configs/smoke_test.json"
PYTHON_BIN="${PYTHON:-python}"
ALLOW_FALLBACK=1
PARSE_EXTERNAL=0
BUILD_MANUSCRIPT=0
STAGES=()

usage() {
  cat <<'EOF'
Segmented cipher-topology-lab runner

Usage:
  bash scripts/run_segmented.sh smoke
  bash scripts/run_segmented.sh full
  bash scripts/run_segmented.sh stage generate embed features
  bash scripts/run_segmented.sh stage randomness analysis coherence consistency effects evidence

Modes:
  smoke              Run the full segmented workflow with configs/smoke_test.json and fallback allowed.
  full               Run the full segmented workflow with configs/experiment_v0.json.
  stage <names...>   Run only the listed micro-stages with the selected config.
  list               Print available micro-stages.

Options:
  --config PATH          Override config path.
  --python PATH          Override Python executable.
  --strict              Do not allow fallback backend during consistency validation.
  --allow-fallback      Allow fallback backend during consistency validation.
  --parse-external      Parse external randomness-test outputs after export.
  --build-manuscript    Build manuscript PDF after evidence generation.
  -h, --help            Show this help.

Available stages:
  clean generate embed features randomness analysis export external-parse coherence consistency effects evidence manuscript

Examples:
  bash scripts/run_segmented.sh smoke
  bash scripts/run_segmented.sh full
  bash scripts/run_segmented.sh stage generate embed features
  bash scripts/run_segmented.sh --config configs/experiment_v0.json stage coherence consistency effects evidence
EOF
}

if [[ $# -eq 0 ]]; then
  usage
  exit 0
fi

MODE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    smoke|full|stage|list)
      MODE="$1"
      shift
      if [[ "${MODE}" == "stage" ]]; then
        while [[ $# -gt 0 && "$1" != --* ]]; do
          STAGES+=("$1")
          shift
        done
      fi
      ;;
    --config)
      CONFIG="$2"
      shift 2
      ;;
    --python)
      PYTHON_BIN="$2"
      shift 2
      ;;
    --strict)
      ALLOW_FALLBACK=0
      shift
      ;;
    --allow-fallback)
      ALLOW_FALLBACK=1
      shift
      ;;
    --parse-external)
      PARSE_EXTERNAL=1
      shift
      ;;
    --build-manuscript)
      BUILD_MANUSCRIPT=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "${MODE}" in
  smoke)
    CONFIG="${CONFIG:-configs/smoke_test.json}"
    ;;
  full)
    if [[ "${CONFIG}" == "configs/smoke_test.json" ]]; then
      CONFIG="configs/experiment_v0.json"
    fi
    ALLOW_FALLBACK=0
    ;;
  stage)
    if [[ ${#STAGES[@]} -eq 0 ]]; then
      echo "stage mode requires at least one stage name." >&2
      usage >&2
      exit 2
    fi
    ;;
  list)
    echo "clean generate embed features randomness analysis export external-parse coherence consistency effects evidence manuscript"
    exit 0
    ;;
  "")
    echo "Missing mode." >&2
    usage >&2
    exit 2
    ;;
esac

CMD=("${PYTHON_BIN}" "scripts/11_run_micro_workflow.py" "--config" "${CONFIG}")

if [[ "${MODE}" == "stage" ]]; then
  CMD+=("--stage" "${STAGES[@]}")
fi

if [[ "${ALLOW_FALLBACK}" -eq 1 ]]; then
  CMD+=("--allow-fallback")
fi

if [[ "${PARSE_EXTERNAL}" -eq 1 ]]; then
  CMD+=("--parse-external")
fi

if [[ "${BUILD_MANUSCRIPT}" -eq 1 ]]; then
  CMD+=("--build-manuscript")
fi

echo "Repo: ${ROOT_DIR}"
echo "Config: ${CONFIG}"
echo "Python: ${PYTHON_BIN}"
echo "Command: ${CMD[*]}"
exec "${CMD[@]}"
