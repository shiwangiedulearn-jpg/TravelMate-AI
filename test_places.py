from places_tools import search_places

result = search_places.invoke({
    "city": "Goa",
    "place_type": "museum",
    "min_rating": 4.0
})

print(result)