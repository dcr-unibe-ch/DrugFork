# analysis/1995/all_decisions/

Agency set: all agencies in `data/datasets/1995/<decision set>/Overall.csv` (EMA, Swissmedic, TGA, FDA, Health Canada). Decisions: all regulatory decisions (incl. refused/withdrawn).

**Created by:** `notebooks/analyze_output.ipynb` with `DATASET_FILTER = ""`, `DECISION_FILTER = "all_decisions"`.
**Input:** `data/datasets/1995/all_decisions/Overall.csv`, filtered to the agencies of this set.

Each plot exists per agency (`_EMA`, `_Swissmedic`, ...) and for all agencies together (`_Overall`).

| File pattern | Content |
|---|---|
| `timeline_Decision_year_<agency>.png`, `timeline_Application_year_<agency>.png` | Number of decisions per decision / application year |
| `decision_distribution_by_agency_combined.png` | Decision types by agency |
| `orphan_drug_status_distribution_combined.png`, `nonclinical_abridged_distribution_combined.png` | Orphan status; abridged nonclinical dossier, by agency |
| `disease_class_per_decision_year_absolute_<agency>.png`, `some_class_per_year_stacked_Decision_year_Disease_class(es)_<agency>.png` | Disease classes (ICD-11 chapters) per year |
| `drug_class_per_decision_year_absolute_<agency>.png`, `drug_class_per_year_stacked_Decision_year_<agency>.png` | Drug classes per year |
| `drug_class_distribution_pie_<agency>.png` | Share of drug classes |
| `drug_class_by_pharmaceutical_form_<agency>.png`, `pharmaceutical_form_per_year_Decision_date_<agency>.png` | Pharmaceutical forms |
| `administration_route_per_year_<agency>.png` | Administration routes per year |
| `marketing_holder_distribution_pie_<agency>.png`, `<agency>_marketing_authorisation_holders.txt` | Marketing authorisation holders (plot; list of unique holders) |
| `review_duration_by_agency_combined.png`, `review_duration_by_disease_class_<agency>[_abridged/_nonabridged].png`, `short_review_durations_analysis.txt` | Review duration (application → decision) |
| `panel_*.png` | Multi-panel versions of the plots above (all agencies side by side) |
| `*_legend.png`, `*_legend_.png`, `*_legend__pars.png` | Same plot with legend, from different notebook runs |
| `burden/` | Approvals per disease class vs. global deaths, incidence and prevalence |
