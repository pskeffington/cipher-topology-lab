# Manuscript Scaffold Pass 2

## Purpose

This pass expands the thesis manuscript from a minimal article skeleton into a chapter-ready thesis scaffold. The emphasis is on object-oriented LaTeX structure, claim-control discipline, and evidence-traceable prose.

## Updated manuscript sections

- `manuscript/sections/abstract.tex`
  - Reframed the abstract around the full current evidence base.
  - Added the six-condition run, weak-control sensitivity extension, and alternate-seed robustness check.
  - Preserved the non-cryptanalytic claim boundary.

- `manuscript/sections/introduction.tex`
  - Added thesis subsections for motivation, research question, contributions, and scope/non-claims.
  - Positioned the work as computational diagnostics and reproducible evidence infrastructure.

- `manuscript/sections/background.tex`
  - Expanded background on AES-CTR output, reproducible baselines, OS CSPRNG sensitivity, weak controls, persistent homology, and evidence registration.
  - Added section labels for cross-reference hygiene.

- `manuscript/sections/related_work.tex`
  - Expanded related work around statistical randomness testing, persistent homology, positive-control discrimination, reproducibility, and diagnostic limits.
  - Added a gap statement for the thesis contribution.

- `manuscript/sections/replication_appendix.tex`
  - Added registered evidence files, full run commands, validation commands, artifact expectations, and claim traceability checklist.

## LaTeX practices reinforced

- Section and subsection labels are now present in the expanded sections.
- Manuscript claims are tied to registered configs, evidence registers, validation logs, and artifact scales.
- Non-claims are repeated where they matter: no cipher break, no vulnerability claim, no security certification, no completed external randomness claim without populated external results.

## Next scaffold pass

The next pass should focus on tables and figures:

1. Move key tables into separate LaTeX table modules under `manuscript/tables/`.
2. Add figure wrapper files under `manuscript/figures/` or a documented figure-input convention.
3. Add a manuscript evidence-to-section map showing which evidence register supports each result subsection.
4. Compile locally with `make manuscript` and fix any LaTeX errors.
