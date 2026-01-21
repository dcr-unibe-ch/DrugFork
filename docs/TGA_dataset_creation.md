# TGA (Australia) Dataset Creation Documentation

## Overview
The Therapeutic Goods Administration (TGA) dataset is created through an automated LLM-based extraction pipeline from Australian Public Assessment Reports (AusPARs). Unlike Health Canada and FDA datasets which combine structured database files, the TGA dataset follows a PDF-parsing approach similar to EMA, Swissmedic, and PMDA workflows. The process covers drug approvals from 1995 onwards for cross-agency comparison.

## Data Sources

### 1. Primary Source: Australian Public Assessment Reports (AusPARs)
- **Location**: `data/TGA/downloads/`
- **Document Type**: PDF assessment reports
- **Format**: AusPAR documents (e.g., `auspar-drug-name-YYMMDD.pdf`)
- **Content**: Comprehensive evaluation reports including:
  - Product information and drug characteristics
  - Clinical trial data and efficacy
  - Safety and pharmacology assessments
  - Regulatory decision and approval history
  - Marketing authorization details

### 2. Supplementary Database Files
- **Location**: `data/TGA/TGA_csv_files/`
- **Files**:
  - `AusPAR_merged_final.csv` - Merged product information
  - `COGNOS_V_GEN_COMPONENT.csv` - Drug components
  - `COGNOS_V_GEN_INGREDIENT.csv` - Active ingredients
  - `COGNOS_V_GEN_FORMULATION.csv` - Pharmaceutical formulations
  - `COGNOS_V_GEN_PRODUCT.csv` - Product details
  - `COGNOS_V_GEN_LICENCE.csv` - License information
  - `COGNOS_V_GEN_COMPONENT_ADMIN_ROUTE.csv` - Administration routes
  - `COGNOS_V_GEN_SPECIFIC_INDIC.csv` - Specific indications

**Note**: These CSV files from the Australian Register of Therapeutic Goods (ARTG) provide structured metadata but are primarily used for supplementary reference. The main extraction relies on AusPAR PDFs for comprehensive regulatory information.

### 3. PDF List
- **File**: `data/TGA/TGA_list.txt`
- **Content**: List of 1,082 AusPAR filenames to process
- **Purpose**: Master list for batch processing and tracking

## Dataset Creation Workflow

### Step 1: Download AusPAR PDFs
**Manual or Semi-Automated Download**

**Source**: TGA website (https://www.tga.gov.au/products/medicines/prescription-medicines/artg-auspar)

**Process**:
1. Access TGA's AusPAR database
2. Download assessment reports as PDFs
3. Store in `data/TGA/downloads/`
4. Maintain list in `data/TGA/TGA_list.txt`

**Document naming convention**: `auspar-[drug-name]-[YYMMDD].pdf`

### Step 2: Parse PDFs and Extract Structured Data
**Script**: Custom PDF parser with LLM extraction

**Input**: `data/TGA/downloads/*.pdf`

**Question-Response Schema**: `src/extraction/question_response.py::TGA_pairs`

**Extraction fields** (24 standardized fields):

#### Identification & Authorization
- **Marketing_authorisation_number**: ARTG number (Australian Register of Therapeutic Goods)
- **Procedure_number**: Procedure number from page footers
- **Marketing_authorisation_holder**: Sponsor/company name
- **Marketing_authorisation_holder_extracted**: Cleaned company name (LLM-extracted)

#### Drug Characteristics
- **Drug_name**: Product/brand name
- **Non_proprietary_name**: Active ingredient/INN name
- **Drug_class**: Classification (Small molecule, Biologics, Peptides and proteins, Cell and gene therapy, Vaccine, Other)
- **Pharmaceutical_form**: Dose form (solution, tablet, powder, etc.)
- **Administration_route**: Route (oral, intravenous, subcutaneous, intravitreal, etc.)

#### Regulatory Decision
- **Decision**: Approval outcome (approved, withdrawn, refused, conditional marketing authorisation, temporary authorisation)
- **Current_status**: Current authorization status (authorised, authorised (under additional monitoring), withdrawn, revoked, NA)
- **Decision_date**: Date of regulatory decision (DD.MM.YYYY format)
- **Decision_year**: Year of decision (1995-2025)
- **Application_date**: Date of initial application submission
- **Application_year**: Year of application

#### Indication & Classification
- **Indication_requested**: Original indication sought by applicant
- **Indication_approved**: Final approved indication(s)
- **Indication_extended**: Whether this is an indication extension (yes/no)
- **Disease_class(es)**: Disease categories based on ICD-11 classification
- **Indication_requested_extracted**: Extracted disease names from requested indication
- **Indication_approved_extracted**: Extracted disease names from approved indication

#### Additional Information
- **Orphan_drug_status**: Orphan designation status (yes/no)
- **Nonclinical_abridged**: Whether non-clinical data was abbreviated (yes/no)
- **Referral_body**: Referral information for abridged applications

**LLM Configuration**:
- **Model**: GPT-4o (default) or other compatible models
- **Temperature**: 0.1 (for consistency and reproducibility)
- **Max Pages**: First 40 pages of each PDF (optimized for TGA document structure)
- **Output Format**: JSON with document filename as key

**Extraction Process**:
```python
# From src/generate_predictions.py
if dataset_name == "Australia":
    max_pages = 40  # TGA-specific page limit
text = "".join([page.extract_text() for page in reader.pages[:max_pages]])

# Apply TGA-specific question-response pairs
from extraction.question_response import TGA_pairs
responses = llm_extract(text, TGA_pairs, model="gpt-4o", temperature=0.1)
```

**Output**: `output/YYYYMMDD_TGA_[model-name].json`

Example output structure:
```json
{
    "auspar-eculizumab-201124.pdf": {
        "Marketing_authorisation_number": "138885",
        "Procedure_number": "PM-2019-04825-1-1",
        "Drug_name": "Soliris",
        "Non_proprietary_name": "Eculizumab",
        "Marketing_authorisation_holder": "Alexion Pharmaceuticals Australasia Pty Ltd",
        "Drug_class": "Biologics",
        "Pharmaceutical_form": "Concentrated solution",
        "Administration_route": "Intravenous",
        "Decision": "approved",
        "Current_status": "authorised (under additional monitoring)",
        "Decision_date": "26.06.2020",
        "Decision_year": "2020",
        "Orphan_drug_status": "yes",
        "Indication_extended": "yes",
        "Indication_requested": "Adult patients with Neuromyelitis Optica Spectrum Disorder (NMOSD) who are anti-aquaporin-4 (AQP4) antibody-positive.",
        "Indication_approved": "Adult patients with Neuromyelitis Optica Spectrum Disorder (NMOSD) who are anti-aquaporin-4 (AQP4) antibody-positive."
    }
}
```

### Step 3: Convert to CSV Format
**Script**: `src/utils/json_to_csv.py`

```bash
python src/utils/json_to_csv.py \
  --input output/20250729_TGA_gpt-4o.json \
  --output output/20250729_TGA_gpt-4o.csv
```

**Process**:
- Converts nested JSON to tabular CSV format
- Each document becomes a row
- 24 fields become columns
- Preserves all extracted information

**Output**: `output/YYYYMMDD_TGA_gpt-4o.csv`

### Step 4: Extract Disease Classifications
**Script**: `src/utils/extract_from_columns.py`

```bash
./run_extract_from_columns.sh
```

**Input**: LLM-extracted JSON/CSV with indication fields

**Process**:
1. **Extract disease names** from `Indication_requested` and `Indication_approved`
2. **Map to ICD-11 disease classes** using LLM classification:
   - Diseases of the nervous system
   - Neoplasms
   - Diseases of the immune system
   - Diseases of the blood
   - Diseases of the eye and adnexa
   - Endocrine, nutritional or metabolic diseases
   - Mental, behavioural or neurodevelopmental disorders
   - Diseases of the circulatory system
   - Diseases of the respiratory system
   - Diseases of the digestive system
   - Diseases of the skin
   - Diseases of the musculoskeletal system or connective tissue
   - Diseases of the genitourinary system
   - Conditions originating in the perinatal period
   - Developmental anomalies
   - Injury, poisoning or certain other consequences of external causes
   - Certain infectious or parasitic diseases
   - Other

3. **Generate extracted fields**:
   - `Indication_requested_extracted`: `<Disease Name>; <Disease Name>`
   - `Indication_approved_extracted`: `<Disease Name>; <Disease Name>`
   - `Disease_class(es)`: Semicolon-separated ICD-11 categories

**LLM Configuration**:
- Temperature: 0.1
- Max tokens: 500
- Extraction format: Structured disease names in angle brackets

**Output**: Updated JSON/CSV with disease classification columns populated

### Step 5: Manual Review and Quality Control (Optional)
**Location**: `data/datasets/manually_cleaned/AUSTRALIA.json`

**Process**:
1. Review LLM extractions for accuracy
2. Correct any parsing errors
3. Validate dates and decision types
4. Standardize company names
5. Fix indication text formatting

**Common issues to check**:
- Missing ARTG numbers
- Inconsistent date formats
- Ambiguous decision types
- Truncated indication text
- Duplicate entries

### Step 6: Filter to 1995+ and Standardize
**Notebook**: `src/consolidate_datasets.ipynb`

**Process**:
1. **Load extracted data**:
   ```python
   tga_df = pd.read_json('output/20250729_TGA_gpt-4o.json').T
   # or load from manually cleaned version
   tga_df = pd.read_json('data/datasets/manually_cleaned/AUSTRALIA.json').T
   ```

2. **Clean and standardize**:
   ```python
   # Replace various "not reported" variations with NaN
   tga_df.replace(["not reported", "Not reported", "NA", ""], np.nan, inplace=True)
   
   # Convert to lowercase for consistency
   tga_df = tga_df.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
   
   # Convert decision year to integer
   tga_df['Decision_year'] = pd.to_numeric(tga_df['Decision_year'], errors='coerce')
   ```

3. **Filter by decision year** (≥1995):
   ```python
   tga_1995 = tga_df[tga_df['Decision_year'] >= 1995]
   ```

4. **Add agency identifier**:
   ```python
   tga_1995['Dataset'] = 'AUSTRALIA'
   tga_1995['Agency'] = 'TGA'
   ```

5. **Create decision-based subsets**:
   ```python
   # All decisions (approved, withdrawn, refused)
   all_decisions = tga_1995.copy()
   
   # Approved only
   approved = tga_1995[tga_1995['Decision'].isin(['approved', 'conditional marketing authorisation', 'temporary authorisation'])]
   ```

6. **Save standardized datasets**:
   - All decisions: `data/datasets/1995/all_decisions/AUSTRALIA.csv`
   - Approved only: `data/datasets/1995/approved/AUSTRALIA.csv`
   - Also saved as JSON: `data/datasets/AUSTRALIA.json`, `data/datasets/AUSTRALIA.csv`

**Final dataset statistics** (1995+):
- **Total records**: ~1,042 drug approvals
- **Approved drugs**: ~950+ (approval rate ~91%)
- **Time period**: 1995-2025
- **Document types**: New drug applications, indication extensions, biosimilars

## Dataset Characteristics

### TGA-Specific Features

#### 1. Document Structure
- **AusPAR format**: Standardized public assessment report structure
- **Length**: Typically 20-40 pages (shorter than EMA EPARs)
- **Content focus**: Clinical evaluation, benefit-risk assessment
- **Sections**: Product information, clinical studies, evaluation, recommendations

#### 2. ARTG Numbers
- **Format**: Numeric identifier (e.g., "138885")
- **Purpose**: Unique product identifier in Australian Register of Therapeutic Goods
- **Multiple numbers**: Products may have multiple ARTG numbers for different strengths/formulations

#### 3. Procedure Numbers
- **Format**: PM-YYYY-XXXXX-X-X (e.g., "PM-2019-04825-1-1")
- **Location**: Footer of each AusPAR page
- **Tracking**: Links to TGA's internal review process

#### 4. Regulatory Pathways
- **Standard approval**: Full clinical dossier review
- **Priority review**: Expedited for serious conditions
- **Provisional approval**: Conditional authorization with post-market requirements
- **Orphan drug program**: Available for rare diseases

#### 5. Monitoring Categories
- **Authorised**: Standard post-market surveillance
- **Authorised (under additional monitoring)**: Enhanced pharmacovigilance
  - New active substances
  - Biologics
  - Conditional approvals

### Comparison with Other Agencies

| Feature | TGA (Australia) | EMA (EU) | FDA (US) | PMDA (Japan) |
|---------|-----------------|----------|----------|--------------|
| **Document Type** | AusPAR | EPAR | Approval Package | Japanese PAR |
| **Document Length** | 20-40 pages | 50-100+ pages | Variable | 40-80 pages |
| **Data Source** | PDF parsing | PDF parsing | API + PDFs | PDF parsing |
| **Language** | English | English | English | English translation |
| **Approval Count (1995+)** | ~1,042 | ~1,687 | ~18,558 | ~409 |
| **Orphan Drug Program** | Yes | Yes | Yes | Yes |
| **Public Assessment** | Comprehensive | Very detailed | Moderate | Detailed |

### Data Quality Considerations

#### Strengths
1. **Comprehensive reports**: AusPARs provide detailed clinical and regulatory rationale
2. **Structured format**: Consistent document organization aids extraction
3. **English language**: No translation required (unlike PMDA)
4. **Complete timeline**: Application and decision dates typically well-documented
5. **Clear decisions**: Approval status explicitly stated

#### Limitations
1. **Smaller dataset**: Fewer approvals than FDA/EMA (reflects market size)
2. **ARTG numbers**: Sometimes not reported in AusPARs; requires ARTG database lookup
3. **Application dates**: Occasionally missing in older reports
4. **PDF quality**: Older documents may have scanning artifacts
5. **Indication text**: Can be verbose; requires careful extraction

#### Common Extraction Challenges
1. **Multiple ARTG numbers**: Products with different formulations listed together
2. **Company name variations**: Full legal entity name vs. common name
3. **Date formats**: Occasionally inconsistent (DD.MM.YYYY vs. other formats)
4. **Procedure numbers**: May span multiple pages; footer extraction needed
5. **Orphan status**: Not always explicitly stated; may require cross-reference

## Usage in Research and Analysis

### 1. Cross-Agency Comparison
The TGA dataset enables comparative studies:
- **Approval timelines**: Compare Australia vs. EU, US, Japan
- **Regulatory standards**: Analyze decision criteria across agencies
- **Orphan drug policies**: Compare rare disease approval pathways
- **Non-clinical requirements**: Compare evidence standards

### 2. Drug Availability Analysis
- **Geographic availability**: Track which drugs reach Australian market
- **Time-to-market**: Compare approval delays vs. other regions
- **Biosimilar adoption**: Analyze biosimilar approval patterns

### 3. Indication Analysis
- **Disease coverage**: Identify therapeutic areas with high activity
- **Indication extensions**: Track post-approval expansion strategies
- **Rare diseases**: Analyze orphan drug approvals

### 4. Evaluation Metrics
The TGA dataset contributes to:
- **Manual annotations**: 30 TGA records in evaluation set
- **LLM accuracy**: Benchmark automated extraction quality
- **Field-specific metrics**: Precision/recall for each data field

## Integration with Overall DrugFork Pipeline

### File Locations
```
DrugFork/
├── data/
│   ├── TGA/
│   │   ├── downloads/                    # Raw AusPAR PDFs
│   │   ├── TGA_list.txt                  # Master PDF list
│   │   └── TGA_csv_files/                # ARTG database exports
│   ├── datasets/
│   │   ├── AUSTRALIA.json                # Full extracted dataset
│   │   ├── AUSTRALIA.csv                 # CSV format
│   │   ├── manually_cleaned/
│   │   │   └── AUSTRALIA.json            # Quality-controlled version
│   │   └── 1995/
│   │       ├── all_decisions/
│   │       │   └── AUSTRALIA.csv         # 1995+ all decisions
│   │       └── approved/
│   │           └── AUSTRALIA.csv         # 1995+ approved only
│   ├── eval_data/                        # Evaluation sample lists
│   ├── inference_data/
│   │   ├── Australia.txt                 # Full inference list
│   │   └── Australia_clean.txt           # Cleaned list
│   └── randomized_data/
│       └── Australia_*.txt               # Random subsets for evaluation
└── output/
    ├── 20250729_TGA_gpt-4o.json          # Latest extraction
    └── 20250729_TGA_gpt-4o.csv
```

### Evaluation Pipeline
**Manually annotated TGA records**: 30 drugs in `data/annotations/Drug_Approval_Annotations_all_datasets-Sheet1_cleaned.csv`

**Evaluation workflow**:
1. Random sampling: `./run_randomize_data.sh` → `data/randomized_data/Australia_*.txt`
2. Manual annotation: Expert review of sampled records
3. LLM prediction: `src/evaluation/generate_predictions.py --dataset TGA`
4. Comparison: `src/evaluation/evaluate.py` calculates metrics
5. Analysis: Field-specific accuracy, error patterns

### Generation Pipeline
```bash
# Generate predictions for TGA dataset
python src/evaluation/generate_predictions.py \
  --dataset TGA \
  --model gpt-4o \
  --output output/20250729_TGA_gpt-4o.json

# Convert to CSV
python src/utils/json_to_csv.py \
  --input output/20250729_TGA_gpt-4o.json \
  --output output/20250729_TGA_gpt-4o.csv

# Extract disease classifications
python src/utils/extract_from_columns.py \
  --input output/20250729_TGA_gpt-4o.json \
  --columns Indication_requested Indication_approved
```

## Best Practices

### Data Collection
1. **Maintain PDF list**: Keep `TGA_list.txt` updated with new AusPARs
2. **Version control**: Track extraction dates and model versions
3. **Backup downloads**: Store original PDFs securely

### Extraction Quality
1. **Page limits**: Use first 40 pages for TGA (balances coverage and efficiency)
2. **Temperature setting**: Keep at 0.1 for reproducibility
3. **Model selection**: GPT-4o recommended for accuracy
4. **Validation**: Spot-check random samples after extraction

### Data Standardization
1. **Lowercase conversion**: Apply consistently across all text fields
2. **Date format**: Standardize to DD.MM.YYYY
3. **Missing values**: Use consistent NaN/null handling
4. **Agency identifier**: Always include "AUSTRALIA" and "TGA" fields

### Integration
1. **Cross-dataset joins**: Use `Non_proprietary_name` + `Decision_year` for matching
2. **Temporal analysis**: Ensure consistent year filtering (≥1995)
3. **Decision types**: Standardize to approved/withdrawn/refused/conditional/temporary

## References and Resources

### TGA Official Resources
- **TGA Website**: https://www.tga.gov.au
- **AusPAR Database**: https://www.tga.gov.au/products/medicines/prescription-medicines/artg-auspar
- **ARTG Search**: https://www.tga.gov.au/artg

### Documentation
- **FDA Dataset Creation**: `docs/FDA_dataset_creation.md`
- **Health Canada Dataset Creation**: `docs/HealthCanada_dataset_creation.md`
- **Main README**: `README.md`

### Related Scripts
- **Question-Response Schema**: `src/extraction/question_response.py::TGA_pairs`
- **Generation Script**: `src/evaluation/generate_predictions.py`
- **Consolidation Notebook**: `src/consolidate_datasets.ipynb`

## Summary

The TGA (Australia) dataset represents a crucial component of the DrugFork multi-agency comparison study. With ~1,042 drug approvals from 1995 onwards, it provides:

1. **Southern hemisphere perspective**: Complements Northern hemisphere regulatory data
2. **English-language reports**: Facilitates direct comparison with FDA and EMA
3. **Medium-sized dataset**: Balances between small agencies (Swissmedic) and large ones (FDA)
4. **High-quality assessments**: Detailed AusPARs enable reliable extraction

The automated LLM-based extraction pipeline achieves high accuracy with minimal manual curation, making it feasible to process the complete TGA dataset. The resulting standardized data integrates seamlessly with other agencies for comparative regulatory science research, supporting evidence-based policy analysis and drug development strategy optimization.
