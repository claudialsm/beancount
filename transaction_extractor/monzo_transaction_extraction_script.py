import numpy as np
import pandas as pd
import re
import os

# -----------------------------------------------------Need to re-read beancount's directory policy-----------------------------------------------------

directory = os.getcwd()
col_list = ['Date', 'Description', 'Notes and #tags', 'Amount', 'Category']

# Loop through each monzo csv statement
for file in os.listdir(directory):
    if not file.endswith(".csv"):
        continue
# Read csv into DataFrame
    else:
        df = pd.read_csv(file, sep=',', parse_dates=['Date'], usecols=col_list)
        df['Date_only'] = df['Date'].dt.date
        pd.set_option('max_columns', None)
        pd.set_option('max_rows', None)
        # replacing NaN null values with empty string
        df = df.fillna("") 

df

# ---------------------------------------for each transaction row in the dataframe, create the beancount text file---------------------------------------

# for each transaction row in the dataframe, create the beancount text file

df = df.applymap(str)

for row in df.itertuples(index=False):
    if row[4][-3:] == 'GBR':
        abbreviation = 'UK'
    elif row[4][-3:] == 'USD':
        abbreviation = 'US'
    elif row[4][-3:] == 'CZE':
        abbreviation = 'CZ'
    elif row[4][-3:] == 'MYR':
        abbreviation = 'MY'
    else:
        #very rarely occur
        abbreviation = '' 
        
    if row[2][0] == '-':
        posvalue = row[2][1:]
    elif row[2] == '0.00': # only appear as 0.0 not 0.00?
        posvalue = '0.00'
    else:
        posvalue = '-' + row[2][:]

    x = """{dat} * "{desc}" "{notes}"
  {asset}:{country}:  {amount} GBP
  {expense}::{cat} {absval} GBP
        """ 
    
    print(x.format(dat=row[5], desc=row[4], notes=row[3], asset='Bank', country=abbreviation, expense='Expenses', cat=row[1], amount=row[2], absval=posvalue))