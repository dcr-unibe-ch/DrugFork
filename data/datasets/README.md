# data/datasets/

Main datasets: LLM-extracted, cleaned, unified and filtered regulatory decisions.

## Processing order

| Step | Folder / files | Created by |
|---|---|---|
| 1 | `manually_cleaned/<AGENCY>.json` | Raw LLM extraction (evaluation + inference outputs combined) |
| 2 | `manually_cleaned/<AGENCY>_manually_cleaned.json/.csv` | [manual] cleaning of step 1 |
| 3 | `with_extracted_data/<AGENCY>.csv/.json` | `run_extract_from_columns.sh` (LLM: disease names/classes, holder) on step 2 |
| 4 | `<AGENCY>.csv/.json` (this folder) | `notebooks/consolidate_datasets.ipynb`, part 1 |
| 5 | `1995/all_decisions/`, `1995/approved/` | `notebooks/consolidate_datasets.ipynb`, part 2 |

## Files in this folder (step 4)

`EMA`, `SWISSMEDIC`, `AUSTRALIA` (=TGA), `JAPAN` (=PMDA), `FDA`, `HEALTHCANADA` as `.csv` and `.json`.

`consolidate_datasets.ipynb` (part 1, "Unify and consolidate all data") does, per agency:
1. Load `manually_cleaned/<AGENCY>_manually_cleaned.json`.
2. Add `Indication_approved_extracted`, `Indication_requested_extracted`, `Marketing_authorisation_holder_extracted`
   from `with_extracted_data/Diseases_manually_cleaned/<AGENCY>_manually_cleaned.csv`, matched on `Document_name`.
3. Rename `Indication_approved_extracted` → `Disease_name(s)`; add column `Dataset` (agency label).
4. PMDA only: `Marketing_authorisation_number` = document file name without `.pdf`.
5. Sort columns alphabetically, save as CSV and JSON.

| File | Rows |
|---|---|
| `EMA.csv` | 1993 |
| `SWISSMEDIC.csv` | 234 |
| `AUSTRALIA.csv` | 1050 |
| `JAPAN.csv` | 408 |

## Variables

Source of each column:
**PAR** = extracted by GPT-4o from the PAR PDF (`src/extraction/question_response.py`);
**LLM-col** = extracted by GPT-4o from another column (`src/utils/extract_from_columns.py`);
**added** = added in `notebooks/consolidate_datasets.ipynb`.

Missing information is coded as `Not reported` (or `NA` where the question does not apply).

| Column | Source | Description | Format / allowed values |
|---|---|---|---|
| `Document_name` | added | File name of the source PAR; unique key to trace each row back to the PDF | e.g. `pluvicto-epar-public-assessment-report_en.pdf` |
| `Dataset` | added | Agency | `EMA`, `Swissmedic`, `TGA`, `PMDA` |
| **Identification** | | | |
| `Marketing_authorisation_number` | PAR | Authorisation/product number as given by the agency (PMDA: file name without `.pdf`) | EMA: `EMA/{6 digits}/{year}`; Swissmedic: 5 digits; several numbers comma-separated |
| `Procedure_number` | PAR | Procedure number | EMA: `EMEA/H/C/{6 digits}` |
| `Marketing_authorisation_holder` | PAR | Company holding or applying for the authorisation, as written in the PAR | free text |
| `Marketing_authorisation_holder_extracted` | LLM-col | Holder name normalised to the parent company (from `Marketing_authorisation_holder`) | e.g. `Pfizer`, `Novartis` |
| **Drug characteristics** | | | |
| `Drug_name` | PAR | Brand (market) name | free text |
| `Non_proprietary_name` | PAR | International non-proprietary name (INN) / active substance | free text |
| `Drug_class` | PAR | Drug class | `Small molecule`, `Biologics`, `Peptides and proteins`, `Cell and gene therapy`, `Vaccine`, `Other` |
| `Pharmaceutical_form` | PAR, manually cleaned | Dosage form | e.g. `tablet`, `solution`, `capsule`, `powder` |
| `Administration_route` | PAR, manually cleaned | Route of administration | e.g. `oral`, `intravenous`, `subcutaneous`; several `;`-separated |
| **Regulatory decision** | | | |
| `Decision` | PAR | Decision of the agency | `approved`, `conditional marketing authorisation`, `temporary authorisation`, `refused`, `withdrawn` |
| `Current_status` | PAR | Status at the time of the report | `authorised`, `authorised (under additional monitoring)`, `withdrawn`, `revoked`, `NA` |
| `Application_date` | PAR | Date of submission of the application | `DD.MM.YYYY` |
| `Application_year` | PAR | Year of submission | `YYYY` |
| `Decision_date` | PAR | Date of the decision | `DD.MM.YYYY` |
| `Decision_year` | PAR | Year of the decision; used for all time trends | `YYYY` |
| **Indication** | | | |
| `Indication_requested` | PAR | Indication initially requested by the applicant | free text |
| `Indication_approved` | PAR | Indication approved (`NA` if not approved) | free text |
| `Indication_extended` | PAR | Drug previously authorised for a different indication | `yes`, `no` |
| `Disease_name(s)` | LLM-col | Disease names extracted from `Indication_approved`, as MeSH concept terms (column `Indication_approved_extracted` in earlier files) | `<Disease 1>; <Disease 2>` |
| `Indication_requested_extracted` | LLM-col | Same, extracted from `Indication_requested` | `<Disease 1>; <Disease 2>` |
| `Disease_class(es)` | PAR, manually cleaned | Disease class(es), based on ICD chapters; all that apply | 17 fixed classes, e.g. `Neoplasms`, `Diseases of the nervous system`; several `;`-separated |
| **Additional information** | | | |
| `Orphan_drug_status` | PAR | Designated as orphan drug | `yes`, `no` |
| `Nonclinical_abridged` | PAR | Nonclinical part of the application abridged (`yes` also if no nonclinical data are mentioned at all) | `yes`, `no` |
| `Referral_body` | PAR | For abridged applications: agency whose assessment was relied on; else `NA` | e.g. `EMA`, `FDA` |

Notes:
- Upper/lower case is not yet harmonised in these files (e.g. `oral` / `Oral`, `yes` / `Yes`).
  This is done in `notebooks/consolidate_datasets.ipynb`, part 2 (→ `1995/`).
- A few cells contain `Error: The response is not valid JSON ...` where the LLM output could not be
  parsed; these rows are removed in part 2 (→ `1995/`).