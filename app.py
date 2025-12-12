import os
import streamlit as st
from dotenv import load_dotenv
from weather import get_current_weather, get_forecast
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Weather App", page_icon="☁️", layout="wide")
st.title("🌤️ Advanced Weather App")
st.markdown("Real-time weather forecasts, favorites, and search history")

# Initialize session state for favorites and history
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Sidebar: API Key & Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    with st.expander("API Key (optional)"):
        st.write("Provide an OpenWeatherMap API key for real-time data.")
        key_input = st.text_input("Paste OPENWEATHER_API_KEY", type="password", value="")
        if key_input:
            if st.button("Save key to .env"):
                try:
                    with open('.env', 'w', encoding='utf-8') as f:
                        f.write(f'OPENWEATHER_API_KEY={key_input}')
                    st.success('✅ Key saved! Restarting app...')
                    st.rerun()
                except Exception as e:
                    st.error(f'Failed: {e}')
    
    st.markdown("---")
    
    # Favorites
    if st.session_state.favorites:
        st.subheader("❤️ Favorite Cities")
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"📍 {fav}", key=f"fav_{fav}"):
                    st.session_state.selected_city = fav
                    st.rerun()
            with col2:
                if st.button("✕", key=f"del_{fav}", help="Remove"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()
    
    st.markdown("---")
    
    # Search History
    if st.session_state.search_history:
        st.subheader("🕐 Recent Searches")
        for hist in st.session_state.search_history[-5:]:
            if st.button(f"🔍 {hist}", key=f"hist_{hist}"):
                st.session_state.selected_city = hist
                st.rerun()

# Main search form
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    city = st.text_input("Enter city name", value="London", placeholder="e.g., Tokyo, Paris, Sydney")
with col2:
    units = st.selectbox("Units", ["metric", "imperial"], label_visibility="collapsed")
with col3:
    submit = st.button("🔍 Search", use_container_width=True)

if not API_KEY:
    st.info("💡 No API key found. Using demo mode (London, New York, Tokyo). Add a key in Settings for real data.")

# Handle search
if submit and city:
    if city not in st.session_state.search_history:
        st.session_state.search_history.append(city)
    
    key = os.getenv("OPENWEATHER_API_KEY") or key_input if 'key_input' in locals() else os.getenv("OPENWEATHER_API_KEY")
    
    with st.spinner(f"📡 Fetching weather for {city}..."):
        res = get_current_weather(city, key or "demo", units=units)
    
    if res.get("error"):
        st.error(f"❌ {res['error']}")
    else:
        data = res["data"]
        
        # Store for display
        st.session_state.last_weather = data
        st.session_state.last_city = city
        st.session_state.last_units = units

# Display weather if available
if "last_weather" in st.session_state:
    data = st.session_state.last_weather
    city_name = st.session_state.last_city
    units = st.session_state.last_units
    unit_label = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    # Header with favorite button
    header_col1, header_col2, header_col3 = st.columns([3, 1, 1])
    with header_col1:
        st.markdown(f"## {data.get('name', '?')}, {data.get('country', '')}")
    with header_col2:
        if city_name not in st.session_state.favorites:
            if st.button("❤️ Add to Favorites", use_container_width=True):
                st.session_state.favorites.append(city_name)
                st.success("Added to favorites!")
    with header_col3:
        pass
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Current Weather", "📈 5-Day Forecast", "ℹ️ Details"])
    
    with tab1:
        # Current weather main display
        col1, col2, col3 = st.columns([1, 2, 1.5])
        
        with col1:
            if data.get("icon_url"):
                st.image(data["icon_url"], width=120)
            st.metric("Temperature", f"{data.get('temp', '-')}{unit_label}", 
                     delta=f"Feels like {data.get('feels_like', '-')}{unit_label}")
        
        with col2:
            st.metric("Condition", data.get("description", "-").title())
            st.metric("Humidity", f"{data.get('humidity', '-')}%")
            st.metric("Wind Speed", f"{data.get('wind_speed', '-')} {speed_unit}")
        
        with col3:
            st.metric("Pressure", f"{data.get('pressure', '-')} hPa")
            st.metric("Clouds", f"{data.get('clouds', '-')}%")
            if data.get('visibility'):
                vis = data['visibility'] / 1000 if units == 'metric' else data['visibility'] / 1609
                st.metric("Visibility", f"{vis:.1f} {'km' if units == 'metric' else 'mi'}")
        
        # Sunrise/Sunset
        st.markdown("---")
        sunrise_col, sunset_col = st.columns(2)
        with sunrise_col:
            if data.get('sunrise'):
                sunrise_time = datetime.fromtimestamp(data['sunrise']).strftime("%H:%M")
                st.info(f"🌅 Sunrise: {sunrise_time}")
        with sunset_col:
            if data.get('sunset'):
                sunset_time = datetime.fromtimestamp(data['sunset']).strftime("%H:%M")
                st.warning(f"🌆 Sunset: {sunset_time}")
    
    with tab2:
        # 5-day forecast
        st.subheader("5-Day Forecast")
        key = os.getenv("OPENWEATHER_API_KEY") or (key_input if 'key_input' in locals() else None)
        
        with st.spinner("Loading forecast..."):
            forecast_res = get_forecast(city_name, key or "demo", units=units)
        
        if forecast_res.get("error"):
            st.warning(f"⚠️ Forecast unavailable: {forecast_res['error']}")
        else:
            forecast = forecast_res.get("forecast", [])
            if forecast:
                # Display as columns
                cols = st.columns(min(5, len(forecast)))
                for i, day_forecast in enumerate(forecast[:5]):
                    with cols[i % 5]:
                        st.markdown(f"**{day_forecast['date']}**")
                        if day_forecast['icon_url']:
                            st.image(day_forecast['icon_url'], width=80)
                        st.write(f"🌡️ {day_forecast['temp_min']}–{day_forecast['temp_max']}{unit_label}")
                        st.write(f"💧 {day_forecast['humidity']}%")
                        st.write(f"💨 {day_forecast['wind_speed']} {speed_unit}")
                        st.caption(day_forecast['description'].title())
    
    with tab3:
        # Detailed info
        st.subheader("Detailed Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Temperature**")
            st.write(f"Current: {data.get('temp', '-')}{unit_label}")
            st.write(f"Feels Like: {data.get('feels_like', '-')}{unit_label}")
        
        with col2:
            st.write("**Atmospheric Pressure**")
            st.write(f"Pressure: {data.get('pressure', '-')} hPa")
            st.write(f"Humidity: {data.get('humidity', '-')}%")
        
        st.write("**Wind & Visibility**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Wind Speed: {data.get('wind_speed', '-')} {speed_unit}")
        with col2:
            if data.get('visibility'):
                vis = data['visibility'] / 1000 if units == 'metric' else data['visibility'] / 1609
                st.write(f"Visibility: {vis:.1f} {'km' if units == 'metric' else 'mi'}")
        with col3:
            st.write(f"Cloud Coverage: {data.get('clouds', '-')}%")
        
        st.markdown("---")
        with st.expander("📋 Raw API Data"):
            st.json(data.get('raw', {}))

st.markdown("---")
st.caption("Data provided by OpenWeatherMap | 🌍 Global Weather Data")

