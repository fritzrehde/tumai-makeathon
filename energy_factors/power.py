# get yearly power
from .sun_radiation import get_sun_radiation

def get_power(irradiance, area):
    return irradiance * area
