import httpx
from typing import Optional, Dict, Any

WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"


async def get_coordinates(city: str) -> Optional[Dict[str, Any]]:
    """
    Get coordinates for a city using Open-Meteo geocoding API.
    
    Args:
        city: City name
    
    Returns:
        Dictionary with latitude, longitude and city info, or None if not found
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GEOCODING_API_URL,
                params={
                    "name": city,
                    "count": 1,
                    "language": "es",
                    "format": "json"
                },
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                return {
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "name": result.get("name"),
                    "country": result.get("country"),
                }
            return None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None


async def get_weather(latitude: float, longitude: float, days: int = 7) -> Optional[Dict[str, Any]]:
    """
    Get weather forecast for coordinates using Open-Meteo API.
    
    Args:
        latitude: Latitude of location
        longitude: Longitude of location
        days: Number of days for forecast
    
    Returns:
        Dictionary with weather information or None if request fails
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                WEATHER_API_BASE_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation,weather_code",
                    "temperature_unit": "celsius",
                    "timezone": "auto",
                    "forecast_days": min(days, 16)  # Open-Meteo free tier supports up to 16 days
                },
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "timezone": data.get("timezone"),
                "daily": data.get("daily", {}),
            }
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None


async def get_destination_weather(city: str, days: int = 7) -> Optional[Dict[str, Any]]:
    """
    Get complete weather information for a destination.
    
    Args:
        city: City name
        days: Number of days for forecast
    
    Returns:
        Dictionary with location and weather info, or None if request fails
    """
    # Get coordinates
    location = await get_coordinates(city)
    if not location:
        return None
    
    # Get weather
    weather = await get_weather(location["latitude"], location["longitude"], days)
    if not weather:
        return None
    
    return {
        "location": {
            "name": location["name"],
            "country": location["country"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "weather": weather,
    }
