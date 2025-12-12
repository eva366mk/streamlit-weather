import requests
from datetime import datetime

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"

# Mock data for demo mode
MOCK_DATA = {
    "london": {
        "name": "London",
        "country": "GB",
        "description": "Partly cloudy",
        "temp": 12,
        "feels_like": 10,
        "humidity": 65,
        "wind_speed": 5.2,
        "pressure": 1013,
        "visibility": 10000,
        "clouds": 50,
        "sunrise": 1702278000,
        "sunset": 1702308000,
        "icon": "02d"
    },
    "new york": {
        "name": "New York",
        "country": "US",
        "description": "Clear sky",
        "temp": 8,
        "feels_like": 5,
        "humidity": 55,
        "wind_speed": 6.1,
        "pressure": 1015,
        "visibility": 10000,
        "clouds": 10,
        "sunrise": 1702274400,
        "sunset": 1702307400,
        "icon": "01d"
    },
    "tokyo": {
        "name": "Tokyo",
        "country": "JP",
        "description": "Rainy",
        "temp": 15,
        "feels_like": 13,
        "humidity": 80,
        "wind_speed": 3.8,
        "pressure": 1010,
        "visibility": 5000,
        "clouds": 90,
        "sunrise": 1702283400,
        "sunset": 1702319400,
        "icon": "10d"
    }
}


def get_current_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch current weather for a city from OpenWeatherMap.

    Returns a dict with either {'data': {...}} or {'error': 'message'}.
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}

    # Handle common API errors with clearer messages
    if r.status_code == 401:
        # Demo mode: return mock data if API key is invalid
        city_lower = city.lower().strip()
        if city_lower in MOCK_DATA:
            mock = MOCK_DATA[city_lower].copy()
            mock["icon_url"] = ICON_URL.format(icon=mock.pop("icon"))
            mock["raw"] = {"cod": "200"}
            return {"data": mock}
        return {"error": "Authentication failed (401). Check your OPENWEATHER_API_KEY. [Demo mode: try London, New York, or Tokyo]"}
    if r.status_code == 404:
        return {"error": "City not found (404). Check the city name and try again."}

    if r.status_code != 200:
        try:
            err = r.json().get("message", r.text)
        except ValueError:
            err = r.text
        return {"error": f"API error ({r.status_code}): {err}"}

    try:
        j = r.json()
    except ValueError:
        return {"error": "Invalid JSON response from API"}

    # Parse useful fields
    weather = j.get("weather", [{}])[0]
    main = j.get("main", {})
    wind = j.get("wind", {})
    sys = j.get("sys", {})
    clouds = j.get("clouds", {})

    icon = weather.get("icon")
    icon_url = ICON_URL.format(icon=icon) if icon else None

    data = {
        "name": j.get("name"),
        "country": sys.get("country"),
        "description": weather.get("description"),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "pressure": main.get("pressure"),
        "visibility": j.get("visibility"),
        "clouds": clouds.get("all"),
        "sunrise": sys.get("sunrise"),
        "sunset": sys.get("sunset"),
        "icon_url": icon_url,
        "raw": j,
    }

    return {"data": data}


def get_forecast(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch 5-day forecast for a city.
    
    Returns a dict with either {'forecast': [...]} or {'error': 'message'}.
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
        "cnt": 40,  # 5 days * 8 (3-hourly)
    }

    try:
        r = requests.get(FORECAST_URL, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}

    if r.status_code == 401:
        return {"error": "Invalid API key"}
    if r.status_code == 404:
        return {"error": "City not found"}
    if r.status_code != 200:
        return {"error": f"API error ({r.status_code})"}

    try:
        j = r.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    forecast_list = j.get("list", [])
    
    # Group by day
    daily_forecasts = {}
    for item in forecast_list:
        dt = datetime.fromtimestamp(item.get("dt", 0))
        day = dt.strftime("%Y-%m-%d")
        
        if day not in daily_forecasts:
            daily_forecasts[day] = {
                "date": day,
                "temps": [],
                "descriptions": [],
                "humidity": [],
                "wind_speed": [],
                "icon": None,
            }
        
        daily_forecasts[day]["temps"].append(item.get("main", {}).get("temp"))
        daily_forecasts[day]["descriptions"].append(item.get("weather", [{}])[0].get("description", ""))
        daily_forecasts[day]["humidity"].append(item.get("main", {}).get("humidity"))
        daily_forecasts[day]["wind_speed"].append(item.get("wind", {}).get("speed"))
        if not daily_forecasts[day]["icon"]:
            daily_forecasts[day]["icon"] = item.get("weather", [{}])[0].get("icon", "")
    
    # Compute averages
    forecast = []
    for day in sorted(daily_forecasts.keys()):
        d = daily_forecasts[day]
        forecast.append({
            "date": day,
            "temp_min": round(min(d["temps"]), 1) if d["temps"] else "-",
            "temp_max": round(max(d["temps"]), 1) if d["temps"] else "-",
            "description": d["descriptions"][0] if d["descriptions"] else "-",
            "humidity": round(sum(d["humidity"]) / len(d["humidity"]), 0) if d["humidity"] else "-",
            "wind_speed": round(sum(d["wind_speed"]) / len(d["wind_speed"]), 1) if d["wind_speed"] else "-",
            "icon_url": ICON_URL.format(icon=d["icon"]) if d["icon"] else None,
        })
    
    return {"forecast": forecast}

