#!/bin/bash

INPUT_DIR="data/HealthCanada/downloads"
OUTPUT_DIR="data/HealthCanada/downloads_parsed"
TO_EXTRACT=("indications")

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Beginning extraction of ${TO_EXTRACT[@]} from all PDFs in $INPUT_DIR..."

# Counter for progress tracking
count=0
total=$(find "$INPUT_DIR" -name "*.pdf" | wc -l)

# Process each PDF file in the input directory
for pdf_file in "$INPUT_DIR"/*.pdf; do
    if [[ -f "$pdf_file" ]]; then
        count=$((count + 1))
        
        # Get the base filename without extension
        base_name=$(basename "$pdf_file" .pdf)
        
        # Define output file path
        output_file="$OUTPUT_DIR/parsed.json"
        
        echo "[$count/$total] Processing: $base_name"
        
        # Run the extraction
        python src/parse_pdf.py \
          --input "$pdf_file" \
          --output "$output_file" \
          --to_extract "${TO_EXTRACT[@]}" \
          --id "$base_name"

        # Check if extraction was successful
        if [[ $? -eq 0 ]]; then
            echo "Successfully processed $base_name"
        else
            echo "Error processing $base_name"
        fi
    fi
done

echo ""
echo "Processing complete! Processed $count PDF files."
echo "Results saved in: $OUTPUT_DIR"