#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
FILE_LIST="data/inference_data/Australia_clean.txt"
DATASET="Australia" # EMA, Swissmedic, PMDA, TGA"
# ==========================================================




if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/downloads"
elif [ "$DATASET" == "Swissmedic" ]; then    
    DATA_DIR="data/Swissmedic/downloads"
elif [ "$DATASET" == "PMDA" ]; then
    DATA_DIR="data/PMDA/downloads"
elif [ "$DATASET" == "TGA" ]; then
    DATA_DIR="data/TGA/downloads"
fi

SAVE_DIR="./output"
mkdir -p "$SAVE_DIR"

python ./src/generate_predictions.py\
    --file_list "$FILE_LIST" \
    --data_dir "$DATA_DIR" \
    --model "gpt-4o" \
    --save_dir "./output" \
    --temperature "0.1" \
    --max_tokens "1200" \
    --dataset "$DATASET" 