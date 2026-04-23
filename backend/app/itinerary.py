from datetime import timedelta
from typing import List

from .dataset import get_places
from .attractions import get_attractions_by_interests, format_attraction_for_itinerary, estimate_attraction_cost
from .schemas import PlannerRequest, ItineraryDay

PRICE_OVERRIDES = {
    "cultural": 20,
    "naturaleza": 10,
    "comida": 25,
    "fiesta": 15,
}

CATEGORY_TO_ACTIVITIES = {
    "cultura": "visita cultural",
    "naturaleza": "excursión natural",
    "comida": "experiencia gastronómica",
    "fiesta": "vida nocturna",
}


def estimate_activity_cost(place: dict) -> float:
    base = place.get("price", 0)
    return float(base + 5)


async def make_itinerary_with_real_attractions(request: PlannerRequest) -> List[ItineraryDay]:
    """
    Generate itinerary using real attractions from Open Trip Map API.
    Falls back to dataset if API fails.
    """
    days = (request.end_date - request.start_date).days + 1
    if days < 1:
        days = 1

    # Try to get real attractions from API
    try:
        attractions = await get_attractions_by_interests(request.destination, request.interests, limit=days * 4)
        
        if attractions:
            itinerary = []
            attraction_index = 0
            
            for day_number in range(1, days + 1):
                activities = []
                estimated_cost = 0.0
                slots = 3
                
                for _ in range(slots):
                    if attraction_index >= len(attractions):
                        attraction_index = 0
                    
                    attraction = attractions[attraction_index]
                    activities.append(format_attraction_for_itinerary(attraction))
                    estimated_cost += estimate_attraction_cost(attraction)
                    attraction_index += 1
                
                itinerary.append(ItineraryDay(day=day_number, activities=activities, estimated_cost=round(estimated_cost, 2)))
            
            return itinerary
    except Exception as e:
        print(f"Error generating itinerary with attractions API: {e}")
        # Fall back to dataset-based itinerary
    
    # Fallback to dataset-based itinerary
    return make_itinerary(request)


def make_itinerary(request: PlannerRequest) -> List[ItineraryDay]:
    """Fallback: Generate itinerary using local dataset."""
    days = (request.end_date - request.start_date).days + 1
    if days < 1:
        days = 1

    places = get_places(request.destination, request.interests)
    if not places:
        return [ItineraryDay(day=1, activities=["Explora la ciudad por tu cuenta"], estimated_cost=0.0)]

    itinerary = []
    place_index = 0
    for day_number in range(1, days + 1):
        activities = []
        estimated_cost = 0.0
        slots = 3
        for _ in range(slots):
            if place_index >= len(places):
                place_index = 0
            place = places[place_index]
            activities.append(place["name"])
            estimated_cost += estimate_activity_cost(place)
            place_index += 1
        itinerary.append(ItineraryDay(day=day_number, activities=activities, estimated_cost=round(estimated_cost, 2)))

    return itinerary
