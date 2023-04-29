from pyrosm import OSM
import pandas as pd
import pyproj
import shapely
from shapely import wkt
from pyproj import Geod

from shapely.ops import transform

# Define the source and destination coordinate systems
# in_proj = pyproj.CRS('EPSG:4326')  # WGS 84
# out_proj = pyproj.CRS('EPSG:3857')  # Web Mercator
# transformer = pyproj.Transformer.from_proj(in_proj, out_proj)

def get_roofarea(polygon):
    # input polygon is passed directly in the WKT format

    # specify a name ellipsoid
    geod = Geod(ellps="WGS84")
    area = abs(geod.geometry_area_perimeter(polygon)[0])

    # # Convert the polygon string to a Shapely Polygon object
    # # polygon = shapely.wkt.loads(polygon)
    # projected_polygon = shapely.ops.transform(transformer.transform, polygon)

    # # Calculate the area of the reprojected polygon in square meters
    # area_m2 = projected_polygon.area

    return area

