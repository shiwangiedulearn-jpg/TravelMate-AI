from hotel_tools import search_hotels

result = search_hotels.invoke({
    "city": "Goa",
    "max_price": 4000,
    "min_stars": 4
})

print(result)