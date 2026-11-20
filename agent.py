
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.runner import run_travel_agent

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.3,
    timeout=30,
    max_retries=0
)



if __name__ == "__main__":
    request = "Plan a 3-day trip to Goa from Bangalore under 20000 rupees."

    try:
        result = run_travel_agent(request, llm)
        print(result)

    except Exception as e:
        print("Agent error:", e)