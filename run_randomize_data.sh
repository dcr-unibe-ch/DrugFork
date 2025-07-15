#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed
NUM_SAMPLES=20
DATASET="Japan" # options: EMA, SwissPar, Japan, Australia
# ==========================================================


if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/EMA_downloads"
elif [ "$DATASET" == "SwissPar" ]; then    
    DATA_DIR="data/SwissPar/SwissPAR_Jan19_2025"
elif [ "$DATASET" == "Japan" ]; then
    DATA_DIR="data/Japan/Japan_PAR_download"
elif [ "$DATASET" == "Australia" ]; then
    DATA_DIR="data/Australia/AusPAR_download"
fi

python src/randomize_data.py\
    --dataset "$DATASET" \
    --data_dir "$DATA_DIR" \
    --num_samples "$NUM_SAMPLES" \
    --save_dir "./data/randomized_data" \
    --seed "42"