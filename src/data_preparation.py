"""
Data Preparation Module for DrugFork Evaluation Pipeline

This module consolidates data splitting and preparation logic:
- Creates evaluation splits from full datasets
- Removes evaluation samples from inference datasets
- Validates splits to prevent data leakage
- Supports both randomized sampling and predefined splits
"""

import argparse
import os
import random
from pathlib import Path
from typing import Set, List, Tuple
import yaml


class DatasetSplitter:
    """Handles splitting datasets into evaluation and inference sets."""
    
    def __init__(self, eval_dir: str, inference_dir: str):
        """
        Initialize the DatasetSplitter.
        
        Args:
            eval_dir: Directory containing evaluation filenames
            inference_dir: Directory containing full inference filenames
        """
        self.eval_dir = Path(eval_dir)
        self.inference_dir = Path(inference_dir)
        
    def find_common_lines(self, eval_file: str, full_file: str) -> Set[str]:
        """
        Find common lines between evaluation and full dataset files.
        
        Args:
            eval_file: Path to evaluation file
            full_file: Path to full dataset file
            
        Returns:
            Set of common lines (filenames)
        """
        with open(eval_file, 'r') as f1, open(full_file, 'r') as f2:
            lines1 = set(line.strip() for line in f1 if line.strip())
            lines2 = set(line.strip() for line in f2 if line.strip())
            common_lines = lines1.intersection(lines2)
        return common_lines
    
    def remove_common_lines(self, input_file: str, common_lines: Set[str], output_file: str) -> int:
        """
        Remove common lines from input file and write to output.
        
        Args:
            input_file: Path to input file
            common_lines: Set of lines to remove
            output_file: Path to output file
            
        Returns:
            Number of lines removed
        """
        lines_removed = 0
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.strip() not in common_lines:
                    outfile.write(line)
                else:
                    lines_removed += 1
        return lines_removed
    
    def split_dataset(self, dataset: str, skip_if_exists: bool = True) -> Tuple[str, str]:
        """
        Split a dataset into evaluation and inference sets.
        
        Args:
            dataset: Name of the dataset (e.g., 'EMA', 'Japan')
            skip_if_exists: Skip if clean file already exists
            
        Returns:
            Tuple of (eval_file_path, clean_inference_file_path)
        """
        eval_file = self.eval_dir / f"eval_{dataset}.txt"
        full_file = self.inference_dir / f"{dataset}.txt"
        output_file = self.inference_dir / f"{dataset}_clean.txt"
        
        # Check if already processed
        if skip_if_exists and output_file.exists():
            print(f"{dataset}: Clean inference file already exists at {output_file}")
            return str(eval_file), str(output_file)
        
        # Validate input files exist
        if not eval_file.exists():
            print(f"{dataset}: Evaluation file not found at {eval_file}")
            return None, None
        
        if not full_file.exists():
            print(f"{dataset}: Full dataset file not found at {full_file}")
            return None, None
        
        # Perform split
        print(f"{dataset}: Splitting evaluation from inference...")
        common_lines = self.find_common_lines(str(eval_file), str(full_file))
        lines_removed = self.remove_common_lines(str(full_file), common_lines, str(output_file))
        
        print(f"{dataset}: Removed {lines_removed} eval samples from inference")
        print(f"  Clean inference saved to {output_file}")
        
        return str(eval_file), str(output_file)
    
    def validate_split(self, eval_file: str, inference_file: str) -> bool:
        """
        Validate that there's no overlap between eval and inference sets.
        
        Args:
            eval_file: Path to evaluation file
            inference_file: Path to inference file
            
        Returns:
            True if valid (no overlap), False otherwise
        """
        if not eval_file or not inference_file:
            return False
            
        if not os.path.exists(eval_file) or not os.path.exists(inference_file):
            return False
            
        with open(eval_file, 'r') as f1, open(inference_file, 'r') as f2:
            eval_lines = set(line.strip() for line in f1 if line.strip())
            inference_lines = set(line.strip() for line in f2 if line.strip())
            overlap = eval_lines.intersection(inference_lines)
        
        if overlap:
            print(f"Validation failed: Found {len(overlap)} overlapping samples")
            print(f"   First few overlaps: {list(overlap)[:3]}")
            return False
        else:
            print(f"Validation passed: No overlap between eval and inference")
            return True


class RandomSampler:
    """Handles random sampling of datasets for evaluation."""
    
    def __init__(self, seed: int = 42):
        """
        Initialize the RandomSampler.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)
    
    def create_random_eval_split(self, data_dir: str, dataset: str, 
                                 n_samples: int, output_file: str) -> List[str]:
        """
        Create a random evaluation split from a directory of files.
        
        Args:
            data_dir: Directory containing data files
            dataset: Dataset name
            n_samples: Number of samples to select
            output_file: Where to save the selected filenames
            
        Returns:
            List of selected filenames
        """
        files = os.listdir(data_dir)
        random.shuffle(files)
        selected = files[:n_samples]
        
        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            for filename in selected:
                f.write(f"{filename}\n")
        
        print(f"Created random eval split: {n_samples} samples -> {output_file}")
        return selected


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Prepare datasets by splitting evaluation from inference sets"
    )
    parser.add_argument(
        "--dataset",
        help="Specific dataset to process (e.g., 'EMA', 'Japan'). If not provided, processes all datasets in config"
    )
    parser.add_argument(
        "--config",
        default="config/evaluation_config.yaml",
        help="Path to evaluation configuration file"
    )
    parser.add_argument(
        "--skip-if-exists",
        action="store_true",
        default=True,
        help="Skip processing if clean files already exist"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        default=True,
        help="Validate splits after processing"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_args()
    
    # Load configuration
    print(f"Loading configuration from {args.config}")
    config = load_config(args.config)
    
    # Initialize splitter
    data_split_config = config.get('data_split', {})
    splitter = DatasetSplitter(
        eval_dir=data_split_config.get('eval_files_dir', 'data/eval_data'),
        inference_dir=data_split_config.get('inference_files_dir', 'data/inference_data')
    )
    
    # Determine which datasets to process
    if args.dataset:
        datasets = [args.dataset]
    else:
        datasets = config.get('datasets', [])
    
    print(f"\nProcessing {len(datasets)} dataset(s): {', '.join(datasets)}\n")
    
    # Process each dataset
    results = {}
    for dataset in datasets:
        print(f"{'='*60}")
        print(f"Processing: {dataset}")
        print(f"{'='*60}")
        
        eval_file, clean_file = splitter.split_dataset(
            dataset,
            skip_if_exists=args.skip_if_exists
        )
        
        results[dataset] = {
            'eval_file': eval_file,
            'inference_file': clean_file,
            'success': eval_file is not None and clean_file is not None
        }
        
        # Validate if requested
        if args.validate and results[dataset]['success']:
            print(f"\nValidating split for {dataset}...")
            is_valid = splitter.validate_split(eval_file, clean_file)
            results[dataset]['valid'] = is_valid
        
        print()
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results.values() if r.get('success', False))
    print(f"Successfully processed: {successful}/{len(datasets)} datasets")
    
    if args.validate:
        valid = sum(1 for r in results.values() if r.get('valid', False))
        print(f"Validated splits: {valid}/{successful} datasets")
    
    # Print any failures
    failed = [ds for ds, r in results.items() if not r.get('success', False)]
    if failed:
        print(f"\nFailed datasets: {', '.join(failed)}")
    
    print("\nData preparation complete!")


if __name__ == "__main__":
    main()
