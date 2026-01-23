# Burden Mapping Utilities

This directory contains utilities for preprocessing and loading disease burden data.

## Files

- `preprocess_burden_data.py`: Script to preprocess global disease burden statistics and map them to standardized disease classes
- `burden_utils.py`: Helper functions for loading preprocessed burden data in notebooks and scripts

## Usage

### 1. Preprocess burden data (run once or when data updates)

```bash
python src/burden_mapping/preprocess_burden_data.py
```

This will:
- Load global disease burden statistics
- Apply disease class mapping
- Aggregate data by year and disease class
- Save preprocessed files to `data/Disease_burden_mapping/preprocessed/`

### 2. Load preprocessed data in notebooks

```python
from burden_mapping.burden_utils import load_burden_data, extract_canonical_classes

# Load burden data for a specific measure
burden_deaths = load_burden_data("Deaths")
burden_dalys = load_burden_data("DALYs (Disability-Adjusted Life Years)")
burden_prevalence = load_burden_data("Prevalence")

# Extract canonical disease classes from text
disease_classes = extract_canonical_classes("Diseases of the circulatory system")
```

## Output Files

Preprocessed data is saved to:
- `data/Disease_burden_mapping/preprocessed/burden_Deaths.csv`
- `data/Disease_burden_mapping/preprocessed/burden_DALYs_DisabilityAdjusted_Life_Years.csv`
- `data/Disease_burden_mapping/preprocessed/burden_Prevalence.csv`

Each file contains:
- `Year`: Year of the burden data
- `Disease_class`: Canonical disease class
- `<Measure>`: The burden measure value (Deaths, DALYs, or Prevalence)
