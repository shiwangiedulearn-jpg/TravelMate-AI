
from langchain.tools import tool


@tool
def estimate_budget(
    flight_cost: float,
    hotel_per_night: float,
    nights: int,
    daily_expenses: float,
    days: int,
    travelers: int = 1
):
    """
    Estimate total trip expenses including flights,
    hotel accommodation and daily expenses.
    """

    if min(flight_cost, hotel_per_night, daily_expenses) < 0:
        return {"error": "Expenses cannot be negative."}

    if nights < 0 or days <= 0 or travelers <= 0:
        return {
            "error": "Nights cannot be negative; days and travelers must be positive."
        }

    hotel_total = hotel_per_night * nights
    daily_total = daily_expenses * days * travelers

    # Flight cost is assumed to be the total cost for all travelers
    total = flight_cost + hotel_total + daily_total

    return {
        "flight_cost": flight_cost,
        "hotel_cost": hotel_total,
        "daily_expenses": daily_total,
        "total_budget": total
    }
