# Clinical input provenance

Manually curated aggregate statistics, checked November 23, 2026. Four rows represent endpoint/arm summaries, not four patients. No individual data or survival curves were generated.

Primary study: Sartor O et al. (2021), *Lutetium-177–PSMA-617 for Metastatic Castration-Resistant Prostate Cancer*, NEJM 385:1091–1103, [doi:10.1056/NEJMoa2107322](https://doi.org/10.1056/NEJMoa2107322). [PubMed abstract and figure captions](https://pubmed.ncbi.nlm.nih.gov/34161051/), [author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC8446332/).

- Abstract Results: endpoint medians and published hazard ratios with their confidence intervals.
- Figure 2A: imaging-based progression-free survival (imaging-documented progression or death), analyzed in the post-March-5-2019 randomized population. Figure 2B: overall survival in all randomized patients. The former restriction followed measures addressing early control-arm withdrawal; endpoint populations must not be pooled.
- Median confidence intervals: [EMA Pluvicto public assessment report](https://www.ema.europa.eu/en/documents/assessment-report/pluvicto-epar-public-assessment-report_en.pdf), section 3.2, printed page 113. This regulatory report reproduces the VISION results. Median intervals are not standard deviations or intervals for the difference between medians.
- Arm sizes and median intervals are also reproduced in the sponsor's [Pluvicto prescribing information](https://www.novartis.com/sg-en/sites/novartis_sg/files/Pluvicto-Sep2025.SIN-app261225-pdf.pdf), Table 12-1, VISION rows. Do not substitute results from other trials in that document.

Access note: the original abstract and figure captions were accessible; subsequent full-text requests encountered a browser check. Median interval values were cross-checked in the indexed EMA report and sponsor prescribing information rather than inferred from a graph.

`treatment` means Lu-177-PSMA-617 plus protocol-permitted standard care; `control` means protocol-permitted standard care alone. The study involved previously treated, PSMA-positive metastatic castration-resistant prostate cancer. It does not represent every cancer expressing PSMA. Standard care excluded some anticancer therapies; see original Methods.

`n` is the endpoint analysis population per arm, not the number of deaths or an uncensored sample size. `median_months`, `ci_low_months`, and `ci_high_months` are published survival estimates in months. `ci_level_percent` is 95 for overall survival and 99.2 for imaging-PFS; the same endpoint-specific levels apply to the published hazard-ratio intervals. Hazard-ratio fields are repeated for both arms to retain comparison context and must not be counted as two estimates.

The analysis calculates descriptive median differences only. It neither estimates individual benefit nor reproduces the trial's significance tests. It does not analyze safety, quality of life, or a full benefit-risk profile.

Simulation reference: [MIRDspecs Lu-177 data sheet](https://mirdsoft.org/products/MIRDspecs/MIRDspecs_HTMLs/Lu-177.htm), Summary data / Radioactive decay: physical half-life 6.647 days. Biological half-lives in this project are hypothetical, not extracted from VISION. The simulation is independent of the trial analysis.
