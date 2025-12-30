Experiment Code
===============

This directory hosts the code and assets used to run the EM2 behavioral experiments.

Structure
---------
- experiment/ — Main study scripts and stimuli (faces, primes, masks, babbling, audio) with outputs in data/ and data_control/.
- control_experiment/ — Control/detection variant (d-prime) with its own stimuli and data_detection/ output.

Key Entry Points
----------------
- experiment/mainV1.py — Run the main experiment.
- experiment/forced_choice.py — Run the forced-choice variant.
- control_experiment/d-prime_detection.py — Run the control detection task.

Running
-------
1) From the repository root, create/activate a Python environment that has PsychoPy and standard scientific stack installed.
2) Navigate here: cd experiment.
3) Launch one of the scripts above (e.g., python experiment/mainV1.py).

Data Output
-----------
- Main experiments write to experiment/data/ and experiment/data_control/.
- Control detection writes to control_experiment/data_detection/.
Keep these paths stable; analysis notebooks reference them by relative location.