#!/bin/bash


# ==========================================================
# TODO change the below arguments as needed

EVAL_SHEET_NAME="poster1_20250522_EMA_gpt-4o-mini.json.csv" # name, not path!

MODEL_NAME="gpt-4o-mini"
# ==========================================================


python ./src/eval_with_llm.py \
    --eval_sheet "./evaluation/$EVAL_SHEET_NAME" \
    --output_file "./evaluation/compared_$EVAL_SHEET_NAME" \
    --model_name "$MODEL_NAME" \
    # --slice_size 1 \
    --temperature 0.1 \
    --max_tokens 5
    