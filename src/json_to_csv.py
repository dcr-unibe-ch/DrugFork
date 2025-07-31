import pandas as pd
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Path to the input json file", required=True)
    parser.add_argument("--output_file", type=str, help="Path to the output csv file", required=True)
    return parser.parse_args()

def json_to_csv(json_file, csv_file):
    df = pd.read_json(json_file)
    df = df.transpose()
    # sort columns alphabetically
    df = df.reindex(sorted(df.columns), axis=1)
    return df

    # df.to_csv(csv_file, header=False)

def main():
    args = parse_arguments()
    if not args.input_file.endswith('.json'):
        raise ValueError("Input file must be a JSON file.")
    if not args.output_file.endswith('.csv'):
        raise ValueError("Output file must be a CSV file.")
    df = json_to_csv(args.input_file, args.output_file)
    print(df.head())
    
    df.to_csv(args.output_file, index=False)

if __name__ == "__main__":
    main()