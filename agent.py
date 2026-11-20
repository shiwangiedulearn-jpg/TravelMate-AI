
from llm_config import llm
from agent.runner import run_travel_agent


if __name__ == "__main__":

    request = "Plan a 3-day trip to Goa from Bangalore under 20000 rupees."

    try:
        result = run_travel_agent(request, llm)
        print(result)

    except Exception as e:
        print("Agent error:", e)
