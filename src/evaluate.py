import argparse
import pandas as pd
import json


def parse_args():
    parser = argparse.ArgumentParser(description="Compute agreement metrics per evaluation column.")
    parser.add_argument("--input_file", required=True, help="CSV file with evaluator verdicts.")
    parser.add_argument("--output_file", required=True, help="JSON file to save column-level metrics.")
    return parser.parse_args()


def parse_verdict(value):
    if not isinstance(value, str):
        return 0.0
    value = value.strip().lower()
    if value == "match":
        return 1.0
    if value == "no_match":
        return 0.0
    if value.startswith("partial_"):
        try:
            return float(value.split("_")[1])
        except Exception:
            return None
    return None


def summarize_column(series):
    parsed = series.apply(parse_verdict)
    valid = parsed.dropna()
    total = len(series)
    series_str = series.astype(str).str.strip().str.lower()
    match_count = (series_str == "match").sum()
    no_match_count = (series_str == "no_match").sum()
    partial_count = series_str.str.startswith("partial_").sum()

    return {
        "num_total": total,
        "num_valid": len(valid),
        "num_match": int(match_count),
        "num_no_match": int(no_match_count),
        "num_partial": int(partial_count),
        "mean_score": round(valid.mean(), 4) if not valid.empty else None
    }


def main():
    args = parse_args()
    df = pd.read_csv(args.input_file, encoding='utf-8')

    # Find all verdict columns
    verdict_cols = [col for col in df.columns if col.endswith("_verdict_human")]
    if not verdict_cols:
        raise ValueError("No columns ending with '_verdict_human' found.")

    results = {}
    for col in verdict_cols:
        col_name = col.replace("_verdict_human", "")
        print(f"Processing column: {col_name}")
        results[col_name] = summarize_column(df[col])

    # Save to JSON
    with open(args.output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {args.output_file}")


if __name__ == "__main__":
    main()
