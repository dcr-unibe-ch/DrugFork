#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed
NUM_SAMPLES=20
DATASET="PMDA" # options: EMA, Swissmedic, PMDA, TGA
# ==========================================================


if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/EMA_downloads"
elif [ "$DATASET" == "Swissmedic" ]; then    
    DATA_DIR="data/Swissmedic/Swissmedic_Jan19_2025"
elif [ "$DATASET" == "PMDA" ]; then
    DATA_DIR="data/PMDA/PMDA_downloads"
elif [ "$DATASET" == "TGA" ]; then
    DATA_DIR="data/TGA/TGA_downloads"
fi

python src/preprocessing/randomize_data.py\
    --dataset "$DATASET" \
    --data_dir "$DATA_DIR" \
    --num_samples "$NUM_SAMPLES" \
    --save_dir "./data/randomized_data" \
    --seed "42"