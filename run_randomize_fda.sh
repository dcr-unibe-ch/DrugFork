#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed
NUM_SAMPLES=1000
# ==========================================================


python src/preprocessing/randomize_fda.py\
    --dataset "FDA" \
    --file_path "./data/FDA/Products.csv" \
    --num_samples "$NUM_SAMPLES" \
    --save_dir "./data/randomized_data" \
    --seed "42"