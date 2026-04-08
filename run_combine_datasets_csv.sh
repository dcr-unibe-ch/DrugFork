#!/bin/bash

echo "Combining datasets into a single CSV file..."

INPUT_FILES=(
    "evaluation/processed_files/20250717_TGA_gpt-4o_assessed.csv"
    "evaluation/processed_files/20250717_Swissmedic_gpt-4o_assessed.csv"
    "evaluation/processed_files/20250717_PMDA_gpt-4o_assessed.csv"
    "evaluation/processed_files/20250717_EMA_gpt-4o_assessed.csv"
)

python ./src/utils/combine_datasets_csv.py \
    --input_files "${INPUT_FILES[@]}" \
    --output_file "evaluation/processed_files/combined_datasets_shuffled.csv"

echo "Combined datasets saved to evaluation/processed_files/combined_datasets_shuffled.csv"