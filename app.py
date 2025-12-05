import os
import streamlit as st
from dotenv import load_dotenv
from weather import get_current_weather

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Weather App", page_icon="☁️", layout="centered")
st.title("Simple Weather App ☁️")

st.markdown("Enter a city name and click 'Get weather' to fetch current conditions from OpenWeatherMap.")


@st.cache_data(ttl=600)
def fetch_weather(city, api_key, units):
    return get_current_weather(city, api_key, units=units)


with st.sidebar.expander("API Key (optional)"):
    st.write("Provide an OpenWeatherMap API key here to avoid creating a `.env` file. You can also use the `setup_env.ps1` or `write_env.py` helpers in the repo.")
    key_input = st.text_input("Paste OPENWEATHER_API_KEY (hidden)", type="password", value="" )
    if key_input:
        if st.button("Save key to .env"):
            try:
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f'OPENWEATHER_API_KEY={key_input}')
                st.success('.env written. Restarting to pick up new key...')
                st.experimental_rerun()
            except Exception as e:
                st.error(f'Failed to write .env: {e}')


with st.form(key="weather_form"):
    city = st.text_input("City", value="New York")
    units = st.selectbox("Units", options=["metric", "imperial"], index=0)
    submit = st.form_submit_button("Get weather")

if not API_KEY:
    st.warning("No `OPENWEATHER_API_KEY` found. Use the sidebar to paste a key, create a `.env`, or see README.")

if submit:
    if not city:
        st.error("Please enter a city name.")
    else:
        key = os.getenv("OPENWEATHER_API_KEY") or key_input
        if not key:
            st.error("Cannot fetch weather because `OPENWEATHER_API_KEY` is not set.")
        else:
            with st.spinner("Fetching weather..."):
                res = fetch_weather(city, key, units)

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
                    unit_label = 'C' if units == 'metric' else 'F'
                    st.metric(label="Temperature", value=f"{temp} °{unit_label}")

                with col2:
                    st.write(f"**Condition:** {data.get('description','-').title()}")
                    st.write(f"**Feels like:** {data.get('feels_like','-')}°{unit_label}")
                    st.write(f"**Humidity:** {data.get('humidity','-')}%")
                    st.write(f"**Wind:** {data.get('wind_speed','-')} {'m/s' if units=='metric' else 'mph'}")

                with st.expander("Raw API response (debug)"):
                    st.json(data.get('raw', {}))

                st.markdown("---")
                st.write("Data provided by OpenWeatherMap (free API). See README for setup and tips.")
