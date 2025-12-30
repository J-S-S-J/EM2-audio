# Effects of Cross-Modal Emotional Subliminal Priming

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![PsychoPy](https://img.shields.io/badge/PsychoPy-00A651?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAACXBIWXMAAAsTAAALEwEAmpwYAAABNUlEQVQokZWSvyvFYRTHP8/rvhe3XCUlg8FgsJjcTRYLZTBZbP4Ag8FkM1gsBoPFYrFYDAaDwWAwGAwGg8Fg8ava+/bce9/3vE/nfM/5fs/3nO8RVUVEcBwHx3FQVUQEEUFVERFUFRHBdV1UVURE8DyPQqGA7/sYY1BVjDGoKsYYVBVjDKqKMQZVxff9QiAYDBIMBlFVVBVVRVURkUIgFAoRCoUKAVUlHA4TDodRVYwxhEIhQqEQqooxhlAoVAgEg0GCwSCqiqqiqoVANBolGo2iqhhjUFVUFWMMqooxBlVFVTHGFAKxWIxYLIaqYoxBVVFVjDGoKsYYVBVjDKqKMaYQiMfjxONxVBVjDKqKqmKMQVUxxqCqqCrGGFQVY0whkEgkSCQSqCqua2OMwXVdjDG4ro0xBte1Mcbgujb/BL4BNwKWyquoted/ggAAAAASUVORK5CYII=&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

</div>

---

## 📋 Overview

This repository contains experimental scripts, data processing tools, and analysis code for our EM2 exam project investigating the effects of cross-modal emotional subliminal priming on perception and decision-making.

---

## 📂 Repository Structure

### 📊 `Dataframes/`
**Purpose:** Data consolidation and preprocessing  
**Tools:** `pandas`, `numpy`, Jupyter Notebook

Contains processed data files and notebooks for combining experimental data:
- ✅ Combined CSV files from control, main, and d-prime experiments
- 📓 Interactive notebooks for dataframe creation and validation
- 🔄 Data transformation and cleaning scripts

---

### 🧪 `experiment/`
**Purpose:** Core experimental implementation  
**Tools:** PsychoPy, Python

#### `control_experiment/`
Detection threshold experiment using d-prime analysis to determine optimal compression rates
- 🎵 Audio stimuli at varying compression levels (0.1-0.7)
- 📈 Participant detection performance data
- 🎭 Auditory masks and babbling stimuli

#### `experiment/`
Main forced-choice paradigm
- 😊 Face stimuli from KDEF database
- ⚡ Subliminal prime presentation
- 🎯 Participant choice data and response times

---

### 🔍 `find_compression_rate/`
**Purpose:** Stimulus optimization  
**Tools:** `scipy.stats`, `pandas`, Jupyter Notebook

Scripts and analyses for determining optimal audio compression:
- 📉 D-prime calculations across compression levels
- 📊 Signal detection theory analysis
- 🧮 Chi-square statistical tests
- 🎚️ Test audio files at multiple compression rates

---

### 👤 `KDEF_Face_database_scripts/`
**Purpose:** Stimulus preparation  
**Tools:** Python, `pandas`

Processing pipeline for KDEF (Karolinska Directed Emotional Faces) database:
- 🖼️ Face image organization and selection
- 📋 Metadata management and filtering
- ⚙️ Automated stimulus preparation

---

### 🎨 `noise_gif/`
**Purpose:** Visual masking  
**Tools:** Python imaging libraries

Script for generating dynamic visual noise patterns used as backward masks in the experimental paradigm

---

### 📈 `R-code/`
**Purpose:** Statistical analysis and reporting  
**Tools:** R, Quarto, `ggplot2`, `tidyverse`

Comprehensive statistical analyses and visualizations:
- 🔬 Control experiment analysis (detection thresholds)
- 🧠 Main experiment analysis (priming effects)
- 📊 D-prime visualizations and significance testing
- 📄 HTML reports with reproducible analysis

---

### 🔊 `sound/`
**Purpose:** Auditory stimulus creation  
**Tools:** Python audio libraries, Jupyter Notebook

Audio processing and stimulus generation:
- 🎵 Sound file format conversion
- 🔀 Audio manipulation and editing
- 🗣️ Babbling and prime creation
- 📝 Emotional word selection and validation
  - Positive, negative, and neutral word sets
  - Word norming data

---

## 🚀 Getting Started

### Prerequisites
```bash
# Python dependencies
pip install -r sound/requirements.txt

# Core libraries
pip install psychopy pandas numpy scipy jupyter
```

### Running Experiments
1. **Control Experiment:** [experiment/control_experiment/d-prime_detection.py](experiment/control_experiment/d-prime_detection.py)
2. **Main Experiment:** [experiment/experiment/mainV1.py](experiment/experiment/mainV1.py)

### Data Analysis
1. Process raw data: Use notebooks in `Dataframes/`
2. Statistical analysis: Run Quarto documents in `R-code/`

---

## 📚 Key Concepts

- **D-prime (d′):** Sensitivity measure from signal detection theory
- **Subliminal Priming:** Brief stimulus presentation below conscious threshold
- **Cross-modal:** Integration of auditory and visual information
- **Forced-choice:** Binary decision paradigm for measuring perception

---

## 📝 Citation

If you use this code or methodology, please cite:
```
EM2 Project: Effects of Cross-Modal Emotional Subliminal Priming (2025)
```
