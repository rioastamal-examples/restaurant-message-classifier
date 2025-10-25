import json
from litellm import completion
import os

def classify_message(message: str) -> dict:
    """Classify restaurant message using GPT-5-nano"""
    
    system_prompt = """You are an intelligent message classification system for a restaurant support application.
Analyze messages in Bahasa Indonesia and return structured JSON with urgency and groups.

Output Format (strict JSON):
{
  "urgency": "Not Urgent | Urgent | Extremely Urgent",
  "groups": ["Facility", "The Waiters", "The Chef", "Cleanse", "Administration", "Hospitality", "The Foods"]
}

Urgency Levels:
- Not Urgent: General feedback, suggestions, compliments
- Urgent: Issues needing attention but not critical
- Extremely Urgent: Safety issues, serious complaints, potential harm, billing related problems

Groups:
- Facility: Physical infrastructure (AC, furniture, electricity, WiFi)
- The Waiters: Service staff related
- The Chef: Kitchen staff or food preparation
- Cleanse: Hygiene, cleaning, sanitation
- Administration: Billing, payment, reservations, management
- Hospitality: General experience, atmosphere
- The Foods: Food taste, quality, portion, availability

Return only valid JSON, no extra text."""

    try:
        response = completion(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classify this message: {message}"}
            ],
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"urgency": "Not Urgent", "groups": ["Administration"], "error": str(e)}
