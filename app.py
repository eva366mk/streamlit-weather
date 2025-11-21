import os
import streamlit as st
from dotenv import load_dotenv
from weather import get_current_weather

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Weather App", page_icon="☁️", layout="centered")
st.title("Simple Weather App ☁️")

st.markdown("Enter a city name and click 'Get weather' to fetch current conditions from OpenWeatherMap.")

with st.form(key="weather_form"):
    city = st.text_input("City", value="New York")
    units = st.selectbox("Units", options=["metric", "imperial"], index=0)
    submit = st.form_submit_button("Get weather")

if not API_KEY:
    st.warning("No `OPENWEATHER_API_KEY` found. Set it in your environment or in a `.env` file. See README.")

if submit:
    if not city:
        st.error("Please enter a city name.")
    else:
        if not API_KEY:
            st.error("Cannot fetch weather because `OPENWEATHER_API_KEY` is not set.")
        else:
            with st.spinner("Fetching weather..."):
                res = get_current_weather(city, API_KEY, units=units)

            if res.get("error"):
                st.error(res["error"])
            else:
                data = res["data"]
                # Header
                st.subheader(f"{data['name']}, {data.get('country','')}")

                col1, col2 = st.columns([1, 2])
                with col1:
                    icon_url = data.get("icon_url")
                    if icon_url:
                        st.image(icon_url, width=100)
                    temp = data.get("temp")
                    st.metric(label="Temperature", value=f"{temp} °{ 'C' if units=='metric' else 'F'}")

                with col2:
                    st.write(f"**Condition:** {data.get('description','-').title()}")
                    st.write(f"**Feels like:** {data.get('feels_like','-')}°")
                    st.write(f"**Humidity:** {data.get('humidity','-')}%")
                    st.write(f"**Wind:** {data.get('wind_speed','-')} {'m/s' if units=='metric' else 'mph'}")

                st.markdown("---")
                st.write("Data provided by OpenWeatherMap (free API). See README for setup and tips.")
