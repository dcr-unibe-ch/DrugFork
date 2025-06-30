#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed
NUM_SAMPLES=30
DATASET="Japan" # options: EMA, SwissPar, Japan
# ==========================================================


if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/EMA_downloads"
elif [ "$DATASET" == "SwissPar" ]; then    
    DATA_DIR="data/SwissPar/SwissPAR_Jan19_2025"
elif [ "$DATASET" == "Japan" ]; then
    DATA_DIR="data/Japan/Japan_PAR_download"
fi

python src/randomize_data.py\
    --dataset "$DATASET" \
    --data_dir "$DATA_DIR" \
    --num_samples "$NUM_SAMPLES" \
    --save_dir "./data/randomized_data" \
    --seed "42"