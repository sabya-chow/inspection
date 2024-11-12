

## Objective of this module to calculate the ideal interst overdue for all NPA accounts and tallying the same with the overdue OIRA balance
"""

import pandas as pd
import numpy as np
# Try loading the file with 'ISO-8859-1' encoding
dump = pd.read_excel(r"C:\Users\Admin\OneDrive - rbionline\inspection 2024\Bharat\indent\5. Loans & Advances\2 Advances Master Data.xlsx", dtype={'Account Number': str})

data=dump.copy()

data.head()

data.columns

"""### Data cleaning"""

import pandas as pd
import numpy as np
import re

# Define new, shorter column names to match the original number of columns (52 in this case)
short_names = ['Branch_Code', 'Branch_Name', 'Scheme_Code', 'GL_Code', 'Scheme_Desc',
               'Acc_Number', 'Acc_Name', 'UCIC', 'Sanctioned_Limit', 'Sanction_Authority',
               'Acc_Open_Date', 'Sanction_Date', 'Limit_Change_YN', 'Limit_Change_Detail',
               'Previous_Sanction_Limit', 'Adhoc_TOD_YN', 'First_Installment_Date',
               'Maturity_Date', 'Closure_Date', 'First_Disbursement_Date', 'Sum_Disbursements',
               'Total_Balance_os_Dr', 'Total_Balance_os_Cr', 'Principal_os', 'Interest_os',
               'OIR', 'Interest_Rate', 'Card_Interest_Rate', 'Overdue_Amount',
               'Installments_Sanctioned', 'Moratorium_Installments', 'Installment_Amount',
               'Installments_Overdue', 'Days_Past_Due', 'Loan_Against_Deposit_YN',
               'Staff_Loan_YN', 'NPA_YN', 'NPA_Date', 'NPA_Category', 'Provision_Required',
               'Provision_Held', 'Security_Type', 'Security_Value', 'Priority_Sector_YN',
               'Priority_Sector_Category', 'Weaker_Section_YN', 'Weaker_Section_Category',
               'Real_Estate_CRE_YN', 'Avg_Debit_Balance', 'Avg_Monthly_Debit_Turnover',
               'Avg_Monthly_Credit_Turnover', 'Avg_Utilization']

# Apply new column names to the dataframe
data.columns = short_names

# Define function to convert column to numeric, handling errors
def convert_to_numeric(col):
    try:
        # Replace all non-numeric characters with nothing and convert to numeric
        return pd.to_numeric(col.replace(re.compile(r'\D'), ''))
    except ValueError:
        return col

# Convert problematic numeric columns
numeric_cols = ['Sanctioned_Limit', 'Previous_Sanction_Limit', 'Sum_Disbursements',
                'Interest_os', 'OIR',
                'Overdue_Amount', 'Installments_Sanctioned', 'Moratorium_Installments',
                'Installment_Amount',
                'Provision_Required', 'Provision_Held', 'Security_Value',
                'Total_Balance_os_Dr', 'Total_Balance_os_Cr','Principal_os', 'Interest_Rate', 'Card_Interest_Rate']

for col in numeric_cols:
    data[col] = round(convert_to_numeric(data[col]),2)


date_columns = ['Acc_Open_Date', 'Sanction_Date', 'First_Installment_Date', 'Maturity_Date', 'Closure_Date', 'First_Disbursement_Date', 'NPA_Date']
for col in date_columns:
    data[col] = pd.to_datetime(data[col], dayfirst=True)

data[data['Acc_Number']=="000113100004855"] # to check that the account number has been correctly brought as string value

#data.dtypes

#data.to_csv(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\day1_cleaned.csv")

import pandas as pd

# Columns to consider
columns_to_consider = ['Acc_Number', 'Acc_Name', 'Principal_os', 'Interest_os',
                       'OIR', 'Interest_Rate', 'Installment_Amount',
                       'Days_Past_Due', 'NPA_YN']

# Assuming 'data' is your original DataFrame
# Step 1: Shorten the DataFrame
shortened_data = data[columns_to_consider].copy()

# Step 2: Check if the account is NPA or not and calculate pending interest
def calculate_pending_interest(row):
    interest_rate_per_day = row['Interest_Rate'] / 100 / 365  # Daily interest rate
    pending_interest = row['Principal_os'] * interest_rate_per_day * row['Days_Past_Due']

    if row['NPA_YN'] == 'Y':
        difference = pending_interest - row['OIR']
    else:
        difference = pending_interest - row['Interest_os']

    return pending_interest, difference

# Apply the function to calculate the pending interest and difference
shortened_data[['IR/OIR_recalc', 'Difference']] = shortened_data.apply(
    lambda row: pd.Series(calculate_pending_interest(row)), axis=1
)

# Display the resulting DataFrame
shortened_data.to_csv(r"C:\Users\Admin\Downloads\NPA_interest_tally.csv")

