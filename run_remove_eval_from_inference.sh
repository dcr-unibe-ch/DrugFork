#!/bin/bash

# ==========================================================
# TODO change the below argument as needed
DATASET="EMA" # EMA, SwissPAR, Japan, Australia

# ==========================================================
echo "whatsup"

python src/remove_eval_from_inference.py \
    --eval_list "./data/eval_data/eval_${DATASET}.txt" \
    --full_list "./data/inference_data/${DATASET}.txt" \
    --output_file "./data/inference_data/${DATASET}_clean.txt"

echo "Cleaned inference data saved to ./data/inference_data/${DATASET}_clean.txt"