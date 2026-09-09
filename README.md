# Assignment 1: Reproducible Neutrino Workflow

This is the starter repository for PHYS690 Assignment 1. You will use VS Code, a local Python virtual environment, Jupyter notebooks, CSV input data, plotting, command-line Python scripts, documentation, and Git to produce a reproducible result.

## Repository Layout

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   └── raw/
│       ├── neutrino_data.csv
│       └── neutrino_simulation.csv
├── figures/
│   └── .gitkeep
├── notebooks/
│   └── assignment1_reproducible_neutrino_workflow.ipynb
└── scripts/
    └── make_neutrino_figure.py
```

## Setup

Open this repository folder in VS Code and use `Terminal > New Terminal`.

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

After installing packages, open `notebooks/assignment1_reproducible_neutrino_workflow.ipynb` and select the `.venv` Python kernel.

## Assignment Work

Complete the notebook in `notebooks/`. Then write a command-line Python script at `scripts/make_neutrino_figure.py` that reproduces the same figure from the CSV files without relying on notebook state. Your final result should include a plot saved to:

```text
figures/neutrino_data_simulation_ratio.png
```

You should also update this `README.md` so another person can rerun both the notebook and the command-line script from the CSV files.

## Submission

This repository should remain private inside the `WM-PHYS690-Fall2026` GitHub organization. Make meaningful commits as you work, then push your final work.

Finally, submit a "pull request" from the `submission` branch into `main` in your private assignment repository.  This will inform Prof. Stevens that your submission is ready to be evaluated.