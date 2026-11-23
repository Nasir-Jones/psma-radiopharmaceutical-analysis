# Suggested 3–4 minute demonstration

Adjust this outline to the professor's required length and rubric. Speak in your own words and identify Codex's role according to course rules.

1. **Question (about 25 seconds).** Introduce the two parts: published clinical outcomes and a separate numerical physics model. State the prostate-cancer population, rather than claiming all PSMA-expressing cancers are covered.
2. **Clinical data (about 45 seconds).** Show `data/clinical/vision_summary.csv` and its source notes. Explain what one row represents. Show the median comparison plot and explain the descriptive subtraction. Point out different analysis populations and confidence levels. Do not interpret median differences as individual benefit.
3. **Equations and code (about 60 seconds).** Open `src/simulation.py`. Explain physical decay and hypothetical biological removal, their additive rate constants, and the forward Euler update. Explain why the physical-only case retains activity longest.
4. **Run and results (about 45 seconds).** Run `.\.venv\Scripts\python.exe run_analysis.py`. Open the activity, cumulative activity, and convergence figures. Explain how smaller steps reduce error against an exact reference. Choose one scenario and read its actual error values from `convergence.csv` before recording.
5. **Validation and limitations (about 35 seconds).** Run `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`. Explain one meaningful test: half the activity remains after one physical half-life without biological removal. Mention that the simulation is not absorbed dose or clinical efficacy, and that clinical summary data cannot reproduce patient-level statistics.
6. **Reproducibility (about 20 seconds).** Show the public GitHub repository and commit history once published. Explain how the professor can install dependencies and regenerate the results. Close with what you learned about numerical error and scientific interpretation.

Before recording, rehearse the commands, open the generated figures, and be able to explain each line of the Euler loop without reading a script.
