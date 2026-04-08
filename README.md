# DrugFork

DrugFork is a research codebase for extracting, standardizing, and analyzing drug approval information across multiple regulatory agencies.

## What This Repository Contains

- `src/`: core Python modules for preprocessing, extraction, evaluation, and analysis helpers
- `data/`: input datasets, curated datasets, and annotation files
- `notebooks/`: analysis and paper-support notebooks
- `evaluation/`: evaluation sheets, processed assessments, metrics, and plots
- `output/`: model outputs and derived exports
- `scripts/pipelines/`: main pipeline entrypoints
- `scripts/ad_hoc/`: utility scripts for one-off tasks
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

- Root `run_*.sh` scripts are compatibility wrappers.
- Canonical script locations are under `scripts/`.

## License

MIT. See `LICENSE`.
