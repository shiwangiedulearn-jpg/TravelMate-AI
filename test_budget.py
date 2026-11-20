from budget_tools import estimate_budget

result = estimate_budget.invoke({
    "flight_cost": 4000,
    "hotel_per_night": 3000,
    "nights": 3,
    "daily_expenses": 1500,
    "days": 3
})

print(result)