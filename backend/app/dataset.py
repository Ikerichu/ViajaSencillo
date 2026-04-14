from typing import List, Dict

PLACES = [
    {
        "name": "Museo del Prado",
        "destination": "Madrid",
        "categories": ["cultura", "museo"],
        "popularity": 95,
        "price": 20,
        "coordinates": [40.4138, -3.6922],
    },
    {
        "name": "Parque del Retiro",
        "destination": "Madrid",
        "categories": ["naturaleza", "paseo"],
        "popularity": 88,
        "price": 0,
        "coordinates": [40.4153, -3.6844],
    },
    {
        "name": "Mercado de San Miguel",
        "destination": "Madrid",
        "categories": ["comida", "gastronomia"],
        "popularity": 90,
        "price": 30,
        "coordinates": [40.4153, -3.7081],
    },
    {
        "name": "Barrio de Malasaña",
        "destination": "Madrid",
        "categories": ["fiesta", "cultura"],
        "popularity": 82,
        "price": 15,
        "coordinates": [40.4240, -3.7074],
    },
    {
        "name": "Sagrada Familia",
        "destination": "Barcelona",
        "categories": ["cultura", "arquitectura"],
        "popularity": 98,
        "price": 30,
        "coordinates": [41.4036, 2.1744],
    },
    {
        "name": "Parc Güell",
        "destination": "Barcelona",
        "categories": ["naturaleza", "cultura"],
        "popularity": 92,
        "price": 12,
        "coordinates": [41.4145, 2.1527],
    },
    {
        "name": "La Boqueria",
        "destination": "Barcelona",
        "categories": ["comida", "gastronomia"],
        "popularity": 89,
        "price": 25,
        "coordinates": [41.3829, 2.1714],
    },
    {
        "name": "Las Ramblas",
        "destination": "Barcelona",
        "categories": ["cultura", "paseo"],
        "popularity": 85,
        "price": 0,
        "coordinates": [41.3809, 2.1734],
    },
]

DESTINATIONS = sorted({place["destination"] for place in PLACES})

def get_places(destination: str, interests: List[str] = None) -> List[Dict]:
    filtered = [place for place in PLACES if place["destination"].lower() == destination.lower()]
    if not interests:
        return filtered
    interests_lower = {interest.lower() for interest in interests}
    scored = []
    for place in filtered:
        match_score = len(interests_lower.intersection(set(place["categories"])))
        scored.append((match_score, place["popularity"], place))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [item[2] for item in scored]
