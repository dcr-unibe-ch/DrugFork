"""
Helper functions for loading preprocessed burden data.
"""

import pandas as pd
import os


def get_burden_data_path(measure="Deaths"):
    """
    Get the path to preprocessed burden data for a given measure.
    
    Parameters:
    -----------
    measure : str
        The measure name (e.g., "Deaths", "DALYs (Disability-Adjusted Life Years)", "Prevalence")
        
    Returns:
    --------
    str
        Path to the preprocessed CSV file
    """
    # Normalize measure name for filename
    safe_measure_name = measure.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    
    # Get path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    data_path = os.path.join(project_root, "data", "Disease_burden_mapping", 
                             "preprocessed", f"burden_{safe_measure_name}.csv")
    
    return data_path


def load_burden_data(measure="Deaths"):
    """
    Load preprocessed burden data for a given measure.
    
    Parameters:
    -----------
    measure : str
        The measure name (e.g., "Deaths", "DALYs (Disability-Adjusted Life Years)", "Prevalence")
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed burden data with columns: Year, Disease_class, <measure>
        
    Raises:
    -------
    FileNotFoundError
        If the preprocessed data file doesn't exist
    """
    data_path = get_burden_data_path(measure)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Preprocessed burden data not found: {data_path}\n"
            f"Please run: python src/burden_mapping/preprocess_burden_data.py"
        )
    
    df = pd.read_csv(data_path)
    print(f"Loaded burden data: {len(df)} records, {df['Disease_class'].nunique()} disease classes")
    print(f"  Year range: {df['Year'].min()} - {df['Year'].max()}")
    
    return df


# Canonical disease classes for reference
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


def extract_canonical_classes(text):
    """
    Extract canonical disease classes from text using substring matching.
    
    This function is useful for mapping disease classes in drug approval datasets
    to the canonical classes used in burden data.
    
    Parameters:
    -----------
    text : str
        Text to search for disease classes
        
    Returns:
    --------
    list
        List of found canonical disease classes
    """
    if not isinstance(text, str):
        return []
    
    canon_map = {c.lower(): c for c in CANONICAL_CLASSES}
    t = " ".join(text.strip().split()).lower()
    found, seen = [], set()
    
    for cls_low, cls in canon_map.items():
        if cls_low in t and cls not in seen:
            found.append(cls)
            seen.add(cls)
    
    return found
