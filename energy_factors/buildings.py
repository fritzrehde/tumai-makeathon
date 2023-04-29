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

from azureml.core import Workspace, Datastore, Dataset

# create a FileDataset pointing to files in 'animals' folder and its subfolders recursively
# datastore_paths = [(datastore, 'animals')]
# animal_ds = Dataset.File.from_files(path=datastore_paths)

# create a FileDataset from image and label files behind public web urls
web_paths = ['https://makeathon0835510051.blob.core.windows.net/azureml-blobstore-4f800bf3-3089-4757-9d89-d2a8a7c7b1b6/UI/2023-04-29_191451_UTC/germany-latest.osm.pbf']
# mnist_ds = Dataset.File.from_files(path=web_paths)

def get_df():
    # import .pbf buildings as df
    print('Debug: loading data from OSM')
    osm = OSM(web_paths)
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
