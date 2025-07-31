#!/bin/bash

echo "Combining datasets into a single CSV file..."

INPUT_FILES=(
    "inference/combined/with_extracted_data/JAPAN.csv"
    # "inference/combined/with_extracted_data/AUSTRALIA.csv"
    "inference/combined/with_extracted_data/EMA.csv"
    "inference/combined/with_extracted_data/SWISSMEDIC.csv"
)

python ./src/combine_datasets_csv.py \
    --input_files "${INPUT_FILES[@]}" \
    --output_file "inference/combined/with_extracted_data/combined_datasets_shuffled.csv"

echo "Combined datasets saved to inference/combined/with_extracted_data/combined_datasets_shuffled.csv"