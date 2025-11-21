import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"


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
        "icon_url": icon_url,
        "raw": j,
    }

    return {"data": data}
