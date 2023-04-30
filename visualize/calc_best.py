import pandas as pd

def get_stuff():
    df = pd.read_csv('generated_data/bremen_test.csv')
    df = df.sort_values(by=['power'])

    keep_cols = ['addr:housenumber', 'addr:postcode', 'addr:street', 'roof_area',
                 'power', 'irradiance', 'roof_location_latitude', 'roof_location_longitude']
    drop_cols = list(set(df.columns) - set(keep_cols))
    df = df.drop(drop_cols, axis=1)

    df.head(100).to_csv('visualize/top_100.csv')

    df = pd.read_csv('generated_data/bremen_test.csv')

    fossil = 292239900000  # kWh of power used in germany
    i = 0
    summe = 0
    j = len(df.index)

    print('Start calc')
    while summe < fossil:
        x = float(df.loc[i, 'power'])
        if pd.isna(x):
            print(f'NaN value found in row {i}: {x}')
        else:
            summe = summe + x
        i += 1
        if i == j:
            break

    print(summe)
    print('Houses needed: ' + str(i))
    print('total Hosues: ' + str(j))

get_stuff()