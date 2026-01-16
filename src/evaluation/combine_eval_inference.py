# load 2 json files and combine them into a single json
import argparse
import os
import pandas as pd
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Combine two JSON files")
    parser.add_argument("--input_file_1", help="Path to the first input JSON file")
    parser.add_argument("--input_file_2", help="Path to the second input JSON file")
    parser.add_argument("--output_file", help="Path to the output JSON file")
    return parser.parse_args()

def combine_json_files(input_file_1, input_file_2, output_file):
    with open(input_file_1, 'r') as file1, open(input_file_2, 'r') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    combined_data = {**data2, **data1}  # Combine the two dictionaries
    overlapping_keys = set(data1.keys()) & set(data2.keys())
    if overlapping_keys:
        print(f"Warning: Overlapping keys found: {overlapping_keys}")
    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

def main():
    args = parse_arguments()
    combine_json_files(args.input_file_1, args.input_file_2, args.output_file)
    print(f"Combined JSON files saved to {args.output_file}")

if __name__ == "__main__":
    main()