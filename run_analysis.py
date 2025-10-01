"""
Complete analysis script for Southwest Airlines OTP and Load Factor study.

This script runs the entire analysis pipeline:
1. Loads raw data
2. Cleans and filters for Southwest
3. Identifies top 5 routes
4. Merges datasets
5. Calculates correlations and statistics
6. Saves all results

Run this script from the project root directory.
"""

import sys
import os
sys.path.append('.')

from src import DataLoader, DataCleaner, MetricsCalculator
import pandas as pd
import numpy as np
from pathlib import Path


def create_directories():
    """Ensure necessary directories exist."""
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    print("✓ Directories verified")


def main():
    print("="*80)
    print("SOUTHWEST AIRLINES: OTP AND LOAD FACTOR ANALYSIS")
    print("="*80)
    print()
    
    # Create directories
    create_directories()
    
    # Step 1: Load Data
    print("STEP 1: LOADING DATA")
    print("-" * 80)
    loader = DataLoader(base_path='data/raw')
    try:
        lf_raw, otp_raw = loader.load_all_data()
        print("✓ Data loaded successfully\n")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("Please ensure data files are in data/raw/OTP_Data and data/raw/Load_Factor_Data")
        return
    
    # Step 2: Clean Data
    print("\nSTEP 2: CLEANING DATA")
    print("-" * 80)
    cleaner = DataCleaner(carrier_code='WN')
    lf_clean = cleaner.clean_load_factor_data(lf_raw)
    print()
    otp_clean = cleaner.clean_otp_data(otp_raw)
    print("✓ Data cleaned successfully\n")
    
    # Save cleaned data
    lf_clean.to_csv('data/processed/lf_clean_southwest.csv', index=False)
    otp_clean.to_csv('data/processed/otp_clean_southwest.csv', index=False)
    print("✓ Cleaned data saved to data/processed/\n")
    
    # Step 3: Identify Top 5 Routes
    print("\nSTEP 3: IDENTIFYING TOP 5 ROUTES")
    print("-" * 80)
    top_5_routes = cleaner.get_top_routes(lf_clean, n=5, metric='PASSENGERS')
    print("✓ Top 5 routes identified\n")
    
    # Filter for top routes
    lf_top5 = lf_clean[lf_clean['ROUTE'].isin(top_5_routes)].copy()
    otp_top5 = otp_clean[otp_clean['ROUTE'].isin(top_5_routes)].copy()
    
    # Save top 5 data
    lf_top5.to_csv('data/processed/lf_top5_routes.csv', index=False)
    otp_top5.to_csv('data/processed/otp_top5_routes.csv', index=False)
    pd.DataFrame({'ROUTE': top_5_routes}).to_csv('data/processed/top5_routes.csv', index=False)
    print("✓ Top 5 routes data saved\n")
    
    # Step 4: Merge Datasets
    print("\nSTEP 4: MERGING DATASETS")
    print("-" * 80)
    calc = MetricsCalculator()
    merged = calc.merge_lf_otp_by_route_month(lf_top5, otp_top5)
    print(f"✓ Merged dataset created: {merged.shape[0]} route-months\n")
    
    # Save merged data
    merged.to_csv('data/processed/merged_lf_otp_top5.csv', index=False)
    print("✓ Merged data saved\n")
    
    # Step 5: Calculate Statistics
    print("\nSTEP 5: CALCULATING STATISTICS")
    print("-" * 80)
    
    # Overall correlations
    print("\nOVERALL CORRELATIONS (All Routes Combined):")
    print("-" * 80)
    corr_dep = calc.calculate_correlation(merged, 'LOAD_FACTOR', 'DEP_ONTIME_PCT')
    corr_arr = calc.calculate_correlation(merged, 'LOAD_FACTOR', 'ARR_ONTIME_PCT')
    
    print(f"Load Factor vs Departure OTP:")
    print(f"  Pearson r = {corr_dep['correlation']:.4f}")
    print(f"  p-value   = {corr_dep['p_value']:.6f}")
    print(f"  n         = {corr_dep['n']}")
    
    if corr_dep['p_value'] < 0.001:
        sig = "***"
    elif corr_dep['p_value'] < 0.01:
        sig = "**"
    elif corr_dep['p_value'] < 0.05:
        sig = "*"
    else:
        sig = "ns"
    print(f"  Significance: {sig}")
    
    print(f"\nLoad Factor vs Arrival OTP:")
    print(f"  Pearson r = {corr_arr['correlation']:.4f}")
    print(f"  p-value   = {corr_arr['p_value']:.6f}")
    print(f"  n         = {corr_arr['n']}")
    
    if corr_arr['p_value'] < 0.001:
        sig = "***"
    elif corr_arr['p_value'] < 0.01:
        sig = "**"
    elif corr_arr['p_value'] < 0.05:
        sig = "*"
    else:
        sig = "ns"
    print(f"  Significance: {sig}")
    
    # Route-by-route statistics
    print("\n\nROUTE-BY-ROUTE ANALYSIS:")
    print("-" * 80)
    
    summary_stats = []
    for i, route in enumerate(top_5_routes, 1):
        stats = calc.route_summary_stats(merged, route)
        if stats:
            summary_stats.append(stats)
            print(f"\n{i}. {route}")
            print(f"   Total Flights:        {stats['total_flights']:,.0f}")
            print(f"   Avg Load Factor:      {stats['avg_load_factor']:.2f}%")
            print(f"   Avg Departure OTP:    {stats['avg_dep_ontime_pct']:.2f}%")
            print(f"   Avg Arrival OTP:      {stats['avg_arr_ontime_pct']:.2f}%")
            print(f"   Correlation (LF-Dep): {stats['corr_lf_dep_ontime']:.4f} (p={stats['corr_lf_dep_pvalue']:.4f})")
            print(f"   Correlation (LF-Arr): {stats['corr_lf_arr_ontime']:.4f} (p={stats['corr_lf_arr_pvalue']:.4f})")
    
    # Save summary statistics
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('data/processed/route_summary_statistics.csv', index=False)
    print("\n✓ Summary statistics saved\n")
    
    # Step 6: Load Factor Bin Analysis
    print("\nSTEP 6: LOAD FACTOR BIN ANALYSIS")
    print("-" * 80)
    
    merged['LF_BIN'] = pd.cut(merged['LOAD_FACTOR'], 
                               bins=[0, 70, 75, 80, 85, 100],
                               labels=['<70%', '70-75%', '75-80%', '80-85%', '85%+'])
    
    bin_analysis = merged.groupby('LF_BIN').agg({
        'DEP_ONTIME_PCT': 'mean',
        'ARR_ONTIME_PCT': 'mean',
        'CANCELLATION_PCT': 'mean',
        'TOTAL_FLIGHTS': 'sum'
    }).round(2)
    
    print("\nOTP by Load Factor Bin:")
    print(bin_analysis)
    print("✓ Bin analysis complete\n")
    
    # Summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nResults saved to:")
    print("  - data/processed/lf_clean_southwest.csv")
    print("  - data/processed/otp_clean_southwest.csv")
    print("  - data/processed/lf_top5_routes.csv")
    print("  - data/processed/otp_top5_routes.csv")
    print("  - data/processed/top5_routes.csv")
    print("  - data/processed/merged_lf_otp_top5.csv")
    print("  - data/processed/route_summary_statistics.csv")
    
    print("\nNext steps:")
    print("  1. Open notebooks for detailed visualizations")
    print("  2. Update reports/final_report.md with findings")
    print("  3. Review correlation results and patterns")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease check your data files and try again.")