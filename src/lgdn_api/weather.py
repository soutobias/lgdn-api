import httpx


async def get_weather_data(lon: float, lat: float) -> dict:
    """Get current weather conditions for a given latitude and longitude."""
    try:
        async with httpx.AsyncClient() as client:
            # Open-Meteo API - free weather API
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
            }

            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data.get("current_weather", {})

    except Exception as e:
        return {"error": str(e)}
