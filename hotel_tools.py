
import json
from langchain.tools import tool


@tool
def search_hotels(city: str, max_price: float, min_stars: int):
    """
    Search hotels in a city using maximum price per night
    and minimum star rating. Results are sorted by price.
    """

    if not city.strip():
        return {"error": "City is required."}

    if max_price <= 0:
        return {"error": "Maximum price must be greater than zero."}

    if not 1 <= min_stars <= 5:
        return {"error": "Minimum stars must be between 1 and 5."}

    try:
        with open("data/hotels.json", "r", encoding="utf-8") as file:
            hotels = json.load(file)

        results = [
            hotel for hotel in hotels
            if hotel["city"].lower() == city.strip().lower()
            and hotel["price_per_night"] <= max_price
            and hotel["stars"] >= min_stars
        ]

        if not results:
            return {"message": "No hotels found matching your requirements."}

        results.sort(key=lambda x: (x["price_per_night"], -x["stars"]))

        return {"hotels": results}

    except FileNotFoundError:
        return {"error": "Hotel dataset not found."}

    except (KeyError, ValueError, TypeError) as e:
        return {"error": f"Invalid hotel data: {str(e)}"}
