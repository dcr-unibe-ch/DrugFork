#!/bin/bash
# ===========================================================
FILE_LIST="data/random/SwissPar_5.txt"
# ==========================================================

DATA_DIR="./data/SwissPar/SwissPAR_Jan19_2025"
MODEL="gpt-4o-mini"
SAVE_DIR="./output"
TEMPERATURE=0.1
MAX_TOKENS=300

mkdir -p "$SAVE_DIR"

python ./src/main.py\
    --file_list "$FILE_LIST" \
    --data_dir "$DATA_DIR" \
    --model "$MODEL" \
    --save_dir "$SAVE_DIR" \
    --temperature "$TEMPERATURE" \
    --max_tokens "$MAX_TOKENS"