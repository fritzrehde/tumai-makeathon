import numpy as np
from pyproj import Transformer
import math

# Calculate Sun Radiation for a given coordinate as annual sum of global radiation (kWh/m^2)
# DWD (Deutscher wetterdienst) Climate dataset

# TODO: maybe add year parameter, as dataset contains yearly data

def get_sun_radiation(latitude, longitude):
    # Define coordinate systems
    from_crs = "EPSG:4326"  # WGS 84
    to_crs = "EPSG:31467"  # Gauss Krüger Zone 3

    # Create transformer object
    transformer = Transformer.from_crs(from_crs, to_crs)

    # Convert latitude and longitude to Gauss Krüger coordinates
    h, r = transformer.transform(latitude, longitude)

    # Information extracted from the dataset header
    XLLCORNER = 3280500
    YLLCORNER = 5237500
    NROWS = 866
    CELLSIZE = 1000
    NODATA_VALUE = -999

    # Load data as 2d array
    data = np.loadtxt("data/radiation/grids_germany_annual_radiation_global_2022.asc", skiprows=28)
    data[data == -999] = np.nan

    y, x = np.floor((r - XLLCORNER) / CELLSIZE), NROWS - np.ceil((h - YLLCORNER) / CELLSIZE)
    print(y)
    print(x)
    radiance = data[np.int(x), np.int(y)]

    return radiance
