import streamlit as st
from geopy.geocoders import Nominatim
from energy_factors.sun_radiation import get_sun_radiation
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap

# For area production heatmap
df_reduced = pd.read_csv('visualize/reduced_data.csv')
heat_df = df_reduced.loc[:,["mean_latitude","mean_longitude","mean_power"]]

# Set up the Streamlit app
st.title("Solar Opposites")

with st.sidebar:
    st.title("Userstuff")
    # Get user input
    buff, col, buff2 = st.columns([1, 3, 1])
    street_num = col.text_input("Enter your address")
    zip_code = col.text_input("Enter your zip code")

    # Create a button to trigger the execution of the code
    button = col.button("Calculate yearly energy saving")

    if button:
        # Combine street number and zip code to form the complete address
        address = f"{street_num}, Germany, {zip_code}"

        # Initialize the geolocator
        geolocator = Nominatim(user_agent="my-app")

        # Use the geolocator to get the latitude and longitude of the address
        if address:
            location = geolocator.geocode(address)
            if location:
                latitude, longitude = location.latitude, location.longitude

                # Check if location is in Germany
                if not(47.3 <= latitude <= 55.1 and 5.9 <= longitude <= 15.2):
                    st.write("Address is outside of Germany")
                    st.stop()

                # Calculate potential energy harvested per year
                potential_energy = get_sun_radiation(latitude, longitude) # Use correct function!!

                # Columns for layout purpose
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.metric(label="Potential Energy saving", value=str(potential_energy) + str(' kWh'),
                              delta=str('Money saved: ') + str(0.510 * potential_energy) + str(" €/a"))

                # Create a DataFrame with the latitude and longitude information
                data = pd.DataFrame({"LATITUDE": [latitude], "LONGITUDE": [longitude]})

                # Display map with marker on address
                col1, col2, col3 = st.columns([1, 5, 1])
                with col2:
                    st.map(data)
                    st.write("Latitude:", latitude)
                    st.write("Longitude:", longitude)
                    st.write("Your house's total potential energy harvested per year (in kWh/m^2), if you were to install solar panels:", potential_energy)
                    st.write('Money saving assumes 0.510€/kWh.')
            else:
                st.write("Address not found")

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

with tab1:
    tab1.subheader("A tab with a chart")
    map_hooray = folium.Map(location=[51, 10], zoom_start=6.05)
    heat_data = heat_df.values.tolist()
    HeatMap(heat_data, radius=13).add_to(map_hooray)
    folium_static(map_hooray)
    st.caption('Map displaying the potential of solar cells for energy production.')
    st.text("Solar cells are crucial for reducing Germany's carbon footprint \n and combating climate change."
            " Germany is one of the world's leading industrial nations and heavily relies \n"
            "on fossil fuels for energy production. The expansion of solar energy in Germany \n"
            "has already made significant progress, but there is still a need for further expansion.\n"
            "Efficient distribution of solar cells is essential to achieving widespread adoption of solar energy\n"
            "in the country.\n"
            "This will help to reduce greenhouse gas emissions, \n"
            "thereby contributing to a \n cleaner and more sustainable future.\n")

tab2.subheader("A tab with the data")

