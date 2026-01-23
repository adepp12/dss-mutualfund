# data cleaning function
def cleaning_data(raw_df):
    '''
    documentation
    '''
    df = raw_df.copy()

    columns_to_clean = ["Last NAV", "Return 1Y", "Drawdown 1Y", "Expense Ratio", "Min. Pembelian"]

    # cleaning persen (%) and comma (,) 
    for column in columns_to_clean:
        df[column] = df[column].str.replace('%', '')
        df[column] = df[column].str.replace(',', '')
    
    df['Expense Ratio'] = df['Expense Ratio'].str.replace('-', '0')
    df['Total AUM'] = df['Total AUM'].str.replace('Rp', '')
    df['Min. Pembelian'] = df['Min. Pembelian'].str.replace('IDR ', '')

    # change the format of the “Total AUM” column to Billion (B)
    df["isTrillion"] = 0

    for i, row in df.iterrows():
        if 'T' in row['Total AUM']:
            df.loc[i, "isTrillion"] = 1
            df.loc[i, "Total AUM"] = row['Total AUM'].replace('T', '')
        else:
            df.loc[i, "Total AUM"] = row['Total AUM'].replace('B', '')

    df.loc[df["isTrillion"] == 1, "Total AUM"] = (
        df.loc[df["isTrillion"] == 1, "Total AUM"].astype(float) * 1000).round()

    # convert data type to float
    float_columns = ['Return 1Y', 'Drawdown 1Y', 'Total AUM', 'Last NAV', 'Expense Ratio']

    for col in float_columns:
        df[col] = df[col].astype(float)

    # remove help column
    df.drop(columns=["isTrillion"], inplace=True)

    return df