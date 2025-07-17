#!/bin/bash

# ==========================================================
# TODO change the below argument as needed

INPUT_FILE="20250717_Australia_gpt-4o.json.csv"
# remove the .csv extension if not needed from the name

# ==========================================================


python src/evaluate.py\
    --input_file "./evaluation/${INPUT_FILE}" \
    --output_file "./evaluation/results_${INPUT_FILE}.json"

echo "Evaluation results saved to ./evaluation/results_${INPUT_FILE}.json"