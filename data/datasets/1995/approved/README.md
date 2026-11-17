# data/datasets/1995/approved/

Approved decisions only (approved / marketed / conditional marketing authorisation) from 1995 onwards.
Created by `notebooks/consolidate_datasets.ipynb`, part 2 (see `../README.md` for the filtering steps).

Rows: EMA 1491, Swissmedic 233, TGA 988, PMDA 407, (FDA 18558, HealthCanada 10286), Overall 31556.

> ⚠️ `Overall.csv` does **not contain PMDA** (PMDA is commented out in the notebook), although `PMDA.csv` is in
> this folder, and it **does contain FDA and Health Canada**. **TODO:** re-run the notebook with the final set of four
> PAR agencies, or document why the files differ.

> Note: `PMDA.csv` is identical to `../all_decisions/PMDA.csv` because PMDA publishes review reports only for approved drugs (all records `approved`). It has 407 instead of 408 rows because one record has no valid decision year.

Input for the notebooks `analyze_output.ipynb` and `analyze_overall.ipynb` (→ `../../../analysis/`).
