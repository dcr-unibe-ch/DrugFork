#!/bin/bash
# ==========================================================
# TODO change the below arguments as needed
DATASETS=(
    # "JAPAN" 
    # "AUSTRALIA" 
    # "EMA" 
    "SWISSMEDIC"
    # "FDA"
    # "HEALTHCANADA"
)

for DATASET in "${DATASETS[@]}"; do
    echo "Processing dataset: $DATASET"

    # INPUT_FILE="inference/combined/$DATASET.json"
    # INPUT_FILE="data/FDA/$DATASET.json"
    # INPUT_FILE="data/HealthCanada/$DATASET.json"
    # INPUT_FILE="data/HealthCanada/downloads_parsed/parsed.json"
    # INPUT_FILE="inference/combined/JAPAN_manually_cleaned.json"
    # INPUT_FILE="inference/combined/EMA_manually_cleaned.json"
    # INPUT_FILE="inference/combined/AUSTRALIA_manually_cleaned.json"
    INPUT_FILE="inference/combined/SWISSMEDIC_manually_cleaned.json"



    # iterate over the columns of interest

    COLUMNS_OF_INTEREST=(
        "Marketing_authorisation_holder"
        # "Non_proprietary_name"
        # "Indications_and_usage"
    )

    # ==========================================================

    # SAVE_DIR="./inference/combined/with_extracted_data"
    # SAVE_DIR="data/FDA/with_extracted_data"
    # SAVE_DIR="./data/HealthCanada/with_extracted_data"
    SAVE_DIR="inference/combined"
    mkdir -p "$SAVE_DIR"}

    python ./src/extract_from_columns.py\
        --input_file "$INPUT_FILE" \
        --columns_of_interest "${COLUMNS_OF_INTEREST[@]}" \
        --slice -1 \
        --model "gpt-4o" \
        --save_file "$SAVE_DIR/${DATASET}_manually_cleaned.json" \
        --temperature "0.1" \
        --max_tokens "1000" \
        --dataset "$DATASET" 


    echo "Extraction completed. Output saved to $SAVE_DIR/${DATASET}_manually_cleaned.json"
    echo "Converting JSON to CSV..."

    python ./src/json_to_csv.py\
         --input_file "$SAVE_DIR/${DATASET}_manually_cleaned.json" \
         --output_file "$SAVE_DIR/${DATASET}_manually_cleaned.csv" \

    echo "Conversion completed. Output saved to $SAVE_DIR/${DATASET}_manually_cleaned.csv"
    

done