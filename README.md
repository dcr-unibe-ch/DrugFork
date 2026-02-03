# DrugFork: A Multi-Agency Drug Approval Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔬 Overview

DrugFork is a comprehensive medical data science project that systematically analyzes and compares drug approval processes across **6 major regulatory agencies worldwide** from **1995 to present**. This repository contains **separate automated pipelines for each dataset** for extracting structured data from public assessment reports (PARs) using large language models. The project focuses exclusively on **approved drugs from 1995 onwards**, enabling large-scale comparative studies of successful drug approvals and regulatory decision-making.

### Key Statistics (1995-Current)

- **🌍 6 Regulatory Agencies**: EMA, FDA, PMDA (Japan), TGA (Australia), Swissmedic (Switzerland), Health Canada
- **📊 32,000+ Approved Drug Records**: Approved drugs from 1995 onwards across all agencies
- **🔍 282 Manually Curated Records**: High-quality ground truth for evaluation (157 EMA, 65 Swissmedic, 30 PMDA, 30 TGA)
- **🤖 Agency-Specific Pipelines**: Separate extraction pipelines tailored to each regulatory agency's data format

## 🎯 Objectives

This project aims to:

1. **Standardize** drug approval data across different regulatory frameworks
2. **Extract** structured information from approved drugs using agency-specific pipelines
3. **Analyze** successful drug approvals and study designs across agencies (1995-present)
4. **Enable** comparative research on regulatory approval patterns
5. **Provide** open-source tools and separate pipelines for each regulatory agency

## 🏛️ Regulatory Agencies Covered (1995-Present)

### 1. **EMA (European Medicines Agency)** 🇪🇺
- **Region**: European Union
- **Dataset Size (1995+)**: ~1,687 records
- **Document Type**: European Public Assessment Reports (EPARs)

### 2. **FDA (Food and Drug Administration)** 🇺🇸
- **Region**: United States
- **Dataset Size (1995+)**: ~18,558 records
- **Document Type**: FDA Approval Packages, Drug Labels

### 3. **PMDA (Pharmaceuticals and Medical Devices Agency)** 🇯🇵
- **Region**: Japan
- **Dataset Size (1995+)**: ~409 records
- **Document Type**: Japanese Public Assessment Reports

### 4. **TGA (Therapeutic Goods Administration)** 🇦🇺
- **Region**: Australia
- **Dataset Size (1995+)**: ~1,042 records
- **Document Type**: Australian Public Assessment Reports (AusPARs)

### 5. **Swissmedic** 🇨🇭
- **Region**: Switzerland
- **Dataset Size (1995+)**: ~230 records
- **Document Type**: Swiss Public Assessment Reports (SwissPARs)

### 6. **Health Canada** 🇨🇦
- **Region**: Canada
- **Dataset Size (1995+)**: ~10,286 records
- **Document Type**: Product Monographs, Regulatory Decision Summaries

## 📚 Dataset Description

### Main Datasets (Approved Drugs, 1995-Current)

The primary datasets are located in `data/datasets/1995/approved/` and contain **approved drug records from 1995 onwards only**. Each regulatory agency has its own **dedicated extraction pipeline** tailored to that agency's specific data format. Each record includes **24 standardized fields** extracted automatically from assessment reports:

#### Identification & Authorization
- **Marketing_authorisation_number**: Regulatory product identifier
- **Procedure_number**: Application procedure identifier
- **Document_name**: Source PDF filename
- **Marketing_authorisation_holder**: Company holding the authorization
- **Marketing_authorisation_holder_extracted**: Extracted company name
- **Agency**: Regulatory agency (EMA, FDA, PMDA, TGA, Swissmedic, HealthCanada)

#### Drug Characteristics
- **Drug_name**: Proprietary/brand name
- **Non_proprietary_name**: Generic/INN name
- **Drug_class**: Classification (Small molecule, Biologics, Peptides and proteins, Cell and gene therapy, Vaccine, Other)
- **Pharmaceutical_form**: Formulation (tablet, solution for injection, capsule, etc.)
- **Administration_route**: Route of administration (oral, intravenous, subcutaneous, etc.)

#### Regulatory Decision
- **Decision**: Approval outcome (approved only in this dataset)
- **Current_status**: Current authorization status (authorised, withdrawn, revoked, NA)
- **Decision_date**: Date of regulatory decision
- **Decision_year**: Year of decision (1995-2025)
- **Application_date**: Date of initial application
- **Application_year**: Year of application

#### Indication & Classification
- **Indication_requested**: Original indication sought by applicant
- **Indication_extended**: Extended/additional indications
- **Indication_approved**: Final approved indication(s)
- **Disease_class(es)**: Disease categories (based on ICD-11 classification)

#### Additional Information
- **Orphan_drug_status**: Orphan designation (yes/no)
- **Nonclinical_abridged**: Whether non-clinical data was abbreviated (yes/no)
- **Referral_body**: Referral information if applicable

### Datasets Structure

The project focuses exclusively on **approved drugs from 1995 onwards**, with separate processing pipelines for each regulatory agency:

```
data/datasets/1995/
└── approved/                  # Approved drugs only (1995-present)
    ├── EMA.csv
    ├── FDA.csv
    ├── PMDA.csv
    ├── TGA.csv
    ├── Swissmedic.csv
    ├── HealthCanada.csv
    └── Overall.csv           # Combined dataset across all agencies
```

Each dataset is generated using an **agency-specific pipeline** tailored to that regulatory body's data format and structure.

## 🛠️ Repository Structure

```
DrugFork/
├── data/                           # All data files
│   ├── datasets/                   # Processed datasets
│   │   └── 1995/                   # 1995-current subset (approved drugs only)
│   │       └── approved/           # Approved drugs (primary dataset)
│   ├── annotations/                # Manual annotations for evaluation
│   ├── eval_data/                  # Evaluation sample lists
│   ├── inference_data/             # Inference sample lists
│   ├── EMA/                        # EMA raw PDFs
│   ├── PMDA/                       # PMDA raw PDFs
│   ├── TGA/                        # TGA raw PDFs
│   ├── Swissmedic/                 # Swissmedic raw PDFs
│   ├── HealthCanada/               # Health Canada raw data
│   ├── FDA/                        # FDA raw data
│   └── Disease_burden_mapping/     # Disease classification mappings
├── src/                            # Source code (organized by function)
│   ├── evaluation/                 # Evaluation pipeline
│   │   ├── run_evaluation_pipeline.py
│   │   ├── data_preparation.py
│   │   ├── generate_predictions.py
│   │   ├── create_evaluation_sheet.py
│   │   ├── evaluate.py
│   │   ├── eval_with_llm.py
│   │   └── combine_eval_inference.py
│   ├── extraction/                 # Data extraction schemas & prompts
│   │   ├── schema.py               # JSON validation schemas
│   │   └── question_response.py   # Agency-specific prompts
│   ├── preprocessing/              # Data preprocessing
│   │   ├── parse_pdf.py
│   │   ├── clean_filenames.py
│   │   ├── randomize_data.py
│   │   └── preprocess_FDA/         # FDA-specific preprocessing
│   ├── utils/                      # General utilities
│   │   ├── combine_datasets_csv.py
│   │   ├── json_to_csv.py
│   │   └── extract_from_columns.py
│   ├── download/                   # Download scripts by agency
│   │   ├── ema_download/
│   │   ├── fda_download/
│   │   └── health_canada_download/
│   └── *.ipynb                     # Analysis notebooks
├── analysis/                       # Analysis results
│   └── approved/                   # Approved drugs analyses (1995-present)
├── evaluation/                     # Evaluation pipeline outputs
│   ├── output/                     # Evaluation sheets (LLM vs human)
│   ├── processed_files/            # Manually assessed sheets
│   ├── results/                    # Metrics (JSON)
│   └── plots/                      # Visualizations
├── output/                         # LLM prediction outputs
├── config/                         # Configuration files
│   └── evaluation_config.yaml
├── requirements.txt                # Python dependencies
├── run_full_evaluation.sh          # Main evaluation pipeline
└── run_*.sh                        # Individual task scripts
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ineichen-Group/DrugFork.git
   cd DrugFork
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

#### 1. Explore the Main Dataset
```python
import pandas as pd

# Load the manually annotated dataset
df = pd.read_csv('data/Drug_Approval_Annotations_all_datasets-Sheet1.csv')

# Basic statistics
print(f"Total records: {len(df)}")
print(f"Agencies: {df['Origin'].value_counts()}")
print(f"Drug classes: {df['Drug_class'].value_counts()}")
```

#### 2. Load Agency-Specific Datasets
```python
# Load EMA approved drugs dataset (1995+)
ema_df = pd.read_csv('data/datasets/1995/approved/EMA.csv')

# Load FDA approved drugs dataset (1995+)
fda_df = pd.read_csv('data/datasets/1995/approved/FDA.csv')

# Compare approval counts (all records are approved)
print(f"EMA approvals since 1995: {len(ema_df)}")
print(f"FDA approvals since 1995: {len(fda_df)}")
```

#### 3. Extract Data from PDFs
```bash
# Parse PDF documents to extract drug information
./run_parse_pdf.sh
```

#### 4. Generate Predictions
```bash
# Run ML models to extract structured data
./run_generate_predictions.sh
```

## 📖 Data Schema

### Key Fields

| Field | Description | Example |
|-------|-------------|---------|
| `Origin` | Regulatory agency | EMA, FDA, PMDA, TGA, Swissmedic, Health Canada |
| `Drug_name` | Proprietary drug name | Keytruda, Humira |
| `Non_proprietary_name` | Generic/scientific name | pembrolizumab, adalimumab |
| `Drug_class` | Drug category | Biologics, Small molecule, Vaccine, Cell and gene therapy |
| `Decision` | Regulatory decision | approved (all records in dataset) |
| `Decision_date` | Date of approval decision (1995+) | 2021-03-15 |
| `Indication_approved` | Approved medical use | Treatment of metastatic melanoma |
| `Disease_class(es)` | Disease categories | Neoplasms, Infectious diseases |
| `Orphan_drug_status` | Orphan designation | yes, no |
| `Nonclinical_pharmacology_*` | Preclinical study details | Species, models, outcomes |
| `Nonclinical_pharmacokinetics_*` | ADME study data | Distribution, metabolism data |
| `Nonclinical_toxicology_*` | Toxicity study details | Species, adverse events |

See `src/schema.py` for the complete data schema definition.

## 🔧 Available Scripts

### 🚀 Unified Evaluation Pipeline (Recommended)

**Quick Start:**
```bash
# Run complete evaluation pipeline for a single dataset
./run_full_evaluation.sh EMA

# Run for all datasets
./run_full_evaluation.sh --all

# Use existing predictions and assessed sheets (fastest)
./run_full_evaluation.sh --all --no-split --use-existing-predictions --use-assessed-sheets
```

#### 📋 Complete Evaluation Workflow

The evaluation process consists of 4 main steps:

**Step 1: Data Preparation**
```bash
# Splits evaluation samples from inference datasets
./run_full_evaluation.sh --all
# Output: data/inference_data/*_clean.txt
```

**Step 2: Generate LLM Predictions**
```bash
# Runs LLM on evaluation set to extract drug information
./run_full_evaluation.sh EMA
# Output: output/YYYYMMDD_EMA_gpt-4o.json
```

**Step 3: Create Evaluation Sheets**
```bash
# Creates side-by-side comparison of LLM vs human annotations
# Output: evaluation/output/YYYYMMDD_EMA_gpt-4o.csv
# Format: Each field has three columns:
#   - field_llm: LLM's prediction
#   - field_human: Human annotation
#   - field_verdict_human: Empty (needs manual assessment)
```

**Step 4: Manual Assessment** *(Required - Not automated)*
- Open the evaluation sheet CSV file
- For each row, compare LLM vs human values
- Fill in the `_verdict_human` columns with:
  - `match` - LLM output matches human annotation
  - `no_match` - LLM output is incorrect
  - `partial_0.X` - Partial match (e.g., `partial_0.5` for 50% correct)
- Save the assessed file to: `evaluation/processed_files/YYYYMMDD_EMA_gpt-4o_assessed.csv`

**Step 5: Compute Metrics**
```bash
# Computes accuracy, precision, recall, F1 on assessed files
./run_full_evaluation.sh --all --use-assessed-sheets
# Output: 
#   - evaluation/results/YYYYMMDD_EMA_gpt-4o_assessed.csv.json
#   - evaluation/plots/YYYYMMDD_EMA_gpt-4o_assessed.png
```

#### 🎯 Pipeline Modes

**Full Pipeline (Fresh Start):**
```bash
./run_full_evaluation.sh --all
# Runs: Data split → LLM generation → Create eval sheets
# Then: Manually assess sheets → Run with --use-assessed-sheets
```

**Using Existing Predictions:**
```bash
./run_full_evaluation.sh --all --use-existing-predictions
# Skips: LLM generation (expensive)
# Uses: Most recent JSON files from output/ directory
```

**Using Assessed Sheets:**
```bash
./run_full_evaluation.sh --all --use-assessed-sheets
# Skips: Creating new eval sheets
# Uses: Manually assessed CSV files from evaluation/processed_files/
```

**Fast Mode (All Existing):**
```bash
./run_full_evaluation.sh --all --no-split --use-existing-predictions --use-assessed-sheets
# Skips: Data split, LLM generation, eval sheet creation
# Uses: All existing files, only computes metrics
# Note: When --use-assessed-sheets is set, new evaluation sheets are NOT created
#       The pipeline only looks for and uses existing *_assessed.csv files
```

#### ⚙️ Configuration

Edit `config/evaluation_config.yaml` to customize:
- Datasets to evaluate (EMA, Swissmedic, PMDA, TGA)
- Model parameters (name, temperature, max_tokens)
- File paths and directories
- Processing options (skip_if_exists, validate_split)

#### 📂 File Structure

```
DrugFork/
├── data/
│   ├── eval_data/                    # Evaluation sample lists
│   │   └── eval_EMA.txt
│   └── inference_data/               # Full dataset lists
│       ├── EMA.txt                   # Original full list
│       └── EMA_clean.txt             # After removing eval samples
├── output/                           # LLM predictions
│   └── 20250729_EMA_gpt-4o.json
├── evaluation/
│   ├── output/                       # Unassessed eval sheets (only created when needed)
│   │   └── 20250729_EMA_gpt-4o.csv   # Created ONLY without --use-assessed-sheets
│   ├── processed_files/              # Manually assessed sheets (required for metrics)
│   │   └── 20250717_EMA_gpt-4o_assessed.csv
│   ├── results/                      # Metrics JSON
│   │   └── 20250717_EMA_gpt-4o_assessed.csv.json
│   └── plots/                        # Visualization plots
│       └── 20250717_EMA_gpt-4o_assessed.png
```

**Individual Components:**
- `src/evaluation/` - Complete evaluation pipeline module
  - `run_evaluation_pipeline.py` - Main pipeline orchestrator
  - `data_preparation.py` - Data splitting and preparation
  - `generate_predictions.py` - LLM prediction generation
  - `create_evaluation_sheet.py` - Comparison sheet creation
  - `evaluate.py` - Metrics computation
  - `eval_with_llm.py` - LLM-based evaluation
  - `combine_eval_inference.py` - Result combination utility
- `src/extraction/` - Data extraction schemas and templates
  - `schema.py` - JSON validation schemas
  - `question_response.py` - Agency-specific prompt templates
- `src/preprocessing/` - Data preprocessing utilities
  - `parse_pdf.py` - PDF text extraction
  - `clean_filenames.py` - Filename standardization
  - `randomize_data.py` - Data randomization
- `src/utils/` - General utility scripts
  - `combine_datasets_csv.py` - Dataset merging
  - `json_to_csv.py` - Format conversion
  - `extract_from_columns.py` - Column extraction
- `config/evaluation_config.yaml` - Centralized configuration

### Data Processing Scripts
- `run_parse_pdf.sh` - Extract text and data from PDF documents
- `run_clean_filenames.sh` - Standardize file naming conventions
- `run_combine_datasets_csv.sh` - Merge datasets from different agencies
- `run_extract_from_columns.sh` - Extract specific data columns
- `run_randomize_data.sh` - Randomize data for sampling

### Additional Evaluation Utilities
- `run_eval_with_llm.sh` - LLM-based evaluation (standalone)
- `run_combine_eval_inference.sh` - Combine evaluation and inference results

> **Note:** Most evaluation workflows are now handled by the unified pipeline (`run_full_evaluation.sh`). Individual scripts remain available for specific tasks.

## 🔬 Research Applications

This dataset of approved drugs (1995-present) enables various research questions:

1. **Comparative Regulatory Science**
   - How do approval timelines differ across agencies?
   - What are the differences in non-clinical data requirements for successful approvals?

2. **Drug Development Analysis**
   - Which drug classes are most frequently approved?
   - What animal models are most commonly used in approved drugs?
   - How have approval patterns changed since 1995?

3. **Safety & Efficacy Assessment**
   - How do toxicology requirements vary by drug class in approved products?
   - What are common preclinical study designs in successful applications?

4. **Machine Learning & NLP**
   - Automated extraction of structured data using agency-specific pipelines
   - Pattern recognition in successful drug approvals
   - Classification of drug indications and disease classes

## 🤝 Contributing

We welcome contributions from the research community! Here's how you can help:

1. **Report Issues**: Found a bug or data inconsistency? Open an issue.
2. **Add Data**: Help annotate more drug approval reports.
3. **Improve Tools**: Enhance data extraction or analysis scripts.
4. **Share Research**: Use the dataset and share your findings.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 Data Extraction Protocol

For detailed information on the data extraction methodology, see:
- `assets/Protocol_PublicAssessmentReports.docx` - Complete extraction protocol

## 📊 Visualizations & Analysis

Jupyter notebooks for analysis are available in the `src/` directory:
- `paper_writing_jd.ipynb` - Publication-ready analyses and figures
- `analyze_output.ipynb` - Output analysis
- `consolidate_datasets.ipynb` - Dataset consolidation workflows
- `exploring_fda.ipynb` - FDA-specific analysis
- `exploring_canada.ipynb` - Health Canada-specific analysis

## 📝 Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{drugfork2026,
  title={DrugFork: Automated assessment of global patterns in drug approvals across six major regulatory agencies, 1995–2025},
  author={{TODO add authors}},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/Ineichen-Group/DrugFork}}
}
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TODO add

## ⚠️ Disclaimer

This dataset is compiled from publicly available information for research purposes. Users should verify critical information with official regulatory sources. The authors are not responsible for any decisions made based on this data.

---

**Last Updated**: January 2026  
**Version**: 1.0  
**Maintained by**: Ineichen-Group
