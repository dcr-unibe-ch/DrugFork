# data/TGA/

Source data for **TGA** (Australian Public Assessment Reports (AusPARs)).

## Source
- **Website:** https://www.tga.gov.au/resources/australian-public-assessment-reports-auspar
- **Document type:** Australian Public Assessment Reports (AusPARs)
- **Download method:** manually downloaded
- **Download date:** 2025-07-11
- **Selection criteria:** all available AusPARs 

## Files
| File | Description |
|---|---|
| `TGA_list.txt` | List of all downloaded PAR file names (1081 documents), used to draw the random evaluation sample for manual annotation. Identical to `../inference_data/TGA.txt`. |
| `TGA_csv_files/` | TGA database exports — **not used**, see README there. |

AusPARs are available from 12/2009 onwards (1082 at the time of download).

The PDFs themselves are stored locally in `downloads/` and are **not** part of the repository (`.gitignore`).