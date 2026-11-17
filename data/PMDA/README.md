# data/PMDA/

Source data for **PMDA** (PMDA Review Reports (English translations)).

## Source
- **Website:** https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html
- **Document type:** PMDA Review Reports (English translations)
- **Download method:** manual download
- **Download date:** 2025-06-30
- **Selection criteria:** all available PARs in English

## Files
| File | Description |
|---|---|
| `PMDA_list.txt` | List of all downloaded PAR file names (408 documents), used to draw the random evaluation sample for manual annotation. Identical to `../inference_data/PMDA.txt`. |

PMDA provides no API or CSV export; review reports are the only source. All 408 English review reports available were downloaded. PMDA publishes review reports **only for approved drugs**, so all PMDA records have `Decision = approved`.

The PDFs themselves are stored locally in `downloads/` and are **not** part of the repository (`.gitignore`).
