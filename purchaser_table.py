import numpy as np
import pandas as pd
import os
from typing import Literal

def load_data(file_name):
    raw_df = pd.read_excel(file_name)
    raw_df.columns = raw_df.columns.str.lower()
    cost = []
    for idx in raw_df.index:
        cost.append(raw_df['purchaser'][idx] - raw_df.iloc[idx][['wholesale','retail','transport','import']].sum())
    raw_df['cost'] = cost
    # df[['purchaser','wholesale','retail','transport','import']] = df[['purchaser','wholesale','retail','transport','import']]*1000
    
    return raw_df

def etl(raw_df,target: Literal['purchaser','cost']):
    all_col = sorted(list(set(raw_df['column'].to_list())))
    df = pd.DataFrame(columns = all_col)

    # Transform
    for col in df.columns:
        df[col] = list(raw_df.loc[raw_df['column']==int(col),target])

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


    return df, target


def validate(df,target):
    validate_vertical = {}
    row_index_001 = list(df.index).index('001')
    row_index_016 = list(df.index).index('190')
    row_index_201 = list(df.index).index('201')
    row_index_204 = list(df.index).index('209')
    for col in df.columns:
        if df[col][row_index_001:row_index_016].sum() == df[col]['190'] and df[col][row_index_201:row_index_204].sum() == df[col]['209']:
            validate_vertical[col] = True
        else:
            validate_vertical[col] = False

    validate_horizontal = {}
    col_index_001 = list(df.columns).index('001')
    col_index_016 = list(df.columns).index('190')
    col_index_301 = list(df.columns).index('301')
    col_index_306 = list(df.columns).index('309')
    col_index_401 = list(df.columns).index('401')
    col_index_404 = list(df.columns).index('409')
    for row in df.index:
        if (df.iloc[list(df.index).index(row)][col_index_001:col_index_016].sum() == df.iloc[list(df.index).index(row)]['190']
            and df.iloc[list(df.index).index(row)][col_index_301:col_index_306].sum() == df.iloc[list(df.index).index(row)]['309']
            and df.iloc[list(df.index).index(row)][col_index_401:col_index_404].sum() == df.iloc[list(df.index).index(row)]['409']):
            validate_horizontal[row] = True
        else:
            validate_horizontal[row] = False

    if all(value == True for value in validate_vertical.values()) and all(value == True for value in validate_horizontal.values()):
        validate_status = f"===== YOUR {target} TABLE IS VALIDATED =====".upper()
    else:
        validate_status = f"xxxxx YOUR {target} TABLE IS UNVALIDATED xxxxx".upper()

    return validate_status


if __name__ == '__main__':
    raw_df = load_data(file_name = "DataIO2015x16.xlsx")

    df_purchaser,target = etl(raw_df = raw_df,target='purchaser')
    validate_status = validate(df = df_purchaser,target=target)
    print(f"\n\n\n {validate_status}")

    df_producer,target = etl(raw_df = raw_df,target='cost')
    validate_status = validate(df = df_producer,target=target)
    print(f"\n\n\n {validate_status}")
    df_purchaser.to_excel('purchaser.xlsx')
    a =3