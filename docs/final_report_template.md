# Cipher Topology Diagnostic Platform — Final Pilot Report Template

## 1. Executive summary

**Pilot question:** `[state the bounded diagnostic question]`

**Scope:** `[state configs, conditions, baselines, and exclusions]`

**Primary conclusion:** `[state what the evidence supports, including uncertainty or null findings]`

**Claim boundary:** This report is diagnostic and reproducibility-focused. It does not provide production security certification, vulnerability disclosure, proof of randomness, or unsupported comparator claims.

## 2. Pilot scope lock

| Field | Value |
|---|---|
| Pilot owner | `[name/team]` |
| Repository | `pskeffington/cipher-topology-lab` |
| Config path | `[config]` |
| Run profile | `[demo/full/custom]` |
| Conditions | `[conditions]` |
| Baseline | `[baseline]` |
| External randomness path | `[completed/unavailable/deferred]` |
| Claim-boundary status | `[passed/needs revision]` |

## 3. Methods summary

Describe the workflow stages used in the pilot:

1. Generated or selected byte-stream inputs.
2. Converted streams into configured representations.
3. Computed topological summaries.
4. Ran internal diagnostics and baseline-distance summaries.
5. Ran validation, coherence, and consistency checks.
6. Built evidence register and platform report.
7. Applied claim-boundary validation.

## 4. Artifact inventory

| Artifact family | Path | Status | Notes |
|---|---|---|---|
| Config | `[path]` | `[present/missing]` | `[notes]` |
| Generated streams | `[path]` | `[present/missing]` | `[notes]` |
| Embeddings | `[path]` | `[present/missing]` | `[notes]` |
| TDA features | `[path]` | `[present/missing]` | `[notes]` |
| Internal diagnostics | `[path]` | `[present/missing]` | `[notes]` |
| Effect-size tables | `[path]` | `[present/missing]` | `[notes]` |
| Evidence register | `[path]` | `[present/missing]` | `[notes]` |
| Platform report | `results/platform/platform_report.md` | `[present/missing]` | `[notes]` |
| Claim-boundary report | `results/logs/claim_boundary_report.md` | `[present/missing]` | `[notes]` |

## 5. Evidence summary

Summarize the observed evidence without overstating the result.

Recommended wording pattern:

> Under the configured diagnostic workflow, `[condition/control]` showed `[pattern]` relative to `[baseline]` under `[summary/embedding]`. `[other conditions]` did/did not show comparable broad top-ranked separation. This is diagnostic evidence under the registered workflow, not a production security claim.

## 6. External dependency status

| Dependency | Status | Interpretation |
|---|---|---|
| TDA backend | `[available/fallback/unavailable]` | `[impact]` |
| LaTeX | `[available/unavailable]` | `[impact]` |
| External randomness battery | `[completed/unavailable/deferred]` | `[impact]` |

Clearly distinguish unavailable tooling from failed analysis.

## 7. Limitations

List known limitations:

- `[limitation]`
- `[limitation]`
- `[limitation]`

Required limitations language:

- The result is not cryptanalysis.
- The result is not a security certification.
- The result does not prove randomness.
- Comparator claims are limited to implemented and registered configurations.

## 8. Claim-boundary check

| Check | Result |
|---|---|
| Public/reviewer docs scanned | `[yes/no]` |
| Prohibited unbounded claims detected | `[count]` |
| Report path | `results/logs/claim_boundary_report.md` |
| Remediation needed | `[yes/no]` |

## 9. Pilot decision

Choose one:

- **Proceed:** evidence package is sufficient for next pilot/reporting stage.
- **Repeat:** rerun with modified configuration or stronger validation.
- **Expand:** run seed sweep, replicate-scale check, embedding sensitivity, or external comparison.
- **Defer:** preserve as future work.

Decision: `[proceed/repeat/expand/defer]`

Rationale: `[bounded rationale]`

## 10. Next action

| Priority | Action | Owner | Output |
|---:|---|---|---|
| 1 | `[action]` | `[owner]` | `[output]` |
| 2 | `[action]` | `[owner]` | `[output]` |
| 3 | `[action]` | `[owner]` | `[output]` |
