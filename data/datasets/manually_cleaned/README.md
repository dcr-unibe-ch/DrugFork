# data/datasets/manually_cleaned/

LLM extraction output **before** (`<AGENCY>.json`) and **after** (`<AGENCY>_manually_cleaned.*`) manual cleaning.

## Files

| File | Content |
|---|---|
| `<AGENCY>.json` | Uncleaned LLM output (all documents: evaluation + inference set combined). `AUSTRALIA.json` is identical to `../../../output/20250729_TGA_gpt-4o.json`; `FDA.json` and `HEALTHCANADA.json` are copies of `../../FDA/with_extracted_data_holder/FDA.json` and `../../HealthCanada/with_extracted_data_holder_drug_class/HEALTHCANADA.json`. |
| `<AGENCY>_manually_cleaned.json` | After manual cleaning (input for `../with_extracted_data/` and `../<AGENCY>.csv`) |
| `<AGENCY>_manually_cleaned.csv` | CSV version (EMA 1993, SWISSMEDIC 234, AUSTRALIA 1050, JAPAN 408 rows). **This is the input of `notebooks/paper_writing_jd.ipynb`, i.e. of all numbers in the manuscript.** |
| `approved_manually_cleaned/` | See README there |

## How `<AGENCY>.json` was created
1. [script] LLM extraction (GPT-4o, `src/evaluation/generate_predictions.py`) on the evaluation sample
   → `../../../evaluation/output/20250717_<AGENCY>_gpt-4o.json` (EMA: 156 documents)
2. [script] Same on the remaining documents → `../../../output/2025072x_<AGENCY>_gpt-4o.json` (EMA: 1837 documents)
3. [script] Both combined with `run_combine_eval_inference.sh` → `inference/combined/<AGENCY>.json` (not in repo),
   copied here (EMA: 156 + 1837 = 1993 documents).

> Note: the CSV versions in `../../../output/` contain fewer rows than the JSON files (e.g. EMA 758 vs. 1837);
> always use the JSON files. **TODO:** regenerate or delete the incomplete CSVs.

## Manual cleaning (→ `<AGENCY>_manually_cleaned.*`)

**Why:** the agencies report the same information at very different granularity. Example — administration route
in Health Canada: `INTRAVENOUS; INTRATHECAL; INTRAMUSCULAR; INTRA-ARTERIAL; INTRACEREBROVENTRICULAR`; in EMA:
`Intradermal use, Subcutaneous use, Intratumoral use, Peritumoral use`. Values were harmonised so that agencies
can be compared and plotted.

| Agency | Period | Uncleaned LLM output | Cleaned file | Columns changed |
|---|---|---|---|---|
| EMA | 28.07.–08.08.2025 | `output/20250722_EMA_gpt-4o.json` | `EMA_manually_cleaned.json` | Administration_route, Disease_class(es), Drug_class, Pharmaceutical_form |
| Swissmedic | 28.07.–08.08.2025 | `output/20250722_SwissMedic_gpt-4o.json` | `SWISSMEDIC_manually_cleaned.json` | Administration_route, Disease_class(es), Pharmaceutical_form, Decision |
| TGA | 28.07.–08.08.2025 | `output/20250729_TGA_gpt-4o.json` | `AUSTRALIA_manually_cleaned.json` | Administration_route, Disease_class(es), Pharmaceutical_form |
| PMDA | 28.07.–08.08.2025 | `output/20250722_PMDA_gpt-4o.json` | `JAPAN_manually_cleaned.json` | Administration_route, Pharmaceutical_form |
| FDA | 11.08.–15.08.2025 | `data/FDA/FDA.json` | `FDA_manually_cleaned.json` | Administration_route, Decision, Pharmaceutical_form |
| Health Canada | 11.08.–15.08.2025 | `data/HealthCanada/HEALTHCANADA.json` | `HEALTHCANADA_manually_cleaned.json` | Administration_route, Current_status, Pharmaceutical_form |

**How:** All cleaning was done by one person (J. D.) by hand in the text editor BBEdit, on a copy of each uncleaned JSON file (`<AGENCY>.json` → `<AGENCY>_manually_cleaned.json`).
The original files were not modified.

**All value changes are logged** in `../../../output/cleaning_audit/<AGENCY>_cleaning_audit.csv`
(created by `notebooks/manual_cleaning_log.ipynb` by comparing the uncleaned and cleaned JSON):
columns `field`, `cleaned_value`, `total_count`, `original_variants`.
