# get yearly power
from .sun_radiation import get_sun_radiation


def get_power_basic(irradiance, area):
    power = area * irradiance
    return power


def get_power(latitude, longitude, area):
    irradiance = get_sun_radiation(latitude, longitude)
    power = get_power_basic(irradiance, area)
    return power, irradiance
