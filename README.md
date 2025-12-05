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

### Secure `.env` helpers

You can create a `.env` file securely from the project root without putting the key into shell history.

- PowerShell helper (Windows):

```powershell
.\setup_env.ps1
```

- Python helper (cross-platform):

```powershell
# or on Unix/macOS use `python3`
python write_env.py
```

Both scripts prompt for the `OPENWEATHER_API_KEY` (input is hidden) and write a `.env` file. The repository's `.gitignore` already ignores `.env`, so the key won't be accidentally committed.

## Notes and next steps
- The app uses the free Current Weather API from OpenWeatherMap.
- You can extend the app to show forecasts, search history, or use geolocation.

## Quick verification
After creating a `.env` (or exporting the API key into your shell), you can run a quick smoke test to verify the key and the helper:

```powershell
python test_api.py
```

If the script prints the weather for `London`, your key is valid and the app should work.

## Files
- `app.py` — Streamlit frontend
- `weather.py` — helper to call OpenWeatherMap
- `requirements.txt` — Python deps
- `.env.example` — example environment file

Enjoy! 🌤️
