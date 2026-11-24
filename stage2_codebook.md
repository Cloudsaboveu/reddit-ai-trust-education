# Stage 2 codebook — Trust in generative AI for education

## Dataset and screening
Source: Data 2.csv (Mendeley Reddit generative AI education dataset). Screening script: stage2_analysis.py. Preview review: stage2_finalize.py. Fixed random seed 20261123. One sampled comment per parent post per group.

## Eligibility
Include only comments substantively discussing perceived reliability, accuracy, authenticity, credibility, trustworthiness or checking of **generative AI outputs in learning, teaching or research**. Exclude references solely to trust in students, teachers, administrators, or AI detectors (unless the AI-generated output itself is evaluated); exclude irrelevant keyword matches. The preview-based decisions are provisional; read full text and parent-post context before finalising.

## Coding fields (apply to eligible comments only)
**Trust stance (one primary code):**
- T: Expresses confidence in GenAI output reliability or credibility, without meaningful qualification.
- D: Expresses distrust of GenAI output reliability or credibility.
- C: Conditional/mixed: expresses usefulness or trust only under verification, supervision, task limitations, or specific circumstances.
- U: Unclear/neutral: discusses credibility without discernible trust stance.

**Credibility themes (multiple codes allowed):**
- ACC: Accuracy or factual errors.
- HAL: Hallucinated/fabricated claims, citations or sources.
- VER: Verification, fact-checking, human oversight or source cross-checking.
- AUT: Authenticity, provenance or AI-generated disclosure.
- SRC: Source authority, attribution, evidence quality.
- BIA: Bias, misleading presentation or misinformation.
- OTH: Other credibility concern (specify).

**Context:** student-oriented vs educator-oriented subreddit label; does not establish actual commenter identity.

## Coding procedure
1. Read the complete comment and parent post where available.
2. Confirm inclusion/exclusion and record the reason.
3. Assign exactly one trust stance, allowing U for insufficient evidence.
4. Assign zero or more theme codes, with a short anonymised paraphrase justifying each.
5. Independently recode 15–20% of records after a delay; document disagreements and revise definitions.
6. Summarise frequencies with denominators and distinguish overlapping theme codes from mutually exclusive stance codes.

## Privacy and reproducibility
Do not publish original Reddit comment text or comment IDs without confirming permitted redistribution. Share scripts, codebook, aggregate counts and appropriately anonymised examples where authorised. Repository CC licence does not automatically clear Reddit third-party content.
