import pandas as pd
import argparse

def concatenate_csv_files(input_files, output_file):
    df_list = [pd.read_csv(file) for file in input_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # sort cols alphabetically
    combined_df = combined_df.reindex(sorted(combined_df.columns), axis=1)

    # shuffle rows
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to {output_file}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Combine multiple CSV files into one.")
    parser.add_argument("--input_files", nargs='+', required=True, help="List of input CSV files to combine.")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output combined CSV file.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    concatenate_csv_files(args.input_files, args.output_file)


if __name__ == "__main__":
    main()