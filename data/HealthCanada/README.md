# data/HealthCanada/

> **Not used in the final analysis.** Part of an earlier project version (six agencies).
> Full description of how this dataset was built: `../../docs/HealthCanada_dataset_creation.md`.

Built from the Health Canada Drug Product Database (DPD) plus product monographs (PDFs).

| File / folder | Content |
|---|---|
| `allfiles/` | Unzipped DPD database download |
| `scraping_results.csv/.json` | Output of a scraping run that failed halfway — **incomplete, not used** |
| `pdf_dict.json` | Product monograph PDF → DIN(s) of the corresponding drugs. **Required to map indications to drugs.** |
| `HEALTHCANADA.json/.csv` | All information from the `allfiles/` txt files, before manual cleaning |
| `HEALTHCANADA_with_links.csv` | As above, with links to the product pages (used to download the product monographs) |

Product monographs (PDFs) are in `downloads/` (not in the repository). The mapping of DPD fields to the
extraction fields is documented in `../../docs/HealthCanada_dataset_creation.md`.
| `downloads_parsed/` | Indications parsed from the product monographs (`run_parse_pdf.sh`) |
| `with_extracted_data_holder_drug_class/` | + LLM-extracted holder and drug class |
| `with_extracted_data_pdfs_disease_name_class/` | + LLM-extracted disease names/classes from monographs |
