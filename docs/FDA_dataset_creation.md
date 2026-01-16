# FDA Dataset Creation Documentation

## Overview
The FDA dataset is created through a semi-automated process that combines data from multiple sources: the openFDA API, orphan drug designations, and drug label extractions. Unlike other agency datasets (EMA, PMDA, etc.) which are parsed from PDFs, the FDA dataset is built from structured API data and requires manual curation.

## Data Sources

### 1. Primary Source: OpenFDA API
- **Input**: `data/FDA/drugs@fda_openFDA.json`
- **Supplementary files** (from FDA ZIP):
  - `Products.txt`
  - `Marketing_Status.txt`
  - `Marketing_Status_Lookup.txt`
  - `TE.txt`
- **Script**: `src/download/fda_download/open_fda_data_mining.py`
- **Output**: `data/FDA/formatted_output_openFDA.json`

This script extracts and formats:
- Marketing authorization numbers
- Drug names (brand and generic)
- Marketing authorization holders (sponsors)
- Pharmaceutical forms and routes
- Approval decisions and dates
- Current status

### 2. Orphan Drug Designations
- **Input**: `data/FDA/Orphan_Drug_Status_FDA.xls`
- **Process**: Manual matching against base FDA data
- **Purpose**: Identify which approved drugs have orphan drug status

### 3. Drug Label Information
- **Input**: `data/FDA/combined_labels.json` (from FDA label API)
- **Script**: `src/explore_parse_fda.ipynb` (cells extracting indications_and_usage)
- **Output**: 
  - `data/FDA/indications_and_usage.json`
  - `data/FDA/indications_and_usage.csv`
- **Purpose**: Extract detailed indication text from official drug labels

## Dataset Creation Workflow

### Step 1: Format Base FDA Data
```bash
python src/download/fda_download/open_fda_data_mining.py
```

**What it does**:
- Reads raw openFDA JSON data
- Supplements with additional FDA text files
- Standardizes field names to match project schema
- Maps status codes (AP = Approved, etc.)
- Formats dates consistently

**Output**: `data/FDA/formatted_output_openFDA.json`

### Step 2: Extract Indications from Labels
**Notebook**: `src/explore_parse_fda.ipynb`

**Process**:
- Loads `data/FDA/combined_labels.json` (drug labels from FDA API)
- Extracts `indications_and_usage` field for each drug
- Matches labels to marketing authorization numbers
- Creates indication mappings

**Outputs**:
- `data/FDA/indications_and_usage.json`
- `data/FDA/indications_and_usage.csv`

### Step 3: Manual Curation
**Critical step requiring human review**

**Input**: `data/FDA/formatted_output_openFDA.json` + orphan drug data + indications

**Tasks**:
1. Review and correct drug names
2. Verify marketing authorization holders
3. Match orphan drug designations manually
4. Validate indication text
5. Add missing fields where possible
6. Filter relevant approvals (e.g., exclude ANDAs if desired)

**Output**: `inference/combined/FDA_manually_cleaned.json`

**Why manual curation is needed**:
- FDA data quality varies (missing fields, inconsistent naming)
- Orphan drug matching requires verification
- Multiple submission types (NDA, ANDA, BLA) need review
- Indication extraction from labels may need correction

### Step 4: Extract Disease Classifications
```bash
./run_extract_from_columns.sh
```

**Input**: `inference/combined/FDA_manually_cleaned.json`

**Process**:
- Uses LLM to extract disease classes from indication text
- Extracts disease names from indication text
- Configured in `src/utils/extract_from_columns.py`:
  - Column: `Indications_and_usage`
  - Extracts: `Indications_and_usage_disease_class_extracted`
  - Extracts: `Indications_and_usage_disease_name_extracted`

**Output**: `data/FDA/with_extracted_data_disease_class/FDA.json`

### Step 5: Combine All Data
**Notebook**: `src/preprocessing/FDA_combine_data.ipynb`

**Process**:
```python
# Load manually cleaned base data
clean_df = pd.read_json("inference/combined/FDA_manually_cleaned.json").transpose()

# Load LLM-extracted disease classifications
indications_df = pd.read_json("data/FDA/with_extracted_data_disease_class/FDA.json").transpose()
indications_df = indications_df[["MA_Number", 
                                "Indications_and_usage_disease_class_extracted", 
                                "Indications_and_usage_disease_name_extracted"]]

# Merge
merged_df = pd.merge(clean_df, indications_df, on="MA_Number", how="outer")

# Rename to standard schema
merged_df = merged_df.rename(columns={
    "Indications_and_usage_disease_class_extracted": "Disease_class(es)",
    "Indications_and_usage_disease_name_extracted": "Disease_name(s)"
})

# Save final combined data
merged_df.to_json("inference/combined/FDA_final.json", orient="index", indent=4)
```

**Output**: `inference/combined/FDA_final.json`

### Step 6: Filter and Standardize for 1995+ Dataset
**Final processing to create standardized dataset**

**Input**: `inference/combined/FDA_final.json`

**Process**:
1. Filter to decisions from 1995 onwards
2. Standardize column order to match other agencies
3. Add `Agency: 'FDA'` column
4. Create separate approved-only subset

**Outputs**:
- `data/datasets/1995/all_decisions/FDA.csv`
- `data/datasets/1995/approved/FDA.csv`

## Key Files and Their Roles

### Scripts
- `src/download/fda_download/open_fda_data_mining.py` - Base data formatting
- `src/utils/extract_from_columns.py` - LLM extraction for disease classifications

### Notebooks
- `src/explore_parse_fda.ipynb` - Indication extraction from labels
- `src/preprocessing/FDA_combine_data.ipynb` - Final data combination

### Data Files
```
data/FDA/
├── drugs@fda_openFDA.json              # Raw API data
├── Orphan_Drug_Status_FDA.xls          # Orphan designations
├── combined_labels.json                # Drug labels from FDA
├── formatted_output_openFDA.json       # Formatted base data
├── indications_and_usage.json          # Extracted indications
└── with_extracted_data_disease_class/
    └── FDA.json                        # LLM-extracted disease info

inference/combined/
├── FDA_manually_cleaned.json           # After manual curation
└── FDA_final.json                      # Final combined data

data/datasets/1995/
├── all_decisions/FDA.csv               # Final dataset (all)
└── approved/FDA.csv                    # Final dataset (approved only)
```

## Shell Scripts

### `run_extract_from_columns.sh`
Used in Step 4 to run LLM extraction:
```bash
python src/utils/extract_from_columns.py \
    --input inference/combined/FDA_manually_cleaned.json \
    --column Indications_and_usage \
    --output data/FDA/with_extracted_data_disease_class/FDA.json
```

## Important Notes

### Why FDA is Different
1. **Structured API data** vs PDF parsing for other agencies
2. **Multiple submission types** (NDA, ANDA, BLA) vs single type
3. **Requires manual curation** due to data quality variations
4. **Label extraction** is separate step vs embedded in PDFs

### Manual Curation Checkpoint
The manual curation step (`FDA_manually_cleaned.json`) is essential because:
- OpenFDA data has inconsistencies
- Orphan drug matching needs verification  
- Submission types need filtering (e.g., keeping only NDAs)
- Missing fields need to be filled where possible

### Column Mapping
FDA uses different source field names that are mapped to standard schema:
- `application_number` → `Marketing_authorisation_number`
- `brand_name` → `Drug`
- `generic_name` → `Non_proprietary_name`
- `sponsor_name` → `Marketing_authorisation_holder`
- `submission_status` → `Decision`

## Quick Reference: Complete Workflow

```bash
# 1. Format base data
python src/download/fda_download/open_fda_data_mining.py

# 2. Extract indications (run notebook cells)
# Open: src/explore_parse_fda.ipynb

# 3. MANUAL CURATION REQUIRED
# Review: data/FDA/formatted_output_openFDA.json
# Save to: inference/combined/FDA_manually_cleaned.json

# 4. Extract disease classifications
./run_extract_from_columns.sh

# 5. Combine all data (run notebook)
# Open: src/preprocessing/FDA_combine_data.ipynb

# 6. Filter and standardize
# (This step is manual - filter FDA_final.json to 1995+ and save as CSV)
```

## Output Schema
Final FDA dataset matches standard project schema with 24 fields:
- Marketing_authorisation_number
- Indications_and_usage
- Drug_name
- Non_proprietary_name
- Marketing_authorisation_holder
- Pharmaceutical_form
- Administration_route
- Decision
- Decision_date
- Decision_year
- Current_status
- Orphan_drug_status
- Disease_class(es)
- Disease_name(s)
- Agency (= 'FDA')
- ... (other standardized fields)
