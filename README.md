# Streamlit Weather App

A minimal Streamlit app to fetch current weather for a city using OpenWeatherMap.

## Features
- Enter a city name and fetch current weather
- Choose units (metric or imperial)
- Displays temperature, feels-like, humidity, wind and an icon

## Setup
1. Install dependencies (prefer a virtual environment):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Obtain an API key from OpenWeatherMap: https://openweathermap.org/api

3. Set the API key in your environment or a `.env` file at the project root:

Create a file named `.env` with:

```
OPENWEATHER_API_KEY=your_api_key_here
```

4. Run the app:

```powershell
streamlit run app.py
```

## Notes and next steps
- The app uses the free Current Weather API from OpenWeatherMap.
- You can extend the app to show forecasts, search history, or use geolocation.

## Files
- `app.py` — Streamlit frontend
- `weather.py` — helper to call OpenWeatherMap
- `requirements.txt` — Python deps
- `.env.example` — example environment file

Enjoy! 🌤️
