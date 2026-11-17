# data/TGA/TGA_csv_files/

Structured TGA database exports (ARTG, "COGNOS" views) used as supplementary information for TGA.

| File | Content |
|---|---|
| `COGNOS_V_GEN_PRODUCT.csv` | Product details |
| `COGNOS_V_GEN_LICENCE.csv` | Licence information |
| `COGNOS_V_GEN_COMPONENT.csv` | Product components |
| `COGNOS_V_GEN_COMPONENT_ADMIN_ROUTE.csv` | Administration routes |
| `COGNOS_V_GEN_FORMULATION.csv` | Formulations |
| `COGNOS_V_GEN_INGREDIENT.csv` | Active ingredients |
| `COGNOS_V_GEN_SPECIFIC_INDIC.csv` | Specific indications |
| `AusPAR_merged_final.csv` | Merge of the AusPAR list with the tables above |

- **Source:** https://apps.tga.gov.au/downloads/
- **Download date:** 2025-06-30
- **How `AusPAR_merged_final.csv` was created:** with Python. `COGNOS_V_GEN_PRODUCT.csv` was joined with
  `COGNOS_V_GEN_LICENCE.csv` on `LICENCE_ID` (left join, one row per product) and
  reduced to 9 columns: PRODUCT_ID, PRODUCT_NAME, LICENCE_ID, PRODUCT_STATUS,
  PRODUCT_STATUS_EFFECTIVE_DATE, PRODUCT_TYPE, PRODUCT_CODE, SPONSOR_ID,
  LICENCE_STATUS. Despite its name, the file contains no information from the AusPARs.

**Not used in the analysis.** To keep the methods consistent across the four PAR
agencies (EMA, Swissmedic, TGA, PMDA), all datasets were built the same way: by
LLM extraction from the public assessment reports. In addition, these tables cover
all products in the Australian Register of Therapeutic Goods (ARTG), not only those
with an AusPAR, contain no identifier linking them to the AusPARs, and lack key
information extracted in this project (e.g. regulatory decision, nonclinical data
such as animal species).
