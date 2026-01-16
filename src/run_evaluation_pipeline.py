"""
Evaluation Pipeline Orchestrator for DrugFork

This script coordinates the full evaluation workflow:
1. Data preparation (split eval from inference)
2. Generate predictions on evaluation set
3. Create evaluation sheets (compare LLM vs human annotations)
4. Compute metrics (accuracy, precision, recall, F1)
5. Optionally combine results

Usage:
    python src/run_evaluation_pipeline.py --dataset EMA --config config/evaluation_config.yaml
    python src/run_evaluation_pipeline.py --all --config config/evaluation_config.yaml
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import yaml
import json


class EvaluationPipeline:
    """Orchestrates the full evaluation pipeline."""
    
    def __init__(self, config_path: str):
        """
        Initialize the pipeline with configuration.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.timestamp = datetime.now().strftime("%Y%m%d")
        
    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _run_command(self, cmd: list, description: str) -> bool:
        """
        Run a shell command and handle errors.
        
        Args:
            cmd: Command and arguments as list
            description: Human-readable description of the step
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"{description}")
        print(f"{'='*60}")
        print(f"Command: {' '.join(cmd)}\n")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
            print(f"{description} - COMPLETE\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{description} - FAILED")
            print(f"Error: {e.stderr}")
            return False
    
    def step_1_prepare_data(self, dataset: str) -> bool:
        """
        Step 1: Prepare data by splitting eval from inference.
        
        Args:
            dataset: Dataset name (e.g., 'EMA', 'Japan')
            
        Returns:
            True if successful
        """
        if not self.config.get('data_split', {}).get('enabled', True):
            print("Data split disabled in config, skipping...")
            return True
        
        skip_flag = "--skip-if-exists" if self.config.get('processing', {}).get('skip_if_exists', True) else ""
        validate_flag = "--validate" if self.config.get('processing', {}).get('validate_split', True) else ""
        
        cmd = [
            sys.executable,
            "src/data_preparation.py",
            "--dataset", dataset,
            "--config", self.config_path
        ]
        
        if skip_flag:
            cmd.append(skip_flag)
        if validate_flag:
            cmd.append(validate_flag)
        
        return self._run_command(
            cmd,
            f"Step 1: Prepare data for {dataset}"
        )
    
    def step_2_generate_predictions(self, dataset: str, use_existing: bool = False) -> tuple[bool, str]:
        """
        Step 2: Generate predictions using LLM on evaluation set.
        
        Args:
            dataset: Dataset name
            use_existing: If True, skip generation and use existing output file
            
        Returns:
            Tuple of (success, output_file_path)
        """
        paths = self.config.get('paths', {})
        model_config = self.config.get('model', {})
        
        # Determine expected output file path
        output_dir = paths.get('output_dir', 'output')
        output_file = os.path.join(
            output_dir,
            f"{self.timestamp}_{dataset}_{model_config.get('name', 'gpt-4o')}.json"
        )
        
        # Check if we should use existing predictions
        if use_existing:
            if os.path.exists(output_file):
                print(f"Using existing predictions from: {output_file}")
                return True, output_file
            else:
                # Try to find any existing output file for this dataset
                import glob
                pattern = os.path.join(output_dir, f"*_{dataset}_*.json")
                existing_files = sorted(glob.glob(pattern), reverse=True)
                if existing_files:
                    output_file = existing_files[0]
                    print(f"Using existing predictions from: {output_file}")
                    return True, output_file
                
                print(f"No existing predictions found for {dataset}, will generate new ones...")
                use_existing = False
        
        if not use_existing:
            data_split = self.config.get('data_split', {})
            
            # Determine input file (evaluation list)
            eval_file = os.path.join(
                data_split.get('eval_files_dir', 'data/eval_data'),
                f"eval_{dataset}.txt"
            )
            
            if not os.path.exists(eval_file):
                print(f"Evaluation file not found: {eval_file}")
                return False, None
            
            # Determine data directory (where PDFs are located)
            data_dir = f'data/{dataset}'
            
            # Output file
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = [
                sys.executable,
                "src/generate_predictions.py",
                "--file_list", eval_file,
                "--data_dir", data_dir,
                "--dataset", dataset,
                "--model", model_config.get('name', 'gpt-4o'),
                "--temperature", str(model_config.get('temperature', 0.1)),
                "--max_tokens", str(model_config.get('max_tokens', 1000)),
                "--save_dir", output_dir
            ]
            
            success = self._run_command(
                cmd,
                f"Step 2: Generate predictions for {dataset}"
            )
            
            return success, output_file if success else None
        
        return True, output_file
    
    def step_3_create_evaluation_sheet(self, dataset: str, llm_output_file: str) -> tuple[bool, str]:
        """
        Step 3: Create evaluation sheet comparing LLM output with human annotations.
        
        Args:
            dataset: Dataset name
            llm_output_file: Path to LLM predictions JSON file
            
        Returns:
            Tuple of (success, evaluation_sheet_path)
        """
        if not self.config.get('evaluation', {}).get('create_comparison_sheets', True):
            print("Evaluation sheet creation disabled, skipping...")
            return True, None
        
        paths = self.config.get('paths', {})
        human_annotations = paths.get('human_annotations')
        
        if not human_annotations or not os.path.exists(human_annotations):
            print(f"Human annotations file not found: {human_annotations}")
            return False, None
        
        # Output evaluation sheet
        eval_output_dir = paths.get('evaluation_output_dir', 'evaluation/output')
        os.makedirs(eval_output_dir, exist_ok=True)
        
        output_basename = os.path.basename(llm_output_file).replace('.json', '.csv')
        eval_sheet = os.path.join(eval_output_dir, output_basename)
        
        cmd = [
            sys.executable,
            "src/create_evaluation_sheet.py",
            "--llm_file", llm_output_file,
            "--human_file", human_annotations,
            "--output_file", eval_sheet
        ]
        
        success = self._run_command(
            cmd,
            f"Step 3: Create evaluation sheet for {dataset}"
        )
        
        return success, eval_sheet if success else None
    
    def step_4_compute_metrics(self, dataset: str, eval_sheet: str, use_assessed: bool = False) -> bool:
        """
        Step 4: Compute evaluation metrics.
        
        Args:
            dataset: Dataset name
            eval_sheet: Path to evaluation sheet CSV
            use_assessed: If True, look for manually assessed version
            
        Returns:
            True if successful
        """
        paths = self.config.get('paths', {})
        
        # If using assessed files, look in processed_files directory
        if use_assessed:
            processed_dir = paths.get('evaluation_processed_dir', 'evaluation/processed_files')
            # Try to find assessed version
            import glob
            import os
            basename = os.path.basename(eval_sheet).replace('.csv', '_assessed.csv')
            assessed_file = os.path.join(processed_dir, basename)
            
            if os.path.exists(assessed_file):
                print(f"Using manually assessed file: {assessed_file}")
                eval_sheet = assessed_file
            else:
                # Try to find any assessed file for this dataset
                pattern = os.path.join(processed_dir, f"*_{dataset}_*_assessed.csv")
                existing_files = sorted(glob.glob(pattern), reverse=True)
                if existing_files:
                    eval_sheet = existing_files[0]
                    print(f"Using manually assessed file: {eval_sheet}")
                else:
                    print(f"Warning: No assessed file found for {dataset}")
                    print(f"Looking for: {assessed_file}")
                    print(f"The evaluation sheet needs manual assessment before computing metrics.")
                    return False
        
        if not eval_sheet or not os.path.exists(eval_sheet):
            print(f"Evaluation sheet not found: {eval_sheet}")
            return False
        
        results_dir = paths.get('evaluation_results_dir', 'evaluation/results')
        plots_dir = paths.get('evaluation_plots_dir', 'evaluation/plots')
        
        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)
        
        output_basename = os.path.basename(eval_sheet).replace('.csv', '.json')
        results_file = os.path.join(results_dir, output_basename)
        
        cmd = [
            sys.executable,
            "src/evaluate.py",
            "--input_file", eval_sheet,
            "--output_file", results_file,
            "--output_dir", plots_dir
        ]
        
        return self._run_command(
            cmd,
            f"Step 4: Compute metrics for {dataset}"
        )
    
    def step_5_combine_results(self, dataset: str, eval_output: str, inference_output: str) -> bool:
        """
        Step 5: Optionally combine evaluation and inference results.
        
        Args:
            dataset: Dataset name
            eval_output: Path to evaluation results JSON
            inference_output: Path to inference results JSON
            
        Returns:
            True if successful
        """
        if not self.config.get('evaluation', {}).get('combine_results', False):
            print("Result combination disabled, skipping...")
            return True
        
        if not inference_output or not os.path.exists(inference_output):
            print(f"Inference output not found: {inference_output}")
            print("   Skipping combination step")
            return True
        
        combined_dir = "inference/combined"
        os.makedirs(combined_dir, exist_ok=True)
        combined_file = os.path.join(combined_dir, f"{dataset}.json")
        
        cmd = [
            sys.executable,
            "src/combine_eval_inference.py",
            "--input_file_1", eval_output,
            "--input_file_2", inference_output,
            "--output_file", combined_file
        ]
        
        return self._run_command(
            cmd,
            f"Step 5: Combine evaluation and inference results for {dataset}"
        )
    
    def run_pipeline(self, dataset: str, use_existing_predictions: bool = False, use_assessed_sheets: bool = False) -> bool:
        """
        Run the complete evaluation pipeline for a dataset.
        
        Args:
            dataset: Dataset name (e.g., 'EMA', 'Japan')
            use_existing_predictions: If True, skip LLM generation and use existing outputs
            use_assessed_sheets: If True, use manually assessed evaluation sheets
            
        Returns:
            True if all steps successful
        """
        print(f"\n{'#'*60}")
        print(f"# EVALUATION PIPELINE: {dataset}")
        print(f"# Timestamp: {self.timestamp}")
        if use_existing_predictions:
            print(f"# Mode: Using existing predictions")
        if use_assessed_sheets:
            print(f"# Mode: Using manually assessed sheets")
        print(f"{'#'*60}\n")
        
        # Step 1: Prepare data
        if not self.step_1_prepare_data(dataset):
            print(f"\nPipeline failed at Step 1 for {dataset}")
            return False
        
        # Step 2: Generate predictions
        success, llm_output = self.step_2_generate_predictions(dataset, use_existing=use_existing_predictions)
        if not success:
            print(f"\nPipeline failed at Step 2 for {dataset}")
            return False
        
        # Step 3: Create evaluation sheet
        success, eval_sheet = self.step_3_create_evaluation_sheet(dataset, llm_output)
        if not success:
            print(f"\nPipeline failed at Step 3 for {dataset}")
            return False
        
        # Step 4: Compute metrics
        if not self.step_4_compute_metrics(dataset, eval_sheet, use_assessed=use_assessed_sheets):
            print(f"\nPipeline failed at Step 4 for {dataset}")
            return False
        
        # Step 5: Combine results (optional)
        # Note: inference_output path would need to be determined based on your setup
        # self.step_5_combine_results(dataset, llm_output, inference_output)
        
        print(f"\n{'#'*60}")
        print(f"# PIPELINE COMPLETE: {dataset}")
        print(f"{'#'*60}\n")
        
        return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the complete evaluation pipeline for DrugFork datasets"
    )
    parser.add_argument(
        "--dataset",
        help="Specific dataset to evaluate (e.g., 'EMA', 'Swissmedic', 'PMDA', 'TGA')"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run pipeline for all datasets in config"
    )
    parser.add_argument(
        "--config",
        default="config/evaluation_config.yaml",
        help="Path to evaluation configuration file"
    )
    parser.add_argument(
        "--use-existing-predictions",
        action="store_true",
        help="Skip LLM generation and use existing prediction files"
    )
    parser.add_argument(
        "--use-assessed-sheets",
        action="store_true",
        help="Use manually assessed evaluation sheets (with verdict columns filled)"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_args()
    
    # Validate arguments
    if not args.dataset and not args.all:
        print("Error: Must specify either --dataset or --all")
        sys.exit(1)
    
    if not os.path.exists(args.config):
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    
    # Initialize pipeline
    pipeline = EvaluationPipeline(args.config)
    
    # Determine which datasets to process
    if args.all:
        datasets = pipeline.config.get('datasets', [])
        print(f"Running pipeline for all datasets: {', '.join(datasets)}")
    else:
        datasets = [args.dataset]
        print(f"Running pipeline for dataset: {args.dataset}")
    
    # Run pipeline for each dataset
    results = {}
    for dataset in datasets:
        results[dataset] = pipeline.run_pipeline(
            dataset, 
            use_existing_predictions=args.use_existing_predictions,
            use_assessed_sheets=args.use_assessed_sheets
        )
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    
    for dataset, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{dataset}: {status}")
    
    # Exit with appropriate code
    all_successful = all(results.values())
    sys.exit(0 if all_successful else 1)


if __name__ == "__main__":
    main()
