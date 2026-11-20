from flight_tools import search_flights

result = search_flights.invoke({
    "source": "Bangalore",
    "destination": "Delhi",
    "sort_by": "price"
})

print(result)