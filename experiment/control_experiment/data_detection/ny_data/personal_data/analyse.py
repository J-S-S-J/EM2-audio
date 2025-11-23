#!/usr/bin/env python3
"""
Automated D-Prime Analysis Script
Processes all CSV files in the data directory and generates results.
Can be run manually or as a git hook/cron job.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm, chi2_contingency
import os
import sys
from datetime import datetime
from pathlib import Path

# === Configuration ===
DATA_DIR = "/Users/johanandersen/Desktop/Python/EM2-audio/experiment/control_experiment/data_detection/ny_data/personal_data"
OUTPUT_DIR = "/Users/johanandersen/Desktop/Python/EM2-audio/experiment/control_experiment/data_detection/ny_data/personal_data"
OUTPUT_FILE = "personal_dprime_results_{timestamp}.csv"
SUMMARY_FILE = "dprime_summary.txt"

# === Analysis Functions ===

def dprime(hit_rate, fa_rate, n_trials=100):
    """Compute d′ from hit and false alarm rates with correction for 0/1."""
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
    if p < 0.001: return "***"
    elif p < 0.01: return "**"
    elif p < 0.05: return "*"
    else: return ""

def concat_csvs(file_list):
    """Concatenate list of DataFrames."""
    return pd.concat(file_list, ignore_index=True)

def compute_rate_results(df):
    """Compute d-prime results for each compression rate."""
    list_of_compression_rates = df["compression_level"].unique()
    results = pd.DataFrame()
    
    for rate in list_of_compression_rates:
        df_rate = df[df["compression_level"] == rate]
        
        # Calculate hit and false alarm rates
        hit_rate = len(df_rate[df_rate["trial_outcome"] == "Hit"]) / len(df_rate)
        false_alarm_rate = len(df_rate[df_rate["trial_outcome"] == "False Alarm"]) / len(df_rate)
        
        # Compute statistics
        d_prime = dprime(hit_rate, false_alarm_rate, n_trials=len(df_rate))
        chi2, p = chi_square_from_rates(hit_rate, false_alarm_rate, n_trials=len(df_rate))
        
        # Create result row
        new_row = pd.DataFrame({
            "compression_rate": [rate],
            "d_prime": [f"{d_prime:.2f}{signif_marker(p)}"],
            "d_prime_raw": [d_prime],
            "hit_rate": [f"{hit_rate:.3f}"],
            "fa_rate": [f"{false_alarm_rate:.3f}"],
            "chi2": [f"{chi2:.2f}"],
            "p": [f"{p:.3f}"],
            "n_trials": [len(df_rate)]
        })
        results = pd.concat([results, new_row], ignore_index=True)
    
    # Sort by compression rate
    results["compression_rate"] = results["compression_rate"].astype(float)
    results = results.sort_values("compression_rate").reset_index(drop=True)
    
    return results

def load_csv_files(data_dir):
    """Load all CSV files from the data directory."""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        sys.exit(1)
    
    csv_files = list(data_path.glob("*.csv"))
    
    if not csv_files:
        print(f"WARNING: No CSV files found in {data_dir}")
        return None
    
    print(f"Found {len(csv_files)} CSV file(s)")
    
    df_list = []
    for csv_file in csv_files:
        try:
            print(f"  Loading: {csv_file.name}")
            df = pd.read_csv(csv_file)
            df_list.append(df)
        except Exception as e:
            print(f"  ERROR loading {csv_file.name}: {e}")
    
    if not df_list:
        print("ERROR: No valid CSV files could be loaded")
        sys.exit(1)
    
    return concat_csvs(df_list)

def save_results(results, output_dir, timestamp):
    """Save results to CSV and generate summary text file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    csv_filename = OUTPUT_FILE.format(timestamp=timestamp)
    csv_path = output_path / csv_filename
    results.to_csv(csv_path, index=False)
    print(f"\n✓ Results saved to: {csv_path}")
    
    # Save summary text file
    summary_path = output_path / SUMMARY_FILE
    with open(summary_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write(f"D-Prime Analysis Summary\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        # Write table
        f.write(results[['compression_rate', 'd_prime', 'hit_rate', 'fa_rate', 'chi2', 'p', 'n_trials']].to_string(index=False))
        
        f.write("\n\n" + "=" * 70 + "\n")
        f.write("Significance markers:\n")
        f.write("  *** p < 0.001\n")
        f.write("  **  p < 0.01\n")
        f.write("  *   p < 0.05\n")
        f.write("=" * 70 + "\n")
    
    print(f"✓ Summary saved to: {summary_path}")
    
    return csv_path, summary_path

def print_results(results):
    """Print results to console."""
    print("\n" + "=" * 70)
    print("D-PRIME ANALYSIS RESULTS")
    print("=" * 70)
    print(results[['compression_rate', 'd_prime', 'hit_rate', 'fa_rate', 'p', 'n_trials']].to_string(index=False))
    print("=" * 70)
    print("\nSignificance: *** p<0.001, ** p<0.01, * p<0.05")
    print("=" * 70 + "\n")

def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("D-PRIME AUTOMATED ANALYSIS")
    print("=" * 70 + "\n")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Load data
    print(f"Loading CSV files from: {DATA_DIR}")
    df = load_csv_files(DATA_DIR)
    
    if df is None:
        return
    
    print(f"Total rows loaded: {len(df)}")
    print(f"Unique participants: {df.get('Participant ID', pd.Series()).nunique()}")
    
    # Compute results
    print("\nComputing d-prime statistics...")
    results = compute_rate_results(df)
    
    # Display results
    print_results(results)
    
    # Save results
    save_results(results, OUTPUT_DIR, timestamp)
    
    print("\n✓ Analysis complete!\n")
    
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)