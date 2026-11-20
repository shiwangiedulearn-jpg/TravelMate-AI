
from tools import tools

tool_map = {tool.name: tool for tool in tools}


def generate_fallback_plan(
    source,
    destination,
    days,
    budget,
    travelers,
    preferences,
    travel_date
):
    """Generate a travel plan without requiring an LLM."""

    print("Generating travel plan...")

    if days <= 0 or travelers <= 0 or budget <= 0:
        return {"error": "Days, travelers and budget must be positive."}

    nights = max(days - 1, 1)

    # 1. Search flights
    flight_results = tool_map["search_flights"].invoke({
        "source": source,
        "destination": destination,
        "travel_date": travel_date,
        "sort_by": "price"
    })

    flights = flight_results.get("flights", [])
    selected_flight = flights[0] if flights else None

    # 2. Search hotels
    hotel_budget_per_night = (budget * 0.40) / nights

    hotel_results = tool_map["search_hotels"].invoke({
        "city": destination,
        "max_price": hotel_budget_per_night,
        "min_stars": 3
    })

    hotels = hotel_results.get("hotels", [])
    selected_hotel = hotels[0] if hotels else None

    # 3. Search attractions
    place_results = tool_map["search_places"].invoke({
        "city": destination,
        "place_type": "all",
        "min_rating": 3.5
    })

    places = place_results.get("places", [])

    # Remove duplicate attractions
    unique_places = []
    seen_places = set()

    for place in places:
        place_name = place["name"].lower()

        if place_name not in seen_places:
            unique_places.append(place)
            seen_places.add(place_name)

    places = unique_places

    # 4. Filter attractions based on preferences
    preference = preferences.lower()

    if "historical" in preference or "history" in preference:
        keywords = ["fort", "museum", "palace", "monument"]

        preferred_places = [
            place for place in places
            if any(word in place["name"].lower() for word in keywords)
        ]
    else:
        preferred_places = places

    # 5. Get weather for travel dates
    weather_results = tool_map["weather_tool"].invoke({
        "city": destination,
        "travel_date": travel_date,
        "days": days
    })

    # 6. Generate day-wise itinerary
    itinerary = []

    for day in range(1, days + 1):

        day_places = preferred_places[day - 1::days]

        day_weather = None

        if isinstance(weather_results, list) and day - 1 < len(weather_results):
            day_weather = weather_results[day - 1]

        itinerary.append({
            "day": day,
            "activities": [
                place["name"] for place in day_places
            ],
            "weather": day_weather
        })

    # 7. Calculate budget
    flight_cost = (
        selected_flight["price"] * travelers
        if selected_flight else 0
    )

    hotel_cost_per_night = (
        selected_hotel["price_per_night"]
        if selected_hotel else 0
    )

    daily_expenses = 1000

    budget_results = tool_map["estimate_budget"].invoke({
        "flight_cost": flight_cost,
        "hotel_per_night": hotel_cost_per_night,
        "nights": nights,
        "daily_expenses": daily_expenses,
        "days": days,
        "travelers": travelers
    })

    total_cost = budget_results.get("total_budget", 0)

    # 8. Check whether the estimate is complete
    missing_costs = []

    if selected_flight is None:
        missing_costs.append("Flight cost unavailable")

    if selected_hotel is None:
        missing_costs.append("Hotel cost unavailable")

    estimate_complete = len(missing_costs) == 0

    if not estimate_complete:
        budget_status = "Incomplete estimate"
    elif total_cost <= budget:
        budget_status = "Within budget"
    else:
        budget_status = "Exceeds budget"

    # 9. Return complete travel plan
    return {
        "source": source,
        "destination": destination,
        "travel_date": travel_date,
        "days": days,
        "nights": nights,
        "travelers": travelers,
        "preferences": preferences,
        "selected_flight": selected_flight,
        "flight_notice": flight_results.get("notice") or flight_results.get("message"),
        "selected_hotel": selected_hotel,
        "places": preferred_places,
        "itinerary": itinerary,
        "weather": weather_results,
        "budget_breakdown": budget_results,
        "user_budget": budget,
        "budget_status": budget_status,
        "estimate_complete": estimate_complete,
        "missing_costs": missing_costs
    }


if __name__ == "__main__":

    result = generate_fallback_plan(
        source="Bangalore",
        destination="Delhi",
        days=3,
        budget=20000,
        travelers=1,
        preferences="Historical places and sightseeing",
        travel_date="2026-11-21"
    )

    print(result)
