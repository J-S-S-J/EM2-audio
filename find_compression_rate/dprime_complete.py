import numpy as np
import pandas as pd
from scipy.stats import norm, chi2_contingency
import os

def dprime(hit_rate, fa_rate, n_trials=100):
    """Compute d′ from hit and false alarm rates with correction for 0/1."""
    # Correction to avoid inf z-scores
    if hit_rate == 1: hit_rate = 1 - 1/(2*n_trials)
    if hit_rate == 0: hit_rate = 1/(2*n_trials)
    if fa_rate == 1:  fa_rate  = 1 - 1/(2*n_trials)
    if fa_rate == 0:  fa_rate  = 1/(2*n_trials)
    return norm.ppf(hit_rate) - norm.ppf(fa_rate)

def chi_square_from_rates(hit_rate, fa_rate, n_trials=112):
    """Run chi test comparing detection vs. guessing."""
    n_signal = n_noise = n_trials / 2
    obs = np.array([
        [hit_rate * n_signal, (1 - hit_rate) * n_signal],
        [fa_rate  * n_noise,  (1 - fa_rate)  * n_noise]
    ])
    chi2, p, _, _ = chi2_contingency(obs)
    return chi2, p

def signif_marker(p):
    """Return asterisk for significance."""
    if p < 0.001: return "**"
    elif p < 0.05: return "*"
    else: return ""

def concat_csvs(file_list):
    return pd.concat(file_list, ignore_index=True)

def compute_rate_results(df):
    list_of_compression_rates = df["compression_level"].unique()
    results = pd.DataFrame()
    for rate in list_of_compression_rates:
        df_rate = df[df["compression_level"] == rate]
        hit_rate = len(df_rate[df_rate["trial_outcome"] == "Hit"]) / len(df_rate)
        false_alarm_rate = len(df_rate[df_rate["trial_outcome"] == "False Alarm"]) / len(df_rate)
        d_prime = dprime(hit_rate, false_alarm_rate, n_trials=len(df_rate))
        chi2, p = chi_square_from_rates(hit_rate, false_alarm_rate, n_trials=len(df_rate))
        # create df with rate on rows and d', chi2, p as columns
        new_row = pd.DataFrame({
            "compression_rate": [rate],
            "d_prime": [f"{d_prime:.2f}{signif_marker(p)}"],
            "chi2": [f"{chi2:.2f}"],
            "p": [f"{p:.3f}"]
        })
        results = pd.concat([results, new_row], ignore_index=True)
    results["compression_rate"] = results["compression_rate"].astype(float)
    results = results.sort_values("compression_rate").reset_index(drop=True)
    return results

df_list = []
for file in os.listdir("../experiment/control_experiment/data_detection/ny_data"):
    if file.endswith(".csv"):
        print(f"Loading {file}")
        df_list.append(pd.read_csv(os.path.join("../experiment/control_experiment/data_detection/ny_data", file)))
df = concat_csvs(df_list)

results = compute_rate_results(df)