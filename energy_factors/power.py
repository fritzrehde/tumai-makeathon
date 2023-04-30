# get yearly power
from .sun_radiation import get_sun_radiation

CONVERSION_EFFICIENCY = 0.2
ROOF_RATIO = 0.5

def get_power(irradiance, area):
    return irradiance * area * CONVERSION_EFFICIENCY * ROOF_RATIO
