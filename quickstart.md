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
└── processed/  (will be created automatically once you run the notebooks (in order))
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

### Option B: Use a Code Editor (e.g., VS Code, PyCharm)

If you prefer working in a code editor instead of the terminal, follow these steps:

1. **Open the project folder** in your preferred code editor (such as **Visual Studio Code**, **PyCharm**, or **JupyterLab**).

2. **Create and activate a virtual environment** (in the built-in terminal of your editor):

```bash
   python -m venv venv

   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
```

3. **Install Required Packages**:
``` bash
pip install -r requirements.txt
``` 

4. **Run the notebooks in order inside your editor’s Jupyter environment**:
- **If using VS Code:**
   - Install the **Python** and **Jupyter** extensions if prompted.
   - Open the first notebook:  
   `notebooks/01_data_exploration.ipynb`
   - Click **“Run All”** or run the cells one by one.
   - Continue running the notebooks in order:
      1. `01_data_exploration.ipynb`
      2. `02_route_analysis.ipynb`
      3. `03_otp_loadfactor_analysis.ipynb`

- **If using JupyterLab:**
   - Launch JupyterLab from the terminal:
      ``` bash
         jupyter lab
      ```

- **Open each notebook and run the cells sequentially**

5. **Watch underneath each cell for outputs and review plots as they’re generated**



## Step 4: Review Results

1. **Check processed data:**
   - `data/processed/` folder contains cleaned datasets
      - These files are too large for GitHub, thus they were not already pre-generated.
   - Open CSV files to verify data quality

2. **Review visualizations:**
   - All plots are generated in the notebooks
   - Time series, scatter plots, correlations

3. **Read the final report:**
   - Use either `reports/final_report_completed.md` (Markdown) or `reports/final_report_completed.ipynb` (Notebook, Markdown cells) for your final report.
    - If you need to generate or update the report, run:
       ```bash
       python generate_report.py
       ```
    - This will create or update both report files in the `reports/` directory: one as Markdown (`final_report_completed.md`) and one as a Jupyter Notebook (`final_report_completed.ipynb`).
    - The `.ipynb` version is ideal for sharing or further editing in Jupyter, while the `.md` version is easy to view or print as plain text. Both contain the same content.
    - (The old `reports/final_report.md` is a template only.)

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

Thanks for reviewing the analysis!