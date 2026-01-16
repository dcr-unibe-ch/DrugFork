# Health Canada Dataset Creation Documentation

## Overview
The Health Canada dataset is created by combining data from the Drug Product Database (DPD) text files with LLM-extracted information for marketing authorization holders and drug classes. This dataset follows a fully automated pipeline without manual curation, unlike FDA. The process covers all approved drugs from 1946 onwards, with the final 1995+ subset extracted for cross-agency comparison.

## Data Sources

### 1. Primary Source: Drug Product Database (DPD) Text Files
- **Location**: `data/HealthCanada/allfiles/`
- **Input files**:
  - `drug.txt` - Core drug information (DRUG_CODE, CLASS, DRUG_ID/DIN, BRAND_NAME)
  - `ingred.txt` - Active ingredients
  - `form.txt` - Pharmaceutical forms
  - `route.txt` - Routes of administration
  - `status.txt` - Marketing status and dates
  - `comp.txt` - Company information (marketing authorization holders)
  - `ther.txt` - Therapeutic classification (ATC codes)

### 2. PDF Monographs (Optional)
- **Location**: `data/HealthCanada/downloads/`
- **Purpose**: Product monographs from Health Canada website for detailed indication text
- **Note**: Not required for basic dataset; primarily used for disease classification extraction

## Dataset Creation Workflow

### Step 1: Process DPD Text Files
**Notebook**: `src/exploring_canada.ipynb`

**Process**:
1. **Load and parse text files** - Custom CSV parser for Health Canada format:
   ```python
   def txt_into_df(txt_file, columns):
       # Parse quoted, comma-separated format
       # Remove placeholder columns marked as "_"
   ```

2. **Filter drug classes** - Keep only Human and Radiopharmaceutical drugs

3. **Combine ingredients** - Multiple ingredients per drug aggregated with semicolons:
   ```python
   df_ingred_combined = df_ingred.groupby('DRUG_CODE')['INGREDIENT'].apply(
       lambda x: '; '.join(x.astype(str).unique())
   ).reset_index()
   ```

4. **Combine pharmaceutical forms** - Handle multiple forms per drug

5. **Combine routes of administration** - Aggregate all routes

6. **Extract status history**:
   - Earliest status = Initial decision
   - Latest status = Current status
   - Extract decision dates

7. **Merge company information** - Add marketing authorization holders

8. **Standardize column names**:
   ```python
   mapping = {
       "DRUG_ID": "Marketing_authorisation_number",  # DIN
       "BRAND_NAME": "Drug_name",
       "INGREDIENT": "Non_proprietary_name",
       "PHARMACEUTICAL_FORM": "Pharmaceutical_form",
       "ROUTE_OF_ADMINISTRATION": "Administration_route",
       "STATUS": "Decision",
       "HISTORY_DATE": "Decision_date",
       "COMPANY_NAME": "Marketing_authorisation_holder"
   }
   ```

9. **Extract decision year** from decision date

**Outputs**:
- `data/HealthCanada/HEALTHCANADA.csv`
- `data/HealthCanada/HEALTHCANADA.json`

**Key characteristics**:
- Total records: ~11,500 drugs (all time periods)
- Date range: 1946 - present
- All drugs with marketing status in Canada

### Step 2: Extract Marketing Authorization Holders and Drug Classes
**Script**: `src/utils/extract_from_columns.py`

**Configuration**:
```bash
--input_file data/HealthCanada/HEALTHCANADA.json
--columns_of_interest Marketing_authorisation_holder Non_proprietary_name
--dataset HEALTHCANADA
```

**Process**:
- **Extract holder names** using LLM (GPT-4o-mini):
  - Prompt: Extract core parent company name
  - Remove legal suffixes (Ltd, Inc, S.A., etc.)
  - Remove generic words (Group, Company, Pharma)
  - Example: "Takeda Pharmaceutical Company" → "Takeda"

- **Extract drug classes** using LLM:
  - Based on non-proprietary (generic) name
  - Categories: Small molecule, Biologics, Peptides and proteins, Cell and gene therapy, Vaccine, Other
  - Temperature: 0.1 for consistency
  - Max tokens: 100

**Output**: `data/HealthCanada/with_extracted_data_holder_drug_class/HEALTHCANADA.csv`

**New columns added**:
- `Marketing_authorisation_holder_extracted` - Cleaned company name
- `Drug_class` - Automated drug classification

### Step 3: Filter to 1995+ and Standardize
**Notebook**: `src/consolidate_datasets.ipynb`

**Process**:
1. **Load data** with extracted fields

2. **Clean and standardize**:
   ```python
   def prepare_for_analysis(filepath):
       df = load_data(filepath).transpose()
       df.replace(["not reported", "Not reported", ""], np.nan, inplace=True)
       df = remove_invalid_rows(df)
       df = to_lower(df)  # Standardize to lowercase
       df = date_to_int(df, 'Decision_year')
       return df
   ```

3. **Filter by decision year** (≥1995):
   ```python
   filtered, stats = filter_by_decision_year(df, min_year=1995)
   ```

4. **Filter by decision type** - Keep only approved/marketed drugs

5. **Add agency identifier**:
   ```python
   HealthCanada['Agency'] = 'HealthCanada'
   ```

6. **Save standardized datasets**:
   - All decisions: `data/datasets/1995/all_decisions/HealthCanada.csv`
   - Approved only: `data/datasets/1995/approved/HealthCanada.csv`

**Final dataset stats**:
- Total records (1995+): ~10,286 drugs
- Approval rate: ~32.5%

### Optional Step: Download PDF Monographs
**Script**: `src/download/health_canada_download/health_canada_download.py`

**Purpose**: Download product monograph PDFs for detailed indication extraction

**Process**:
1. **Generate DPD info links**:
   ```python
   BASE_URL = "https://health-products.canada.ca/dpd-bdpp/info?lang=eng&code="
   # Link format: {BASE_URL}{Drug_number}
   ```

2. **Scrape PDF links** from DPD pages:
   - Parse HTML to find PDF links
   - Extract product monograph URLs
   - Handle duplicates (same PDF for multiple DINs)

3. **Download PDFs**:
   - Retry logic with exponential backoff
   - Checkpoint system for interrupted downloads
   - Deduplication via `pdf_dict.json`

4. **Track results**:
   - `data/HealthCanada/scraping_results.json` - Download status
   - `data/HealthCanada/pdf_dict.json` - PDF to DIN mappings

**Note**: This step is optional and primarily used if you need to extract detailed indication text for disease classification.

### Optional Step: Parse PDFs for Indications
**Script**: `src/preprocessing/parse_pdf.py` via `run_parse_pdf.sh`

**Configuration**:
```bash
INPUT_DIR="data/HealthCanada/downloads"
OUTPUT_DIR="data/HealthCanada/downloads_parsed"
TO_EXTRACT=("indications")
```

**Output**: `data/HealthCanada/downloads_parsed/parsed.json`

**Note**: Only needed if extracting disease information from monographs.

## Key Files and Their Roles

### Scripts
- `src/exploring_canada.ipynb` - Main data processing from DPD text files
- `src/utils/extract_from_columns.py` - LLM extraction for holders and drug classes
- `src/consolidate_datasets.ipynb` - Filter to 1995+ and standardize
- `src/download/health_canada_download/health_canada_download.py` - Optional PDF download

### Data Files
```
data/HealthCanada/
├── allfiles/                           # Source DPD text files
│   ├── drug.txt
│   ├── ingred.txt
│   ├── form.txt
│   ├── route.txt
│   ├── status.txt
│   ├── comp.txt
│   └── ther.txt
├── HEALTHCANADA.csv                    # Base dataset (all years)
├── HEALTHCANADA.json
├── with_extracted_data_holder_drug_class/
│   └── HEALTHCANADA.csv                # With LLM extractions
├── downloads/                          # Optional: PDF monographs
├── downloads_parsed/                   # Optional: Parsed indications
│   └── parsed.json
└── scraping_results.json               # Optional: Download tracking

data/datasets/1995/
├── all_decisions/HealthCanada.csv      # Final 1995+ dataset
└── approved/HealthCanada.csv           # Approved only subset
```

## Important Notes

### Why Health Canada is Different from Other Agencies

1. **Structured text files** - Uses DPD database exports instead of PDF parsing
2. **No manual curation** - Fully automated pipeline (unlike FDA)
3. **Multiple sources per drug** - Ingredients, forms, routes stored separately and merged
4. **Status history tracking** - Earliest status = decision, Latest = current status
5. **Longer time span** - Data from 1946 onwards (vs 1995+ for analysis)

### ATC Classification
Health Canada data includes therapeutic classification via `ther.txt` with ATC codes:
```python
ATC_mapping = {
    "A": "Alimentary tract and metabolism",
    "B": "Blood and blood-forming organs",
    "C": "Cardiovascular system",
    "L": "Antineoplastic and immunomodulating agents",
    "N": "Nervous system",
    # ... etc
}
```

### Data Quality Considerations
- **Dates**: Many early records use 31.12.YYYY (end of year) as placeholder dates
- **Company names**: Extracted names standardized to core parent company
- **Multiple entries**: Same drug may have multiple entries for different:
  - Pharmaceutical forms (tablet, capsule, liquid)
  - Routes of administration
  - Strengths/dosages

### Column Mapping
Health Canada standard fields:
- `DRUG_ID` (DIN) → `Marketing_authorisation_number`
- `DRUG_CODE` → Internal identifier (kept for reference)
- `BRAND_NAME` → `Drug_name`
- `INGREDIENT` → `Non_proprietary_name`
- Status from earliest record → `Decision`
- Earliest `HISTORY_DATE` → `Decision_date`
- Latest status → `Current_status`

## Quick Reference: Complete Workflow

```bash
# 1. Process DPD text files (notebook)
# Open: src/exploring_canada.ipynb
# Run all cells to generate HEALTHCANADA.csv

# 2. Extract holder names and drug classes
python src/utils/extract_from_columns.py \
    --input_file data/HealthCanada/HEALTHCANADA.json \
    --columns_of_interest Marketing_authorisation_holder Non_proprietary_name \
    --dataset HEALTHCANADA \
    --save_file data/HealthCanada/with_extracted_data_holder_drug_class/HEALTHCANADA.csv

# 3. Filter to 1995+ and standardize (notebook)
# Open: src/consolidate_datasets.ipynb
# Load HealthCanada data, filter by year, save to data/datasets/1995/

# Optional: Download PDFs
# python src/download/health_canada_download/health_canada_download.py

# Optional: Parse PDFs for indications
# ./run_parse_pdf.sh
```

## Output Schema

Final Health Canada dataset (1995+) includes:
- **Core identification**:
  - DRUG_CODE (internal)
  - Marketing_authorisation_number (DIN)
  - Drug_name (brand name)
  - Non_proprietary_name (generic/ingredient)

- **Pharmaceutical details**:
  - Pharmaceutical_form
  - Administration_route
  - Drug_class (extracted: small molecule, biologics, etc.)

- **Regulatory information**:
  - Decision (marketed/approved status)
  - Decision_date
  - Decision_year
  - Current_status

- **Company information**:
  - Marketing_authorisation_holder (full legal name)
  - Marketing_authorisation_holder_extracted (cleaned core name)

- **Metadata**:
  - Agency = "HealthCanada"
