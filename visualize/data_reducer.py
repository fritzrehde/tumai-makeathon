import numpy as np
from pyproj import Transformer
import math
from energy_factors.buildings import get_df
import pandas as pd
import folium
from folium.plugins import HeatMap


"""
Takes df or csv with buildings and calculates mean power for certain area
"""


area_border = 1000  # in m


def to_GK(lat, long):
    # convert latitude, longitudine to Gauss
    # Define coordinate systems
    from_crs = "EPSG:4326"  # WGS 84
    to_crs = "EPSG:31467"  # Gauss Krüger Zone 3

    # Create transformer object
    transformer = Transformer.from_crs(from_crs, to_crs)

    # Convert latitude and longitude to Gauss Krüger coordinates
    h, r = transformer.transform(lat, long)
    return h, r


# get df
df = get_df()
# only keep necessary columns
df = df[['roof_location_latitude', 'roof_location_longitude', 'power']]
df.rename(columns={"roof_location_latitude": "latitude", "roof_location_longitude": "longitude"})
# convert lat, long to meter

df['h'], df['r'] = df['latitude', 'longitude'].apply(to_GK)

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
    data = df.loc[df['h'] < upper]
    data = df.loc[data['h'] >= lower]

    for j in range(r_iterations):
        left = area_border*i + r_min
        right = left + area_border

        # select horizontal strip in bounds
        square = data.loc[data['h'] < upper]
        square = data.loc[square['h'] >= lower]

        mean_power = square["power"].mean()
        mean_lat = square["latitude"].mean()
        mean_long = square["longitude"].mean()

        long_list.append(mean_long)
        lat_list.append(mean_lat)
        power_list.append(mean_power)

d = {'mean_longitude': long_list, 'mean_latitude': lat_list, 'mean_power': power_list}
df_reduced = pd.DataFrame(data=d)

map_obj = folium.Map(location = [16, 42], zoom_start = 5)


lats_longs = [
                [38.27312, -98.5821872, 0.5], # Kansas
                [34.395342, -111.763275,0.2], # Arizona
                [37.5726028, -85.1551411, 0.7], # Kentucky
                [32.3293809, -83.1137366,0.9], # Georgia
                [40.0796606, -89.4337288,0.1], # Illinois
            ]


HeatMap(lats_longs).add_to(map_obj)

map_obj




