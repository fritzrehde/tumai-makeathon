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
    print('loading data')
    osm = OSM('../data/buildings/bremen.osm.pbf')

    print('get buildings')
    buildings = osm.get_buildings()
    df = pd.DataFrame(buildings)

    # Drop certain columns and rows without streetnumber
    drop_list = ['addr:country', 'addr:full', 'addr:housename', 'email',
                 'name', 'opening_hours', 'operator', 'phone', 'ref', 'url', 'website', 'internet_access', 'wikipedia']
    df = df.drop(drop_list, axis=1)

    # df = df[df['addr:housenumber'].str.strip().astype(bool)]

    # Add columns with roof area and shape
    # df['roof_shape'] = df['tags'].apply(get_roofshape)
    df['roof_area'] = df['geometry'].apply(get_roofarea)
    df['roof_location_latitude'] = df['geometry'].apply(get_rooflocation_latitude)
    df['roof_location_longitude'] = df['geometry'].apply(get_rooflocation_longitude)
    df['power'] = df.apply(get_power(df['latitude'], ['longitude'], 1), axis=1)
    return df
