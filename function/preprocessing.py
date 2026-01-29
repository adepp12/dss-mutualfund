# data cleaning function
def cleaning_data(raw_df):
    '''
    Membersihkan dan mengonversi data reksa dana dari format string ke format numerik
    
    Parameters:
    -----------
    raw_df : DataFrame
        Data mentah reksa dana yang masih dalam format string
    
    Returns:
    --------
    DataFrame
        Data yang sudah dibersihkan dengan tipe data numerik (float)
    
    Proses Cleaning:
    ----------------
    1. Menghapus simbol '%' dan ',' dari kolom numerik
    2. Mengubah '-' menjadi '0' pada kolom Expense Ratio
    3. Menghapus prefix 'Rp' dan 'IDR' dari kolom mata uang
    4. Konversi nilai kolom Total AUM dari Triliun (T) ke Miliar (B)
    5. Mengonversi semua kolom numerik ke tipe data float
    
    Example:
    --------
    # Data sebelum cleaning
    >>> raw_data = pd.DataFrame({
    ...     'Last NAV': ['1,234.56'],
    ...     'Return 1Y': ['10.5%'],
    ...     'Total AUM': ['1.5T'],
    ...     'Expense Ratio': ['-'],
    ...     'Min. Pembelian': ['IDR 10,000']
    ... })
    >>> 
    >>> # Data setelah cleaning
    >>> clean_data = cleaning_data(raw_data)
    >>> print(clean_data)
        Last NAV  Return 1Y  Total AUM  Expense Ratio  Min. Pembelian
    0   1234.56       10.5     1500.0            0.0         10000.0
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
    float_columns = ['Return 1Y', 'Drawdown 1Y', 'Total AUM', 'Last NAV', 'Expense Ratio', 'Min. Pembelian']

    for col in float_columns:
        df[col] = df[col].astype(float)

    # remove help column
    df.drop(columns=["isTrillion"], inplace=True)

    return df