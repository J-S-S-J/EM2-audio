EM2 Repository Overview
=======================

This repository collects the experiment code, data processing scripts, analysis notebooks, and results for the EM2 project. Use this README as a map to the key components and typical workflows.

Quick Start
-----------
- Clone and set the working directory: `cd EM2`.
- Recommended Python: 3.10+ (see `sound/requirements.txt` for a reference list of packages used in the audio pipeline).
- Notebooks live under `Analysis/`, `find_compression_rate/`, `sound/`, and `project/`—open in Jupyter or VS Code.

Repository Map
--------------
- `Analysis/` — Dataframes and statistical notebooks (main experiment, control, d-prime, and summary reports) plus intermediate CSVs.
- `data-from-28-11-maybe-duplicate/` — Raw control and detection CSV/psydat files for a specific collection date.
- `experiment/` — Experiment presentation code (forced choice, main, and control detection) with stimuli (audio, babbling, faces, masks, primes) and collected data folders.
- `find_compression_rate/` — Scripts and notebooks to compute d-prime under varying audio compression rates; includes generated result CSVs.
- `noise_gif/` — Utility to generate noise GIFs.
- `project/` — Project-level scripts and supplementary material (e.g., KDEF face dataset metadata) plus sample data.
- `R-code/` — Quarto/R scripts for analysis (`control-analysis.qmd`, `main_analyse.qmd`, d-prime exploration) and combined CSVs.
- `sound/` — Audio processing notebooks, helper scripts, and input sound files used in experiments.
- `words-for-EM/` — Word lists and related resources for the experiment.

Main Workflows
--------------
- Run experiments: use the scripts in `experiment/experiment/` (e.g., `mainV1.py`, `forced_choice.py`) and `experiment/control_experiment/` (`d-prime_detection.py`); collected data lands in the adjacent `data/` and `data_control/` folders.
- Process audio and compression: notebooks and scripts in `find_compression_rate/` handle generating compressed stimuli and computing d-prime metrics; results are saved under `find_compression_rate/results/`.
- Analyze behavior and stats: notebooks in `Analysis/` and Quarto docs in `R-code/` produce summaries and statistical outputs from combined datasets.

Data and Results
----------------
- Raw experiment outputs: see `experiment/experiment/data/`, `experiment/experiment/data_control/`, and `data-from-28-11-maybe-duplicate/`.
- Intermediate/combined datasets: `Analysis/combined_data.csv`, `Analysis/combined_control_data.csv`, and related d-prime CSVs.
- Derived results: `find_compression_rate/results/` holds dated d-prime result files; additional summaries live in `Analysis/bayes_summary.txt` and R outputs.

Notebooks
---------
- Python: `Analysis/*.ipynb`, `find_compression_rate/*.ipynb`, `sound/*.ipynb`, `project/test.ipynb`, `experiment/experiment/temporary.ipynb`.
- R/Quarto: `R-code/*.qmd` for control and main experiment analyses.

Repro Tips
----------
- Keep raw data in place; many notebooks reference relative paths within this repo.
- For Python notebooks, create a virtual environment and install dependencies (see `sound/requirements.txt`; add any missing packages as needed).
- For R/Quarto workflows, ensure you have the required packages from the `.qmd` documents installed.

Conventions
-----------
- Directory names reflect experiment phases (main vs control) and processing stages (raw, combined, results).
- D-prime calculations are performed in both Python (`find_compression_rate/`, `Analysis/`) and R (`R-code/Looking_at_d-prime.qmd`).

Maintainers
-----------
- Add names/contact details here for collaborators and future contributors.
