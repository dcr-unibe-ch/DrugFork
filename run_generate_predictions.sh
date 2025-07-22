#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
FILE_LIST="data/inference_data/SwissPAR_clean.txt"
DATASET="SwissMedic" # EMA, SwissMedic, Japan, Australia"
# ==========================================================




if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/downloads"
elif [ "$DATASET" == "SwissMedic" ]; then    
    DATA_DIR="data/SwissPar/downloads"
elif [ "$DATASET" == "Japan" ]; then
    DATA_DIR="data/Japan/downloads"
elif [ "$DATASET" == "Australia" ]; then
    DATA_DIR="data/Australia/downloads"
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