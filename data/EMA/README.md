# data/EMA/

Source data for **EMA** (European Public Assessment Reports (EPARs)).

## Source
- **Website:** https://www.ema.europa.eu/en/medicines
- **Document type:** European Public Assessment Reports (EPARs)
- **Download method:** script `src/download/ema_download/download_epars.py`
- **Download date:** 2025-05-21
- **Selection criteria:** all available PARs

## Files
| File | Description |
|---|---|
| `–` | List of all downloaded PAR file names (1993 documents), used to draw the random evaluation sample for manual annotation. Identical to `../inference_data/EMA.txt`. |
| `medicines_output_medicines_en.xlsx` | EMA medicines table as downloaded from https://www.ema.europa.eu/en/medicines/download-medicine-data |
| `EMA.csv` | Same table as the xlsx, saved as CSV (2143 rows): authorisation numbers, dates, therapeutic areas, INN. |

The PDFs themselves are stored locally in `downloads/` and are **not** part of the repository (`.gitignore`).
