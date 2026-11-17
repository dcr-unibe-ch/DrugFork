# data/datasets/with_extracted_data/

Manually cleaned datasets with **additional LLM-extracted columns**:
`Indication_approved_extracted` / `Indication_requested_extracted` (disease names and ICD-11 disease classes)
and `Marketing_authorisation_holder_extracted` (normalised holder name).

**Created by:** `run_extract_from_columns.sh` → `src/utils/extract_from_columns.py` (GPT-4o, temperature 0.1),
then `src/utils/json_to_csv.py`.
**Input:** the **uncleaned** LLM output `../manually_cleaned/<AGENCY>.json`
(not the manually cleaned version). Only the extracted columns
(`Indication_approved_extracted`, `Indication_requested_extracted`,
`Marketing_authorisation_holder_extracted`) are used later: they are joined to the
manually cleaned data by `Document_name` in `notebooks/consolidate_datasets.ipynb`.
All other columns in these files are uncleaned.

| File | Rows | Note |
|---|---|---|
| `EMA`, `SWISSMEDIC`, `AUSTRALIA`, `JAPAN` `.csv/.json` | 1993 / 234 / 1051 / 408 | |
| `combined_datasets_shuffled.csv` | 3686 | All four agencies combined and shuffled. **TODO:** purpose (evaluation of the disease extraction?) |
| `combined_datasets_shuffled_annotated.csv` | 3686 | [manual] validation of the `extract_from_columns.py` output. **TODO:** who validated, which columns, result |
| `Diseases_manually_cleaned/` | | See README there |

`AUSTRALIA.csv` has 1051 rows (vs. 1050 in the cleaned data) because it still
contains `auspar-riastap.pdf`. This PDF is encrypted and could not be read
(extraction output: `Error: PyCryptodome is required for AES algorithm`); it was
removed during manual cleaning and is therefore not in the final dataset.
