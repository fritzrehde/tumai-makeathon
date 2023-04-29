import pyproj
import shapely
import shapely.wkt

def get_rooflocation_latitude(polygon):
    # input polygon is passed directly in the WKT format

    # Get the centroid of the polygon
    centroid = polygon.centroid
    
    # Assign the longitude and latitude to the corresponding columns in the DataFrame
    latitude = centroid.y

    return latitude

def get_rooflocation_longitude(polygon):
    # input polygon is passed directly in the WKT format

    # Get the centroid of the polygon
    centroid = polygon.centroid
    
    # Assign the longitude and latitude to the corresponding columns in the DataFrame
    longitude = centroid.x

    return longitude
