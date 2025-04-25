#!/bin/bash
# ===========================================================
FILE_NAME="SwissPAR_Levocalm.pdf"
# ==========================================================

DATA_DIR="./data/SwissPar/SwissPAR_Jan19_2025"
FILE_PATH="$DATA_DIR/$FILE_NAME"
MODEL="gpt-4o-mini"
SAVE_DIR="./output"
TEMPERATURE=0.1
MAX_TOKENS=300

mkdir -p "$SAVE_DIR"
# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "File not found!"
    exit 1
fi

python ./src/main.py\
    --filepath "$FILE_PATH" \
    --file_name "$FILE_NAME" \
    --model "$MODEL" \
    --save_dir "$SAVE_DIR" \
    --temperature "$TEMPERATURE" \
    --max_tokens "$MAX_TOKENS"