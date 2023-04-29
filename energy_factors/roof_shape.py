from pyrosm import OSM
import pandas as pd
import pyproj
import shapely
import shapely.wkt

from shapely.ops import transform

def get_roofshape(dict_):
    if isinstance(dict_, dict):
        shape = dict_.get('roof:shape')
        return shape
    else:
        return None
