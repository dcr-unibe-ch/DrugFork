#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
DATASET="JAPAN" # EMA, SWISSMEDIC, JAPAN, AUSTRALIA"
DATA_DIR="./inference/combined/with_extracted_data"
INPUT_FILE="$DATA_DIR/$DATASET.json"

# ==========================================================


python ./src/utils/json_to_csv.py\
    --input_file "$INPUT_FILE" \
    --output_file "$DATA_DIR/$DATASET.csv" \