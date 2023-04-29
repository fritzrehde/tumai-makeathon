# get yearly power
from .sun_radiation import get_sun_radiation


def get_power_basic(latitude, longitude, area):
    irradiance = get_sun_radiation(latitude, longitude)
    power = area * irradiance
    return power


def get_power(latitude, longitude, area):
    power = get_power_basic(latitude, longitude, area)
    return power
