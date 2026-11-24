# Trust in Generative AI for Education — MSc research

**Status: PROVISIONAL AI-ASSISTED WORKING RESULTS. NOT INDEPENDENTLY VALIDATED.**

Exploratory comparison of student-oriented and educator-oriented Reddit discussions on the credibility of generative AI for education. Subreddit category is **not** a verified author occupation.

## Data provenance
Kumarage, P.M., Gunasekara, S. and Saarela, M. (2026), *Reddit discussions on generative AI in education dataset*, v3, Mendeley Data. https://doi.org/10.17632/z6794ft3fs.3

The source file `Data 2.csv` is **not included**. Obtain it separately from the source repository, subject to the applicable terms. The analysis uses semicolon-separated input. No original Reddit text or record IDs are distributed in this repository.

## Contents
- `scripts/`: the five **original Stage 2 scripts**, preserved for audit. These are **historical research scripts**, not a polished single-command pipeline. They use absolute `/mnt/data/` paths and some depend on **private intermediate CSVs not distributed here**. They cannot be run end-to-end from this public package alone. Do not claim otherwise.
- `scripts/plot_aggregate_results.py`: portable script to regenerate provisional charts **from the two public aggregate CSVs**. No private input needed.
- `documentation/stage2_codebook.md`: relevance rules and code definitions.
- `documentation/stage2_methodology_and_limitations.md`: screening, sampling and methodological caveats.
- `documentation/stage2_validation_report.md`: audit trail, figures and outstanding verification.
- `results/`: group-level provisional stance and theme counts (no individual records).
- `figures/`: provisional charts.

## Recreate the aggregate figures

```bash
python -m pip install -r requirements.txt
python scripts/plot_aggregate_results.py
```

This regenerates the figures from **already-calculated aggregate counts**. It does not independently validate the underlying comment classifications.

## Provisional aggregate results

Trust stance, educator-oriented / student-oriented: T 0/0, D 24/17, C 33/43, U 3/0 (n=60 per group).

Credibility theme, educator-oriented / student-oriented: ACC 19/21, HAL 35/31, VER 21/23, AUT 9/3, SRC 24/20, BIA 2/1. Theme codes overlap.

## Validation and ethical constraints
Only 13 records were individually reviewed by an AI assistant; 107 remain rule-coded candidates. None has independent human validation. These are **not representative estimates** of student or educator trust. Do not publish the private CSVs or raw Reddit quotations without checking permissions and research ethics. A human researcher must verify eligibility, stance and themes and regenerate aggregate results before reporting validated findings.

## Poster
An editable A1 PowerPoint poster was produced separately. Add the verified repository URL to its ethics/reproducibility section. Keep the **PROVISIONAL** label until validation is completed.
