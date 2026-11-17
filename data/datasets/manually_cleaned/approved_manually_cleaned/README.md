# data/datasets/manually_cleaned/approved_manually_cleaned/

Approved decisions from 1995 onwards, per agency, derived from the manually cleaned datasets.
Used in `notebooks/paper_writing_jd.ipynb` only as a **consistency check**: the notebook recomputes the
approved set from `../<AGENCY>_manually_cleaned.csv` and checks that the document names are identical.

| File | Rows |
|---|---|
| `EMA.csv` | 1491 |
| `Swissmedic.csv` | 233 |
| `TGA.csv` | 988 |
| `PMDA.csv` | 408 |
| `FDA.csv`, `HealthCanada.csv` | not used |
| `Overall.csv` | all agencies combined |

**Created by:** earlier version of `notebooks/consolidate_datasets.ipynb`
(part 2, "Cut off 1995 & Filtering"); the exact origin is not documented. Evidence:
same documents as `../../1995/approved/` for EMA, Swissmedic and TGA; all text
lower-cased including `Dataset` (`ema`, `japan`, ...); disease names still in the
old column `Indication_approved_extracted` (now `Disease_name(s)`); an additional
column `Agency` with the agency name in standard spelling.

PMDA has 408 rows here but 407 in `../../1995/approved/PMDA.csv`: the record without
a valid decision year was not yet removed in this earlier version.
