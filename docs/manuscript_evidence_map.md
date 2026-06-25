# Manuscript Evidence Map

## Purpose

This map links manuscript sections to registered evidence artifacts. It is a working control document for avoiding unsupported thesis claims.

## Evidence sources

| Evidence source | Role |
| --- | --- |
| `docs/evidence_register.md` | Primary six-condition 64-replicate evidence register. |
| `docs/evidence_register_weak_controls.md` | Eight-condition weak-control sensitivity evidence register. |
| `docs/evidence_register_weak_controls_seed_robustness.md` | Alternate-seed weak-control robustness evidence register. |
| `docs/CONTRIBUTION_BOUNDARY.md` | Public claim boundary and non-claim language. |
| `docs/lab_notes/2026-06-25-weak-control-sensitivity.md` | Weak-control sensitivity interpretation note. |
| `docs/lab_notes/2026-06-25-seed-robustness-pass.md` | Seed-robustness and thesis-readiness note. |

## Section-to-evidence mapping

| Manuscript section | Supported claims | Primary evidence |
| --- | --- | --- |
| `sec:introduction` | Diagnostic framing, research question, non-cryptanalytic scope. | `docs/CONTRIBUTION_BOUNDARY.md`, `docs/thesis_scaffold.md` |
| `sec:background` | Definitions and interpretation boundaries for baselines, weak controls, and evidence registration. | `docs/CONTRIBUTION_BOUNDARY.md`, configs, README |
| `sec:related-work` | Literature framing and gap statement. | Bibliography and diagnostic scope docs |
| `sec:methods` | Object-oriented staged workflow, manifests, embeddings, TDA features, validation, evidence registration. | Scripts, configs, evidence registers, `docs/latex_workflow.md` |
| `subsec:primary-six-condition-results` | Six-condition artifact scale, backend, baseline, validation status. | `docs/evidence_register.md` |
| `subsec:lcg-results` | LCG weak-control separation in the primary 64-replicate run. | `docs/evidence_register.md`, `results/tables/tda_effects_combined.csv` from the registered run |
| `subsec:primary-non-lcg-comparisons` | AES-CTR, OS CSPRNG, and xorshift32 did not show comparable separation in the primary run. | `docs/evidence_register.md`, primary effect-size table |
| `subsec:weak-control-sensitivity-results` | Periodic and biased controls separate strongly in the eight-condition extension. | `docs/evidence_register_weak_controls.md`, weak-control lab note |
| `subsec:seed-robustness-results` | Weak-control sensitivity pattern reproduces under alternate deterministic master seed. | `docs/evidence_register_weak_controls_seed_robustness.md`, seed-robustness lab note |
| `subsec:external-randomness-status-results` | Dieharder unavailable locally; no completed external randomness comparison claimed. | Evidence-register external randomness status fields |
| `sec:discussion` | Diagnostic interpretation, non-separation limits, external-test limitation, no cipher vulnerability claim. | `docs/CONTRIBUTION_BOUNDARY.md`, evidence registers |
| `app:replication` | Run commands, eligibility criteria, evidence files, claim checklist. | Configs, evidence registers, run-plan docs |

## Claim-control checklist

Before adding or revising a manuscript claim, verify:

1. The claim names or implies a registered configuration.
2. The claim is supported by a registered table, figure, validation log, or evidence register.
3. The backend is manuscript-grade and fallback-free for the claim.
4. The baseline is named when using distance-to-baseline language.
5. External randomness-test claims are not made unless external rows are populated by a completed external run.
6. The wording does not imply cipher breaking, vulnerability discovery, exploit development, or security certification.

## Next table/figure work

- Keep hand-curated thesis tables under `manuscript/tables/`.
- Keep figure wrappers or figure inventory files under `manuscript/figures/`.
- Preserve generated figures under `results/figures/` and reference only figures that appear in an evidence register.
