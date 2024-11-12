
# Day 1

#### Data loading
"""

import pandas as pd
import numpy as np
# Try loading the file with 'ISO-8859-1' encoding
dump = pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\credit\2. Advances Master - Copy.xlsx", dtype={'Account Number': str})

data=dump.copy()

data.head()

"""### Data cleaning"""

import pandas as pd
import numpy as np
import re

# Define new, shorter column names
short_names = ['Branch_Code', 'Branch_Name', 'Scheme_Code', 'Scheme_Desc', 'Acc_Number', 'UCIC',
               'Sanctioned_Limit', 'Sanction_Authority', 'Acc_Open_Date', 'Sanction_Date',
               'Limit_Change_YN', 'Limit_Change_Detail', 'Previous_Sanction_Limit',
               'Adhoc_TOD_YN', 'First_Installment_Date', 'Maturity_Date', 'Closure_Date',
               'First_Disbursement_Date', 'Sum_Disbursements', 'Total_Balance_os', 'Cr_Balance',
               'Principal_os', 'Interest_os', 'Interest_Receivable', 'Interest_Rate',
               'Card_Interest_Rate', 'Overdue_Amount', 'Installments_Sanctioned',
               'Moratorium_Installments', 'Installment_Amount', 'Installments_Overdue',
               'Days_Past_Due', 'Loan_Against_Deposit_YN', 'Staff_Loan_YN', 'NPA_YN',
               'NPA_Date', 'NPA_Category', 'Provision_Required', 'Provision_Held',
               'Security_Type', 'Security_Value', 'Priority_Sector_YN', 'Priority_Sector_Category',
               'Weaker_Section_YN', 'Weaker_Section_Category', 'Real_Estate_CRE_YN']

# Apply new column names to dataframe
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
                'Interest_os', 'Interest_Receivable', 'Interest_Rate', 'Card_Interest_Rate',
                'Overdue_Amount', 'Installments_Sanctioned', 'Moratorium_Installments',
                'Installment_Amount',
                'Provision_Required', 'Provision_Held', 'Security_Value',
                'Total_Balance_os', 'Cr_Balance', 'Principal_os', 'Interest_os',
                'Interest_Receivable', 'Interest_Rate', 'Card_Interest_Rate']
for col in numeric_cols:
    data[col] = round(convert_to_numeric(data[col]),2)

data[['Provision_Required', 'Provision_Held']]=round(data[['Provision_Required', 'Provision_Held']]*10**5,2)
# Convert date columns to appropriate data types
date_columns = ['Acc_Open_Date', 'Sanction_Date', 'First_Installment_Date', 'Maturity_Date', 'Closure_Date', 'First_Disbursement_Date', 'NPA_Date']
for col in date_columns:
    data[col] = pd.to_datetime(data[col], dayfirst=True)

data[data['Acc_Number']=="000113100004855"] # to check that the account number has been correctly brought as string value

#data.dtypes

#data.to_csv(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\day1_cleaned.csv")

data.fillna(value={
    'Cr_Balance': 0,
    'Principal_os': 0,
    'Interest_os': 0,
    'Interest_Receivable': 0,
    'Overdue_Amount': 0,
    'Installment_Amount': 0,
    'Installments_Overdue': 0,
    'Days_Past_Due': 0
}, inplace=True)

data.Principal_os.sum()

"""# Day 2

## shortening the dataframe
"""

# List of columns to keep
columns_to_keep = ['Branch_Name', 'Scheme_Desc', 'Acc_Number', 'UCIC', 'Sanctioned_Limit',
                   'Sanction_Authority', 'Acc_Open_Date', 'Sanction_Date', 'Sum_Disbursements',
                   'Total_Balance_os', 'Cr_Balance', 'Principal_os', 'Interest_os',
                   'Interest_Receivable', 'Overdue_Amount', 'Installment_Amount',
                   'Installments_Overdue', 'Days_Past_Due', 'Loan_Against_Deposit_YN',
                   'Staff_Loan_YN', 'NPA_YN', 'NPA_Date', 'NPA_Category', 'Provision_Required',
                   'Provision_Held', 'Security_Type', 'Security_Value']

# Keep only the columns in columns_to_keep
data = data[columns_to_keep]

# Display the first 5 rows of the new dataframe
data.head()

#### Unique modification :Ensuring Interest_os(IR)=Interest receivable(OIR). Advance should be principle+Interest_os

# Adjust 'Advance' based on 'NPA_YN'
data.loc[data['NPA_YN'] == 'N', 'Advance'] = data['Principal_os'] + data['Interest_os']
data.loc[data['NPA_YN'] == 'Y', 'Advance'] = data['Principal_os']

# Display the first 5 rows of the updated dataframe
data.head()

"""### checking the shape of the dataframe"""

data.shape

"""### checking total numbers of accounts and total advance

#### source : Advance master dump
"""

data['Advance'].shape

data['Total_Balance_os'].sum()

data['Advance'].sum()

data['Advance'].count()

data_mismatch = data[data['Total_Balance_os'] != data['Advance']]
data_mismatch[['Branch_Name', 'Scheme_Desc', 'Acc_Number', 'UCIC', 'Acc_Open_Date', 'Sanction_Date',
       'Total_Balance_os', 'Cr_Balance', 'Principal_os',
       'Interest_os',  'NPA_YN', 'Advance']].to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\mismatch.xlsx")

"""#### Source : Annual Report/Stat Audit Report"""

audited_accounts=29638

audited_advance=70147809000

"""#### Difference betrween advance sump and audited report:

#### By value
"""

(audited_advance-data['Advance'].sum()) # converting the difference in ₹cr

"""#### By count"""

audited_accounts-data['Advance'].count()

"""****This difference was towards 54 TOD accounts which was not part of the CBS but was manually taken by the auditor.****"""

## Generating modified advance_master_dump
data.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\advance_master_cleaned.xlsx")





"""## Data dump from CBS generated during inspection"""

# Load the Excel file with pandas, read 'ACCOUNT_OPEN_DATE' as string
march_dump = pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\CBS_dump\loan_dump_310323 - Copy.xlsx",
                           dtype={'ACCOUNT_NO': str, 'ACCOUNT_OPEN_DATE': str})

# Check if the date strings are in the correct format
print(march_dump['ACCOUNT_OPEN_DATE'].head())

# If the above output is correct, convert the 'ACCOUNT_OPEN_DATE' column to datetime format
march_dump['ACCOUNT_OPEN_DATE'] = pd.to_datetime(march_dump['ACCOUNT_OPEN_DATE'], format='%d-%b-%Y')

print(march_dump['ACCOUNT_OPEN_DATE'].head())

#march_dump["ACCOUNT_NO"]="'" +march_dump["ACCOUNT_NO"]

march_dump

import pandas as pd


# Convert columns to correct data types
data['Total_Balance_os'] = data['Total_Balance_os'].abs()
march_dump['OUTSTANDING_BALANCE'] = march_dump['OUTSTANDING_BALANCE'].abs()

# Merge dataframes
merged_df = pd.merge(data[['Acc_Number', 'Total_Balance_os', 'Acc_Open_Date']],
                     march_dump[['ACCOUNT_NO', 'OUTSTANDING_BALANCE', 'ACCOUNT_OPEN_DATE']],
                     left_on='Acc_Number',
                     right_on='ACCOUNT_NO',
                     how='inner')

# Rename columns
merged_df.columns = ['Acc_Number', 'data_dump_os', 'data_dump_acc_open_date', 'database(GAM)_Acc_Number', 'database_balance', 'database_acc_open_date']

# Find mismatches
mismatch_df = merged_df.loc[(merged_df['data_dump_os'] != merged_df['database_balance']) |
                            (merged_df['data_dump_acc_open_date'] != merged_df['database_acc_open_date'])]

# Calculate differences
mismatch_df['balance_diff(dump-database)'] = mismatch_df['data_dump_os'] - mismatch_df['database_balance']
mismatch_df['date_diff(dump-database)'] = (mismatch_df['data_dump_acc_open_date'] - mismatch_df['database_acc_open_date']).dt.days

# Rename columns
mismatch_df = mismatch_df.rename(columns={
    'Acc_Number': 'Acc_Number',
    'Total_Balance_os_data': 'data_dump_os',
    'Acc_Open_Date_data': 'data_dump_acc_open_date',
    'ACCOUNT_NO': 'database(GAM)_Acc_Number',
    'OUTSTANDING_BALANCE_march_dump': 'database_balance',
    'ACCOUNT_OPEN_DATE_march_dump': 'database_acc_open_date',
    'balance_diff': 'balance_diff(dump-database)',
    'date_diff': 'date_diff(dump-database)'
})

mismatch_df

# Add a leading single quote to account number columns
mismatch_df['Acc_Number'] = "'" + mismatch_df['Acc_Number']
mismatch_df['database(GAM)_Acc_Number'] = "'" + mismatch_df['database(GAM)_Acc_Number']

# Save mismatched balances to CSV
mismatch_df[mismatch_df['balance_diff(dump-database)'] != 0].to_csv(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\ouput_files\balance_mismatch.csv", index=False)

# Save mismatched opening dates to CSV
mismatch_df[mismatch_df['date_diff(dump-database)'] != 0].to_csv(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\ouput_files\opening_date_mismatch.csv", index=False)

#mismatch_df[mismatch_df['date_diff(dump-database)'] != 0]





sanctioned_limit_missing = data[data['Sanctioned_Limit'].isna()]
#sanctioned_limit_missing['Acc_Number'] = "'" + sanctioned_limit_missing['Acc_Number']
sanctioned_limit_missing.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\missing_sanct_limit.xlsx", index=False)

"""### Extract rows with missing Acc_Open_Date values and save to a CSV file:"""

missing_acc_open_date = data[data['Acc_Open_Date'].isna()]
#missing_acc_open_date['Acc_Number'] = "'" + missing_acc_open_date['Acc_Number']
missing_acc_open_date.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\missing_acc_open_date.xlsx", index=False)

"""### Extract rows with missing Sanction_Date values and save to a CSV file:"""

missing_sanction_date = data[data['Sanction_Date'].isna()]
#missing_sanction_date['Acc_Number'] = "'" + missing_sanction_date['Acc_Number']
missing_sanction_date.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\missing_sanc_date.xlsx", index=False)

"""### Find out if there are any cases where Sanction_Date is greater than Acc_Open_Date:"""

# Then we can find the cases where Sanction_Date is greater than Acc_Open_Date
cases = data[data['Sanction_Date'] > data['Acc_Open_Date']]
cases.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\open_lesserthan_sanc_date.xlsx", index=False)

"""### Find out cases where Sum_Disbursement value is missing:"""

missing_sum_disbursement = data[data['Sum_Disbursements'].isna()]
#missing_sum_disbursement['Acc_Number'] = "'" + missing_sum_disbursement['Acc_Number']
missing_sum_disbursement.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\missing_sum_disbursement.xlsx", index=False)

"""### conversion in cr : `data_cr`"""

import pandas as pd
data_cr=data.copy()
# List of columns to be divided
columns_to_divide = ['Sanctioned_Limit', 'Sum_Disbursements', 'Total_Balance_os', 'Cr_Balance',
                     'Principal_os', 'Interest_os', 'Interest_Receivable', 'Overdue_Amount', 'Installment_Amount',
                     'Provision_Required', 'Provision_Held','Security_Value','Advance']

# Dividing the selected columns by 10^7 and rounding off to 2 decimal places
data_cr[columns_to_divide] = data_cr[columns_to_divide] / 10**7
data_cr[columns_to_divide] = data_cr[columns_to_divide].round(2)

data_cr.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\data_cleaned.xlsx", index=False)

data_cr.columns



"""# Day 4

### find out the cases where : `Total_Balance_os`>`Sum_Disbursements`
"""

# Add a new column 'excess_bal'
data_cr['excess_bal'] = data_cr['Advance'] - data_cr['Sum_Disbursements']

# Filter out the cases where NPA_YN is 'Y'
npa_data = data_cr[data_cr['NPA_YN'] == 'Y']


# Filter out the cases where Total_Balance_os is greater than Sum_Disbursements
filtered_npa_data = npa_data[npa_data['Advance'] > npa_data['Sum_Disbursements']]

# Group by 'Scheme_Desc' and calculate the count and sum
filtered_npa_analysis = filtered_npa_data.groupby('Scheme_Desc').agg({'Acc_Number': 'count', 'excess_bal': 'sum'}).rename(columns={'Acc_Number': 'volume', 'excess_bal': 'value'})

# Calculate the percentage
filtered_npa_analysis['volume_pct'] = filtered_npa_analysis['volume'] / filtered_npa_analysis['volume'].sum() * 100
filtered_npa_analysis['value_pct'] = filtered_npa_analysis['value'] / filtered_npa_analysis['value'].sum() * 100

# Sort by 'value_pct' and select top 10
filtered_npa_analysis = filtered_npa_analysis.sort_values(by='value_pct', ascending=False).head(10)

filtered_npa_analysis=round(filtered_npa_analysis,2)

filtered_npa_analysis

filtered_npa_data.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\bal_grtr_thn_disbrsemnt.xlsx", index=False)

"""### Segregating NPA from standard"""

import pandas as pd
from datetime import datetime

# Assuming you already have the DataFrame 'data_cr'
# If not, you can create it using: data_cr = pd.DataFrame(your_data)

# Recreate the NPA and standard dataframes
NPA = data_cr[data_cr['NPA_YN'] == 'Y']
standard = data_cr[data_cr['NPA_YN'] == 'N']

# Check if the 'NPA_Date' column contains valid date values before calculating dpd
if pd.api.types.is_datetime64_any_dtype(NPA['NPA_Date']):
    NPA['dpd_calculated'] = (datetime(2023, 3, 31) - NPA['NPA_Date']).dt.days

NPA

"""### Checking the principal amount of NPA and standard loans"""

NPA['Principal_os'].sum()

standard['Principal_os'].sum()

## Auduted NPA

audited_NPA=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\credit\NPA_audited.xlsx")

import pandas as pd

# Assuming you have the two dataframes: audited_NPA and NPA

# Merge the dataframes based on 'Acc_Number'
merged_df = pd.merge(audited_NPA, NPA, left_on='Account No.', right_on='Acc_Number', how='outer', indicator=True)

# Filter the rows that are only present in audited_NPA (not in NPA)
audited_NPA_only = merged_df[merged_df['_merge'] == 'left_only']

# Filter the rows that are only present in NPA (not in audited_NPA)
NPA_only = merged_df[merged_df['_merge'] == 'right_only']

# Display the account numbers that are present in audited_NPA but not in NPA
print("Account Numbers present in audited_NPA but not in NPA:")
print(audited_NPA_only['Account No.'])

# Display the account numbers that are present in NPA but not in audited_NPA
print("Account Numbers present in NPA but not in audited_NPA:")
print(NPA_only['Acc_Number'])

import pandas as pd

# Assuming you have the two dataframes: audited_NPA and NPA

# Count the occurrences of each account number in audited_NPA
audited_NPA_counts = len(audited_NPA['Account No.'])

# Count the occurrences of each account number in NPA
NPA_counts = len(NPA['Acc_Number'])

# Display the counts for each account number in audited_NPA
print("Counts in audited_NPA:")
print(audited_NPA_counts)

# Display the counts for each account number in NPA
print("Counts in NPA:")
print(NPA_counts)

"""## Divergence"""

NPA.columns

"""## Provision"""

NPA.to_excel((r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\credit\NPA_dump.xlsx"))

df=NPA.copy()
# Define the reference date as provided
reference_date = datetime.strptime('31-03-2023', '%d-%m-%Y')

# Calculate Days Past Due (DPD)
df['dpd_calculated'] = (reference_date - df['NPA_Date']).dt.days

# Calculate the provision based on DPD for the corrected portion
df['provision_calculated'] = 0

# If DPD < 365 days, prov_calc = principal_os * 0.1
df.loc[df['dpd_calculated'] < 365, 'provision_calculated'] = df['Principal_os'] * 0.1  # Using 'Principal_os' column as specified in the dataframe structure

# If DPD > 365 but <= 730 days
mask_365_to_730 = (df['dpd_calculated'] > 365) & (df['dpd_calculated'] <= 730)
mask_security_value_gt_principal = df['Security_Value'] > df['Principal_os']
df.loc[mask_365_to_730 & mask_security_value_gt_principal, 'provision_calculated'] = df['Principal_os'] * 0.2
df.loc[mask_365_to_730 & ~mask_security_value_gt_principal, 'provision_calculated'] = df['Security_Value'] * 0.2 + (df['Principal_os'] - df['Security_Value'])

# If DPD > 730 but <= 1460 days
mask_730_to_1460 = (df['dpd_calculated'] > 730) & (df['dpd_calculated'] <= 1460)
mask_security_value_gt_principal = df['Security_Value'] > df['Principal_os']
df.loc[mask_730_to_1460 & mask_security_value_gt_principal, 'provision_calculated'] = df['Principal_os'] * 0.3
df.loc[mask_730_to_1460 & ~mask_security_value_gt_principal, 'provision_calculated'] = df['Security_Value'] * 0.3 + (df['Principal_os'] - df['Security_Value'])

# If DPD > 1460 days, prov_calc = principal_os
df.loc[df['dpd_calculated'] > 1460, 'provision_calculated'] = df['Principal_os']

# Calculate the provision difference and difference category
df['provision_difference'] = abs(df['Provision_Required'] - df['provision_calculated'])
df['difference_category'] = 'Equal'
df.loc[df['provision_difference'] > 0, 'difference_category'] = 'Difference exists'

# Round off to 2 decimal places
numerical_columns = df.select_dtypes(include=[float, int]).columns
df[numerical_columns] = df[numerical_columns].round(2)

# Calculate the sums
sum_provision_required = df['Provision_Required'].sum()
sum_provision_calculated = df['provision_calculated'].sum()
sum_provision_held = df['Provision_Held'].sum()

sum_provision_required, sum_provision_calculated, sum_provision_held # Displaying the top rows of the dataframe for a preview

"""## Difference in provision"""

# Extract rows where Provision_Required is not equal to provision_calculated
df_mismatch = df[df['Provision_Required'] != df['provision_calculated']]

df_mismatch.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\prov_mismatch.xlsx")

"""### 1.checking adequacy of provision"""

def segregate_data(df):
    # Segregate the data into three categories
    NPA_eqprov = df[df['provision_difference'] == 0]
    NPA_highprov = df[df['Provision_Required'] < df['provision_calculated']]
    NPA_lowprov = df[df['Provision_Required'] > df['provision_calculated']]

    # Calculate the count of each dataframe
    count_eqprov = NPA_eqprov.shape[0]
    count_highprov = NPA_highprov.shape[0]
    count_lowprov = NPA_lowprov.shape[0]

    # Calculate the sum of prov_req, prov_held, and prov_calc for each dataframe
    sum_eqprov = NPA_eqprov[['Provision_Required', 'Provision_Held', 'provision_calculated']].sum()
    sum_highprov = NPA_highprov[['Provision_Required', 'Provision_Held', 'provision_calculated']].sum()
    sum_lowprov = NPA_lowprov[['Provision_Required', 'Provision_Held', 'provision_calculated']].sum()

    # Return the results
    return (NPA_eqprov, count_eqprov, sum_eqprov), (NPA_highprov, count_highprov, sum_highprov), (NPA_lowprov, count_lowprov, sum_lowprov)

# Apply the function on the dataframe
(NPA_eqprov, count_eqprov, sum_eqprov), (NPA_highprov, count_highprov, sum_highprov), (NPA_lowprov, count_lowprov, sum_lowprov) = segregate_data(df)

# Output the results
(count_eqprov, sum_eqprov), (count_highprov, sum_highprov), (count_lowprov, sum_lowprov)

#The above table shows the details of provision shortfall, if any
NPA_highprov.to_csv(r"C:\Users\Admin\Downloads\provision_shortfall.csv")

NPA.Principal_os.sum()

"""## standard account check"""

standard.columns

df=standard.copy()
# Filter rows where Days_Past_Due is greater than 90
df_dpd_gt_90 = df[df['Days_Past_Due'] > 90]

# Check the count of such rows
count_dpd_gt_90 = len(df_dpd_gt_90)

count_dpd_gt_90

df_dpd_gt_90.to_excel(r"C:\Users\Admin\Downloads\standard_90.xlsx")





hlp=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\Loans-HLPAYH\Data\RBI_HLPAYH.xlsx",dtype={'FORACID': str})

hlp.head()

hlp.columns

hlp.info()

hlp['DMD_EFF_DATE'] = pd.to_datetime(hlp['DMD_EFF_DATE'])
hlp['LAST_ADJ_DATE'] = pd.to_datetime(hlp['LAST_ADJ_DATE'])



#hlp.info()

std=standard.Acc_Number.to_list()

filtered_hlp = hlp[hlp['FORACID'].isin(std)]

filtered_hlp

filtered_hlp['DATE_DIFF'] = filtered_hlp['LAST_ADJ_DATE'] - filtered_hlp['DMD_EFF_DATE']

import pandas as pd

# Calculate the DATE_DIFF column first (if not calculated already)
filtered_hlp['DATE_DIFF'] = filtered_hlp['LAST_ADJ_DATE'] - filtered_hlp['DMD_EFF_DATE']

# Filter accounts based on DATE_DIFF and date range
start_date = pd.to_datetime('2022-04-01')
end_date = pd.to_datetime('2023-03-31')

accounts_with_diff_gt_90 = filtered_hlp[
    (filtered_hlp['DATE_DIFF'] > pd.Timedelta(days=90)) &
    (filtered_hlp['DMD_EFF_DATE'] >= start_date) &
    (filtered_hlp['DMD_EFF_DATE'] <= end_date)
]

# Extract data for accounts with DATE_DIFF > 90 days at least once and from April 01, 2022
selected_accounts_data = filtered_hlp[
    (filtered_hlp['FORACID'].isin(accounts_with_diff_gt_90['FORACID'])) &
    (filtered_hlp['DMD_EFF_DATE'] >= start_date)
]

selected_accounts_data

selected_accounts_data.to_excel(r"C:\Users\Admin\Downloads\od_gt_90d.xlsx")

import pandas as pd

# Calculate the DATE_DIFF column first (if not calculated already)
filtered_hlp['DATE_DIFF'] = filtered_hlp['LAST_ADJ_DATE'] - filtered_hlp['DMD_EFF_DATE']

# Filter accounts based on DATE_DIFF and date range
start_date = pd.to_datetime('2022-04-01')
end_date = pd.to_datetime('2023-03-31')

accounts_with_diff_gt_90 = filtered_hlp[
    (filtered_hlp['DATE_DIFF'] > pd.Timedelta(days=90)) &
    (filtered_hlp['DMD_EFF_DATE'] >= start_date) &
    (filtered_hlp['DMD_EFF_DATE'] <= end_date)
]

# Filter accounts that never went back to 0 or np.nan after DATE_DIFF > 90
final_accounts = accounts_with_diff_gt_90.groupby('FORACID').filter(
    lambda group: not (group['DATE_DIFF'] <= pd.Timedelta(days=90)).any()
)

# Extract data for final accounts from April 01, 2022
likely_divergence = filtered_hlp[
    (filtered_hlp['FORACID'].isin(final_accounts['FORACID'])) &
    (filtered_hlp['DMD_EFF_DATE'] >= start_date)
]

likely_divergence.FORACID.unique()

# List of account numbers
account_numbers = likely_divergence.FORACID.unique()

# Filter the 'standard' DataFrame based on the account numbers
filtered_standard = standard[standard['Acc_Number'].isin(account_numbers)]

filtered_standard.head()

filtered_standard.Scheme_Desc.value_counts()









"""# day 10- checking of specific accounts"""

import pandas as pd

data=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\data_cleaned.xlsx",dtype={'Acc_Number': str})

data.columns

data[data['Advance'] > 1].Advance.sum()#/data.Advance.sum()

## Selecting CC/OD accounts portfolio

import pandas as pd

ccod = data[data['Scheme_Desc'].str.contains('OVERDRAFT|CASH CREDIT', case=False, na=False)]

ccod

ccod_5cr=ccod[ccod['Advance'] > 5]

ccod_5cr.shape

"""#### Thus there are 72 ccod accounts with more than 5 cr outstanding. Lets extract them in a new dataframe"""

ccod_5cr.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\ccod_5cr.xlsx")

"""# Analysis of average statement"""

avg=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\credit\average_statement.xlsx")

avg[[
    'Paid-up Share Capital', 'Loans', 'Bulk Deposits', 'Loan against Deposits',
    'CD Ratio (Simple in %)', 'Gross NPAs', 'Gross NPAs (in %)',
    'Interest Receivable/ Overdue Interest Reserve'
]]

import pandas as pd

# Load the data from the provided Excel file
data = round(avg.copy(),2)

# Define the columns for which we need YoY trend analysis
columns_to_analyze = [
    'Paid-up Share Capital', 'Loans', 'Bulk Deposits', 'Loan against Deposits',
    'CD Ratio (Simple in %)', 'Gross NPAs', 'Gross NPAs (in %)',
    'Interest Receivable/ Overdue Interest Reserve'
]

# Calculate YoY growth rate for each column
yoy_growth_rates = {}
for column in columns_to_analyze:
    yoy_growth_rates[column] = ((data[column] - data[column].shift(12)) / data[column].shift(12)) * 100

# Add the 'As on Month End' column for reference
yoy_growth_rates['As on Month End'] = data['As on Month End']

# Convert the dictionary to DataFrame
yoy_growth_df = pd.DataFrame(yoy_growth_rates)

# Display the YoY growth rates
yoy_growth_df.dropna()

# Extracting data for each financial year
fy1_data = data[(data['As on Month End'] >= '2021-04-01') & (data['As on Month End'] <= '2022-03-01')]
fy2_data = data[(data['As on Month End'] >= '2022-04-01') & (data['As on Month End'] <= '2023-03-01')]

# Calculating the difference between the end values of each year for each parameter
end_values_diff = fy2_data[parameters].iloc[-1] - fy1_data[parameters].iloc[-1]

# Calculating the percentage change between the two years for each parameter
percentage_changes = (end_values_diff / fy1_data[parameters].iloc[-1]) * 100

percentage_changes



# Calculating Month-on-Month percentage change for the mentioned parameters

parameters = [
    'Paid-up Share Capital',
    'Loans',
    'Bulk Deposits',
    'Loan against Deposits',
    'CD Ratio (Simple in %)',
    'Gross NPAs',
    'Gross NPAs (in %)',
    'Interest Receivable/ Overdue Interest Reserve'
]

mom_changes = data[parameters].pct_change() * 100
mom_changes['As on Month End'] = data['As on Month End']

mom_changes.tail(15)  # Displaying the last 15 months for better visibility

# MoM changes for Paid-up Share Capital during the year
paid_up_share_mom = mom_changes[['As on Month End', 'Paid-up Share Capital']].set_index('As on Month End')

# Extracting the continuous declining periods for Paid-up Share Capital
declining_periods_share_capital = paid_up_share_mom[paid_up_share_mom['Paid-up Share Capital'] < 0].index

paid_up_share_mom.tail(15), declining_periods_share_capital

# MoM changes for Loans during the year
loans_mom = mom_changes[['As on Month End', 'Loans']].set_index('As on Month End')

# Identifying the periods with persistent increases in Loans
increasing_periods_loans = loans_mom[loans_mom['Loans'] > 0].index

loans_mom.tail(15), increasing_periods_loans

# MoM changes for Bulk Deposits during the year
bulk_deposits_mom = mom_changes[['As on Month End', 'Bulk Deposits']].set_index('As on Month End')

# Identifying the periods of decline in Bulk Deposits
declining_periods_bulk_deposits = bulk_deposits_mom[bulk_deposits_mom['Bulk Deposits'] < 0].index

bulk_deposits_mom.tail(15), declining_periods_bulk_deposits

# MoM changes for Loan against Deposits during the year
loan_against_deposits_mom = mom_changes[['As on Month End', 'Loan against Deposits']].set_index('As on Month End')

# Identifying the periods of decline in Loan against Deposits
declining_periods_loan_against_deposits = loan_against_deposits_mom[loan_against_deposits_mom['Loan against Deposits'] < 0].index

loan_against_deposits_mom.tail(15), declining_periods_loan_against_deposits

# MoM changes for CD Ratio (Simple in %) during the year
cd_ratio_mom = mom_changes[['As on Month End', 'CD Ratio (Simple in %)']].set_index('As on Month End')

# Identifying any significant turnarounds in CD Ratio
significant_changes_cd_ratio = cd_ratio_mom[cd_ratio_mom['CD Ratio (Simple in %)'].abs() > cd_ratio_mom['CD Ratio (Simple in %)'].std()]

cd_ratio_mom.tail(15), significant_changes_cd_ratio

# MoM changes for Gross NPAs during the year
gross_npas_mom = mom_changes[['As on Month End', 'Gross NPAs']].set_index('As on Month End')

# Identifying any significant turnarounds in Gross NPAs
significant_changes_gross_npas = gross_npas_mom[gross_npas_mom['Gross NPAs'].abs() > gross_npas_mom['Gross NPAs'].std()]

gross_npas_mom.tail(15), significant_changes_gross_npas

# MoM changes for Gross NPAs (in %) during the year
gross_npas_percent_mom = mom_changes[['As on Month End', 'Gross NPAs (in %)']].set_index('As on Month End')

# Identifying any significant turnarounds in Gross NPAs (in %)
significant_changes_gross_npas_percent = gross_npas_percent_mom[gross_npas_percent_mom['Gross NPAs (in %)'].abs() > gross_npas_percent_mom['Gross NPAs (in %)'].std()]

gross_npas_percent_mom.tail(15), significant_changes_gross_npas_percent

# Calculating Interest Receivable/ Overdue Interest Reserve as a percentage of Loans
interest_receivable_percent_loans = (data['Interest Receivable/ Overdue Interest Reserve'] / data['Loans']) * 100

# MoM changes for Interest Receivable/ Overdue Interest Reserve as a percentage of Loans
interest_receivable_percent_loans_mom = interest_receivable_percent_loans.pct_change() * 100

# Combining with month-end dates
interest_receivable_percent_loans_mom_df = pd.DataFrame({
    'As on Month End': data['As on Month End'],
    'Interest Receivable/ Overdue Interest Reserve as % of Loans MoM': interest_receivable_percent_loans_mom
}).set_index('As on Month End')

# Identifying significant turnarounds
significant_changes_interest_receivable = interest_receivable_percent_loans_mom_df[
    interest_receivable_percent_loans_mom_df['Interest Receivable/ Overdue Interest Reserve as % of Loans MoM'].abs() >
    interest_receivable_percent_loans_mom_df['Interest Receivable/ Overdue Interest Reserve as % of Loans MoM'].std()]

interest_receivable_percent_loans_mom_df.tail(15), significant_changes_interest_receivable




import pandas as pd

data=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\data_cleaned.xlsx",dtype={'Account Number': str})



"""### Analysis of branches"""

import pandas as pd

df = data.copy()

# Grouping and aggregation:
grouped = df.groupby('Branch_Name').agg(
    Total_Advance=pd.NamedAgg(column='Advance', aggfunc='sum'),
    NPA_Advance=pd.NamedAgg(column='Advance', aggfunc=lambda x: x[df['NPA_YN'] == 'Y'].sum())
).reset_index()

# Calculate the overall total advance and total NPA for all branches:
total_advance_overall = grouped['Total_Advance'].sum()
total_npa_overall = grouped['NPA_Advance'].sum()

# Compute the metrics for each branch and convert them to percentages:
grouped['Advance_to_TotalAdvance'] = (grouped['Total_Advance'] / total_advance_overall) * 100
grouped['NPA_to_TotalNPA'] = (grouped['NPA_Advance'] / total_npa_overall) * 100
grouped['NPA_Advance_to_TotalAdvance'] = (grouped['NPA_Advance'] / grouped['Total_Advance']) * 100

# Find top 10 branches for each metric:
top_advance_to_total = set(grouped.nlargest(20, 'Advance_to_TotalAdvance')['Branch_Name'])
top_npa_to_total = set(grouped.nlargest(20, 'NPA_to_TotalNPA')['Branch_Name'])
top_npa_advance_to_total = set(grouped.nlargest(20, 'NPA_Advance_to_TotalAdvance')['Branch_Name'])

# Find common branches among the top 10 lists:
common_branches = top_advance_to_total.intersection(top_npa_to_total).intersection(top_npa_advance_to_total)


# Select and print the desired columns:
result = grouped[['Branch_Name', 'Advance_to_TotalAdvance', 'NPA_to_TotalNPA', 'NPA_Advance_to_TotalAdvance']]


# Select and print the desired columns for the specified branches:

selected_result = result[result['Branch_Name'].isin(common_branches)]

grouped[grouped['Branch_Name']=="KURLA EAST"]

grouped[grouped['Branch_Name']=="VADODARA"]

grouped[grouped['Branch_Name']=="MOODBIDRI"]

import matplotlib.pyplot as plt

# Set up the figure and subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 18))

# Top 10 for 'Advance_to_TotalAdvance'
sorted_data = result.nlargest(10, 'Advance_to_TotalAdvance')
axes[0].bar(sorted_data['Branch_Name'], sorted_data['Advance_to_TotalAdvance'])
axes[0].set_title('Top 10 Branches by Advance to Total Advance')
axes[0].tick_params(axis='x', rotation=45)
axes[0].set_ylabel('% of Total Advance')

# Top 10 for 'NPA_to_TotalNPA'
sorted_data = result.nlargest(10, 'NPA_to_TotalNPA')
axes[1].bar(sorted_data['Branch_Name'], sorted_data['NPA_to_TotalNPA'])
axes[1].set_title('Top 10 Branches by NPA to Total NPA')
axes[1].tick_params(axis='x', rotation=45)
axes[1].set_ylabel('% of Total NPA')

# Top 10 for 'NPA_Advance_to_TotalAdvance'
sorted_data = result.nlargest(10, 'NPA_Advance_to_TotalAdvance')
axes[2].bar(sorted_data['Branch_Name'], sorted_data['NPA_Advance_to_TotalAdvance'])
axes[2].set_title('Top 10 Branches by NPA Advance to Total Advance')
axes[2].tick_params(axis='x', rotation=45)
axes[2].set_ylabel('% of NPA Advance to Total Advance')

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

"""### Analysis of deposits"""

data.Scheme_Desc.unique()

deposit_products=['LOAN AGAINST SELF DEPOSIT', 'LOAN AGAINST LIC/NSC/KVP','LOAN AGAINST THIRD PARTY DEPOSIT']

# Filter the 'data' DataFrame using the 'isin' function to select rows where 'Scheme_Desc' is in 'deposit_products'
lad = data[data.Scheme_Desc.isin(deposit_products)]



dep=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\indent\Bharat co-operative Bank (Mumbai) Ltd-RBI onsite Inspection Indent 2022-23\3.2 Deposit Dump\TD.xlsx",dtype={'Account No.': str})

dep.columns

import pandas as pd

df=dep.copy()

# Set "Account No." as the index and remove the current index
df.set_index('Account No.', inplace=True)

# Convert the balance column values to crore
df['BALANCE as on March 31, 2022'] = df['BALANCE as on March 31, 2022'] / 1e7


dep=df.copy()

lad.columns

dep.columns

# Group by UCIC, aggregate the sum and concatenate the scheme descriptions
lad_grouped = lad.groupby('UCIC').agg({
    'Total_Balance_os': 'sum',
    'Scheme_Desc': lambda x: ', '.join(x.unique())  # only unique values are joined
}).reset_index()

dep_grouped = dep.groupby('Customer ID/ UCIC ').agg({'BALANCE as on March 31, 2022':'sum'}).reset_index()

# Merge the two grouped dataframes on UCIC
merged_df = lad_grouped.merge(dep_grouped, left_on='UCIC', right_on='Customer ID/ UCIC ', how='inner')

# Compute the difference
merged_df['Difference'] = merged_df['Total_Balance_os'] - merged_df['BALANCE as on March 31, 2022']

# Save the results to Excel
merged_df[merged_df['Total_Balance_os'] > merged_df['BALANCE as on March 31, 2022']].to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\dep_fdod_short.xlsx", index=False)

merged_df[merged_df['Total_Balance_os'] > merged_df['BALANCE as on March 31, 2022']].head()

lad[lad.UCIC=="R1171758"]

dep[dep["Customer ID/ UCIC "]=="R1171758"]

"""# Loan against FDOD"""

sec_od=['OVERDRAFT AGAINST LIC / NSC']
od_sec = data[data.Scheme_Desc.isin(sec_od)]



od_sec.columns

od_sec[od_sec.Branch_Name=='BHANDUP VILLAGE ROAD'].Acc_Number.unique()

od_sec['Branch_Name'].value_counts()



od_sec[(od_sec['Acc_Number'] == 1814300000155)]

"""# Checking upgrades of restructured loans"""

data.head()

hlp[hlp.ACCT_NAME=="AKREETA INFRA PRIVATE LIMITED"].tail()

upgrades=pd.read_excel(r"C:\Users\Admin\Downloads\upgraded.xlsx",dtype={'Account No.': str})

hlp.info()

"""## checking info on specific accounts on the basis of its name seen anywhere in any form"""

# A simple function to normalize the account name
def normalize(name):
    return name.lower().replace("and", "").replace("llp", "").replace("private", "").replace("limited", "").replace("pvt", "").replace("ltd", "").strip()

# Use the function in a lambda to filter the DataFrame
filtered_hlp = hlp[hlp['ACCT_NAME'].apply(normalize).str.contains('(?i)Dynamic')]
filtered_hlp[filtered_hlp['diff'] > 60]#.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\SMA_overdues.xlsx")  # Apply '>' to the 'diff' column

filtered_data.columns

filtered_data = data[data['UCIC'].isin(["C186991"])] # Use .isin() with a list of values
filtered_data.Advance.sum()





up_acc_no=upgrades['Account No.'].to_list()

# Assuming '-' represents missing or invalid dates, you can filter out such rows
valid_rows = upgrades['Date of giving effect in system'] != '-'
upgrades = upgrades[valid_rows]

# Now try converting the column to datetime format again
upgrades['Date of giving effect in system'] = pd.to_datetime(upgrades['Date of giving effect in system'])

"""## Checking condition 1- no NPA during specified period"""

import pandas as pd

# Convert the DMD_EFF_DATE column to datetime if it's not already
hlp['DMD_EFF_DATE'] = pd.to_datetime(hlp['DMD_EFF_DATE'])

# First filter the hlp dataframe for rows where diff is greater than 90
filtered_hlp = hlp[hlp['diff'] > 90]

# Merge the filtered hlp dataframe with upgrades on Account No.
merged_df = filtered_hlp.merge(upgrades, left_on='FORACID', right_on='Account No.', how='inner')

# Now filter rows where DMD_EFF_DATE is after the "Date of giving effect in system"
final_filtered_df = merged_df[
    (merged_df['DMD_EFF_DATE'] > merged_df['Date of giving effect in system']) &
    (merged_df['DMD_EFF_DATE'] <= merged_df['Date of giving effect in system'] + pd.Timedelta('1Y')) &
    (merged_df['diff'] != 0)
]

# Display the results
final_filtered_df.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\upgrades_failed3.xlsx")
list1=final_filtered_df.FORACID.unique()

list1

## Checking condition 2- no overdue after one year

import pandas as pd


merged_df = hlp.merge(upgrades, left_on='FORACID', right_on='Account No.', how='inner')
# Create a new column that's 1 year after 'Date of giving effect in system'
merged_df['date_plus_one_year'] = merged_df['Date of giving effect in system'] + pd.Timedelta('1Y')

# Now filter rows where 'DMD_EFF_DATE' is equal to 'date_plus_one_year' and 'diff' is not equal to 0
final_filtered_df = merged_df[
    (merged_df['DMD_EFF_DATE'] == merged_df['date_plus_one_year']) &
    (merged_df['diff'] != 0) &
    (~merged_df['FORACID'].isin(list1))
]

# Save the results to an Excel file
final_filtered_df.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\upgrades_failed4.xlsx")

merged_df.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\merged_table.xlsx")

import pandas as pd

# Assuming you've already merged the dataframes and have 'merged_df' and added the 'date_plus_one_year' column

# Create an empty dataframe to store the final results
result_df = pd.DataFrame()

# Group by 'FORACID'
grouped = merged_df.groupby('FORACID')

for name, group in grouped:
    # Get the earliest date_plus_one_year for this FORACID
    earliest_date_plus_one_year = group['date_plus_one_year'].min()

    # Filter rows for this FORACID from 'earliest_date_plus_one_year' onwards and not in list1
    filtered_group = group[(group['DMD_EFF_DATE'] >= earliest_date_plus_one_year) & (~group['FORACID'].isin(list1))]

    # Check if any row has 'diff' > 0
    if any(filtered_group['diff'] > 0):
        result_df = result_df.append(filtered_group)

# Save the results to an Excel file
result_df.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\filtered_upgrades_after_specified_period.xlsx")

result_df.FORACID.unique()

"""## Para 77 provision_calculation for SR"""

data.columns

import pandas as pd
from datetime import datetime

# Load the data
data = pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\SR_prov_calc_final_sheet\SRdump.xlsx")

# Convert 'Date of NPA' column to datetime format and then to 'dd-mm-yy'
data['Date of NPA'] = pd.to_datetime(data['Date of NPA'], errors='coerce', dayfirst=True).dt.strftime('%d-%m-%y')

# Define the reference dates
reference_date_2022 = datetime.strptime('31-03-2022', '%d-%m-%Y')
reference_date_2023 = datetime.strptime('31-03-2023', '%d-%m-%Y')




# Calculate DPD for 2022 and 2023
data['dpd_2022'] = (reference_date_2022 - pd.to_datetime(data['Date of NPA'], dayfirst=True)).dt.days
data['dpd_2023'] = (reference_date_2023 - pd.to_datetime(data['Date of NPA'], dayfirst=True)).dt.days


# For 2022
# DPD < 365 days for 2022
data.loc[data['dpd_2022'] < 365, 'provision_required_2022'] = data['SR value as on March 31, 2022'] * 0.1

# DPD > 365 but <= 730 days for 2022
mask_365_to_730_2022 = (data['dpd_2022'] > 365) & (data['dpd_2022'] <= 730)
mask_security_value_gt_principal_2022 = data['Security Value 85%'] > data['SR value as on March 31, 2022']
data.loc[mask_365_to_730_2022 & mask_security_value_gt_principal_2022, 'provision_required_2022'] = data['SR value as on March 31, 2022'] * 0.2
data.loc[mask_365_to_730_2022 & ~mask_security_value_gt_principal_2022, 'provision_required_2022'] = data['Security Value 85%'] * 0.2 + (data['SR value as on March 31, 2022'] - data['Security Value 85%'])

# DPD > 730 but <= 1460 days for 2022
mask_730_to_1460_2022 = (data['dpd_2022'] > 730) & (data['dpd_2022'] <= 1460)
data.loc[mask_730_to_1460_2022 & mask_security_value_gt_principal_2022, 'provision_required_2022'] = data['SR value as on March 31, 2022'] * 0.3
data.loc[mask_730_to_1460_2022 & ~mask_security_value_gt_principal_2022, 'provision_required_2022'] = data['Security Value 85%'] * 0.3 + (data['SR value as on March 31, 2022'] - data['Security Value 85%'])

# DPD > 1460 days for 2022
data.loc[data['dpd_2022'] > 1460, 'provision_required_2022'] = data['SR value as on March 31, 2022']

# 2. Calculate asset_class_2022 based on DPD
data['asset_class_2022'] = 'SS'
data.loc[mask_365_to_730_2022, 'asset_class_2022'] = 'D-1'
data.loc[mask_730_to_1460_2022, 'asset_class_2022'] = 'D-2'
data.loc[data['dpd_2022'] > 1460, 'asset_class_2022'] = 'D-3'


# For 2023
data['provision_required_2023'] = 0
data['asset_class_2023'] = 'SS'

# DPD < 365 days for 2023
data.loc[data['dpd_2023'] < 365, 'provision_required_2023'] = data['SR value as on March 31, 2023'] * 0.1

# DPD > 365 but <= 730 days for 2023
mask_365_to_730_2023 = (data['dpd_2023'] > 365) & (data['dpd_2023'] <= 730)
mask_security_value_gt_principal_2023 = data['Security Value 85%'] > data['SR value as on March 31, 2023']
data.loc[mask_365_to_730_2023 & mask_security_value_gt_principal_2023, 'provision_required_2023'] = data['SR value as on March 31, 2023'] * 0.2
data.loc[mask_365_to_730_2023 & ~mask_security_value_gt_principal_2023, 'provision_required_2023'] = data['Security Value 85%'] * 0.2 + (data['SR value as on March 31, 2023'] - data['Security Value 85%'])

# DPD > 730 but <= 1460 days for 2023
mask_730_to_1460_2023 = (data['dpd_2023'] > 730) & (data['dpd_2023'] <= 1460)
data.loc[mask_730_to_1460_2023 & mask_security_value_gt_principal_2023, 'provision_required_2023'] = data['SR value as on March 31, 2023'] * 0.3
data.loc[mask_730_to_1460_2023 & ~mask_security_value_gt_principal_2023, 'provision_required_2023'] = data['Security Value 85%'] * 0.3 + (data['SR value as on March 31, 2023'] - data['Security Value 85%'])

# DPD > 1460 days for 2023
data.loc[data['dpd_2023'] > 1460, 'provision_required_2023'] = data['SR value as on March 31, 2023']

# Calculate asset_class_2023 based on DPD
data['asset_class_2023'] = 'SS'
data.loc[mask_365_to_730_2023, 'asset_class_2023'] = 'D-1'
data.loc[mask_730_to_1460_2023, 'asset_class_2023'] = 'D-2'
data.loc[data['dpd_2023'] > 1460, 'asset_class_2023'] = 'D-3'






# Rename columns for consistency with provided sequence and reorder
column_renaming = {
    'SR value as on March 31, 2022': 'SR_value_2022',
    'redemption upto 2023': 'Redemption_2023',
    'SR value as on March 31, 2023': 'SR_value_2023',
    'Security Value 85%': 'Security_Value',
    'Date of NPA': 'NPA_date'
}

data.rename(columns=column_renaming, inplace=True)

# If 'Date of NPA' is not available (NaT), set asset class to 'Loss'
data.loc[pd.isna(data['NPA_date']), ['asset_class_2022', 'asset_class_2023']] = 'Loss'

# Ensure that provision requirement is 100% for asset_class==Loss
data.loc[data['asset_class_2022'] == 'Loss', 'provision_required_2022'] = data['SR_value_2022']
data.loc[data['asset_class_2023'] == 'Loss', 'provision_required_2023'] = data['SR_value_2023']


column_order = [
    'Tranche', 'Account No.', 'NPA_date', 'Principle', 'Sale Proceeds', 'Loss', 'BDDR',
    'SR_value_2022', 'Redemption_2023', 'SR_value_2023', 'Security_Value', 'NPA_date',
    'dpd_2022', 'provision_required_2022', 'asset_class_2022', 'dpd_2023', 'provision_required_2023', 'asset_class_2023'
]

data_ordered = data[column_order]

# Save the final data
data_ordered.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\para77.xlsx", index=False)

data['provision_required_2023'].sum()

data.columns

# Calculate the sum of provision_required_2023 for each asset class in data_combined
provision_by_asset_class_2023 = data.groupby('asset_class_2023')['SR_value_2023'].sum()

provision_by_asset_class_2023

# Calculate the sum of provision_required_2023 for each asset class in data_combined
provision_by_asset_class_2023 = data.groupby('asset_class_2023')['provision_required_2023'].sum()

provision_by_asset_class_2023

data_combined['provision_required_2023'].sum()

data_combined[data_combined.SR_value_2023>data_combined.SR_value_2022].to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\SR_val_anomaly.xlsx")

dep.info()



import pandas as pd

# Load the data
data = pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\credit\PSL Micro Enterprise26.xlsx")

# Define the investment and turnover limits for micro-enterprise
investment_limit = 1e7  # 1 crore rupees
turnover_limit = 5e7  # 5 crore rupees

# Check for discrepancies function
def discrepancy_reason(row):
    reasons = []

    # Check against micro-enterprise criteria
    if not ((row['Written down value of P & M'] <= investment_limit) & (row['Turnover'] <= turnover_limit)):
        reasons.append("Does not meet micro-enterprise criteria.")

    # Check for abnormal values
    if row['Written down value of P & M'] > 0 and row['Written down value of P & M'] < 1000:
        reasons.append("Abnormal value in Plant & Machinery.")

    if pd.isnull(row['Turnover']) or row['Turnover'] < 10:
        reasons.append("Null or abnormal value in Turnover.")

    # Check for repeated values
    if data[data['Written down value of P & M'] == row['Written down value of P & M']].shape[0] > 10:
        reasons.append("Same Plant & Machinery value in more than ten cases.")
    if data[data['Turnover'] == row['Turnover']].shape[0] > 10:
        reasons.append("Same turnover in more than 10 instances.")

    return "; ".join(reasons)

# Apply the discrepancy_reason function to get the discrepancies column
data['Discrepancies'] = data.apply(discrepancy_reason, axis=1)

# Filter rows with discrepancies
discrepancies_filtered = data[data['Discrepancies'] != ""]

# Save the filtered discrepancies to a new Excel file
output_file_path = r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\discr_PSL.xlsx"
discrepancies_filtered[['Account ID', 'Written down value of P & M', 'Turnover', 'Discrepancies']].to_excel(output_file_path)

# Split the discrepancies and create a separate row for each discrepancy
discrepancies_expanded = discrepancies_filtered['Discrepancies'].str.split('; ').explode()

# Group by discrepancies and count
discrepancy_counts = discrepancies_expanded.value_counts()

print(discrepancy_counts)

data.shape

"""## Checking forex products"""

data.groupby(Scheme_Desc).principal_os.sum()

forex_products = ['FOREIGN CCY TERM LOAN (FCTL)', 'PACKING CREDIT CRYSTALLIZE', 'EXPORT BILL CRYSTALLIZE', 'PACKING CREDIT IN FCY', 'FOREIGN BILL NEGOTIATION PURCHASE AND DISCOUNT', 'PACKING CREDIT IN INR', 'FOREIGN BILL RUPEE ADVANCE', 'BUYERS CREDIT DEVOLVEMENT']

forex_adv = data[data['Scheme_Desc'].isin(forex_products)]

forex_adv["Advance"].sum()

forex_adv.groupby("Scheme_Desc")["Advance"].sum()

# Calculate the sum of 'Advance' without normalization
sum_of_advance = forex_adv.groupby("Scheme_Desc")["Advance"].sum()

# Calculate the normalized sum of 'Advance'
normalized_sum_of_advance = sum_of_advance / sum_of_advance.sum()

print(normalized_sum_of_advance)





## Comparing the september NPA dump

sep=pd.read_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\# 37 NPA as on 30.09.2022 and upgraded 31.03.2023\sep_NPA_dump.xlsx")

npa_accounts=data[data.NPA_YN=="Y"].Acc_Number.unique()

standard_accounts=data[data.NPA_YN=="N"].Acc_Number.unique()

sep_npa=sep["Loan A/c. no."].unique()

# Convert lists to sets for faster membership checking
standard_accounts_set = set(standard_accounts)
sep_npa_set = set(sep_npa)

# Find the difference between the sets
sep_npa_mar_npa = list(sep_npa_set - standard_accounts_set)

len(sep_npa_mar_npa)

# Convert sep_npa_mar_npa list to a set
sep_npa_mar_npa_set = set(sep_npa_mar_npa)

# Perform set subtraction
sep_npa_mar_upg = list(sep_npa_set - sep_npa_mar_npa_set)

data.Acc_Number

sep_npa_mar_upg

extracted_data = data[data['Acc_Number'].isin(sep_npa_mar_upg)]
extracted_data.Advance.sum()

# Filter hlp dataframe based on FORACID values in sep_npa_mar_upg
extracted_hlp = hlp[hlp['FORACID'].isin(sep_npa_mar_upg)]
extracted_hlp.to_excel(r"D:\one drive\OneDrive - rbionline\Inspection 2023\bharat\dump_analysis\sep_upg_accts.xlsx")

