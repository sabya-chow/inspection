
# Inspection Credit Tally: Interest Overdue Calculation

This module calculates the ideal interest overdue for Non-Performing Assets (NPA) accounts and compares it with the Overdue Interest Receivable Account (OIRA) balance for validation.

## Overview

- **Data Loading**: Reads data from an Excel file containing loan and advance details.
- **Data Cleaning**: Renames columns, converts data types, and cleans numeric and date fields.
- **Interest Calculation**: Computes pending interest based on NPA status, comparing calculated interest with OIRA for NPA and Interest Outstanding for non-NPA accounts.

## Features

- Flexible data handling and cleaning
- Automated interest calculations and comparisons
- Efficient processing and output to CSV format

## Usage

1. Load the data file in the specified path.
2. Process the data for interest calculations and tallying.
3. Save the results in a CSV file for further review.
