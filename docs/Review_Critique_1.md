# DrugFork – Reviewer Critique & Revision Plan

Summary of the critique points from Reviewer 1 and Reviewer 2, along with the planned actions and responsibilities.

---

## Reviewer 1

| # | Critique point | Core statement | Planned action | Responsible |
|---|---|---|---|---|
| R1.1 | Unit of analysis / overcounting | Each regulatory decision is counted independently, including repeat approvals for the same product, potentially overestimating therapeutic activity | Sensitivity analysis with a deduplicated dataset (by non-proprietary name); clarify unit of analysis in Methods/Results | Hanna (analysis), Ben (text) |
| R1.2 | Residual differences between datasets | PAR vs. non-PAR datasets capture different regulatory activities, so differences may be an artifact of database structure | Remove aggregated number, clearly state the two analyses are not comparable (see R2.4) | Ben |
| R1.3 | Disease-burden interpretation oversimplified | Approval activity depends on many factors, not just disease burden | Add to limitations, account for time lag (see R1.5/R2.5) | Ben |
| R1.4 | Disease-classification uncertainty | Disease-classification accuracy is lower and more variable than overall extraction accuracy, affecting ICD-10 mapping | Add to limitations; qualitative error analysis (over-/underrepresentation); short explanation of lower F1 scores in Results | Ben (limitations/results), Hanna (error analysis) |
| R1.5 | Temporal lag between disease burden and approvals | Approvals often reflect scientific priorities set years earlier | Add to discussion (see R2.5) | Ben |

## Reviewer 2

| # | Critique point | Core statement | Planned action | Responsible |
|---|---|---|---|---|
| R2.1 | Dataset grossly incomplete (especially PMDA), validation cannot detect it | 408 PMDA approvals (2007-2025) contrast sharply with published figures (e.g. 400 NAS in 2008-2019 alone); likely only English-language review reports were captured; F1/accuracy only measures extraction from retrieved documents, not completeness | PMDA is dropped from the analysis (see below) | Hanna |
| R2.2 | Incompleteness not limited to PMDA (FDA: 0 vaccines) | Drugs@FDA only covers CDER, CBER biologics (incl. vaccines) are entirely missing | Add FDA/CBER data via the Purple Book | Hanna |
| R2.3 | Aggregate temporal trends are an artifact | Data capture starts in different years per agency (EMA 1995, PMDA 2007, TGA 2009, Swissmedic 2019), so the apparent rise reflects data entry, not increasing activity | Clarify in Results, Discussion and Abstract that the rise also reflects improved reporting | Ben |
| R2.4 | PAR and structured data are not comparable and must not be summed | The "31,964 approvals" headline and the 89% vs 56.5% small-molecule contrast are artifacts of generics | Abstract/Conclusions must not compare or combine the two analyses; remove the aggregate count | Ben |
| R2.5 | Disease-burden conclusion is unsupported | No association metric or test is presented, even though "not proportionally matched" is asserted; lag, saturation, and ICD coarseness are ignored | Explicitly state lag/caution, qualify the claim (not controllable) | Ben |
| R2.6 | Counting and duration analyses are flawed | Counting each decision independently inflates already-crowded areas; deduplication only applied to the pathway analysis | Still open / unresolved | open |
| R2.7 | Abridged/non-abridged not defined consistently across agencies | Review-duration comparison invalid: definition varies by agency, duration conditional on approval, FDA/Health Canada excluded | Add to limitations | Ben |
| R2.8 | Figures are unreadable | Figures 1 and 4 are stratified too finely, legends don't state the intended takeaway | More detailed captions with clear reading guidance; do not change the figures themselves | Jacqueline |

---

## Data incompleteness measures

### FDA / CBER (addresses R2.2)
- Source: Purple Book (purplebooksearch.fda.gov) - contains all FDA-licensed biologics including vaccines, cell & gene therapy, allergenic & hematologic products (CBER), plus CDER biologics.
- There is no separate full extract: each monthly file has the monthly changes (N/U/R) at the top and the complete database snapshot at the bottom.
- Approach: take a single, recent monthly file and use only the bottom section (empty first column = regular DB entries). Example Jan 2025 file: 66 change rows at the top, 2023 full rows at the bottom (1032 CDER + 991 CBER).
- Filter: approval date or date of first licensure ≥ 1995.
- Documents are used for everything except indication - this is stated as missing.

### PMDA (addresses R2.1 - not a real fix)
- The English review reports are, by design, a curated NAS subset - this explains the 408 figure and the gap to published numbers.
- A complete approval list exists ("List of Approval New Drugs 2004 to 2026", PMDA website) but is only available in Japanese.
- Decision: drop PMDA from the analysis, code, and figures; add a limitation sentence on potential data incompleteness instead.

---

## Who does what now

### Ben
- Qualitative text additions to Methods, Results, Discussion, Limitations, and Abstract:
  - Clarify unit of analysis + reference sensitivity analysis (R1.1)
  - Remove aggregated number, clearly separate PAR/non-PAR analyses (R1.2, R2.4)
  - Limitation on burden-of-disease interpretation and time lag (R1.3, R1.5, R2.5)
  - Limitation on disease-classification uncertainty + short explanation of lower F1 scores in Results (R1.4)
  - Clarify that temporal trends are partly an artifact of improved data capture, including in the Abstract (R2.3)
  - Limitation on inconsistent abridged/non-abridged definition (R2.7)

### Hanna
- Sensitivity analysis with deduplicated dataset (by INN) (R1.1)
- Qualitative error analysis of the model for disease classification - over-/underrepresentation (R1.4)
- Fully remove PMDA from text, code, and figures (R2.1)
- Add FDA/CBER data via the Purple Book (R2.2)

### Jacqueline
- Summarize the document and upload it to GitHub
- Write more detailed, clearer captions for Figures 1 and 4 (R2.8)
- Remaining organizational tasks

### Still open / unresolved
- R2.1 - how to handle the fundamental PMDA incompleteness beyond the limitation statement is not yet finally decided
- R2.6 - how to address the flawed counting and duration analyses (inconsistent deduplication) is still open
