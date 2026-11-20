
import json
from datetime import datetime
from langchain.tools import tool


@tool
def search_flights(
    source: str,
    destination: str,
    travel_date: str,
    sort_by: str = "price"
):
    """
    Search sample flights between source and destination.
    Match flights with the requested travel date.
    Dataset records are historical samples, not live availability.
    """

    if not source.strip() or not destination.strip():
        return {"error": "Source and destination are required."}

    if sort_by not in ["price", "duration"]:
        return {"error": "Sort by price or duration."}

    try:
        requested_date = datetime.strptime(
            travel_date, "%Y-%m-%d"
        ).date()

    except ValueError:
        return {"error": "Travel date must be in YYYY-MM-DD format."}

    try:
        with open("data/flights.json", "r", encoding="utf-8") as file:
            flights = json.load(file)

        matching_flights = []

        for flight in flights:

            if (
                flight["from"].lower() == source.strip().lower()
                and flight["to"].lower() == destination.strip().lower()
            ):
                departure = datetime.fromisoformat(
                    flight["departure_time"]
                )

                if departure.date() == requested_date:
                    matching_flights.append(flight)

        if not matching_flights:
            return {
                "message": "No sample flights found for the requested date.",
                "notice": (
                    "The dataset contains historical sample records. "
                    "No live flight availability is provided."
                )
            }

        if sort_by == "price":
            matching_flights.sort(key=lambda x: x["price"])

        else:
            matching_flights.sort(
                key=lambda x: (
                    datetime.fromisoformat(x["arrival_time"])
                    - datetime.fromisoformat(x["departure_time"])
                ).total_seconds()
            )

        return {
            "notice": "Historical sample data; not live flight availability.",
            "travel_date": travel_date,
            "flights": matching_flights
        }

    except FileNotFoundError:
        return {"error": "Flight dataset not found."}

    except (KeyError, ValueError, TypeError) as e:
        return {"error": f"Invalid flight data: {str(e)}"}
