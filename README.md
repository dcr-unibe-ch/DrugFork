# DrugFork: A Multi-Agency Drug Approval Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔬 Overview

DrugFork is a comprehensive medical data science project that systematically analyzes and compares drug approval processes across **6 major regulatory agencies worldwide**. This repository contains tools for data extraction, processing, and analysis of public assessment reports (PARs) from regulatory authorities, enabling large-scale comparative studies of drug approvals, non-clinical data requirements, and regulatory decision-making processes.

### Key Statistics

- **🌍 6 Regulatory Agencies**: EMA, FDA, PMDA (Japan), TGA (Australia), Swissmedic (Switzerland), Health Canada
- **📊 50,667 Drug Records**: Comprehensive dataset spanning multiple decades
- **🔍 Detailed Annotations**: 280+ manually curated drug approval reports with extensive metadata
- **🧪 Non-clinical Data**: Extracted pharmacology, pharmacokinetics, and toxicology information

## 🎯 Objectives

This project aims to:

1. **Standardize** drug approval data across different regulatory frameworks
2. **Extract** structured information from unstructured public assessment reports (PDFs)
3. **Analyze** non-clinical requirements and study designs across agencies
4. **Enable** comparative research on regulatory decision-making
5. **Provide** open-source tools for medical data science research

## 🏛️ Regulatory Agencies Covered

### 1. **EMA (European Medicines Agency)** 🇪🇺
- **Region**: European Union
- **Dataset Size**: 4,237 records
- **Document Type**: European Public Assessment Reports (EPARs)

### 2. **FDA (Food and Drug Administration)** 🇺🇸
- **Region**: United States
- **Dataset Size**: 28,288 records
- **Document Type**: FDA Approval Packages, Drug Labels

### 3. **PMDA (Pharmaceuticals and Medical Devices Agency)** 🇯🇵
- **Region**: Japan
- **Dataset Size**: 409 records
- **Document Type**: Japanese Public Assessment Reports

### 4. **TGA (Therapeutic Goods Administration)** 🇦🇺
- **Region**: Australia
- **Dataset Size**: 1,050 records
- **Document Type**: Australian Public Assessment Reports (AusPARs)

### 5. **Swissmedic** 🇨🇭
- **Region**: Switzerland
- **Dataset Size**: 234 records
- **Document Type**: Swiss Public Assessment Reports (SwissPARs)

### 6. **Health Canada** 🇨🇦
- **Region**: Canada
- **Dataset Size**: 16,449 records
- **Document Type**: Product Monographs, Regulatory Decision Summaries

## 📚 Dataset Description

### Main Dataset
The primary dataset (`data/Drug_Approval_Annotations_all_datasets-Sheet1.csv`) contains 280+ manually annotated drug approval records with comprehensive metadata including:

#### Core Drug Information
- Drug name (proprietary and non-proprietary)
- Marketing authorization number and holder
- Drug class (biologics, small molecules, vaccines, cell/gene therapy)
- Pharmaceutical form and administration route
- Decision status and dates

#### Regulatory Information
- Application and decision dates
- Approval status (approved, withdrawn, temporary authorization)
- Orphan drug designation
- Indication (requested vs. approved)
- Disease classifications
- Referral information

#### Non-clinical Data (Extracted from Assessment Reports)
- **Pharmacology Studies**: Species, strain, model, sex, outcomes, adverse findings
- **Pharmacokinetics**: ADME (Absorption, Distribution, Metabolism, Excretion) data
- **Toxicology**: Species, models, outcomes, adverse events
- **Special Studies**: Genotoxicity, carcinogenicity, reproduction toxicity, immunogenicity

### Complete Datasets
Full datasets for each agency are available in `data/datasets/`:
- `EMA.csv` / `EMA.json` (4,237 records)
- `FDA.csv` / `FDA.json` (28,288 records)
- `JAPAN.csv` / `JAPAN.json` (409 records)
- `AUSTRALIA.csv` / `AUSTRALIA.json` (1,050 records)
- `SWISSMEDIC.csv` / `SWISSMEDIC.json` (234 records)
- `HEALTHCANADA.csv` / `HEALTHCANADA.json` (16,449 records)

## 🛠️ Repository Structure

```
DrugFork/
├── data/                           # All data files
│   ├── annotations/                # Manual annotations
│   ├── datasets/                   # Processed datasets by agency
│   ├── eval_data/                  # Evaluation datasets
│   ├── inference_data/             # Data for model inference
│   ├── randomized_data/            # Randomized data for evaluation
│   ├── Australia/                  # TGA raw data
│   ├── EMA/                        # EMA raw data
│   ├── FDA/                        # FDA raw data
│   ├── HealthCanada/               # Health Canada raw data
│   ├── Japan/                      # PMDA raw data
│   ├── Swissmedic/                 # Swissmedic raw data
│   └── Disease_burden_mapping/     # Disease classification mappings
├── src/                            # Source code
│   ├── parse_pdf.py                # PDF parsing utilities
│   ├── extract_from_columns.py     # Data extraction tools
│   ├── generate_predictions.py     # ML model predictions
│   ├── evaluate.py                 # Evaluation scripts
│   ├── schema.py                   # Data schema definitions
│   ├── ema_download/               # EMA data download tools
│   ├── fda_download/               # FDA data download tools
│   ├── health_canada_download/     # Health Canada download tools
│   ├── preprocess_AusPAR/          # Australia preprocessing
│   └── preprocess_FDA/             # FDA preprocessing
├── inference/                      # Model inference outputs
│   └── combined/                   # Combined analysis results
├── analysis/                       # Analysis outputs
│   ├── all_decisions/              # All decision analyses
│   └── approved/                   # Approved drugs analyses
├── assets/                         # Project assets
├── logs/                           # Processing logs
├── output/                         # General outputs
├── requirements.txt                # Python dependencies
└── run_*.sh                        # Execution scripts
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
# Load EMA dataset
ema_df = pd.read_csv('data/datasets/EMA.csv')

# Load FDA dataset
fda_df = pd.read_csv('data/datasets/FDA.csv')

# Compare approval counts
print(f"EMA approvals: {len(ema_df[ema_df['Decision'] == 'approved'])}")
print(f"FDA approvals: {len(fda_df[fda_df['Decision'] == 'approved'])}")
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
| `Decision` | Regulatory decision | approved, withdrawn, refused |
| `Decision_date` | Date of approval decision | 2021-03-15 |
| `Indication_approved` | Approved medical use | Treatment of metastatic melanoma |
| `Disease_class(es)` | Disease categories | Neoplasms, Infectious diseases |
| `Orphan_drug_status` | Orphan designation | yes, no |
| `Nonclinical_pharmacology_*` | Preclinical study details | Species, models, outcomes |
| `Nonclinical_pharmacokinetics_*` | ADME study data | Distribution, metabolism data |
| `Nonclinical_toxicology_*` | Toxicity study details | Species, adverse events |

See `src/schema.py` for the complete data schema definition.

## 🔧 Available Scripts

### Data Processing
- `run_parse_pdf.sh` - Extract text and data from PDF documents
- `run_clean_filenames.sh` - Standardize file naming conventions
- `run_combine_datasets_csv.sh` - Merge datasets from different agencies
- `run_extract_from_columns.sh` - Extract specific data columns

### Model & Evaluation
- `run_generate_predictions.sh` - Generate ML model predictions
- `run_eval_with_llm.sh` - Evaluate using language models
- `run_evaluate.sh` - Run evaluation metrics
- `run_create_evaluation_sheet.sh` - Create evaluation spreadsheets

### Data Preparation
- `run_randomize_data.sh` - Randomize data for evaluation
- `run_remove_eval_from_inference.sh` - Separate evaluation/inference sets
- `run_combine_eval_inference.sh` - Combine evaluation results

## 🔬 Research Applications

This dataset enables various research questions:

1. **Comparative Regulatory Science**
   - How do approval timelines differ across agencies?
   - What are the differences in non-clinical data requirements?

2. **Drug Development Analysis**
   - Which drug classes have highest approval rates?
   - What animal models are most commonly used?

3. **Safety & Efficacy Assessment**
   - How do toxicology requirements vary by drug class?
   - What are common adverse findings in preclinical studies?

4. **Machine Learning & NLP**
   - Automated extraction of structured data from reports
   - Prediction of approval outcomes
   - Classification of drug indications

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
@misc{drugfork2025,
  title={DrugFork: A Multi-Agency Drug Approval Dataset for Medical Data Science},
  author={{Ineichen Research Group}},
  year={2025},
  publisher={GitHub},
  howpublished={\url{https://github.com/Ineichen-Group/DrugFork}},
  note={Accessed: 2025-01-14}
}
```

## 📞 Contact & Support

- **Issues**: Please use the GitHub issue tracker
- **Project Planning**: [Google Doc](https://docs.google.com/document/d/1er_b-P0t4VZV8D_rDrC07WQxEI5QWUZx2Vs_6W2GFDA/edit?usp=sharing)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All regulatory agencies for making public assessment reports available
- The medical data science community
- Contributors to open-source tools used in this project

## ⚠️ Disclaimer

This dataset is compiled from publicly available information for research purposes. Users should verify critical information with official regulatory sources. The authors are not responsible for any decisions made based on this data.

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Maintained by**: Ineichen-Group
