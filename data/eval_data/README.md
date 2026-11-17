# data/eval_data/

File names of the PARs in the **evaluation sample**, i.e. the documents that were annotated by hand
(`../annotations/`) and used to measure LLM extraction accuracy.

| File | Documents |
|---|---|
| `eval_EMA.txt` | 157 |
| `eval_Swissmedic.txt` | 65 |
| `eval_TGA.txt` | 30 |
| `eval_PMDA.txt` | 30 |

**Created by:** created by hand, with `data/annotations/Drug_Approval_Annotations_all_datasets-Sheet1_cleaned.csv`. (Samples come from `../randomized_data/`.)
Read by `src/evaluation/data_preparation.py` to split eval and inference sets (see `../../config/evaluation_config.yaml`).
