# Quick Start Guide

Get your Southwest Airlines OTP and Load Factor analysis up and running in minutes!

## Step 1: Verify Data Files

Make sure your data is in the right place:

```
data/
├── raw/
│   ├── OTP_Data/
│   │   ├── JAN_2020_OTP_SEGMENT.csv
│   │   ├── FEB_2020_OTP_SEGMENT.csv
│   │   └── ... (all monthly files through JUN_2025)
│   │
│   └── Load_Factor_Data/
│       ├── 2020_Segment.csv
│       ├── 2021_Segment.csv
│       ├── 2022_Segment.csv
│       ├── 2023_Segment.csv
│       ├── 2024_Segment.csv
│       └── 2025_Segment.csv
│
└── processed/  (will be created automatically)
```

## Step 2: Set Up Environment

```bash
# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Analysis

### Option A: Run All Notebooks (Recommended)

```bash
# Start Jupyter
jupyter notebook

# Then open and run notebooks in order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_route_analysis.ipynb
# 3. notebooks/03_otp_loadfactor_analysis.ipynb
```

### Option B: Quick Python Script

If you want to run everything programmatically, create `run_analysis.py`:

```python
import sys
sys.path.append('.')

from src import DataLoader, DataCleaner, MetricsCalculator
import pandas as pd

print("Loading data...")
loader = DataLoader(base_path='data/raw')
lf_raw, otp_raw = loader.load_all_data()

print("\nCleaning data...")
cleaner = DataCleaner(carrier_code='WN')
lf_clean = cleaner.clean_load_factor_data(lf_raw)
otp_clean = cleaner.clean_otp_data(otp_raw)

print("\nIdentifying top 5 routes...")
top_5_routes = cleaner.get_top_routes(lf_clean, n=5, metric='PASSENGERS')

print("\nFiltering for top routes...")
lf_top5 = lf_clean[lf_clean['ROUTE'].isin(top_5_routes)]
otp_top5 = otp_clean[otp_clean['ROUTE'].isin(top_5_routes)]

print("\nMerging datasets...")
calc = MetricsCalculator()
merged = calc.merge_lf_otp_by_route_month(lf_top5, otp_top5)

print("\nCalculating correlations...")
for route in top_5_routes:
    stats = calc.route_summary_stats(merged, route)
    if stats:
        print(f"\n{route}:")
        print(f"  LF vs Dep OTP: r={stats['corr_lf_dep_ontime']:.3f}, p={stats['corr_lf_dep_pvalue']:.4f}")
        print(f"  LF vs Arr OTP: r={stats['corr_lf_arr_ontime']:.3f}, p={stats['corr_lf_arr_pvalue']:.4f}")

print("\n✓ Analysis complete! Check the notebooks for detailed visualizations.")
```

Then run:
```bash
python run_analysis.py
```

## Step 4: Review Results

1. **Check processed data:**
   - `data/processed/` folder contains cleaned datasets
   - Open CSV files to verify data quality

2. **Review visualizations:**
   - All plots are generated in the notebooks
   - Time series, scatter plots, correlations

3. **Read the report:**
   - Open `reports/final_report.md`
   - Fill in the findings based on your analysis

## Expected Runtime

- **01_data_exploration.ipynb**: 2-5 minutes
- **02_route_analysis.ipynb**: 1-3 minutes  
- **03_otp_loadfactor_analysis.ipynb**: 3-7 minutes

**Total**: ~10-15 minutes for complete analysis

## Verification Checklist

After running, verify you have:

- [ ] Cleaned data files in `data/processed/`
- [ ] Top 5 routes identified and saved
- [ ] Merged dataset with both LF and OTP metrics
- [ ] Correlation statistics calculated
- [ ] Visualizations generated in notebooks
- [ ] Summary statistics saved to CSV

## Common First-Run Issues

**Problem:** "No files found" error  
**Solution:** Double-check your data folder structure matches Step 1

**Problem:** Import errors  
**Solution:** Make sure you activated your virtual environment

**Problem:** Notebook kernel won't start  
**Solution:** Run `python -m ipykernel install --user --name=venv`

**Problem:** Plots not showing  
**Solution:** Add `%matplotlib inline` at the top of notebooks

## Next Steps

After your first successful run:

1. Examine the correlation results - are they significant?
2. Look at individual route patterns - which routes behave differently?
3. Check the load factor bins - is there a threshold effect?
4. Fill out the final report template with your findings
5. Consider additional analyses (seasonal patterns, COVID impact, etc.)

## Getting Help

If you encounter issues:

1. Check the main README.md for detailed documentation
2. Review error messages carefully
3. Verify data file formats match expected structure
4. Ensure all dependencies are installed correctly

## Advanced: Customize Your Analysis

Want to analyze different routes or carriers?

```python
# In notebooks, modify:
cleaner = DataCleaner(carrier_code='AA')  # Change to American Airlines
top_routes = cleaner.get_top_routes(lf_clean, n=10, metric='PASSENGERS')  # Top 10 routes
```

Want different time periods?

```python
# Filter to specific dates
filtered = cleaner.filter_date_range(df, start_date='2023-01-01', end_date='2023-12-31')
```

## Ready to Start?

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

Happy analyzing! 🛫📊