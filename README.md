# Effects of Cross-Modal Emotional Subliminal Priming

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![PsychoPy](https://img.shields.io/badge/PsychoPy-00A651?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAACXBIWXMAAAsTAAALEwEAmpwYAAABNUlEQVQokZWSvyvFYRTHP8/rvhe3XCUlg8FgsJjcTRYLZTBZbP4Ag8FkM1gsBoPFYrFYDAaDwWAwGAwGg8Fg8ava+/bce9/3vE/nfM/5fs/3nO8RVUVEcBwHx3FQVUQEEUFVERFUFRHBdV1UVURE8DyPQqGA7/sYY1BVjDGoKsYYVBVjDKqKMQZVxff9QiAYDBIMBlFVVBVVRVURkUIgFAoRCoUKAVUlHA4TDodRVYwxhEIhQqEQqooxhlAoVAgEg0GCwSCqiqqiqoVANBolGo2iqhhjUFVUFWMMqooxBlVFVTHGFAKxWIxYLIaqYoxBVVFVjDGoKsYYVBVjDKqKMaYQiMfjxONxVBVjDKqKqmKMQVUxxqCqqCrGGFQVY0whkEgkSCQSqCqua2OMwXVdjDG4ro0xBte1Mcbgujb/BL4BNwKWyquoted/ggAAAAASUVORK5CYII=&logoColor=white)

This repository contains experimental scripts, data processing tools, and analysis code for our EM2 exam project investigating the effects of cross-modal emotional subliminal priming.

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
