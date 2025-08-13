import os
import re
from pathlib import Path
import argparse
import json
from PyPDF2 import PdfReader

def parse_args():
    parser = argparse.ArgumentParser(description="Parse PDF files.")
    parser.add_argument("--input", required=True, help="Path to the input PDF file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file.")
    parser.add_argument("--to_extract", nargs="+", required=True, help="List of sections to extract.")
    parser.add_argument("--id", required=True, help="PDF name.")
    return parser.parse_args()

def extract_indications(pdf_path):
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = re.sub(r'\s+', ' ', text)

    section_titles = [
        r"Indications(?:\s+and\s+Usage)?",
        r"Indications\s+and\s+Clinical\s+Use",
        r"Therapeutic\s+Indications",
        r"Clinical\s+Indications"
    ]
    stop_titles = [
        r"Contraindications",
        r"Special\s+Warnings",
        r"Warnings",
        r"Precautions"
    ]

    section_pattern = "|".join(section_titles)
    stop_pattern = "|".join(stop_titles)
    pattern = re.compile(
        rf"(?:{section_pattern})"
        rf"(?!\s*[.\s]*\d+\s*(?:\n|$))"             # NOT followed by dots and page numbers
        rf"(?!\s*[.\-_\s]+(?:\d+\s*)?(?:\n|$))"     # NOT followed by mostly dots/dashes/spaces
        rf"\s+"                                      # Some whitespace
        rf"(.*?)"                                    # Capture the content (non-greedy)
        rf"(?=\s+(?:{stop_pattern}))",               # Until next section
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(text)
    if matches:
        cleaned_matches = []
        for match in matches:
            match = match.strip()
            
            # Skip if looks like table of contents
            if (re.search(r'[.\-_]{5,}', match) or  # consecutive dots/dashes
                len(match) < 20 or
                re.match(r'^[.\-_\s\d]+$', match)):
                continue
            
            if re.match(r'^\s*(?:AND\s+CL?INICAL\s+USE\s*[.\-_\s]*\d*|[.\-_\s]*\d+\s*$)', match, re.IGNORECASE):
                continue
            
            cleaned_matches.append(match)
        
        if cleaned_matches:
            # Join all found occurrences into one string
            combined = "\n---\n".join(cleaned_matches)
            return combined
    
    return None



def main():
    args = parse_args()
    indications_text = extract_indications(args.input)
    if indications_text:
        print("Indications and Usage section:\n")
        print(indications_text)
    else:
        print("No Indications section found.")

    # Load existing JSON or create empty dict
    output_data = {}
    if os.path.exists(args.output):
        try:
            with open(args.output, 'r') as f:
                content = f.read().strip()
                if content:  # if file is not empty
                    output_data = json.loads(content)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read existing file {args.output}: {e}")
            print("Starting with empty data structure.")
            output_data = {}
    
    if args.id not in output_data:
        output_data[args.id] = {"indications": indications_text}
        print(f"Added {args.id} to output file.")
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=4)
    else:
        print(f"Skipping {args.id} - already exists in output file.")

if __name__ == "__main__":
    main()
