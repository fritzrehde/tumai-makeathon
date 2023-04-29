from pyrosm import OSM
import pandas as pd
import pyproj
import shapely
import shapely.wkt
from shapely.ops import transform

from .power import get_power
from .roof_area import get_roofarea
from .roof_location import get_rooflocation_latitude
from .roof_location import get_rooflocation_longitude
from .roof_shape import get_roofshape

def get_df():
    # import .pbf buildings as df
    print('Debug: loading data from OSM')
    osm = OSM('data/buildings/bremen.osm.pbf')

    print('Debug: extract buildings from OSM')
    buildings = osm.get_buildings()
    df = pd.DataFrame(buildings)

    print('Debug: df cleaning and preparation')
    # Extract stuff that is removed later
    df['roof_shape'] = df['tags'].apply(get_roofshape)

    # drop all the columns except the ones specified in keep_cols
    keep_cols = ['addr:housenumber', 'addr:postcode', 'addr:street', 'building:levels', 'height', 'geometry']
    drop_cols = list(set(df.columns) - set(keep_cols))
    df = df.drop(drop_cols, axis=1)

    df = df[df['addr:housenumber'].str.strip().astype(bool)]  # Drop stuff without housenumber

    # Add columns custom calculated columns
    df['roof_area'] = df['geometry'].apply(get_roofarea)
    df['roof_location_latitude'] = df['geometry'].apply(get_rooflocation_latitude)
    df['roof_location_longitude'] = df['geometry'].apply(get_rooflocation_longitude)

    df['power'] = df.apply(get_power(df['roof_location_latitude'], df['roof_location_longitude'], 1), axis=1)

    # Drop columns with unsupported types in tinydb
    drop_list = ['geometry']
    df = df.drop(drop_list, axis=1)

    return df
