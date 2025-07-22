#!/bin/bash

# ==========================================================
# TODO change the below argument as needed

INPUT_FILE="20250717_EMA_gpt-4o_assessed.csv"

# ==========================================================


python src/evaluate.py\
    --input_file "./evaluation/processed_files/${INPUT_FILE}" \
    --output_file "./evaluation/results/${INPUT_FILE}.json" \
    --output_dir "./evaluation/plots"

echo "Evaluation results saved to ./evaluation/results/${INPUT_FILE}.json"