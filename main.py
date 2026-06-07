from fastapi import FastAPI, Query
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

app = FastAPI(
    title="AI Tourist Guide"
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

@app.get("/")
def home():
    return {"message": "AI Tourist Guide Running"}

@app.get("/recommend")
def recommend_places(city: str = Query(...)):

    prompt = f"""
    Recommend top 5 tourist places in {city}.

    Return JSON format:

    {{
      "places":[
        {{
          "name":"",
          "description":"",
          "rating":""
        }}
      ]
    }}
    """

    response = llm.invoke(prompt)

    return {
        "city": city,
        "recommendation": response.content
    }
