import streamlit as st
from geopy.geocoders import Nominatim
from energy_factors.sun_radiation import get_sun_radiation
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import requests

# For area production heatmap
df_reduced = pd.read_csv('visualize/reduced_data.csv')
heat_df = df_reduced.loc[:,["mean_latitude","mean_longitude","mean_power"]]

# Set up the Streamlit app
st.title("Solar Opposites")

with st.sidebar:
    st.title("Userstuff")
    # Get user input
    buff, col, buff2 = st.columns([1, 3, 1])

    col.write("Enter your address:")
    street = col.text_input("Street name")
    housenumber = col.text_input("House number")
    postcode = col.text_input("Postal code")

    # Create a button to trigger the execution of the code
    button = col.button("Calculate yearly energy saving")

    if button:
        url = 'http://localhost:5000/data'
        params = {
            'street': street,
            'housenumber': housenumber,
            'postcode': postcode
        }

        response = requests.get(url, params=params)

        if not response.ok:
            print(f'Request failed with status code {response.status_code}')
            st.write("Address not found")
        else:
            data = response.json()

            # Calculate potential energy harvested per year
            potential_energy = data['irradiance']
            latitude = data['roof_location_latitude']
            longitude = data['roof_location_longitude']

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

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

with tab1:
    tab1.subheader("A tab with a chart")
    map_hooray = folium.Map(location=[51, 10], zoom_start=6.05)
    heat_data = heat_df.values.tolist()
    HeatMap(heat_data, radius=13).add_to(map_hooray)
    folium_static(map_hooray)
    st.caption('Map displaying the potential of solar cells for energy production.')
    st.write("Solar cells are crucial for reducing Germany's carbon footprint and combating climate change. "
            " Germany is one of the world's leading industrial nations and heavily relies "
            "on fossil fuels for energy production. The expansion of solar energy in Germany "
            "has already made significant progress, but there is still a need for further expansion. "
            "Efficient distribution of solar cells is essential to achieving widespread adoption of solar energy "
            "in the country.\n"
            "This will help to reduce greenhouse gas emissions, "
            "thereby contributing to a cleaner and more sustainable future.")

tab2.subheader("A tab with the data")

