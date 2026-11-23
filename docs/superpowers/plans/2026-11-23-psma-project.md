# PSMA Project Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task by task. Execute inline to respect the student's usage-efficiency preference.

**Goal:** Deliver reproducible clinical summary analysis and a separately labeled discrete decay simulation.

**Architecture:** Two small Python modules expose clinical summarization and numerical simulation. A single entry point writes CSV tables and static figures offline from curated inputs.

**Tech Stack:** Python 3.13, NumPy, pandas, Matplotlib, standard-library unittest.

**Spec:** `docs/superpowers/specs/2026-11-23-psma-project-design.md` (approved).

## Global Constraints
- Favor Python scripts and a small dependency set.
- Separate real clinical summaries from simulated data.
- Cite clinical values, populations, endpoint definitions, units, and extraction locations.
- Use hypothetical clearance half-lives of 1, 3, and 7 days and no clearance; physical half-life 6.647 days from MIRDspecs.
- Simulate 30 days at steps of 1, 0.5, and 0.1 day. Compare Euler and trapezoidal results with analytical references.
- No patient data, clinical predictions, or absorbed-dose claims.
- Commit verified milestones; push only after the public remote is configured and authenticated.

## Review Focus
- Missing, duplicate, or malformed clinical rows must produce a clear error.
- Endpoint populations must remain separate and match the source.
- Nonfinite or nonpositive parameters must be rejected.
- Euler steps that violate positivity must be rejected.
- A final partial time step must reach the requested end time without overshooting.

### Task 1: Clinical data and analysis
**Files:** `data/clinical/vision_summary.csv`, `data/clinical/SOURCES.md`, `src/clinical.py`, `tests/test_clinical.py`, `.gitignore`, `requirements.txt`.

**Interfaces:** `load_clinical(path: Path) -> DataFrame`; `summarize_clinical(data: DataFrame) -> DataFrame`. Rows identify endpoint, arm, n, median and interval months, confidence level, source and population. Summary emits treatment/control medians and their descriptive difference.

- [x] Verify original source values, sample sizes, interval levels and extraction locations.
- [x] Write tests for expected differences (4.0 and 5.3 months), populations, missing/duplicate arms, invalid medians, and mismatched metadata; run and observe import failure before code exists.
- [x] Implement input validation and descriptive summary; add dependency configuration.
- [x] Install/locate Python and create an ignored virtual environment. Run clinical tests and commit when green.

### Task 2: Numerical model
**Files:** `src/simulation.py`, `tests/test_simulation.py`.

**Interfaces:** `simulate(biological_half_life_days: float | None, step_days: float, duration_days: float = 30) -> tuple[DataFrame, dict]`. Return sampled analytical and Euler activity plus integral and error statistics.

- [x] Write tests for physical half-life, accelerated clearance, analytical integral, Euler and trapezoidal convergence, finite positive inputs, positivity bound, and a partial final step. Run and observe import failure.
- [x] Implement rates, grid, Euler recurrence, trapezoidal integration and analytical references. Keep units explicit.
- [x] Run numerical and clinical tests, then commit.

### Task 3: Reproducible report and student handoff
**Files:** `run_analysis.py`, `tests/test_outputs.py`, `README.md`, `docs/video-outline.md`, `results/clinical/*`, `results/simulated/*`.

**Interfaces:** `run(output_dir: Path) -> None`, callable from CLI with optional `--output-dir`. Use paths relative to the script, not caller's working directory.

- [x] Write an integration test requiring four clinical input rows, two clinical summary rows, 12 simulation scenarios, 1,572 time-series rows, and four PNG figures; observe missing entry point failure.
- [x] Implement the entry point and legible plots. Export hazard ratios as published context, not fitted statistics. Pin tested dependency versions.
- [x] Run all tests and entry point; inspect all four figures. Check generated CSVs and offline execution from a different working directory.
- [x] Write setup/run instructions, equations, limitations, GitHub sign-in steps and a short video outline. Document actual software versions and numerical results.
- [x] Review diff and staged files, commit the completed reproducible deliverable, and report any remaining account/authentication blocker.

## Execution record
Approved design; implementing inline in the user's project folder on a dedicated `codex/psma-analysis` branch. No linked worktree is needed for this empty repository. No baseline code or tests exist. GitHub authentication remains user-owned.
