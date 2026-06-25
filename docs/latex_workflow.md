# LaTeX Workflow

## Scope

This repository uses a modular LaTeX manuscript structure for thesis and article development. LaTeX work should be committed through Git and kept separate from generated data artifacts.

## Structure

- `manuscript/main.tex` is the root document.
- `manuscript/preamble/packages.tex` contains package imports and document-level settings.
- `manuscript/preamble/commands.tex` contains semantic commands for project objects.
- `manuscript/sections/*.tex` contains prose sections.
- `manuscript/references.bib` contains bibliography records.
- `manuscript/.latexmkrc` controls local build behavior.

## Object-oriented LaTeX conventions

Use semantic commands for repeated research objects. Do not repeatedly hard-code condition names, backend names, baseline names, or evidence-register paths inside prose when a command exists.

Examples of semantic objects:

- `\PrimaryBaseline`
- `\PrimaryBackend`
- `\LCGWeak`
- `\PeriodicWeak`
- `\BiasedWeak`
- `\BytePair`
- `\SlidingWindow`
- `\EvidenceSeedRobustness`

Use labels consistently:

- Sections: `sec:*`
- Subsections: `subsec:*`
- Tables: `tab:*`
- Figures: `fig:*`
- Appendix sections: `app:*`

## Build commands

From the repository root:

```bash
make manuscript
```

Or directly:

```bash
cd manuscript
latexmk -pdf main.tex
```

The local `.latexmkrc` writes auxiliary and PDF build outputs to `manuscript/build/`.

## Clean command

From the repository root:

```bash
make clean
```

Or directly:

```bash
cd manuscript
latexmk -C main.tex
rm -rf build
```

## Claim-control rule

Every substantive result claim in the manuscript must trace to a registered artifact in an evidence register. For the current thesis scope, use:

- `docs/evidence_register.md`
- `docs/evidence_register_weak_controls.md`
- `docs/evidence_register_weak_controls_seed_robustness.md`

Do not introduce empirical claims for Ascon, DES, TDEA, completed Dieharder comparisons, or cipher vulnerabilities unless a future registered evidence run supports them.
