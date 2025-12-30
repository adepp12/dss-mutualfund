# data cleaning function
def cleaning_data(raw_df):
    '''
    documentation
    '''
    df = raw_df

    # cleaning persen (%) and comma (,) 
    for col in df.columns:
        df[col] = df[col].str.replace('%', '')
        df[col] = df[col].str.replace(',', '')

    # change the format of the “Total AUM” column to Billion (B)
    df["isTrillion"] = 0

    for i, row in df.iterrows():
        if 'T' in row['Total AUM']:
            df.loc[i, "isTrillion"] = 1
            df.loc[i, "Total AUM"] = row['Total AUM'].replace('T', '')
        else:
            df.loc[i, "Total AUM"] = row['Total AUM'].replace('B', '')

    df.loc[df["isTrillion"] == 1, "Total AUM"] = df.loc[df["isTrillion"] == 1, "Total AUM"].astype(float) * 1000

    # convert data type to float
    float_columns = ['Return', 'Drawdown', 'Total AUM', 'Last NAV']

    for col in float_columns:
        df[col] = df[col].astype(float)

    # remove help column
    df.drop(columns=["isTrillion"], inplace=True)

    return df