import pandas as pd

def get_stuff():
    df = pd.read_csv('../generated_data/test_bremen.csv')
    df = df.sort_values(by=['power'])

    df.head(200).to_csv('top_200.csv')

    fossil = 292239900000  # kWh of power used in germany

    i = 0
    sum = 0
    j = len(df.index)

    print('Start calc')

    while sum < fossil:
        sum = sum + df.loc[i, 'power']
        i += 1
        if i>j:
            break

    print(sum)
    print(i)

get_stuff()