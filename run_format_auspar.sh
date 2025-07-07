#!/bin/bash


# ==========================================================

input_dir="./data/AusPAR/"
output_dir="./data/AusPAR/formatted/"
mkdir -p "$output_dir"

# ==========================================================

# iterate through all CSV files in the input directory
for file in "$input_dir"*.csv; do
    # extract the filename without the path
    filename=$(basename "$file")
    
    # construct the output file path
    output_file="$output_dir$filename"
    
    # run the Python script with the input and output file arguments
    python src/preprocess_AusPAR/format_auspar_csv.py \
        --input "$file" \
        --output "$output_file" \
        --delimiter "~" 
done
