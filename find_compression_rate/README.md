Compression Rate Analysis
=========================

Tools for generating compressed audio stimuli and computing d-prime metrics across compression levels.

Contents
--------
- audio/ — Pre-generated compressed audio at multiple rates (0.3–0.8 folders).
- dprime_complete.py — Core script to compute d-prime per condition.
- process_all_data.py — Batch runner to process all compressed files and aggregate results.
- create_test_compressions.ipynb, d_prime.ipynb — Notebooks for exploratory computation and validation.
- results/ — Dated CSV outputs of d-prime computations.

Typical Use
-----------
1) Ensure dependencies are installed (numpy, pandas, scipy, soundfile, etc.).
2) Generate or update compressed audio if needed (see audio/ structure).
3) Run python process_all_data.py to compute and export d-prime results; outputs are saved to results/.
4) Inspect or refine analysis in the notebooks for visualizations or additional checks.

Notes
-----
- D-prime is computed from z rates; chi-square checks follow the approach in Dehaene et al.
- Current stimulus count N = 4 yields a 0.4 time-compression rate in the main configuration.

