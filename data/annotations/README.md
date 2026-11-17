# data/annotations/

Human reference annotations ("ground truth") of the evaluation sample, used to evaluate LLM extraction.

| File | Content |
|---|---|
| `Drug_Approval_Annotations_all_datasets-Sheet1.csv` | Export of the shared Google Sheet with all manual annotations (285 rows, all agencies). Row 1 below the header contains the field instructions (format hints). |
| `..._cleaned.csv` | Same, with document file names harmonised to match the PDF names. Created by `run_clean_filenames_in_annotations.sh` (`src/preprocessing/clean_filenames_in_annotations.py`). |

## How the annotations were made
1. [manual] All documents of the evaluation sample (`../eval_data/`) were annotated by
   one person (J. D.) between February and July 2025, in a shared Google Sheet.
   Each document was annotated once (single annotator, no double annotation).
2. [manual] Annotation followed the field definitions in
   `../../assets/Protocol_PublicAssessmentReports.docx`.
3. [manual] The Google Sheet was exported as CSV on 2025-07-17
   (`Drug_Approval_Annotations_all_datasets-Sheet1.csv`).
4. [script] File names were harmonised with the PDF names using
   `run_clean_filenames_in_annotations.sh`
   (`src/preprocessing/clean_filenames_in_annotations.py`)
   → `..._cleaned.csv`.
