import numpy as np
from pyproj import Transformer
import math
from energy_factors.buildings import get_df
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium import plugins
from folium.plugins import HeatMap


"""
Takes df or csv with buildings and calculates mean power for certain area
"""


area_border = 1000  # in m


def to_GK_h(lat, long):
    # convert latitude, longitudine to Gauss
    # Define coordinate systems
    from_crs = "EPSG:4326"  # WGS 84
    to_crs = "EPSG:31467"  # Gauss Krüger Zone 3

    # Create transformer object
    transformer = Transformer.from_crs(from_crs, to_crs)

    # Convert latitude and longitude to Gauss Krüger coordinates
    h, r = transformer.transform(lat, long)
    return h

def to_GK_r(lat, long):
    # convert latitude, longitudine to Gauss
    # Define coordinate systems
    from_crs = "EPSG:4326"  # WGS 84
    to_crs = "EPSG:31467"  # Gauss Krüger Zone 3

    # Create transformer object
    transformer = Transformer.from_crs(from_crs, to_crs)

    # Convert latitude and longitude to Gauss Krüger coordinates
    h, r = transformer.transform(lat, long)
    return r

def do_reducing():
    # get df
    print('Get data as df')
    # df = get_df()
    df = pd.read_csv('generated_data/bremen_test.csv')

    # only keep necessary columns
    print('do column magic')
    df['power'] = 1
    df = df[['roof_location_latitude', 'roof_location_longitude', 'power']]
    df = df.rename(columns={"roof_location_latitude": "latitude", "roof_location_longitude": "longitude"})

    # convert lat, long to meter
    print('converting h')
    df['h'] = to_GK_h(df['latitude'], df['longitude'])
    print('converting r')
    df['r'] = to_GK_r(df['latitude'], df['longitude'])

    print('make boxes')
    h_min = df['h'].min()
    h_max = df['h'].max()
    r_min = df['r'].min()
    r_max = df['r'].max()

    h_iterations = math.ceil((h_max - h_min)/area_border)
    r_iterations = math.ceil((r_max - r_min)/area_border)

    lat_list = []
    long_list = []
    power_list = []

    for i in range(h_iterations):
        lower = area_border * i + h_min
        upper = lower + area_border

        # select vertical strip in bounds
        data = df.loc[lambda df: df['h'] < upper]
        data = df.loc[lambda data: data['h'] >= lower]

        for j in range(r_iterations):
            left = area_border*i + r_min
            right = left + area_border

            # select horizontal strip in bounds
            square = data.loc[lambda data: data['h'] < upper]
            square = data.loc[lambda square:square['h'] >= lower]

            mean_power = square["power"].mean()
            mean_lat = square["latitude"].mean()
            mean_long = square["longitude"].mean()

            long_list.append(mean_long)
            lat_list.append(mean_lat)
            power_list.append(mean_power)

    d = {'mean_longitude': long_list, 'mean_latitude': lat_list, 'mean_power': power_list}
    df_reduced = pd.DataFrame(data=d)
    df_reduced.to_csv('visualize/reduced_data.csv')

    heat_df = df_reduced.loc[:,["mean_latitude","mean_longitude","mean_power"]]

    # map_hooray = folium.Map(location=[50, 12], zoom_start=12)
    # heat_data = heat_df.values.tolist()
    # HeatMap(heat_data,radius=13).add_to(map_hooray)
    # map_hooray.save('heat_map.html')