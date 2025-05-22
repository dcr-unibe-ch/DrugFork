#!/bin/bash
# ==========================================================
FILE_LIST="data/random/EMA_5.txt"
# ==========================================================

DATA_DIR="data/EMA/EMA_downloads"
MODEL="gpt-4o-mini"
SAVE_DIR="./output"
TEMPERATURE=0.1
MAX_TOKENS=300
DATASET="EMA" # Options: EMA, SwissPar

mkdir -p "$SAVE_DIR"

python ./src/main.py\
    --file_list "$FILE_LIST" \
    --data_dir "$DATA_DIR" \
    --model "$MODEL" \
    --save_dir "$SAVE_DIR" \
    --temperature "$TEMPERATURE" \
    --max_tokens "$MAX_TOKENS" \
    --dataset "$DATASET" 