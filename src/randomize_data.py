import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter
import argparse
import json
import csv


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Select randomized subsets of data in a dir.")
    parser.add_argument("--dataset", required=True, help="The name of the dataset.")
    parser.add_argument("--data_dir", required=True, help="The directory containing the data files.")
    parser.add_argument("--num_samples", type=int, help="Number of samples to select from each file.", default=5)
    parser.add_argument("--save_dir", help="txt file with the list of randomly selected datapoints.", default="randomized_data")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility.", default=42)
    return parser.parse_args()

def save_random_filenames_to_file(filenames, source_dir_path):
    save_dir = os.path.dirname(source_dir_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(source_dir_path, 'w') as f:
        for item in filenames:
            f.write(f"{item}\n")

def get_random_filenames(dataset, data_dir, output_dir, n, seed):
    random.seed(seed) # set seed for reproducibility
    files = os.listdir(data_dir)
    random.shuffle(files)
    r_n = files[:n]
    save_random_filenames_to_file(r_n, f'{output_dir}/{dataset}_{n}.txt')
    return r_n

def main():
    args = parse_arguments()
    get_random_filenames(args.dataset, args.data_dir, args.save_dir, args.num_samples, args.seed)
    print(f"Randomized filenames saved to {args.save_dir}/{args.dataset}_{args.num_samples}.txt")

if __name__ == "__main__":
    main()