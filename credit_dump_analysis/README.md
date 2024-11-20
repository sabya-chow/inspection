
# Data Cleaning and Analysis for Financial Inspection

## Overview

This codeblock focuses on cleaning, analyzing, and validating financial data from various sources, specifically data related to advances and loans for inspection purposes. 

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

### Day 3-4
- **Balance vs Disbursement Check**: Identified cases where total balances exceeded disbursements and grouped data for further analysis.
- **NPA vs Standard Loans Analysis**: Separated data based on NPA status and conducted further analysis on principal amounts.

