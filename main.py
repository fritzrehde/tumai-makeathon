import streamlit as st
from geopy.geocoders import Nominatim
from energy_factors.sun_radiation import get_sun_radiation
import pandas as pd

# Set up the Streamlit app
st.title("Solar Opposites")

# Get user input
street_num = st.text_input("Enter your address")
zip_code = st.text_input("Enter your zip code")

# Combine street number and zip code to form the complete address
address = f"{street_num}, Germany, {zip_code}"

# Initialize the geolocator
geolocator = Nominatim(user_agent="my-app")

# Use the geolocator to get the latitude and longitude of the address
if address:
    location = geolocator.geocode(address)
    if location:
        latitude, longitude = location.latitude, location.longitude
        st.write("Latitude:", latitude)
        st.write("Longitude:", longitude)

        # Check if location is in Germany
        if not(47.3 <= latitude <= 55.1 and 5.9 <= longitude <= 15.2):
            st.write("Address is outside of Germany")
            st.stop()

        # Calculate potential energy harvested per year
        potential_energy = get_sun_radiation(latitude, longitude) # Use correct function!!
        
        # Create a DataFrame with the latitude and longitude information
        data = pd.DataFrame({"LATITUDE": [latitude], "LONGITUDE": [longitude]})

        # Display map with marker on address
        st.map(data)
        
        st.write("Your house's total potential energy harvested per year (in kWh/m^2), if you were to install solar panels:", potential_energy)

    else:
        st.write("Address not found")