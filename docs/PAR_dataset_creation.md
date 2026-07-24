# EMA and Swissmedic Dataset Creation Documentation

## Overview
The EMA and Swissmedic datasets are created with the same LLM-assisted extraction pipeline from public assessment reports. The goal is to keep both agencies aligned enough for comparison while still preserving the agency-specific wording and document structure in each source.

### Shared Characteristics
- Document type: public assessment reports
- Extraction method: PDF parsing followed by structured question-answer extraction
- Data structure: 24 standardized fields
- Time period: 1995 onward
- Automation level: mostly automated, with optional manual review

### Agency-Specific Overview

| Feature | EMA | Swissmedic |
|---|---|---|
| Region | European Union | Switzerland |
| Dataset size (1995+) | Larger | Smaller |
| Document name | EPAR | SwissPAR |
| Document length | Often 50-100+ pages | Often 40-70 pages |
| Language | English | English, German, French |
| Max pages parsed | 70 pages | 70 pages |
| Market context | Pan-European | National |

## Data Sources

### 1. EMA (European Medicines Agency)

#### Primary Source: European Public Assessment Reports (EPARs)
- Location: `data/EMA/downloads/`
- Document format: `[drug-name]-epar-public-assessment-report_en.pdf`
- Source website: https://www.ema.europa.eu/en/medicines
- Content: summary of product characteristics, clinical evaluation, risk management, and committee opinion

#### Supplementary Database
- File: `data/EMA/EMA.csv`
- Source: EMA medicines database export
- Content: marketing authorization numbers, dates, therapeutic areas, and INN names

#### Document List
- File: agency-specific lists under `data/eval_data/` and `data/inference_data/`
- Total count: roughly 1,687 EPARs for the 1995+ slice used in this project

### 2. Swissmedic (Swiss Agency for Therapeutic Products)

#### Primary Source: Swiss Public Assessment Reports (SwissPARs)
- Location: `data/Swissmedic/downloads/`
- Document format: `swisspar_[drug-name]_[version].pdf`
- Source website: https://www.swissmedic.ch/
- Content: product information, benefit-risk evaluation, clinical and non-clinical review, and regulatory decision documentation

#### Document List
- File: `data/Swissmedic/Swissmedic_list.txt`
- Total count: about 235 SwissPARs in the working dataset
- Languages: German, French, and English versions appear in the source set

## Dataset Creation Workflow

The same workflow applies to EMA and Swissmedic, with the prompt schema and source naming adjusted per agency.

### Step 1: Download Public Assessment Reports

#### EMA Download
**Script**: `src/download/ema_download/download_epars.py`

**Process**:
1. Access the EMA medicines database.
2. Identify approved drugs with EPARs.
3. Download the PDF assessment reports.
4. Store them with standardized names.

**Output**: `data/EMA/downloads/[drug-name]-epar-public-assessment-report_en.pdf`

#### Swissmedic Download
**Process**: manual or semi-automated
- Access the Swissmedic SwissPAR database.
- Download reports, preferring English versions when available.
- Store them with drug-name identifiers.

**Output**: `data/Swissmedic/downloads/swisspar_[drug-name].pdf`

### Step 2: Parse PDFs and Extract Structured Data

**Script**: `src/evaluation/generate_predictions.py`

**Question-response schemas**:
- EMA: `src/extraction/question_response.py::EMA_pairs`
- Swissmedic: `src/extraction/question_response.py::Swissmedic_pairs`

**Extraction configuration**:

```python
def handle_file(file_path, dataset_name):
        reader = PdfReader(file_path)
        max_pages = 70
        text = "".join([page.extract_text() for page in reader.pages[:max_pages]])
        return text
```

#### Extracted Fields (24 standardized fields)

The same field set is used across the project, with small wording differences between agency prompts.

##### 1. Identification & Authorization
- Marketing_authorisation_number
- Procedure_number
- Marketing_authorisation_holder
- Marketing_authorisation_holder_extracted

##### 2. Drug Characteristics
- Drug_name
- Non_proprietary_name
- Drug_class
- Pharmaceutical_form
- Administration_route

##### 3. Regulatory Decision
- Decision
- Current_status
- Decision_date
- Decision_year
- Application_date
- Application_year

##### 4. Indication & Classification
- Indication_requested
- Indication_approved
- Indication_extended
- Disease_class(es)
- Indication_requested_extracted
- Indication_approved_extracted

##### 5. Additional Information
- Orphan_drug_status
- Nonclinical_abridged
- Referral_body

#### Agency-Specific Question Variations

**Marketing authorization number**:
- EMA: use the EMA product number format.
- Swissmedic: use the five-digit authorization number when present.

**Decision date**:
- EMA: ask for the decision date.
- Swissmedic: ask for the final decision date.

**Document location hints**:
- EMA: look near the first page and the assessment summary.
- Swissmedic: the first page usually contains the key identifiers.

#### LLM Configuration

**Model**: GPT-4o by default, with compatible alternatives where needed.

**Parameters**:
- Temperature: 0.1
- Max tokens: 4000
- Page limits: 70 pages for both agencies in the current workflow

**Execution**:

```bash
python src/evaluation/generate_predictions.py \
    --dataset EMA \
    --model gpt-4o \
    --output output/YYYYMMDD_EMA_gpt-4o.json

python src/evaluation/generate_predictions.py \
    --dataset Swissmedic \
    --model gpt-4o \
    --output output/YYYYMMDD_Swissmedic_gpt-4o.json
```

**Output format**: JSON keyed by document filename.

### Step 3: Convert to CSV Format

**Script**: `src/utils/json_to_csv.py`

```bash
python src/utils/json_to_csv.py \
    --input output/YYYYMMDD_EMA_gpt-4o.json \
    --output output/YYYYMMDD_EMA_gpt-4o.csv

python src/utils/json_to_csv.py \
    --input output/YYYYMMDD_Swissmedic_gpt-4o.json \
    --output output/YYYYMMDD_Swissmedic_gpt-4o.csv
```

**Process**:
- Transpose nested JSON into tabular format.
- Treat each document as one row.
- Preserve all extracted fields as columns.

### Step 4: Extract Disease Classifications

**Script**: `src/utils/extract_from_columns.py`

```bash
./run_extract_from_columns.sh
```

**Input**: the extracted JSON or CSV files with indication fields.

**Process**:
1. Extract disease names from the requested and approved indication fields.
2. Map them to ICD-11 disease classes.
3. Normalize the classification labels for later analysis.

### Step 5: Manual Review and Quality Control (Optional)

**Goal**: catch prompt drift, OCR issues, and malformed JSON before downstream analysis.

**Typical checks**:
- Missing authorization numbers
- Wrong decision labels
- Broken indication extraction
- Unexpected empty values after parsing

### Step 6: Filter to 1995+ and Standardize

**Goal**: keep only the time window used in the rest of the DrugFork analysis.

**Standardization tasks**:
- Normalize dates
- Normalize drug names
- Standardize agency labels
- Keep a consistent column order across datasets

## Agency-Specific Characteristics

### EMA (European Medicines Agency)

#### Unique Features
- Large and relatively consistent document set.
- Strong CHMP-centered assessment structure.
- Clear EPAR naming and metadata conventions.

#### Data Quality Considerations
- Some older reports use less consistent formatting.
- Drug and procedure identifiers may require cleaning.
- Authorization dates are usually easier to recover than indication wording.

### Swissmedic (Swiss Agency for Therapeutic Products)

#### Unique Features
- Smaller dataset, but still useful for comparison.
- Reports can appear in multiple languages.
- SwissPAR structure is usually concise compared with EPARs.

#### Data Quality Considerations
- Language variation can affect extraction consistency.
- File naming is less uniform than EMA.
- Some reports require extra attention when matching the drug name to metadata.

## Comparison Summary

### Regulatory Framework Comparison

| Aspect | EMA | Swissmedic |
|---|---|---|
| Market access | EU-wide | Switzerland only |
| Regulatory structure | Centralized European process | National process |
| Public report style | EPAR | SwissPAR |
| Typical review length | Longer | Shorter |

### Extraction Performance

| Metric | EMA | Swissmedic |
|---|---|---|
| Authorization number extraction | High | High |
| Decision date extraction | High | High |
| Indication extraction | Moderate to high | Moderate to high |
| Overall consistency | Strong | Good |

## Integration with DrugFork Pipeline

### File Locations

- Raw PDFs live under `data/EMA/` and `data/Swissmedic/`.
- Prediction outputs land in `output/`.
- Derived tables and summaries feed into `analysis/` and `evaluation/`.

### Evaluation Pipeline

1. Parse PDFs and generate predictions.
2. Convert predictions to CSV.
3. Run disease extraction and standardization.
4. Feed the cleaned tables into analysis notebooks and summary scripts.

### Generation Pipeline

The generator is the main bridge between PDF sources and structured tables. It should be rerun whenever prompts, PDF sources, or naming conventions change.

## Best Practices

### Data Collection
- Keep source directories separate by agency.
- Use consistent filenames for new downloads.
- Track any manual fixes in a lightweight log.

### Extraction Quality
- Check a sample of files from each agency before large batch runs.
- Re-run a few known examples after prompt changes.
- Treat empty fields as a signal to inspect the PDF rather than as valid output.

### Agency-Specific Tips
- EMA: check procedure and authorization numbers early, because they anchor the rest of the record.
- Swissmedic: verify the language and file version before parsing.

### Data Standardization
- Keep agency labels stable.
- Normalize dates and capitalization before analysis.
- Use one shared schema for the final CSV files.

### Cross-Agency Integration
- Build shared tables only after agency-specific cleaning is complete.
- Do not mix raw extraction output with standardized analysis data.
- Preserve source filenames so records can be traced back to the original PDF.

## Usage in Research and Analysis

### 1. Multi-Agency Comparison Studies
- Compare approval timing.
- Compare decision language.
- Compare drug-class patterns across the two agencies.

### 2. Regulatory Standards Comparison
- Inspect how the agencies structure public assessment reports.
- Compare what information is emphasized or omitted.
- Review differences in the amount of detail available for the same drug.

### 3. Therapeutic Area Analysis
- Group drugs by disease class.
- Compare which therapeutic areas appear more frequently in each agency.
- Trace trends over time within the shared 1995+ window.

### 4. Model Benchmarking
- Evaluate extraction accuracy on the same field set.
- Compare error patterns across the two document styles.
- Use shared schema outputs for downstream LLM evaluation.

## References and Resources

### Official Resources
- EMA medicines database: https://www.ema.europa.eu/en/medicines
- Swissmedic public assessment reports: https://www.swissmedic.ch/

### Documentation
- `docs/README.md`
- `docs/Metadata_Agencies.md`

### Related Scripts
- `src/download/ema_download/download_epars.py`
- `src/evaluation/generate_predictions.py`
- `src/utils/json_to_csv.py`
- `src/utils/extract_from_columns.py`

## Summary
EMA and Swissmedic use a shared extraction pipeline, but each agency still has distinct naming conventions, report structures, and data-quality quirks. The project keeps the shared schema small enough for comparison while preserving the agency-specific details needed for careful analysis.