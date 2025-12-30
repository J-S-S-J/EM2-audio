# EM2 Project

This repository contains experimental scripts, data processing tools, and analysis code for our EM2 exam project.

## Directory Structure

### Dataframes/
Contains processed data files and Jupyter notebooks for combining and organizing experimental data:
- Combined CSV files from control, main, and d-prime experiments
- Notebooks for creating dataframes from raw experimental data

### experiment/
Main experimental code and data:
- **control_experiment/** - Detection threshold experiment using d-prime analysis to find optimal compression rates
  - Audio stimuli at different compression levels (0.1-0.7)
  - Detection data from participants
  - Masks and babbling audio files
- **experiment/** - Main forced-choice experiment and related data
  - Face stimuli, primes, and masks
  - Participant response data

### find_compression_rate/
Scripts and notebooks for determining optimal audio compression rates:
- D-prime calculations for different compression levels
- Processing tools for analyzing detection performance
- Test compression audio files

### KDEF_Face_database_scripts/
Tools for working with the KDEF (Karolinska Directed Emotional Faces) database:
- Scripts to process and organize face stimuli
- Metadata from the KDEF database

### noise_gif/
Script for generating visual noise patterns used as masks in the experiment

### R-code/
Statistical analysis scripts written in R/Quarto:
- Control experiment analysis
- Main experiment analysis
- D-prime visualizations and reports

### sound/
Audio processing utilities:
- Converting and manipulating sound files
- Creating babbling, primes, and trial audio
- Word selection for emotional priming stimuli
