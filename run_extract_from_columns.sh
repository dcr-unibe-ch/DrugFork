#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
DATASETS=(
    # "JAPAN" 
    # "AUSTRALIA" 
    # "EMA" 
    # "SWISSMEDIC"
    "FDA"
)

for DATASET in "${DATASETS[@]}"; do
    echo "Processing dataset: $DATASET"

    # INPUT_FILE="inference/combined/$DATASET.json"
    INPUT_FILE="data/FDA/$DATASET.json"

    # iterate over the columns of interest

    COLUMNS_OF_INTEREST=(
        "Marketing_authorisation_holder"
        "Non_proprietary_name"
        "Indications_and_usage"
    )

    # ==========================================================

    # SAVE_DIR="./inference/combined/with_extracted_data"
    SAVE_DIR="data/FDA/with_extracted_data"
    mkdir -p "$SAVE_DIR"

    python ./src/extract_from_columns.py\
        --input_file "$INPUT_FILE" \
        --columns_of_interest "${COLUMNS_OF_INTEREST[@]}" \
        --slice 10 \
        --model "gpt-4o" \
        --save_file "$SAVE_DIR/$DATASET.json" \
        --temperature "0.1" \
        --max_tokens "1000" \
        --dataset "$DATASET" 


    echo "Extraction completed. Output saved to $SAVE_DIR/$DATASET.json"
    echo "Converting JSON to CSV..."

    python ./src/json_to_csv.py\
         --input_file "$SAVE_DIR/$DATASET.json" \
         --output_file "$SAVE_DIR/$DATASET.csv" \

    echo "Conversion completed. Output saved to $SAVE_DIR/$DATASET.csv"
    

done