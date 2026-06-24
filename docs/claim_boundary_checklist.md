# Claim Boundary Checklist

Author: Paul Skeffington, MS, MPH  
GitHub: `@pskeffington-github`  
Public contact: `paulskeffington@gmail.com`  
Repository: `pskeffington/cipher-topology-lab`  
Status: draft v1  
Milestone: M2 Validation

## Purpose

This document defines a reusable claim-boundary checklist for technical evaluation work. It supports reproducibility, benchmark discipline, evaluation readiness, and responsible communication by separating supported claims from unsupported claims before release.

The checklist is designed for the evaluation-science lane but can be reused across health security, trusted AI, resilient sensing, and infrastructure-resilience repositories.

## Operating Question

```text
What was tested, what evidence supports the result, and what claims remain outside the validated boundary?
```

## Claim Boundary Object Model

```yaml
claim_boundary:
  boundary_id: string
  repository: string
  artifact_id: string
  evaluation_context_id: string
  supported_claims:
    - string
  unsupported_claims:
    - string
  required_evidence:
    - string
  validation_status: string
  reviewer_required: boolean
  release_status: string
  boundary_notes:
    - string
```

## Minimum Review Checklist

| Check ID | Review Question | Required Evidence | Failure Mode | Status |
|---|---|---|---|---|
| cb_001 | Is the artifact under review identified? | file path, version, commit, or issue reference | Claims cannot be tied to an artifact. | required |
| cb_002 | Is the evaluation context defined? | experiment context or readiness report | Results are detached from setup. | required |
| cb_003 | Are inputs documented? | source, dataset, fixture, or input object | Unclear what was evaluated. | required |
| cb_004 | Are configurations documented? | configuration object or parameter notes | Results cannot be reproduced. | required |
| cb_005 | Are metrics or review criteria defined? | metric set, checklist, or rubric | Claims lack evaluation basis. | required |
| cb_006 | Are supported claims listed? | supported claim list | Evidence contribution is unclear. | required |
| cb_007 | Are unsupported claims listed? | unsupported claim list | Overclaiming risk increases. | required |
| cb_008 | Are limitations explicit? | limitations section | Readers may generalize beyond evidence. | required |
| cb_009 | Is ML readiness bounded? | readiness value and prerequisites | Premature ML claims. | required when ML is discussed |
| cb_010 | Is public-safety boundary explicit? | safety boundary section | Sensitive or inappropriate content may be exposed. | required |
| cb_011 | Are reviewer actions needed? | reviewer flag or release decision | Release accountability is weak. | required |
| cb_012 | Is release status defined? | draft, reviewed, validated, released | Ambiguous artifact maturity. | required |

## Supported Claim Template

Supported claims should be narrow and traceable.

```yaml
supported_claim:
  claim_id: "claim_0001"
  claim_text: "This repository defines an evaluation-readiness framework for claim-bounded technical review."
  evidence_refs:
    - "docs/evaluation_readiness_report.md"
  validation_status: "reviewed"
  limitation_note: "This does not establish production readiness or validated method superiority."
```

## Unsupported Claim Template

Unsupported claims should name what the artifact does not prove.

```yaml
unsupported_claim:
  claim_id: "unsupported_0001"
  claim_text: "This artifact does not prove production readiness, operational effectiveness, or generalizability beyond documented examples."
  reason: "No production deployment, independent validation, or generalization testing has been completed."
  reviewer_required: false
```

## Overclaim Flags

Use these flags when reviewing proof packets, reports, or README language.

```text
production_ready_claim_without_validation
superiority_claim_without_baseline
clinical_claim_without_clinical_validation
security_claim_without_independent_review
operational_claim_without_operational_test
model_performance_claim_without_metrics
generalization_claim_without_external_validation
real_time_claim_without_timing_evidence
automation_claim_without_human_review_boundary
compliance_claim_without_framework_mapping
```

## Release Readiness Values

```text
draft
review_required
reviewed
validated
released
blocked
```

## Validation Status Values

```text
draft
reviewed
validated
failed
deprecated
released
```

## Claim Boundary Review Procedure

1. Identify the artifact under review.
2. Identify the evaluation context.
3. List source inputs and configurations.
4. List metrics, rubric, or review criteria.
5. Draft supported claims.
6. Draft unsupported claims.
7. Add limitations and uncertainty notes.
8. Apply overclaim flags.
9. Check public-safety boundary.
10. Assign release status.

## Minimum Claim Boundary Section

Every proof packet or evaluation report should include:

```markdown
## Supported Claims

## Unsupported Claims

## Limitations

## Public-Safety Boundary

## Release Status
```

## Cross-Repository Use

| Repository | Checklist Use |
|---|---|
| `pskeffington/Portfolio` | Review portfolio proof packets and role-alignment claims. |
| `pskeffington/CDC-mod` | Bound health-security modernization and AI-readiness claims. |
| `pskeffington/authentication-audit-compiler` | Review audit-schema release packets and validation claims. |
| `pskeffington/ECG-denoising` | Bound benchmark, morphology-preservation, and clinical-adjacent claims. |
| `pskeffington/McDowell-County-Commission-on-Aging-Inc.` | Bound infrastructure-resilience and risk-feature claims. |

## Future M3 Outputs

Expected downstream artifacts:

```text
outputs/experiment_registry.csv
outputs/baseline_comparison_table.csv
outputs/evaluation_quality_report.md
```

## ML Readiness Path

Current status:

```text
validation_candidate
```

Candidate future ML tasks:

```text
claim-boundary completeness scoring
overclaim-risk triage
evaluation-quality clustering
release-readiness classification
```

Minimum readiness requirements:

- claim-boundary examples
- reviewed supported and unsupported claim pairs
- overclaim flag labels
- release status labels
- reviewer notes
- validation report examples

## Public-Safety Boundary

This checklist must not include operational exploitation details, credentials, secrets, private workflows, live target data, evasion instructions, or claims of operational capability.

The checklist supports responsible evaluation communication, not operational deployment or sensitive technical use.

## Claim Boundary

This document supports evaluation discipline, release review, and overclaim prevention. It does not establish production readiness, operational security, comparative method superiority, compliance status, clinical validity, or generalizability beyond documented artifacts.
