# DrugFork

DrugFork is a research codebase for extracting, standardizing, and analyzing drug approval information across multiple regulatory agencies.

## What This Repository Contains

- `src/`: core Python modules for preprocessing, extraction, evaluation, and analysis helpers
- `data/`: input datasets, curated datasets, and annotation files
- `notebooks/`: analysis and paper-support notebooks
- `evaluation/`: evaluation sheets, processed assessments, metrics, and plots
- `output/`: model outputs and derived exports
- `run_*.sh` (repo root): pipeline and utility scripts
- `docs/`: agency-specific and metadata documentation

## Quick Start

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Run the main evaluation workflow:

```bash
./run_full_evaluation.sh --help
./run_full_evaluation.sh EMA
```

## Common Paths

- Main datasets: `data/datasets/`
- Notebook analyses: `notebooks/`
- Evaluation outputs: `evaluation/output/`, `evaluation/results/`, `evaluation/plots/`
- Model outputs: `output/`

## Notes

- Scripts live directly in the repository root.
- Main entrypoint: `./run_full_evaluation.sh`.

## License

MIT. See `LICENSE`.
