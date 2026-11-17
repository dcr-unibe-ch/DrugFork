# data/

This folder contains all data used in DrugFork, from pdf downloads to the final analysis datasets.

## Scope

The **final analysis (manuscript) covers the four agencies that publish public assessment reports (PARs):**
EMA (EU), Swissmedic (CH), TGA (Australia) and PMDA (Japan).

FDA and Health Canada were part of an earlier project version. Their data are still in this
folder (`FDA/`, `HealthCanada/`) and in some intermediate datasets, but they are **not used in the final analysis**.

**TODO:** decide whether FDA / Health Canada data stay in the released repository.

## Agency naming

The same agency appears under different names in file names:

| Agency | Names used in files |
|---|---|
| EMA | `EMA` |
| Swissmedic | `Swissmedic`, `SWISSMEDIC`, `SwissMedic` |
| TGA | `TGA`, `AUSTRALIA` |
| PMDA | `PMDA`, `JAPAN` |

**TODO:** decide whether how to name the datasets -> change in codes. 

## Data flow (PAR agencies, in order)

```
 1  Download PARs (PDFs, not in repo)        -> <agency>/<agency>_list.txt
 2  Draw random evaluation sample            -> randomized_data/, eval_data/
 3  Human annotation of evaluation sample    -> annotations/
 4  Split document lists into eval/inference -> inference_data/
 5  LLM extraction (GPT-4o), 24 fields       -> ../evaluation/output/, ../output/
 6  Combine eval + inference outputs, manual cleaning
                                             -> datasets/manually_cleaned/
 7  LLM extraction of disease names/classes and holders
                                             -> datasets/with_extracted_data/
 8  Unify schema across agencies             -> datasets/<AGENCY>.csv/.json
 9  Filter >= 1995, approved decisions       -> datasets/1995/
10  Analysis notebooks                       -> ../analysis/
```

Steps marked as manual in the subfolder READMEs are not reproducible by code and are described there.

## Folder overview

| Folder | Content | Step |
|---|---|---|
| `EMA/`, `Swissmedic/`, `PMDA/`, `TGA/` | Source metadata and lists of downloaded PARs per agency | 1 |
| `randomized_data/` | Random samples of PAR file names (prompt development, evaluation sample) | 2 |
| `annotations/` | Human reference annotations of the evaluation sample | 3 |
| `eval_data/` | File names of the PARs in the evaluation sample | 4 |
| `inference_data/` | File names of all PARs, with and without the evaluation sample | 4 |
| `datasets/` | Extracted, cleaned and filtered datasets (main data) | 6-9 |
| `Disease_burden_mapping/` | Global disease burden data mapped to disease classes | analysis input |
| `FDA/`, `HealthCanada/` | Earlier project version, not used in final analysis | – |

## Not included in the repository

- The PAR PDFs themselves (`*/downloads/`, excluded via `.gitignore` because of size/copyright).
  They can be re-downloaded from the agency websites using the document lists.
- `inference/combined/` (intermediate output referenced by several `run_*.sh` scripts).

Detailed agency documentation: `../docs/PAR_dataset_creation.md`, `../docs/TGA_dataset_creation.md`,
`../docs/Metadata_Agencies.md`.
