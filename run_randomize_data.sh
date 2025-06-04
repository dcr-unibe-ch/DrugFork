#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed
NUM_SAMPLES=33
DATASET="SwissPar" # options: EMA, SwissPar
# ==========================================================


if [ "$DATASET" == "EMA" ]; then
    DATA_DIR="data/EMA/EMA_downloads"
elif [ "$DATASET" == "SwissPar" ]; then    
    DATA_DIR="data/SwissPar/SwissPAR_Jan19_2025"
fi

python src/randomize_data.py\
    --dataset "$DATASET" \
    --data_dir "$DATA_DIR" \
    --num_samples "$NUM_SAMPLES" \
    --save_dir "./data/randomized_data" \
    --seed "42"