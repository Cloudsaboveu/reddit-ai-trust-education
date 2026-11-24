# Stage 2 — Provisional machine-assisted analysis (NOT final human-coded findings)

## Source and reproducibility
Source: uploaded `Data 2.csv`, parsed with `sep=';'`. Re-run `stage2_complete.py` with `Data 2.csv` and `stage2_selected_120_review.csv` in the same directory. Deterministic ranking uses SHA-256 of record ID prefixed with `20261123`. The screening script excludes `parents`, standardises `educator` to `educators`, and retains the original preview exclusions. The final output contains 60 comments from educator-oriented subreddits and 60 from student-oriented subreddits, from 120 distinct parent posts. Of these, 44 were in the earlier 120-comment pilot; 76 are replacement records.

## Screening
A comment is a candidate if an AI term occurs within a sentence adjacent to a credibility term and a stronger credibility expression also occurs in the same local window. This is a **rule-based relevance proxy**, not a completed human full-text assessment. Candidate counts: educator 198, student 111. The code prioritises earlier likely relevant previews and higher counts of strong signals. Thus it is **not a probability sample** and over-selects discussions of hallucinations and verification.

## Provisional coding
One stance label per comment: T trust, D distrust, C conditional/mixed, U unclear. Stance is assigned by regular-expression rules and has NOT been independently validated. In particular, words such as `but`, `helpful`, `wrong` and `hallucinate` may misclassify quoted, hypothetical, sarcastic or unrelated passages. Theme labels ACC, HAL, VER, AUT, SRC and BIA are keyword presence indicators, not interpretive manual thematic codes; they overlap. No inter-coder reliability has been assessed. Treat all charts as **exploratory provisional machine classifications**, not empirical evidence of actual attitude distributions.

## Data ethics
The private review CSV contains original Reddit text and IDs and must not be uploaded to a public repository without appropriate permissions. Aggregate counts and reproducible code are more appropriate for sharing, subject to institutional review. The repository licence does not automatically settle third-party rights.

## Required manual validation before poster submission
1. Read all 120 full comments and available parent posts; decide inclusion/exclusion against codebook and replace any ineligible records.
2. Correct all stance and theme labels and record concise anonymised evidence notes.
3. Independently recode at least 20–24 comments, compare decisions, and document any revisions.
4. Recalculate tables and charts from manually adjudicated labels; replace the provisional charts.
5. Avoid generalisation to Reddit users overall, real students/educators, or causal effects.
