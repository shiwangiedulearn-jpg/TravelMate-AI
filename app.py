
import streamlit as st
from datetime import date, timedelta
import json

from llm_config import llm
from agent.runner import run_travel_agent
from main import generate_fallback_plan


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TravelMate AI",
    page_icon=None,
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main {
    background-color: #f7f9fc;
}

.hero {
    background: linear-gradient(120deg, #102a43, #176b72);
    padding: 38px;
    border-radius: 16px;
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    color: #dce8ec;
    font-size: 16px;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    color: #102a43;
    margin-top: 25px;
    margin-bottom: 15px;
}

.stButton button {
    background-color: #176b72;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 25px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #12545a;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>TravelMate AI</h1>
    <p>
        Your intelligent travel planning assistant.
        Discover destinations, compare stays and create
        personalized travel itineraries.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TRAVEL INPUT FORM
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Plan Your Journey</div>',
    unsafe_allow_html=True
)

destinations = [
    "Goa",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Jaipur"
]

today = date.today()

with st.form("travel_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input(
            "Departure City",
            placeholder="Enter departure city"
        )

    with col2:
        destination = st.selectbox(
            "Destination",
            destinations
        )

    col3, col4 = st.columns(2)

    with col3:
        days = st.slider(
            "Trip Duration (Days)",
            min_value=1,
            max_value=7,
            value=3
        )

    with col4:
        travelers = st.number_input(
            "Number of Travelers",
            min_value=1,
            max_value=20,
            value=1
        )

    latest_start_date = today + timedelta(days=16 - days)

    travel_date = st.date_input(
        "Travel Start Date",
        value=today,
        min_value=today,
        max_value=latest_start_date
    )

    col5, col6 = st.columns(2)

    with col5:
        budget = st.number_input(
            "Total Budget (₹)",
            min_value=1000,
            max_value=1000000,
            value=20000,
            step=1000
        )

    with col6:
        preferences = st.text_input(
            "Travel Preferences",
            placeholder="Historical places, adventure, nature..."
        )

    submitted = st.form_submit_button(
        "Generate My Travel Plan",
        use_container_width=True
    )


# --------------------------------------------------
# GENERATE TRAVEL PLAN
# --------------------------------------------------

if submitted:

    if not source.strip():
        st.error("Please enter your departure city.")

    elif source.strip().lower() == destination.lower():
        st.error("Departure city and destination cannot be the same.")

    else:

        request = f"""
        Plan a {days}-day trip.

        Departure city: {source}
        Destination: {destination}
        Travel start date: {travel_date.isoformat()}
        Number of travelers: {travelers}
        Total budget: {budget} Indian Rupees
        Travel preferences: {preferences or "General sightseeing"}

        Use the available tools to:
        1. Search flights matching the requested travel date.
        2. Find suitable hotels within the budget.
        3. Find highly rated tourist attractions.
        4. Get weather forecasts for the selected travel dates.
        5. Estimate the complete trip budget.
        6. Create a day-wise itinerary.
        7. Explain why the recommendations were selected.

        Clearly identify historical sample flight data.
        Never present historical records as live availability.
        Mention missing costs if the estimate is incomplete.
        Present the final answer in a structured format.
        """

        result = None
        result_mode = None

        # Try Gemini first
        with st.spinner("Gemini is planning your trip..."):

            try:
                result = run_travel_agent(request, llm)
                result_mode = "groq"

            except Exception as e:

                st.warning(
                    "Gemini is currently unavailable. "
                    "Switching to the fallback travel planner."
                )

                st.caption(f"Reason: {str(e)[:250]}")

                # Use fallback planner
                try:

                    result = generate_fallback_plan(
                        source=source,
                        destination=destination,
                        days=days,
                        budget=budget,
                        travelers=travelers,
                        preferences=preferences or "General sightseeing",
                        travel_date=travel_date.isoformat()
                    )

                    result_mode = "fallback"

                except Exception as fallback_error:

                    st.error(
                        f"Fallback planner failed: {fallback_error}"
                    )

        if result is not None:

            st.session_state["travel_result"] = result
            st.session_state["result_mode"] = result_mode


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "travel_result" in st.session_state:

    result = st.session_state["travel_result"]
    result_mode = st.session_state["result_mode"]

    # Prepare structured JSON output
    if isinstance(result, dict):
        json_data = result
    else:
        json_data = {
            "generated_plan": result,
            "mode": result_mode
        }

    st.download_button(
        label="Download Travel Plan (JSON)",
        data=json.dumps(json_data, indent=4, ensure_ascii=False),
        file_name="travel_plan.json",
        mime="application/json"
    )

    st.divider()

    st.markdown(
        '<div class="section-heading">Your Travel Plan</div>',
        unsafe_allow_html=True
    )

    if result_mode == "groq":

        st.success("Your plan was generated using Groq AI.")

        st.markdown(result)

    else:

        st.info("Your plan was generated using the fallback planner.")

        # Trip summary
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Destination",
                result["destination"]
            )

        with col2:
            st.metric(
                "Duration",
                f'{result["days"]} Days'
            )

        with col3:
            st.metric(
                "Travelers",
                result["travelers"]
            )

        # Flight details
        st.markdown("### Flight Details")

        flight = result["selected_flight"]

        if flight:

            st.write(f"**Airline:** {flight['airline']}")
            st.write(f"**Flight ID:** {flight['flight_id']}")
            st.write(f"**Departure:** {flight['departure_time']}")
            st.write(f"**Arrival:** {flight['arrival_time']}")
            st.write(f"**Price:** ₹{flight['price'] * result['travelers']}")

            st.caption("Historical sample data, not live availability.")

            st.caption(
                "Why selected: This is the lowest-priced matching flight "
                "for your requested travel date."
            )

        else:
            st.warning(
                "No matching sample flight was found for your travel date. "
                "Flight cost is excluded from the estimate."
            )

        # Hotel details
        st.markdown("### Hotel Recommendation")

        hotel = result["selected_hotel"]

        if hotel:

            st.write(f"**Hotel:** {hotel['name']}")
            st.write(f"**Rating:** {hotel['stars']} Stars")
            st.write(f"**Price per night:** ₹{hotel['price_per_night']}")
            st.write(
                f"**Amenities:** {', '.join(hotel['amenities'])}"
            )

            st.caption(
                "Why selected: This hotel meets the price and minimum "
                "rating filters. It is selected as the lowest-priced "
                "matching option."
            )

        else:
            st.warning(
                "No matching hotel was found. "
                "Hotel cost is excluded from the estimate."
            )

        # Attractions
        st.markdown("### Recommended Attractions")

        places = result.get("places", [])

        if places:

            for place in places:

                st.write(
                    f"**{place['name']}** — "
                    f"Rating: {place['rating']}/5"
                )

                st.caption(
                    "Why selected: This attraction meets your rating "
                    "preference and is ranked by its rating."
                )

        else:

            st.warning(
                "No matching attractions were found for this destination. "
                "You can explore local places during your free time."
            )

        # Itinerary
        st.markdown("### Day-wise Itinerary")

        for day in result["itinerary"]:

            with st.expander(
                f"Day {day['day']}",
                expanded=True
            ):

                if day["activities"]:

                    for activity in day["activities"]:
                        st.write(f"- {activity}")

                else:
                    st.write("Free time or local exploration.")

                weather = day["weather"]

                if weather:

                    st.write(
                        f"**Date:** {weather['date']}"
                    )

                    st.write(
                        f"**Weather:** {weather['weather']}"
                    )

                    st.write(
                        f"**Temperature:** "
                        f"{weather['min_temperature']}°C – "
                        f"{weather['max_temperature']}°C"
                    )

        # Budget
        st.markdown("### Budget Breakdown")

        breakdown = result["budget_breakdown"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Flight",
            f"₹{breakdown['flight_cost']:,.0f}"
        )

        col2.metric(
            "Hotel",
            f"₹{breakdown['hotel_cost']:,.0f}"
        )

        col3.metric(
            "Daily Expenses",
            f"₹{breakdown['daily_expenses']:,.0f}"
        )

        st.metric(
            "Estimated Total",
            f"₹{breakdown['total_budget']:,.0f}"
        )

        st.write(
            f"**Your Budget:** ₹{result['user_budget']:,.0f}"
        )

        if result["budget_status"] == "Within budget":

            st.success("The estimated trip cost is within your budget.")

        elif result["budget_status"] == "Exceeds budget":

            st.error("The estimated trip cost exceeds your budget.")

        else:

            st.warning(
                "The budget estimate is incomplete. "
                "Some expenses are unavailable."
            )

            for missing in result["missing_costs"]:
                st.write(f"- {missing}")

        st.caption(
            "Fallback estimates use assumed daily expenses and sample "
            "datasets. They are not confirmed booking prices."
        )
