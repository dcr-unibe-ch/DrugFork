# data/inference_data/

Document lists for LLM extraction.

| File | Content | EMA | Swissmedic | TGA | PMDA |
|---|---|---|---|---|---|
| `<AGENCY>.txt` | All downloaded PARs | 1993 | 234 | 1081 | 408 |
| `<AGENCY>_clean.txt` | All PARs **minus** the evaluation sample (`../eval_data/`) | 1837 | 170 | 1051 | 378 |

**Created by:** `src/evaluation/data_preparation.py` (step 0 of `run_full_evaluation.sh`).
`<AGENCY>.txt` is identical to `../<AGENCY>/<AGENCY>_list.txt`.
