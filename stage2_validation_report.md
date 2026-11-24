# Stage 2 research dataset: working analysis and validation status

## Source and purpose
Input: `Data 2.csv`, previously selected 120-comment file, and `stage2_fulltext_audit_PRIVATE.csv`. Topic: expressed credibility and trust in generative AI in education, comparing student-oriented and educator-oriented Reddit communities.

## Sampling and processing
- Source contains 8,346 comment records (and 984 posts).
- Previous sample comprised 60 comments per group from distinct parent posts.
- Previous AI-assisted qualitative audit labelled 13 comments eligible and seven ineligible; 100 had not received qualitative adjudication.
- Retained 113 earlier records and substituted seven candidate comments from the source dataset, applying documented AI/credibility term filters, excluding previous records and parent posts, and deterministic sorting (SHA-256 seeded with `20261123`). A weaker keyword fallback was allowed if the stronger rule yielded too few distinct parent posts.
- Working file has 120 records, 60 per group and 120 distinct parent posts.

## Coding
One provisional stance per comment: T trust, D distrust, C conditional/mixed, U unclear. Multiple possible credibility themes: ACC accuracy, HAL hallucination/fabrication, VER verification, AUT authenticity/disclosure, SRC sources/evidence, BIA bias/misinformation. The 13 previously AI-reviewed records retain their interpreted codes; other records receive automated keyword/rule classifications. These rules are not equivalent to a human qualitative analysis; they may misread negation, quotations, sarcasm, AI-detector discussions, and conditional language.

## Provisional counts
| Stance | Educator-oriented (n=60) | Student-oriented (n=60) |
|---|---:|---:|
| T | 0 | 0 |
| D | 24 | 17 |
| C | 33 | 43 |
| U | 3 | 0 |

| Theme | Educator-oriented | Student-oriented |
|---|---:|---:|
| ACC | 19 | 21 |
| HAL | 35 | 31 |
| VER | 21 | 23 |
| AUT | 9 | 3 |
| SRC | 24 | 20 |
| BIA | 2 | 1 |

## Essential limitations and outstanding checks
1. Only 13 comments have an AI-assisted individual interpretive review from the earlier audit. The other 107 records remain unverified rule-based candidates; none has independent human validation. Thus the working sample is **not** a confirmed sample of 120 eligible comments.
2. Theme and stance counts are actual computational outputs, **not validated qualitative findings**. Do not present these percentages as measured Reddit attitudes without human checking and correction.
3. Candidate selection intentionally enriches for credibility terminology; it is not representative of all Reddit comments or users.
4. Subreddit stakeholder labels indicate community orientation, not the identity of each author.
5. One comment per parent post reduces within-thread concentration but does not eliminate community-level selection bias.
6. A single AI-assisted coder cannot establish inter-coder reliability. A second independent coder or a documented human recoding pass is required to assess coding consistency.
7. Data access does not establish permission to redistribute raw Reddit text or identifiers. Keep the private working CSV private and share only permissible code, methodology and aggregate counts.

## Before poster submission
Manually inspect full text and available parent-post context for each of 107 unverified records; replace further exclusions; correct stance/theme codes with reasons; document the final denominator; recode a subset independently and report disagreements; regenerate figures from validated data. Until then, charts must be marked **PROVISIONAL AI-ASSISTED**.
