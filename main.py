from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
from groq import Groq

# ======================
# LOAD ENV
# ======================
load_dotenv()

app = FastAPI(title="AI Travel Assistant Backend")

# ======================
# GROQ CLIENT
# ======================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ======================
# ROOT
# ======================
@app.get("/")
def home():
    return {"message": "AI Travel Backend Running"}


# ======================
# AI RECOMMENDATION
# ======================
@app.get("/ai-recommend")
def ai_recommend(city: str = Query(...)):

    prompt = f"""
You are a travel expert AI.

Return ONLY valid JSON.

Format:
{{
  "city": "{city}",
  "places": [
    {{
      "name": "",
      "description": "",
      "rating": ""
    }}
  ]
}}

Task:
Suggest top 5 tourist places in {city}.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You output only JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "result": response.choices[0].message.content
    }
