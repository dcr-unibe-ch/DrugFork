#!/bin/bash

# =================================================
# TODO
DATASET="EMA" # EMA, JAPAN, AUSTRALIA, SWISSMEDIC
EVAL="evaluation\output\20250717_EMA_gpt-4o.json"
INFERENCE="output\20250722_EMA_gpt-4o.json"
# ==================================================


# Run the Python script with the specified arguments
python src/combine_eval_inference.py \
    --input_file_1 "$EVAL" \
    --input_file_2 "$INFERENCE" \
    --output_file "inference/combined/$DATASET.json"

# Print a message indicating where the results are saved
echo "Combined evaluation results saved to inference/combined/$DATASET.json"