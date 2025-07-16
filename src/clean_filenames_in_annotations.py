import argparse
import os
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", help="Path to the CSV file to clean.", required=False)
    parser.add_argument("--output_csv", help="Path to save the cleaned CSV.", required=False)
    return parser.parse_args()

def clean_string(s):
    return s.strip().lower().replace(" ", "_")

def clean_csv_column(csv_path, output_csv):
    df = pd.read_csv(csv_path, encoding='utf-8')
    if "Document_name" not in df.columns:
        raise ValueError("CSV file does not contain a 'Document_name' column.")

    df["Document_name"] = df["Document_name"].astype(str).apply(clean_string)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Cleaned 'Document_name' column saved to: {output_csv}")

def main():
    args = parse_args()
    print("Arguments:", args)

    if args.csv_path and args.output_csv:
        clean_csv_column(args.csv_path, args.output_csv)

if __name__ == "__main__":
    main()
