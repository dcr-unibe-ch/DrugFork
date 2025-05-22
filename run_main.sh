#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
FILE_LIST="data/randomized_data/EMA_5.txt"
DATASET="EMA" # Options: EMA, SwissPar
# ==========================================================


if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/EMA_downloads"
elif [ "$DATASET" == "SwissPar" ]; then    
    DATA_DIR="data/SwissPar/SwissPAR_Jan19_2025"
fi

SAVE_DIR="./output"
mkdir -p "$SAVE_DIR"

python ./src/main.py\
    --file_list "$FILE_LIST" \
    --data_dir "$DATA_DIR" \
    --model "gpt-4o-mini" \
    --save_dir "./output" \
    --temperature "0.1" \
    --max_tokens "500" \
    --dataset "$DATASET" 