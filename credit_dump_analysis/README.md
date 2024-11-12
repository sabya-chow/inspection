
# Data Cleaning and Analysis for Financial Inspection

## Overview

This project focuses on cleaning, analyzing, and validating financial data from various sources, specifically data related to advances and loans for inspection purposes. The main objective is to ensure accurate representation and evaluation of financial assets using advanced data analysis techniques, data merging, and data cleaning operations.

## Data Cleaning and Preparation
### Day 1
- **Data Loading**: Imported raw data from an Excel sheet using Pandas and converted data types where needed.
- **Data Cleaning Steps**:
  - Renamed columns for easier handling.
  - Converted columns to appropriate numeric and date formats.
  - Handled missing values for specific columns such as balance and installment data.

### Day 2
- **Data Frame Shortening**: Selected essential columns for further analysis and ensured that the dataset is comprehensive yet manageable.
- **Data Adjustments**: Adjusted 'Advance' column based on 'NPA_YN' status.

### Day 4
- **Balance vs Disbursement Check**: Identified cases where total balances exceeded disbursements and grouped data for further analysis.
- **NPA vs Standard Loans Analysis**: Separated data based on NPA status and conducted further analysis on principal amounts.

## Key Functionalities
1. **Data Merge and Comparison**:
   - Merged data from different sources, ensuring consistency between various data dumps.
   - Identified mismatches between balances and dates to pinpoint discrepancies.
2. **Provision Calculation for Loans**:
   - Computed provision amounts based on the number of days past due (DPD).
   - Differentiated provision requirements based on asset classes.
3. **Segregation of Loans Based on Criteria**:
   - Filtered accounts based on NPA status and provision adequacy.
   - Conducted analysis on loans secured against fixed deposits and other securities.
4. **Trend Analysis for Financial Parameters**:
   - Calculated month-on-month and year-on-year trends for various financial metrics, including loans, deposits, and NPAs.
5. **Custom Analysis and Filtering**:
   - Identified branches with top advances and NPAs.
   - Filtered forex-related products for specific analysis.
   - Conducted an analysis on restructured loans for upgrades.

## Usage Instructions
1. **Dependencies**:
   - `pandas`
   - `numpy`
   - `matplotlib`

2. **Data Input**:
   - The project expects input files in specific formats (e.g., Excel). Ensure all paths and files are correctly specified.
3. **Running the Code**:
   - The main code can be executed step-by-step to perform data loading, cleaning, merging, analysis, and visualization tasks.
   - The results of various analyses are saved to specified output files.

## Example Commands
```python
# Example code snippet to load and clean data
data = pd.read_excel("path_to_input_file.xlsx", dtype={'Account Number': str})
data.columns = ["Shortened_Column_Names"]
data_cleaned = data.copy()
# Perform operations...
```

## Notes and Caveats
- Ensure data privacy and confidentiality when handling sensitive financial data.
- This project is intended for educational and research purposes only and should not be used as financial advice.
- Be aware of dependencies and the need for consistent input data formats.
