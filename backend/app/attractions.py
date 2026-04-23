import httpx
from typing import Optional, List, Dict, Any

OPENTRIPMAP_BASE_URL = "https://api.opentripmap.com/0.3"


async def get_city_coordinates(city_name: str) -> Optional[Dict[str, Any]]:
    """
    Get coordinates for a city using Open Trip Map API.
    
    Args:
        city_name: Name of the city
    
    Returns:
        Dictionary with latitude, longitude and city info, or None if not found
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPENTRIPMAP_BASE_URL}/geonames/search",
                params={
                    "name": city_name,
                    "format": "json"
                },
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                result = data[0]
                return {
                    "latitude": result.get("lat"),
                    "longitude": result.get("lon"),
                    "name": result.get("name"),
                    "country": result.get("country"),
                }
            return None
    except Exception as e:
        print(f"Error getting city coordinates: {e}")
        return None


async def get_attractions(
    latitude: float, 
    longitude: float, 
    radius: int = 5000,
    limit: int = 50,
    kinds: str = "interesting_places,restaurants,museums,natural"
) -> List[Dict[str, Any]]:
    """
    Get attractions around coordinates using Open Trip Map API.
    
    Args:
        latitude: Latitude of center point
        longitude: Longitude of center point
        radius: Search radius in meters (default 5000m)
        limit: Maximum number of results
        kinds: Comma-separated types of attractions
    
    Returns:
        List of attractions with name, type, and GPS coordinates
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPENTRIPMAP_BASE_URL}/places/radius",
                params={
                    "lon": longitude,
                    "lat": latitude,
                    "radius": radius,
                    "limit": limit,
                    "kinds": kinds,
                    "format": "json"
                },
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            
            attractions = []
            if data.get("features"):
                for feature in data["features"][:limit]:
                    props = feature.get("properties", {})
                    geometry = feature.get("geometry", {})
                    
                    attractions.append({
                        "xid": props.get("xid"),
                        "name": props.get("name", "Unknown"),
                        "kinds": props.get("kinds", ""),
                        "latitude": geometry.get("coordinates", [0, 0])[1] if geometry else 0,
                        "longitude": geometry.get("coordinates", [0, 0])[0] if geometry else 0,
                        "distance": props.get("distance", 0),
                    })
            
            return attractions
    except Exception as e:
        print(f"Error getting attractions: {e}")
        return []


async def get_attractions_by_interests(
    city_name: str,
    interests: List[str],
    limit: int = 30
) -> List[Dict[str, Any]]:
    """
    Get attractions for a city filtered by interests.
    
    Args:
        city_name: Name of the city
        interests: List of interests/keywords
        limit: Maximum number of attractions
    
    Returns:
        List of attractions matching interests
    """
    # Map interests to Open Trip Map kinds
    interest_mapping = {
        "cultura": "museums,interesting_places",
        "naturaleza": "natural,parks",
        "comida": "restaurants",
        "fiesta": "restaurants,bars",
        "arte": "museums,interesting_places",
        "compras": "shops",
        "aventura": "natural,parks",
    }
    
    # Get city coordinates
    city_info = await get_city_coordinates(city_name)
    if not city_info:
        return []
    
    # Build kinds parameter from interests
    kinds_set = set()
    for interest in interests:
        interest_lower = interest.lower()
        if interest_lower in interest_mapping:
            kinds = interest_mapping[interest_lower].split(",")
            kinds_set.update(kinds)
    
    kinds = ",".join(kinds_set) if kinds_set else "interesting_places,museums,restaurants,natural"
    
    # Get attractions
    attractions = await get_attractions(
        city_info["latitude"],
        city_info["longitude"],
        radius=10000,
        limit=limit,
        kinds=kinds
    )
    
    return attractions


def format_attraction_for_itinerary(attraction: Dict[str, Any]) -> str:
    """
    Format an attraction for display in itinerary.
    
    Args:
        attraction: Attraction dictionary from API
    
    Returns:
        Formatted string with attraction name and type
    """
    kinds = attraction.get("kinds", "").split(",")
    kind_display = kinds[0].replace("_", " ").title() if kinds else "Lugar de interés"
    return f"{attraction['name']} ({kind_display})"


def estimate_attraction_cost(attraction: Dict[str, Any], kind: str = "") -> float:
    """
    Estimate cost of an attraction based on its type.
    
    Args:
        attraction: Attraction dictionary
        kind: Type of attraction
    
    Returns:
        Estimated cost in euros
    """
    kinds = attraction.get("kinds", "").lower()
    
    cost_mapping = {
        "museums": 12.0,
        "natural": 5.0,
        "parks": 0.0,
        "restaurants": 20.0,
        "bars": 15.0,
        "shops": 0.0,
        "interesting_places": 5.0,
    }
    
    for category, cost in cost_mapping.items():
        if category in kinds:
            return cost
    
    return 5.0  # Default cost
