EM2 Repository Overview
=======================

This repository collects the experiment code, data processing scripts, analysis notebooks, and results for the EM2 project. Use this README as a map to the key components and typical workflows.

Quick Start
-----------
- Clone and set the working directory: `cd EM2`.
- Recommended Python: 3.10+ (see sound/requirements.txt for commonly used packages in the audio pipeline).
- Open notebooks in VS Code or Jupyter from Analysis/, find_compression_rate/, sound/, or project/.
- Keep raw data in place; notebooks assume the existing relative layout.

Repository Map
--------------
- Analysis/ — Dataframes and statistical notebooks (main experiment, control, d-prime, summaries) plus intermediate CSVs.
- Dataframes/ — Additional processed data and plotting scripts (when present).
- data-from-28-11-maybe-duplicate/ — Raw control and detection CSV/psydat files for a specific collection date.
- experiment/ — Experiment presentation code (forced choice, main, control detection) with stimuli (audio, babbling, faces, masks, primes) and collected data folders.
- find_compression_rate/ — Scripts and notebooks to compute d-prime under varying audio compression rates; includes generated result CSVs.
- noise_gif/ — Utility to generate noise GIFs used in stimuli.
- project/ — Project-level scripts and supplementary material (e.g., KDEF face dataset metadata) plus sample data.
- R-code/ — Quarto/R scripts for analysis (control-analysis.qmd, main_analyse.qmd, d-prime exploration) and combined CSVs.
- sound/ — Audio processing notebooks, helper scripts, and input sound files used in experiments.
- words-for-EM/ — Word lists and related resources for the experiment.

Main Workflows
--------------
- Run experiments: use experiment/experiment/mainV1.py or experiment/experiment/forced_choice.py for main tasks; use experiment/control_experiment/d-prime_detection.py for control/detection. Data is saved in the adjacent data/, data_control/, and data_detection/ folders.
- Process audio and compression: run notebooks/scripts in find_compression_rate/ to generate compressed stimuli and compute d-prime metrics; results land in find_compression_rate/results/.
- Analyze behavior and stats: use notebooks in Analysis/ and Quarto docs in R-code/ to produce summaries and statistical outputs from combined datasets.

Data and Results
----------------
- Raw experiment outputs: experiment/experiment/data/, experiment/experiment/data_control/, and data-from-28-11-maybe-duplicate/.
- Intermediate/combined datasets: Analysis/combined_data.csv, Analysis/combined_control_data.csv, and related d-prime CSVs.
- Derived results: find_compression_rate/results/ contains dated d-prime result files; see Analysis/bayes_summary.txt and R-code outputs for summaries.

Notebooks
---------
- Python: Analysis/*.ipynb, find_compression_rate/*.ipynb, sound/*.ipynb, project/test.ipynb, experiment/experiment/temporary.ipynb.
- R/Quarto: R-code/*.qmd for control and main experiment analyses.

Repro Tips
----------
- Create a virtual environment and install dependencies (start from sound/requirements.txt; add any extras noted in notebooks).
- For R/Quarto workflows, install the packages referenced in the .qmd documents.
- Preserve folder names and relative paths; scripts assume the current layout for stimuli and outputs.

Conventions
-----------
- Directory names reflect experiment phases (main vs control) and processing stages (raw, combined, results).
- D-prime calculations appear in both Python (find_compression_rate/, Analysis/) and R (R-code/Looking_at_d-prime.qmd).

Maintainers
-----------
- Add names/contact details here for collaborators and future contributors.

