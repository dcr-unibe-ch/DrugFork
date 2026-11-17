# data/datasets/1995/

Analysis-ready datasets: decisions from **1995 onwards**, one file per agency plus `Overall.csv` (all agencies combined).

| Subfolder | Content |
|---|---|
| `all_decisions/` | All regulatory decisions (approved, refused, withdrawn, ...) |
| `approved/` | Approved decisions only |

**Created by:** `notebooks/consolidate_datasets.ipynb`, part 2 ("Cut off 1995 & Filtering"),
from `../<AGENCY>.json`. Steps, in order (function `prepare_for_analysis`):

1. Replace `"not reported"` and empty strings with missing values.
2. Drop rows where the LLM output was not valid JSON (`"the response is not valid json"`).
3. Lower-case and strip all text columns (except `Dataset`).
4. Harmonise values: `lyophilized powder/product` → `lyophilisate`; `injectable`, `aqueous injection` → `injection`;
   remove stray backticks in disease classes; drug class `antisense oligonucleotide` → `peptides and proteins`.
5. Convert `Decision_year` to an integer; **drop rows without a valid decision year**.
6. Keep `Decision_year >= 1995` → `all_decisions/`.
7. Keep rows where `Decision` contains `approved`, `marketed` or `conditional marketing authorisation` → `approved/`.
8. `Overall.csv` = concatenation of the agency files.

Variable `data_filter` at the top of part 2 controls the output folder (`1995`, `1995_pars`, `1995_nonpars`);
only `1995` exists in the repo.
