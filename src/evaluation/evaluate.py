import argparse
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns


def parse_args():
    parser = argparse.ArgumentParser(description="Compute agreement metrics per evaluation column.")
    parser.add_argument("--input_file", required=True, help="CSV file with evaluator verdicts.")
    parser.add_argument("--output_file", required=True, help="JSON file to save column-level metrics.")
    parser.add_argument("--output_dir")
    return parser.parse_args()


def parse_verdict_binary(value):
    """Parse verdict to binary (0 or 1) for sklearn metrics."""
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    if value == "match":
        return 1
    if value == "no_match":
        return 0
    if value.startswith("partial_"):
        try:
            score = float(value.split("_")[1])
            return 1 if score > 0.5 else 0
        except Exception:
            return None
    return None


def parse_verdict(value):
    """Parse verdict to float score for mean calculation."""
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


def compute_sklearn_metrics(series):
    """Compute sklearn metrics in a simple manner."""
    # Convert to binary values
    binary_values = series.apply(parse_verdict_binary)
    valid_binary = binary_values.dropna()
    
    if len(valid_binary) < 2:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0
        }
    
    # For simple metrics, we'll compare against a baseline of all 1s (assuming positive class)
    # This gives us basic metrics about the distribution
    y_true = valid_binary.values
    y_pred = np.ones_like(y_true)  # Simple baseline prediction
    
    try:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
            
        return {
            "accuracy": round(accuracy, 2),
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1, 2)
        }
    except Exception:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0
        }


def summarize_column(series):
    parsed = series.apply(parse_verdict)
    valid = parsed.dropna()
    total = len(series)
    series_str = series.astype(str).str.strip().str.lower()
    match_count = (series_str == "match").sum()
    no_match_count = (series_str == "no_match").sum()
    partial_count = series_str.str.startswith("partial_").sum()
    
    # Compute binary counts (same way as metrics)
    binary_values = series.apply(parse_verdict_binary)
    valid_binary = binary_values.dropna()
    true_count = (valid_binary == 1).sum()
    false_count = (valid_binary == 0).sum()
    
    # Compute sklearn metrics
    sklearn_metrics = compute_sklearn_metrics(series)

    return {
        "num_total": total,
        "num_valid": len(valid),
        "num_match": int(match_count),
        "num_no_match": int(no_match_count),
        "num_partial": int(partial_count),
        "num_true": int(true_count),
        "num_false": int(false_count),
        "mean_score_partial": round(valid.mean(), 2) if not valid.empty else None,
        "accuracy": sklearn_metrics["accuracy"],
        "precision": sklearn_metrics["precision"],
        "recall": sklearn_metrics["recall"],
        "f1_score": sklearn_metrics["f1_score"]
    }

def plot_results(results, output_dir, output_name):

    plt.figure(figsize=(5, 6))

    # Filter out Document_name
    filtered_results = {k: v for k, v in results.items() if k != 'Document_name'}
    
    labels = [key.replace('_', ' ') for key in filtered_results.keys()]
    true_counts = [res['num_true'] for res in filtered_results.values()]
    false_counts = [res['num_false'] for res in filtered_results.values()]
    
    # Calculate percentages
    totals = [true + false for true, false in zip(true_counts, false_counts)]
    true_percentages = [100 * true / total if total > 0 else 0 for true, total in zip(true_counts, totals)]
    false_percentages = [100 * false / total if total > 0 else 0 for false, total in zip(false_counts, totals)]

    y = range(len(labels))

    bar1 = plt.barh(y, true_percentages, label='True', color='seagreen')
    bar2 = plt.barh(y, false_percentages, left=true_percentages, label='False', color='violet')


    plt.ylabel('Columns')
    plt.xlabel('Percentage (%)')
    plt.xlim(0, 100)
    plt.yticks(y, labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='x')
    plt.savefig(f'{output_dir}/{output_name}.png', dpi=300)
    # plt.show()


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

    # Plot results - use os.path.basename to get just the filename
    import os
    output_name = os.path.basename(args.input_file).replace('.csv', '')
    plot_results(results, args.output_dir, output_name)


if __name__ == "__main__":
    main()
