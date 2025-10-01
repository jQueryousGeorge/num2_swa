# Project Summary: Southwest Airlines OTP and Load Factor Analysis

## Overview

This project provides a complete data analysis pipeline to answer the question: **"How does Southwest Airlines' On-Time Performance (OTP) relate to the Load Factor of its flights on their top 5 domestic routes?"**

## Explanation of each directory in the Project I've created:

### 1. **Core Python Modules** (`src/` directory)

#### `src/data_loader.py`
- **Purpose**: Load CSV files from BTS
- **Key Features**:
  - Loads all Load Factor files (annual)
  - Loads all OTP files (monthly)
  - Combines multiple files automatically
  - Provides progress feedback
- **Main Function**: `quick_load()` - one-line data loading

#### `src/data_cleaner.py`
- **Purpose**: Clean and prepare data for analysis
- **Key Features**:
  - Filters for Southwest Airlines (carrier code: WN)
  - Handles missing values appropriately
  - Creates route identifiers (bidirectional)
  - Standardizes date formats
  - Identifies top N routes by any metric
- **Main Function**: `clean_all_data()` - cleans both datasets

#### `src/metrics.py`
- **Purpose**: Calculate performance metrics
- **Key Features**:
  - Calculates load factors
  - Calculates OTP percentages
  - Merges datasets by route and month
  - Performs correlation analysis
  - Generates route-level summary statistics
- **Main Function**: `merge_lf_otp_by_route_month()` - creates analysis-ready dataset

#### `src/__init__.py`
- **Purpose**: Package initialization
- Makes all modules easily importable

### 2. **Jupyter Notebooks** (`notebooks/` directory)

#### `01_data_exploration.ipynb`
- **Purpose**: Initial data exploration and validation
- **What It Does**:
  - Loads raw data
  - Examines data structure and quality
  - Checks for missing values
  - Filters for Southwest Airlines
  - Visualizes overall trends (2020-2025)
  - Saves cleaned data
- **Outputs**: 
  - `lf_clean_southwest.csv`
  - `otp_clean_southwest.csv`

#### `02_route_analysis.ipynb`
- **Purpose**: Identify top 5 routes
- **What It Does**:
  - Analyzes all Southwest routes
  - Ranks by passenger volume
  - Identifies top 5 routes
  - Examines route characteristics
  - Visualizes passenger trends
  - Checks data availability
- **Outputs**:
  - `lf_top5_routes.csv`
  - `otp_top5_routes.csv`
  - `top5_routes.csv`

#### `03_otp_loadfactor_analysis.ipynb`
- **Purpose**: Main correlation analysis
- **What It Does**:
  - Merges LF and OTP data
  - Calculates correlations (Pearson, Spearman)
  - Creates visualizations:
    - Scatter plots (LF vs OTP)
    - Time series trends
    - Correlation heatmaps
    - Load factor bin analysis
  - Performs statistical tests
  - Generates route-specific analyses
- **Outputs**:
  - `merged_lf_otp_top5.csv`
  - `route_summary_statistics.csv`
  - Multiple visualizations

### 3. **Report Template** (`reports/` directory)

#### `final_report.md`
- **Purpose**: Comprehensive analysis report
- **Sections**:
  1. Executive Summary
  2. Methodology
  3. Top 5 Routes Identified
  4. Overall Relationship Analysis
  5. Route-by-Route Analysis
  6. Load Factor Threshold Analysis
  7. Temporal Patterns
  8. Business Implications
  9. Limitations and Future Research
  10. Conclusion
  11. Appendices
- **Format**: Ready-to-fill template with placeholders

### 4. **Support Files**

#### `README.md`
- Comprehensive project documentation
- Installation instructions
- Usage guide
- Troubleshooting tips

#### `QUICKSTART.md`
- Fast-track guide to get running immediately
- Step-by-step instructions
- Common issues and solutions

#### `requirements.txt`
- All Python dependencies
- Specific version requirements
- Easy installation with pip

#### `.gitignore` and `.gitkeep`
- `.gitignore` excludes all files in `data/processed/` except `.gitkeep`, so the directory is always present in the repo but large processed data files are not tracked.
- `.gitkeep` is a placeholder file to ensure the empty directory is tracked by git.

## Data Flow

```
Raw Data (BTS)
    ↓
[DataLoader] → Load all CSV files
    ↓
[DataCleaner] → Filter for Southwest, clean data
    ↓
[Route Analysis] → Identify top 5 routes
    ↓
[DataCleaner] → Filter for top 5 routes
    ↓
[MetricsCalculator] → Merge LF and OTP data
    ↓
[MetricsCalculator] → Calculate correlations & statistics
    ↓
[Visualizations] → Generate plots and charts
    ↓
[Final Report] → Interpret and document findings
```

## Key Analysis Questions Answered

1. **Which are Southwest's top 5 busiest domestic routes?**
   - Based on passenger volume (2020-2025)
   - Actual routes determined by your data

2. **Is there a correlation between load factor and OTP?**
   - Overall correlation across all routes
   - Statistical significance testing
   - Both departure and arrival OTP considered

3. **Do different routes show different patterns?**
   - Route-specific correlation analysis
   - Individual route visualizations
   - Summary statistics by route

4. **Are there load factor thresholds that affect OTP?**
   - Bin analysis (<70%, 70-75%, 75-80%, 80-85%, 85%+)
   - Average OTP by load factor range
   - Identifies operational stress points

5. **How did COVID-19 affect the relationship?**
   - Time series analysis (2020-2025)
   - Pre-pandemic vs pandemic vs recovery
   - Temporal patterns

## What You Need to Do

### Prerequisites
1. Install Python 3.8+ and dependencies:
   ```bash
   pip install -r requirements.txt
   ```


### Running the Analysis

You can run the analysis in two ways:

**Option 1: Automated Script (Fastest)**
```bash
python run_analysis.py
```
This will generate all processed data and statistics in `data/processed/`.

**Option 2: Jupyter Notebooks (Most Interactive)**
```bash
jupyter notebook
# Then run notebooks 01, 02, 03 in order
```
Each notebook will save outputs to `data/processed/` as you go.

**Note:** The `data/processed/` directory is always present in the repo (due to `.gitkeep`), but the processed data files themselves are not tracked by git due to `.gitignore` rules.

### Interpreting Results

After running, you'll have:

1. **Cleaned datasets** in `data/processed/`
2. **Statistical results** in CSV files
3. **Visualizations** in notebooks
4. **Report template** ready to fill in `reports/final_report.md`

## Expected Insights

Based on the analysis structure, you'll discover:

- **Correlation strength**: Weak/moderate/strong relationship
- **Correlation direction**: Positive/negative/no correlation
- **Route variations**: Some routes may show strong patterns, others weak
- **Threshold effects**: Whether OTP drops above certain load factors
- **Temporal trends**: How the relationship evolved 2020-2025

## Possible Findings (Hypothetical)

### Scenario A: Negative Correlation
- **Finding**: Higher load factors → Lower OTP
- **Interpretation**: Fuller planes harder to turn around, delays cascade
- **Business Impact**: May need longer turnaround times at high load factors

### Scenario B: Positive Correlation
- **Finding**: Higher load factors → Higher OTP
- **Interpretation**: Better capacity utilization coincides with better operations
- **Business Impact**: Operational efficiency improves with scale

### Scenario C: No Correlation
- **Finding**: Load factor doesn't predict OTP
- **Interpretation**: OTP driven by other factors (weather, ATC, crew)
- **Business Impact**: Can maximize load factor without OTP concerns

### Scenario D: Threshold Effect
- **Finding**: OTP fine until 85%+ load factors
- **Interpretation**: System has capacity until near-full
- **Business Impact**: Target 80-85% load factor for optimal balance

## Technical Specifications

### Data Requirements
- **Format**: CSV
- **Encoding**: UTF-8
- **Date Range**: Jan 2020 - Jun 2025
- **Carrier**: Southwest (WN)

### Metrics Calculated
- **Load Factor**: (Passengers / Seats) × 100
- **Departure OTP**: % flights within 15 min of scheduled departure
- **Arrival OTP**: % flights within 15 min of scheduled arrival
- **Cancellation Rate**: % flights cancelled

### Statistical Methods
- **Pearson correlation**: Linear relationship
- **Spearman correlation**: Monotonic relationship
- **p-values**: Significance testing (α = 0.05)
- **Sample sizes**: Route-month observations

### Visualizations Generated
- Time series: Load factor over time
- Time series: OTP over time
- Scatter plots: LF vs OTP (by route)
- Correlation heatmaps
- Bar charts: OTP by LF bin
- Route-specific detail plots

## Extensions and Future Work

This framework can be extended to:

1. **Other carriers**: Change `carrier_code='WN'` to any airline
2. **Different routes**: Modify `n=5` to analyze more/fewer routes
3. **Other metrics**: Add fuel efficiency, revenue per seat, etc.
4. **Predictive models**: Build regression models to forecast OTP
5. **Time-of-day analysis**: Examine morning vs evening flights
6. **Seasonal patterns**: Deep-dive into holiday periods
7. **Weather integration**: Incorporate weather data
8. **Competitive analysis**: Compare Southwest to competitors

## Success Criteria

You've successfully completed the project when you can answer:

1. ✅ What are Southwest's top 5 domestic routes by passengers?
2. ✅ What is the correlation between load factor and OTP?
3. ✅ Is this correlation statistically significant?
4. ✅ Do all routes show the same pattern?
5. ✅ Are there load factor thresholds that impact OTP?
6. ✅ How did this relationship change during COVID-19?
7. ✅ What are the business implications?

## Getting Help

If you encounter issues:

1. Check `README.md` for detailed documentation
2. Review `QUICKSTART.md` for setup issues
3. Examine error messages in notebooks
4. Verify data file locations and formats
5. Ensure all dependencies installed correctly

## Project Maintainability

This project is designed to be:

- **Modular**: Each component works independently
- **Reusable**: Modules can be used in other projects
- **Extensible**: Easy to add new analyses
- **Documented**: Code comments and docstrings throughout
- **Reproducible**: Same inputs → same outputs

## Final Thoughts

You now have a complete, professional data analysis project that:

✅ Loads and cleans real-world airline data  
✅ Performs rigorous statistical analysis  
✅ Generates publication-quality visualizations  
✅ Produces actionable business insights  
✅ Documents methodology and findings  
✅ Follows best practices for data science projects  

**Ready to uncover the relationship between Southwest's load factors and on-time performance? Let's go!** 🛫📊

---

**Questions? Need modifications?** The code is well-documented and easy to customize for your specific needs.