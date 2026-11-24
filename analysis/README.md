# analysis/

Figures and summary tables produced by the analysis notebooks. **Nothing in this folder is edited by hand**


## Structure

```
analysis/<agency set>/<decision set>/[burden|overlap/<name column>]
```

| Level | Values | Meaning |
|---|---|---|
| agency set | `1995` | All agencies in the input file |
| | `1995_pars` | PAR agencies only (EMA, Swissmedic, TGA, PMDA) |
| | `1995_nonpars` | FDA and Health Canada only (not used in final analysis) |
| decision set | `all_decisions`, `approved` | Input `data/datasets/1995/<decision set>/Overall.csv` |
| | `burden/` | Approvals vs. global disease burden |
| | `overlap/Drug_name`, `overlap/Non_proprietary_name` | Overlap of drugs between agencies, matched by brand name or INN |

## How to regenerate

| Output | Notebook | Settings at top of notebook |
|---|---|---|
| `<set>/<decision>/*.png, *.txt` and `burden/` | `notebooks/analyze_output.ipynb` | `DECISION_FILTER` = `"approved"` / `"all_decisions"`; `DATASET_FILTER` = `""` / `"_pars"` / `"_nonpars"` |
| `<set>/<decision>/overlap/<col>/` | `notebooks/analyze_overall.ipynb` | `DECISION_FILTER`, `DATASET_FILTER`, `DRUG_COL` = `"Drug_name"` / `"Non_proprietary_name"` |

Before the burden plots: `python src/burden_mapping/preprocess_burden_data.py`.
Plot functions live in `src/analysis/analysis_utils.py`.

## Relation to the manuscript

Numbers in the Results section, Table 2 and Suppl. Figure 1 are computed in
`notebooks/paper_writing_jd.ipynb` from `data/datasets/manually_cleaned/*_manually_cleaned.csv`.
All figures below are created by `notebooks/analyze_output.ipynb` with
`DATASET_FILTER = "_pars"` (EMA, Swissmedic, TGA, PMDA) and `DECISION_FILTER = "approved"`,
unless stated otherwise.

| Manuscript | Content | File |
|---|---|---|
| Figure 1 | LLM extraction pipeline (schematic, drawn manually) | Not on GitHub |
| Figure 2 | Annual approvals by disease class per agency: counts (top), % (bottom) | `1995_pars/approved/disease_class_per_decision_year_absolute_<agency>.png` (top), `1995_pars/approved/panel_some_class_per_year_stacked_Decision_year_Disease_class(es).png` (bottom) |
| Figure 3 | Drug classes: % over time (top), proportions per agency (bottom) | `1995_pars/approved/panel_some_class_per_year_stacked_Decision_year_Drug_class.png` (top), `1995_pars/approved/panel_drug_class_distribution_pie.png` (bottom) |
| Figure 4A | Review duration by agency, abridged vs non-abridged | `1995_pars/approved/review_duration_by_agency_combined.png` |
| Figure 4B | Review duration by disease class, all PAR agencies | `1995_pars/approved/review_duration_by_disease_class_Overall.png` |
| Table 1 / Suppl. Table 2 | Extraction performance | `evaluation/processed_files/` |
| Table 2 | Key characteristics per agency | `paper_writing_jd.ipynb`, sections 3.2.1–3.2.3 |
| Suppl. Table 1 | Extraction attributes | written manually |
| Suppl. Figure 1 | Flow chart of dataset creation (numbers from `paper_writing_jd.ipynb`, section 3.2.1; drawn manually) | Not on GitHub |
| Suppl. Figure 2 | Administration routes per year | `1995_pars/approved/panel_some_class_per_year_stacked_Decision_year_Administration_route.png` |
| Suppl. Figure 3 | Pharmaceutical forms per year | `1995_pars/approved/panel_some_class_per_year_stacked_Decision_year_Pharmaceutical_form.png` |
| Suppl. Figure 4 | Top 20 marketing authorisation holders | `1995_pars/approved/marketing_holder_distribution_pie_Overall.png` |