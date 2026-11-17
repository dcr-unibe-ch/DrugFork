# data/Disease_burden_mapping/preprocessed/

**Created by:** `python src/burden_mapping/preprocess_burden_data.py` (see `src/burden_mapping/README.md`).
**Input:** `../Global_disease_burden_statistics_download.csv` + `../Mapping_diseases_disease_classes.csv`.

| File | Columns |
|---|---|
| `burden_Deaths.csv` | `Year`, `Disease_class`, `Deaths` |
| `burden_Incidence.csv` | `Year`, `Disease_class`, `Incidence` |
| `burden_Prevalence.csv` | `Year`, `Disease_class`, `Prevalence` |

Read in the analysis notebooks via `src/burden_mapping/burden_utils.py::load_burden_data()`.