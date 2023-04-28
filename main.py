import streamlit as st
from energy_factors.sun_radiation import get_sun_radiation

def run_app():
    st.write("Please provide the location of your house:")

    # TODO: handle long and lat cases outside of germany, which would cause python crash
    longitude = st.number_input("Longitude", format="%.7f")
    latitude = st.number_input("Latitude", format="%.7f")

    if st.button('Calculate'):
        radiance = get_sun_radiation(latitude, longitude)
        st.write("Your house's total potential energy harvested per year (in kWh/m^2), if you were to install solar panels: ", radiance)

if __name__ == '__main__':
    run_app()
