#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed

LLM_FILENAME="20250716_Japan_gpt-4o.json"

HUMAN_ANNOTATIONS_FILEPATH="data/annotations/Drug_Approval_Annotations_all_datasets-Sheet1_cleaned.csv"
# ==========================================================


python src/create_evaluation_sheet.py\
    --llm_file "./output/$LLM_FILENAME" \
    --output_file "./evaluation/$LLM_FILENAME.csv" \
    --human_file "$HUMAN_ANNOTATIONS_FILEPATH" 


echo "Evaluation sheet created at ./evaluation/$LLM_FILENAME"
