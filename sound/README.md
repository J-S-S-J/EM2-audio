Sound Assets and Scripts
========================

This directory includes scripts and notebooks for creating and managing all audio used in the experiments.

Contents
--------
- sound_files/ — Source and generated audio files.
- words-for-EM/ — Word lists and related text inputs.
- convert_files.ipynb, sound.ipynb — Notebooks for conversion, preprocessing, and checks.
- requirements.txt — Reference list of Python packages used for the audio workflow.

Getting Started
---------------
1) Create/activate a Python environment: python -m venv .venv && source .venv/bin/activate.
2) Install dependencies: pip install -r requirements.txt.
3) Open the notebooks to convert or inspect audio; outputs are stored within sound_files/ unless otherwise configured.

Notes
-----
- Keep relative paths unchanged so experiment scripts can find the generated stimuli.
- Add any extra packages noted in the notebooks if new processing steps are introduced.