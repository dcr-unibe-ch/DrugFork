#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
INPUT_FILE="inference/combined/JAPAN.json"
DATASET="JAPAN" # EMA, SwissMedic, Japan, Australia"
# ==========================================================

SAVE_DIR="./inference/combined"
mkdir -p "$SAVE_DIR"

python ./src/extract_from_columns.py\
    --input_file "$INPUT_FILE" \
    --slice 10 \
    --model "gpt-4o-mini" \
    --save_dir "$SAVE_DIR" \
    --temperature "0.1" \
    --max_tokens "100" \
    --dataset "$DATASET" 