# PSMA clinical outcomes and radioactive decay: project design

## Intent
Create a reproducible undergraduate computational methods project in Python, suitable for a public GitHub repository and a short demonstration video. Combine real published treatment outcome summaries with a separate physics simulation that produces discrete numerical data. The user chose the combined approach on November 23, 2026.

## Approaches considered
1. Clinical summaries alone: direct connection to reported efficacy, but limited numerical physics.
2. Decay simulation alone: clear numerical methods, but no measured treatment outcomes.
3. Combined approach (selected): analyze published clinical summaries and separately simulate decay and clearance. This covers the student's clinical interest and computational methods requirement without treating a model as clinical evidence.

## Scope and proposed implementation choices
Use Python scripts with NumPy, pandas, and Matplotlib; no website or notebook is required. These library and interface choices are the assistant's proposal. Finish a small working core before considering optional additions.

### Published clinical data
Use the original VISION trial publication and its publicly accessible supporting material as the primary clinical source:
https://doi.org/10.1056/NEJMoa2107322

Verify every number against the source before inclusion. Store a small manually curated CSV of published aggregate results: group sizes and reported median overall survival and imaging-based progression-free survival, with confidence intervals where explicitly reported. Preserve endpoint-specific analysis populations; do not assume every endpoint uses the full randomized sample. Record treatment arms, units, population restrictions, source URL, and extraction location. Reported hazard ratios and their confidence intervals may be included as source results, not recalculated from medians.

Calculate absolute differences between reported medians and optionally ratios with explicit labels. Generate a comparison figure and a summary table. Differences of medians are descriptive comparisons, not estimates of individual life extension. Do not pool incompatible endpoints, infer significance from plotted medians, construct patient records, or fit survival models without patient-level data. Do not imply the findings cover all PSMA-expressing cancers.

If a desired endpoint or confidence interval cannot be verified from accessible original material, omit it and explain the omission; do not estimate it.

### Discrete physics simulation
Model a hypothetical retained activity after a single administration:

A(t) = A0 exp[-(lambda_physical + lambda_biological)t]

lambda = ln(2) / half_life

Use days throughout time calculations. Source and cite the lutetium-177 physical half-life before coding its value. Use normalized initial activity A0 = 1 (fraction of initial activity), and explicitly hypothetical biological clearance half-lives (proposed scenarios: 1, 3, and 7 days, plus no biological clearance). No patient calibration is claimed. Biological removal leaves the modeled compartment; it does not mean the radionuclide ceases to decay elsewhere.

Sample the analytical curve at discrete times and also solve dA/dt = -lambda_effective A using forward Euler. Proposed duration is 30 days. Compare step sizes such as 1, 0.5, and 0.1 day. Check Euler's stability and positivity for the selected rates; reject invalid parameter combinations instead of silently producing unphysical curves.

Compute cumulative activity with the trapezoidal rule and compare against the finite-window analytical integral A0(1-exp(-lambda_effective T))/lambda_effective. Report absolute errors and relative errors where defined. The normalized integral has units of days; it is neither absorbed dose nor clinical efficacy. Physical-only activity serves as an upper-retention reference under this model.

### Outputs and organization
- `data/clinical/`: curated aggregate CSV and source notes.
- `src/`: readable analysis and simulation scripts with a simple documented entry point.
- `results/clinical/`: clinical comparison table and figure.
- `results/simulated/`: time-series CSV, integration/convergence table, and labeled figures.
- `README.md`: setup, commands, research question, methods, sources, results, and limitations.
- `requirements.txt`, `.gitignore`, and focused numerical/data validation checks.
- A short video outline explaining the question, data, equations, demonstration, numerical error, and limitations.

Keep raw clinical inputs separate from generated results. Running the entry point should recreate all outputs without downloading patient data or requiring network access.

## Validation and acceptance
- Clinical input values and endpoint populations match verified source locations.
- Units and treatment groups are explicit.
- A(0) = 1, activities are nonnegative and nonincreasing, and removal accelerates the modeled decline.
- Numerical results agree with analytical references to documented tolerances and improve as time steps shrink.
- CSV and figure labels consistently distinguish simulation from clinical evidence.
- A fresh environment can install documented dependencies and reproduce outputs with one command.
- The student can explain the model, numerical method, and limitations in a short video.

## Setup and delivery
Git is installed and the project folder is already an empty repository. A Git identity is configured. Python is not currently available through the `python` command; check other installation locations before installing it. Check for VS Code before installing it. GitHub account creation and authentication require the user; never request their password. Connect the intended public remote, then commit and push meaningful verified milestones. Review files before public publication.

## Constraints and non-goals
Roughly a week and a half until submission; about $100 of stated usage credits, with no assumed access to the live balance. Favor concise collaboration and a small dependency set. No clinical recommendations, patient-specific predictions, efficacy fitting, multi-isotope comparison, interactive dashboard, or private health data are included.

## Builder discretion and remaining input
The builder may choose filenames, plot styling, concrete tolerances, and the simplest test/command structure consistent with this design. Exact deadline, rubric, and video duration can be incorporated if supplied; progress need not wait for them. User approval of this design is required before project implementation by the brainstorming workflow.
