
import json
from langchain.tools import tool


@tool
def search_places(city: str, place_type: str, min_rating: float):
    """
    Search attractions in a city by category and minimum rating.
    Use 'all' as place_type to search every category.
    Results are sorted by rating, highest first.
    """

    if not city.strip() or not place_type.strip():
        return {"error": "City and place type are required."}

    if not 0 <= min_rating <= 5:
        return {"error": "Minimum rating must be between 0 and 5."}

    try:
        with open("data/places.json", "r", encoding="utf-8") as file:
            places = json.load(file)

        results = [
            place for place in places
            if place["city"].lower() == city.strip().lower()
            and (
                place_type.strip().lower() == "all"
                or place["type"].lower() == place_type.strip().lower()
            )
            and place["rating"] >= min_rating
        ]

        if not results:
            return {"message": "No places found matching your requirements."}

        results.sort(key=lambda x: x["rating"], reverse=True)

        return {"places": results}

    except FileNotFoundError:
        return {"error": "Places dataset not found."}

    except (KeyError, ValueError, TypeError) as e:
        return {"error": f"Invalid places data: {str(e)}"}
