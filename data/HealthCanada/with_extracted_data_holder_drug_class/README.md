# data/HealthCanada/with_extracted_data_holder_drug_class/

> Not used in the final analysis (earlier project version).

`data/HealthCanada/HEALTHCANADA.json` with two LLM-extracted columns
(`run_extract_from_columns.sh`):
- `Marketing_authorisation_holder_extracted` – normalised holder name
- `Non_proprietary_name_extracted` – drug class derived from the active substance
  (renamed to `Drug_class` during manual cleaning)

This file is the **input for manual cleaning**. A copy is stored as
`../../datasets/manually_cleaned/HEALTHCANADA.json` (before cleaning), next to
`HEALTHCANADA_manually_cleaned.json` (after cleaning).

Note: for Health Canada (and FDA), `extract_from_columns` was run **before** manual
cleaning; for the PAR agencies it was run **after**.
