import argparse
import pandas as pd
import os
import random

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Select randomized subsets of data in a csv.")
    parser.add_argument("--dataset", required=True, help="The name of the dataset.")
    parser.add_argument("--file_path", required=True, help="Path to the csv file containing the data.")
    parser.add_argument("--num_samples", type=int, help="Number of samples to select from each file.", default=5)
    parser.add_argument("--save_dir", help="txt file with the list of randomly selected datapoints.", default="randomized_data")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility.", default=42)
    return parser.parse_args()

def load_data(file_path):
    """Load data from a csv file."""
    df = pd.read_csv(file_path)
    df = df[['Application_ID']]
    return df

def sample_from_data(data, n, seed):
    random.seed(seed)
    sampled = data.sample(n=n, random_state=seed)
    return sampled

def save_sampled_data(sampled_data, save_dir, dataset, n):
    """Save the sampled data to a txt file."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"{dataset}_{n}.txt")
    sampled_data.to_csv(save_path, index=False, header=False)
    print(f"Sampled data saved to {save_path}")

def main():
    args = parse_arguments()
    print("Arguments:", args)
    data = load_data(args.file_path)
    sampled_data = sample_from_data(data, args.num_samples, args.seed)
    save_sampled_data(sampled_data, args.save_dir, args.dataset, args.num_samples)


if __name__ == "__main__":
    main()
    