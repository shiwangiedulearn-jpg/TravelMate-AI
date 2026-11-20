# TravelMate AI – Agentic AI-Based Travel Planning Assistant

TravelMate AI is an intelligent travel planning assistant that helps users plan personalized trips using Agentic AI, LangChain, Groq and real-time weather information.

Users can enter their departure city, destination, travel dates, number of travelers, budget and preferences. The application generates a structured travel plan with transportation options, hotel recommendations, tourist attractions, weather forecasts, itinerary and estimated expenses.

## Features

- **AI-Powered Travel Planning:** Uses LangChain and Groq to generate personalized travel plans.
- **Flight Search:** Searches sample flight datasets based on source, destination and travel date.
- **Hotel Recommendations:** Filters hotels according to budget and minimum star rating.
- **Attraction Discovery:** Finds tourist attractions based on destination, category and rating.
- **Weather Forecast:** Retrieves weather forecasts using the Open-Meteo API.
- **Day-Wise Itinerary:** Generates activities and organizes them across the trip duration.
- **Budget Estimation:** Calculates flight, accommodation and daily expenses.
- **Recommendation Explanations:** Explains why particular options were selected.
- **JSON Export:** Allows users to download their travel plan in structured JSON format.
- **Fallback Planning:** Provides a rule-based travel plan when the AI service is unavailable.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| AI Model | Groq API (GPT-OSS-120B) |
| Agent Framework | LangChain |
| Weather API | Open-Meteo |
| Data Storage | JSON |
| Environment Management | Python dotenv |
| Deployment | Streamlit Community Cloud |

## Project Structure

```text
TravelMate-AI/
│
├── agent/
│   ├── __init__.py
│   ├── prompts.py
│   └── runner.py
│
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
│
├── app.py
├── agent.py
├── llm_config.py
├── tools.py
├── flight_tools.py
├── hotel_tools.py
├── places_tools.py
├── weather_tools.py
├── budget_tools.py
├── main.py
├── requirements.txt
├── .gitignore
└── .env
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shiwangiedulearn-jpg/TravelMate-AI.git
cd TravelMate-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

Never commit your `.env` file or expose your API key publicly.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

1. The user enters travel details through the Streamlit interface.
2. The LangChain agent receives the request and determines which tools are needed.
3. The agent invokes the relevant tools to search flights, hotels, attractions, weather and budget information.
4. The collected information is used to generate a personalized travel plan.
5. If the AI service is unavailable, the fallback planner generates a plan using predefined filtering and selection logic.
6. The final plan is displayed in the application and can be downloaded as JSON.

## Available Tools

| Tool | Function |
|---|---|
| `search_flights` | Searches and sorts sample flights |
| `search_hotels` | Filters hotels by price and rating |
| `search_places` | Searches tourist attractions |
| `weather_tool` | Retrieves weather forecasts |
| `estimate_budget` | Calculates estimated trip expenses |

## APIs and Data Sources

- **Groq API:** Powers the AI travel planning agent.
- **Open-Meteo API:** Provides weather forecast information.
- **JSON Datasets:** Store sample flight, hotel and tourist attraction information.

## Important Notes and Limitations

- Flight, hotel and attraction datasets contain sample records and do not represent live booking availability.
- Flight prices and schedules must be verified through actual booking platforms.
- Weather forecasts are subject to the availability of the Open-Meteo forecast API.
- Budget estimates use available sample prices and assumed daily expenses. Missing costs are identified in the output.
- The fallback planner does not require an AI model response, but uses predefined selection and planning logic.
- AI-generated recommendations should be verified before making actual travel bookings.

## Deployment

The application is deployed using Streamlit Community Cloud.

**Live Application:** https://travelmate-ai-agent.streamlit.app/

For deployment, configure the `GROQ_API_KEY` in the application's Streamlit Secrets settings.

## Future Improvements

- Integration with live flight and hotel booking APIs.
- More destinations and comprehensive travel datasets.
- Improved itinerary optimization.
- Personalized recommendations based on user preferences.
- More advanced budget optimization.

## Author

**Shiwangi **

B.Tech – Computer Science and Engineering

GitHub: https://github.com/shiwangiedulearn-jpg
