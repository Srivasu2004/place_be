from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
from groq import Groq
import json

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
# ROOT CHECK
# ======================
@app.get("/")
def home():
    return {"message": "AI Travel Backend Running"}


# ======================
# AI RECOMMENDATION ENDPOINT
# ======================
@app.get("/ai-recommend")
def ai_recommend(city: str = Query(...)):

    prompt = f"""
You are a travel expert AI.

Return ONLY valid JSON (no extra text).

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
Keep descriptions short and useful.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        # return raw AI output (frontend will parse)
        return {
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }
