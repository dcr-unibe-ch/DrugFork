#!/bin/bash

# ==========================================================
# TODO change the below arguments as needed

LLM_FILENAME="poster1_20250522_EMA_gpt-4o-mini.json"

HUMAN_ANNOTATIONS_FILEPATH="./data/annotations/EMA_Swissmedic_Drug_Approval-Sheet1.csv"
# ==========================================================


python src/create_evaluation_sheet.py\
    --llm_file "./output/$LLM_FILENAME" \
    --output_file "./evaluation/$LLM_FILENAME.csv" \
    --human_file "$HUMAN_ANNOTATIONS_FILEPATH" 


echo "Evaluation sheet created at ./evaluation/$LLM_FILENAME"
