
import requests
from datetime import date, timedelta
from langchain.tools import tool


CITY_COORDINATES = {
    "goa": (15.2993, 74.1240),
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2706),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
    "jaipur": (26.9124, 75.7873)
}


def get_weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    return descriptions.get(code, "Unknown weather")


def get_weather(city, travel_date, days):

    city_name = city.strip().lower()

    if city_name not in CITY_COORDINATES:
        return {"error": f"Weather unavailable for {city}."}

    try:
        start_date = date.fromisoformat(travel_date)
    except ValueError:
        return {"error": "Date must be in YYYY-MM-DD format."}

    if not 1 <= days <= 7:
        return {"error": "Forecast duration must be between 1 and 7 days."}

    end_date = start_date + timedelta(days=days - 1)

    today = date.today()

    if start_date < today:
        return {"error": "Weather forecasts are unavailable for past dates."}

    if start_date > today + timedelta(days=15):
        return {
            "error": "Weather forecasts are available only up to 15 days ahead."
        }

    latitude, longitude = CITY_COORDINATES[city_name]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code"
        ],
        "timezone": "auto",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        weather_data = response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"Weather API request failed: {str(e)}"}

    daily_data = weather_data.get("daily", {})

    dates = daily_data.get("time", [])
    max_temps = daily_data.get("temperature_2m_max", [])
    min_temps = daily_data.get("temperature_2m_min", [])
    codes = daily_data.get("weather_code", [])

    results = []

    for i in range(len(dates)):
        results.append({
            "date": dates[i],
            "max_temperature": max_temps[i],
            "min_temperature": min_temps[i],
            "weather": get_weather_description(codes[i])
        })

    return results


@tool
def weather_tool(city: str, travel_date: str, days: int):
    """
    Get weather forecast for a destination on the requested
    travel date and number of days.
    Date format must be YYYY-MM-DD.
    """

    if not city.strip():
        return {"error": "City is required."}

    return get_weather(city, travel_date, days)
