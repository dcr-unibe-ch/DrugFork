"""
Preprocess disease burden data by mapping disease classes to standardized categories.

This script:
1. Loads global disease burden statistics
2. Applies disease class mapping using canonical categories
3. Aggregates burden data by year and disease class
4. Saves the preprocessed data for use in analysis
"""

import pandas as pd
import os
import sys


# Canonical disease classes matching the burden data
CANONICAL_CLASSES = [
    "Certain infectious and parasitic diseases",
    "Neoplasms",
    "Diseases of the blood and blood-forming organs",
    "Endocrine, nutritional and metabolic diseases",
    "Mental and behavioural disorders",
    "Diseases of the nervous system",
    "Diseases of the eye and adnexa",
    "Diseases of the ear",
    "Diseases of the circulatory system",
    "Diseases of the respiratory system",
    "Diseases of the digestive system",
    "Diseases of the skin",
    "Diseases of the musculoskeletal system and connective tissue",
    "Diseases of the genitourinary system",
    "Pregnancy and childbirth",
    "Congenital malformations and chromosomal abnormalities",
    "Injury, poisoning and certain other consequences of external causes",
    "Other",
]


def extract_canonical_classes(text, canon_map):
    """
    Extract canonical disease classes from text using substring matching.
    
    Parameters:
    -----------
    text : str
        Text to search for disease classes
    canon_map : dict
        Dictionary mapping lowercase canonical classes to proper case
        
    Returns:
    --------
    list
        List of found canonical disease classes
    """
    if not isinstance(text, str):
        return []
    
    t = " ".join(text.strip().split()).lower()
    found, seen = [], set()
    
    for cls_low, cls in canon_map.items():
        if cls_low in t and cls not in seen:
            found.append(cls)
            seen.add(cls)
    
    return found


def load_and_map_burden_data(burden_path, mapping_path, measure="Deaths", min_year=1995):
    """
    Load burden data and apply disease class mapping.
    
    Parameters:
    -----------
    burden_path : str
        Path to the global disease burden statistics CSV
    mapping_path : str
        Path to the disease class mapping CSV
    measure : str
        The measure to extract (e.g., "Deaths", "DALYs", "Prevalence")
    min_year : int
        Minimum year to include in the output (default: 1995)
        
    Returns:
    --------
    pd.DataFrame
        Aggregated burden data with columns: Year, Disease_class, <measure>
    """
    print(f"Loading burden data from: {burden_path}")
    print(f"Loading mapping from: {mapping_path}")
    print(f"Measure: {measure}")
    print(f"Filtering for years >= {min_year}")
    
    # Create canonical class mapping
    canon_map = {c.lower(): c for c in CANONICAL_CLASSES}
    
    # Load and prepare burden data
    burden_raw = pd.read_csv(burden_path)
    burden_data = burden_raw[
        (burden_raw["measure_name"] == measure) &
        (burden_raw["metric_name"] == "Number") &
        (burden_raw["age_name"] == "All ages") &
        (burden_raw["sex_name"] == "Both") &
        (burden_raw["location_name"] == "Global")
    ][["year", "cause_name", "val"]].copy()
    
    burden_data.columns = ["Year", "cause_name", measure]
    burden_data["cause_norm"] = burden_data["cause_name"].str.strip().str.lower()
    
    print(f"  Loaded {len(burden_data)} burden records")
    
    # Load mapping
    map_raw = pd.read_csv(mapping_path, header=None, dtype=str, encoding="utf-8-sig").fillna("")
    causes = map_raw.iloc[:, 0].astype(str).str.strip()
    
    # Build mapping dataframe
    mapping_rows = []
    for i, cause in enumerate(causes):
        for col in map_raw.columns[1:]:
            cell = str(map_raw.iat[i, col]).strip()
            if cell:
                for canonical in extract_canonical_classes(cell, canon_map):
                    mapping_rows.append((cause, canonical))
    
    mapping_df = pd.DataFrame(mapping_rows, columns=["cause_name", "Disease_class"])
    mapping_df["cause_norm"] = mapping_df["cause_name"].str.strip().str.lower()
    
    print(f"  Created mapping with {len(mapping_df)} entries")
    
    # Merge burden with mapping
    burden_mapped = burden_data.merge(
        mapping_df[["cause_norm", "Disease_class"]], 
        on="cause_norm", 
        how="left"
    )
    burden_mapped = burden_mapped.dropna(subset=["Disease_class"])
    burden_mapped[measure] = pd.to_numeric(burden_mapped[measure], errors="coerce").clip(lower=0)
    
    print(f"  Mapped {len(burden_mapped)} burden records to disease classes")
    
    # Aggregate burden by year and disease class
    burden_agg = burden_mapped.groupby(["Year", "Disease_class"], as_index=False)[measure].sum()
    
    # Filter to specified year range
    burden_agg = burden_agg[burden_agg["Year"] >= min_year]
    
    print(f"  Final aggregated data: {len(burden_agg)} records")
    print(f"  Year range: {burden_agg['Year'].min()} - {burden_agg['Year'].max()}")
    print(f"  Disease classes: {burden_agg['Disease_class'].nunique()}")
    
    return burden_agg


def main():
    """
    Main function to preprocess burden data for different measures.
    """
    # Define paths (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    burden_path = os.path.join(project_root, "data", "Disease_burden_mapping", 
                               "Global_disease_burden_statistics_download.csv")
    mapping_path = os.path.join(project_root, "data", "Disease_burden_mapping", 
                                "Mapping_diseases_disease_classes.csv")
    
    output_dir = os.path.join(project_root, "data", "Disease_burden_mapping", "preprocessed")
    os.makedirs(output_dir, exist_ok=True)
    
    # Process different measures
    measures = ["Deaths", "Incidence", "Prevalence"]
    
    for measure in measures:
        print(f"\n{'='*60}")
        print(f"Processing: {measure}")
        print('='*60)
        
        try:
            burden_agg = load_and_map_burden_data(burden_path, mapping_path, measure=measure)
            
            # Save preprocessed data
            safe_measure_name = measure.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
            output_path = os.path.join(output_dir, f"burden_{safe_measure_name}.csv")
            burden_agg.to_csv(output_path, index=False)
            
            print(f"\n Saved: {output_path}")
            
        except Exception as e:
            print(f"\n Error processing {measure}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Preprocessing complete!")
    print('='*60)


if __name__ == "__main__":
    main()
