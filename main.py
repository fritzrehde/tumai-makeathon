import streamlit as st
import streamlit_leaflet as stl
from energy_factors.sun_radiation import get_sun_radiation


stl.css()
stl.js()

st.header("Select a location on the map")

# Set initial map center and zoom level
initial_location = [52.5200, 13.4050]
zoom_level = 10

# Display the map
map_data = stl.Map(center=initial_location, zoom=zoom_level)

# Create empty element to display selected location
location_elem = st.empty()

# Get the user-selected location
if map_data:
    location = map_data["click"]
    location_elem.success(f"Selected location: {location}")
    longitude, latitude = location_elem.json["click"]

    # Check if location is within Germany
    if not (5.87 <= longitude <= 15.04 and 47.28 <= latitude <= 55.06):
        st.error("The selected location is outside of Germany. Please select a location within Germany.")
    else:
        st.write("Please provide the location of your house:")
        if st.button('Calculate'):
            radiance = get_sun_radiation(latitude, longitude)
            st.write("Your house's total potential energy harvested per year (in kWh/m^2), if you were to install solar panels: ", radiance)

