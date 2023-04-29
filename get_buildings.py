from pyrosm import OSM
import pandas as pd
from get_power import get_power
import pyproj
import shapely
import shapely.wkt
from shapely.ops import transform

def get_roofshape(dict_):
    if isinstance(dict_, str):
        return ""
    elif 'roof:shape' in dict_.keys():
        return dict_['roof:shape']
    else:
        return ""

# Define the source and destination coordinate systems
in_proj = pyproj.CRS('EPSG:4326')  # WGS 84
out_proj = pyproj.CRS('EPSG:3857')  # Web Mercator
transformer = pyproj.Transformer.from_proj(in_proj, out_proj)

def get_roofarea(polygon):
    # input polygon is passed directly in the WKT format

    # Convert the polygon string to a Shapely Polygon object
    # polygon = shapely.wkt.loads(polygon)
    projected_polygon = shapely.ops.transform(transformer.transform, polygon)

    # Calculate the area of the reprojected polygon in square meters
    area_m2 = projected_polygon.area

    return area_m2

def get_df():
    # import .pbf buildings as df
    print('loading data')
    osm = OSM('data/buildings/bremen.osm.pbf')

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

    # Export
    print(df.columns)
    # print(df.loc[100, :].values.tolist())
    # print(df.head(100).to_csv("test.csv"))
    print(df.to_csv("test_bremen.csv"))

    return df

if __name__ == '__main__':
    get_df()
