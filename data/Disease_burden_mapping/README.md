# data/Disease_burden_mapping/

Global disease burden data and the mapping of disease names to disease classes, used for the
"approvals vs. disease burden" figures (`../../analysis/*/burden/`).

## Files (in order of creation)

| # | File | Created by | Content |
|---|---|---|---|
| 1 | `Global_disease_burden_statistics_download.csv` | manual download | Disease burden statistics. |
| 2 | `diseases_from_disease_burden_website.txt` | manual | Diseases used for the disease burden plots |
| 3 | `diseases_from_extraction_<agency>.txt` | code | Disease names extracted by the LLM, per agency (EMA, Swissmedic, Australia, Japan) |
| 4 | `*_unique.txt` | `clean_diseases.py` | Unique, alphabetically sorted terms from the files in 2-3 |
| 5 | `Mapping_diseases_disease_classes.csv` | [manual] | Mapping disease name → disease class(es) (ICD-11 chapters). (mapped by J.D.) |
| 6 | `preprocessed/` | `src/burden_mapping/preprocess_burden_data.py` | Burden aggregated per year and disease class |
