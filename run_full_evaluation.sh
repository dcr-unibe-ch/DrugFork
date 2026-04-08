#!/bin/bash
# ==========================================================
# Full Evaluation Pipeline Runner for DrugFork
# 
# This script runs the complete evaluation workflow:
# 1. Data preparation (split eval/inference)
# 2. Generate predictions with LLM
# 3. Create evaluation sheets
# 4. Compute metrics
#
# Usage:
#   ./run_full_evaluation.sh EMA              # Run for single dataset
#   ./run_full_evaluation.sh --all            # Run for all datasets
#   ./run_full_evaluation.sh EMA --no-split   # Skip data preparation
# ==========================================================

# Configuration
CONFIG_FILE="config/evaluation_config.yaml"

# Parse arguments
DATASET=""
RUN_ALL=false
SKIP_SPLIT=false
USE_EXISTING=false
USE_ASSESSED=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            RUN_ALL=true
            shift
            ;;
        --no-split)
            SKIP_SPLIT=true
            shift
            ;;
        --use-existing-predictions)
            USE_EXISTING=true
            shift
            ;;
        --use-assessed-sheets)
            USE_ASSESSED=true
            shift
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [DATASET] [OPTIONS]"
            echo ""
            echo "Arguments:"
            echo "  DATASET          Dataset name (EMA, Swissmedic, PMDA, TGA)"
            echo ""
            echo "Options:"
            echo "  --all                         Run for all datasets in config"
            echo "  --no-split                    Skip data preparation step"
            echo "  --use-existing-predictions    Skip LLM generation, use existing outputs"
            echo "  --use-assessed-sheets         Use manually assessed evaluation sheets"
            echo "  --config FILE                 Use custom config file (default: config/evaluation_config.yaml)"
            echo "  --help, -h                    Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 EMA"
            echo "  $0 --all"
            echo "  $0 PMDA --no-split"
            echo "  $0 --all --use-existing-predictions --use-assessed-sheets"
            echo ""
            echo "Workflow:"
            echo "  1. Without flags: Full pipeline (data split → LLM prediction → create eval sheet)"
            echo "  2. With --use-existing-predictions: Skip LLM generation, use existing JSON files"
            echo "  3. With --use-assessed-sheets: Use manually assessed CSV files for metrics"
            exit 0
            ;;
        *)
            DATASET="$1"
            shift
            ;;
    esac
done

# Validate arguments
if [ "$RUN_ALL" = false ] && [ -z "$DATASET" ]; then
    echo "Error: Must specify a dataset or use --all"
    echo "Run '$0 --help' for usage information"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Display banner
echo "============================================================"
echo "          DrugFork Evaluation Pipeline                     "
echo "============================================================"
echo ""
echo "Configuration: $CONFIG_FILE"
if [ "$RUN_ALL" = true ]; then
    echo "Target: All datasets"
else
    echo "Target: $DATASET"
fi
if [ "$SKIP_SPLIT" = true ]; then
    echo "Skipping: Data preparation step"
fi
if [ "$USE_EXISTING" = true ]; then
    echo "Mode: Using existing predictions (skip LLM generation)"
fi
if [ "$USE_ASSESSED" = true ]; then
    echo "Mode: Using manually assessed sheets"
fi
echo ""

# Optional: Run data preparation separately if requested
if [ "$SKIP_SPLIT" = false ]; then
    echo "==========================================================="
    echo "Step 0: Data Preparation (Optional Pre-check)"
    echo "==========================================================="
    
    if [ "$RUN_ALL" = true ]; then
        python src/evaluation/data_preparation.py --config "$CONFIG_FILE" --skip-if-exists --validate
    else
        python src/evaluation/data_preparation.py --dataset "$DATASET" --config "$CONFIG_FILE" --skip-if-exists --validate
    fi
    
    PREP_EXIT_CODE=$?
    if [ $PREP_EXIT_CODE -ne 0 ]; then
        echo ""
        echo "   Warning: Data preparation had issues (exit code: $PREP_EXIT_CODE)"
        echo "   Continuing with pipeline..."
    fi
    echo ""
fi

# Run the main evaluation pipeline
echo "==========================================================="
echo "Running Evaluation Pipeline"
echo "==========================================================="
echo ""

PIPELINE_ARGS="--config $CONFIG_FILE"

if [ "$RUN_ALL" = true ]; then
    PIPELINE_ARGS="$PIPELINE_ARGS --all"
else
    PIPELINE_ARGS="$PIPELINE_ARGS --dataset $DATASET"
fi

if [ "$USE_EXISTING" = true ]; then
    PIPELINE_ARGS="$PIPELINE_ARGS --use-existing-predictions"
fi

if [ "$USE_ASSESSED" = true ]; then
    PIPELINE_ARGS="$PIPELINE_ARGS --use-assessed-sheets"
fi

python src/evaluation/run_evaluation_pipeline.py $PIPELINE_ARGS

EXIT_CODE=$?

# Final status
echo ""
echo "==========================================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "Evaluation pipeline completed successfully!"
else
    echo "Evaluation pipeline failed with exit code: $EXIT_CODE"
fi
echo "==========================================================="

exit $EXIT_CODE
