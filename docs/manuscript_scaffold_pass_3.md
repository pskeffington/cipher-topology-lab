# Manuscript Scaffold Pass 3

## Purpose

This pass begins converting the thesis manuscript from section-level scaffolding into object-oriented manuscript components for tables, figures, and evidence mapping.

## Changes

- Added `manuscript/tables/primary_lcg_effects.tex`.
- Added `manuscript/tables/seed_robustness_effects.tex`.
- Updated `manuscript/sections/results.tex` to load result tables with `\input{}` rather than embedding table bodies directly in the section prose.
- Added `manuscript/figures/figure_inventory.tex` as a figure-family scaffold.
- Added `docs/manuscript_evidence_map.md` to map manuscript sections to registered evidence sources.

## Rationale

The manuscript should treat tables and figures as first-class objects rather than inline prose fragments. This improves maintainability and reduces the risk that results prose drifts away from the registered evidence base.

## Next pass

1. Compile locally with `make manuscript`.
2. Fix any LaTeX path or package errors.
3. Add final figure wrappers only for figures registered in an evidence register.
4. Add a local manuscript checklist for final thesis submission.
