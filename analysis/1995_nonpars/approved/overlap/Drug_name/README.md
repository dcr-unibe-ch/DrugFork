# analysis/1995_nonpars/approved/overlap/Drug_name/

Drugs matched across agencies by `Drug_name`. Created by `notebooks/analyze_overall.ipynb` (`DRUG_COL = "Drug_name"`).

| File | Content | Notebook section |
|---|---|---|
| `Drug_name_agency_distribution.png` | Number of agencies per drug | top |
| `Drug_name_normalized_heatmap.png` | Pairwise overlap between agencies (normalised) | top |
| `top_15_duplicated_drugs_by_Drug_name.csv` | Rows of the drugs that appear most often | "Analyse duplicates" |
| `analysis.txt` | Summary of drugs shared between agencies | "Analyse duplicates" |
| `overall_deduplicated.csv` | Dataset with one row per drug–agency pair (earliest approval kept) | "Create Deduplicated Dataset" |
| `dataset_statistics.txt` | Counts for the deduplicated dataset | end |
| `approval_trajectories.csv`, `approval_trajectories_top10.png` | Most frequent orders in which agencies approved the same drug | "Approval Trajectories" |
| `approval_trajectories_min<k>_agencies_top20.csv`, `approval_trajectories_by_min_agencies.txt` | Same, for drugs approved by at least k agencies | "Approval Trajectories" |
| `approval_lags_detailed.csv`, `approval_lags_analysis.txt`, `approval_lags_heatmap.png` | Time between approvals of the same drug by different agencies | "Approval Trajectories" |
| `sankey_approval_flow_multilevel.html/.png` | Sankey diagram of approval order | end |