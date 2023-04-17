import numpy as np
import pandas as pd
import os

def load_data(file_name):
    raw_df = pd.read_excel(file_name)
    raw_df.columns = raw_df.columns.str.lower()
    # df[['purchaser','wholesale','retail','transport','import']] = df[['purchaser','wholesale','retail','transport','import']]*1000
    
    return raw_df

def etl(raw_df):
    all_col = sorted(list(set(raw_df['column'].to_list())))
    df = pd.DataFrame(columns = all_col)

    # Transform
    for col_purchase in df.columns:
        df[col_purchase] = list(raw_df.loc[raw_df['column']==int(col_purchase),'purchaser'])

    # Rename columns
    df.columns = df.columns.astype(str)
    for col in df.columns:
        if len(col) == 1:
            df = df.rename(columns={f'{col}':f'00{col}'})
        elif len(col) == 2:
            df = df.rename(columns={f'{col}':f'0{col}'})

    # Rename rows
    df.index = sorted(list(set(raw_df['row'].to_list())))
    df.index = df.index.astype(str)
    for row in df.index:
        if len(row) == 1:
            df = df.rename(index={f'{row}':f'00{row}'})
        elif len(row) == 2:
            df = df.rename(index={f'{row}':f'0{row}'})
    return df

def validate(df):
    validate_vertical = {}
    row_index_001 = list(df.index).index('001')
    row_index_016 = list(df.index).index('016')+1
    row_index_201 = list(df.index).index('201')
    row_index_204 = list(df.index).index('204')+1
    for col in df.columns:
        if df[col][row_index_001:row_index_016].sum() == df[col]['190'] and df[col][row_index_201:row_index_204].sum() == df[col]['209']:
            validate_vertical[col] = True
        else:
            validate_vertical[col] = False

    validate_horizontal = {}
    col_index_001 = list(df.columns).index('001')
    col_index_016 = list(df.columns).index('016')+1
    col_index_301 = list(df.columns).index('301')
    col_index_306 = list(df.columns).index('306')+1
    for row in df.index:
        if df.iloc[list(df.index).index(row)][col_index_001:col_index_016].sum() == df.iloc[list(df.index).index(row)]['190'] and df.iloc[list(df.index).index(row)][col_index_301:col_index_306].sum() == df.iloc[list(df.index).index(row)]['309']:
            validate_horizontal[row] = True
        else:
            validate_horizontal[row] = False

    return validate_vertical, validate_horizontal
if __name__ == '__main__':
    raw_df = load_data(file_name = "DataIO2015x16.xlsx")
    df = etl(raw_df = raw_df)
    validate_vertical,validate_horizontal = validate(df = df)
    if all(value == True for value in validate_vertical.values()) and all(value == True for value in validate_horizontal.values()):
        print(f'\n\n === YOUR PURCHASER TABLE IS VALIDATED === \n\n')
    else:
        print(f'\n\n === YOUR PURCHASER TABLE IS UNVALIDATED === \n\n')
    df.to_excel('test.xlsx')
    a =3