import json
from litellm import completion
import os

def classify_message(message: str) -> dict:
    """Classify restaurant message using GPT-5-nano"""
    
    system_prompt = """You are an intelligent message classification system for a restaurant support application.
Analyze messages in Bahasa Indonesia and return structured JSON with urgency, groups, and action message.

Output Format (strict JSON):
{
  "urgency": "Not Urgent | Urgent | Extremely Urgent",
  "groups": ["Facility", "The Waiters", "The Chef", "Cleanse", "Administration", "Hospitality", "The Foods"],
  "action_message": "A short and actionable summary for the restaurant owner."
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

Action Message:
- Concise, polite, and actionable message in Bahasa Indonesia directed to the restaurant owner
- Examples: "Segera periksa kondisi AC di ruang VIP." / "Berikan apresiasi kepada chef atas masakan yang disukai pelanggan."

Return only valid JSON, no extra text."""

    try:
        llm_model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
        response = completion(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classify this message: {message}"}
            ],
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"urgency": "Not Urgent", "groups": ["Administration"], "action_message": "Terjadi kesalahan sistem, mohon periksa kembali.", "error": str(e)}
