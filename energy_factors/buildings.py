from pyrosm import OSM
import pandas as pd
import pyproj
import shapely
import shapely.wkt
from shapely.ops import transform

from .sun_radiation import get_sun_radiation
from .power import get_power
from .roof_area import get_roofarea
from .roof_location import get_rooflocation_latitude
from .roof_location import get_rooflocation_longitude
from .roof_shape import get_roofshape
from .building_type import get_buildingtype

from azureml.fsspec import AzureMachineLearningFileSystem

fs = AzureMachineLearningFileSystem('azureml://subscriptions/7972acb1-114d-41ac-b5c5-91d74b796b31/resourcegroups/paul.pucknus-rg/workspaces/makeathon/datastores/workspaceblobstore/UI')
uri = 'azureml://subscriptions/7972acb1-114d-41ac-b5c5-91d74b796b31/resourcegroups/paul.pucknus-rg/workspaces/makeathon/datastores/workspaceblobstore/paths/UI/2023-04-29_191451_UTC/germany-latest.osm.pbf'
def get_df():
    # import .pbf buildings as df
    print('Debug: loading data from OSM')
    print('Check: ' + str(fs.exists('./paths/UI/2023-04-29_191451_UTC/germany-latest.osm.pb')))
    print(fs.ls())
    with fs.open('./UI/2023-04-29_191451_UTC/germany-latest.osm.pb') as f:

        # do some process
        osm = OSM(f)
    # osm = OSM(fs.open('./UI/2023-04-29_191451_UTC/germany-latest.osm.pbf'))
    # osm = OSM('azureml://subscriptions/7972acb1-114d-41ac-b5c5-91d74b796b31/resourcegroups/paul.pucknus-rg/workspaces/makeathon/datastores/workspaceblobstore/paths/UI/2023-04-29_191451_UTC/germany-latest.osm.pbf')
    # osm = OSM('data/buildings/bremen.osm.pbf')

    print('Debug: extract buildings from OSM')
    buildings = osm.get_buildings()
    df = pd.DataFrame(buildings)

    print('Debug: df cleaning and preparation')
    # Extract stuff that is removed later
    print('Debug: Get roof shapes')
    df['roof_shape'] = get_roofshape(df['tags'])
    # df['building_type'] = get_buildingtype(df['tags'])

    # drop all rows that don't contain certain columns
    df = df.dropna(subset=['addr:housenumber', 'addr:postcode', 'addr:street'])

    # drop all the columns except the ones specified in keep_cols
    print('Debug: Drop Columns')
    keep_cols = ['addr:housenumber', 'addr:postcode', 'addr:street', 'building:levels', 'height', 'geometry', 'roof:shape']
    drop_cols = list(set(df.columns) - set(keep_cols))
    df = df.drop(drop_cols, axis=1)

    # Add columns custom calculated columns
    print('Debug: Calc area, coordinates, power')
    df['roof_area'] = df['geometry'].apply(get_roofarea)
    df['roof_location_latitude'] = df['geometry'].apply(get_rooflocation_latitude)
    df['roof_location_longitude'] = df['geometry'].apply(get_rooflocation_longitude)

    df['irradiance'] = get_sun_radiation(df['roof_location_latitude'], df['roof_location_longitude'])
    df['power'] = get_power(df['irradiance'], df['roof_area'])

    # Drop columns with unsupported types in tinydb
    print('Debug: Drop Geometry')
    drop_list = ['geometry']
    df = df.drop(drop_list, axis=1)

    return df
