#!/bin/bash


CSV_PATH="data/annotations/Drug_Approval_Annotations_all_datasets-Sheet1.csv"
OUTPUT_CSV="data/annotations/Drug_Approval_Annotations_all_datasets-Sheet1_cleaned.csv"

python src/preprocessing/clean_filenames_in_annotations.py\
    --csv_path "$CSV_PATH" \
    --output_csv "$OUTPUT_CSV"