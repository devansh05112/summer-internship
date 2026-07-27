import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def generate_flashcards(text):

    prompt = f"""
You are an expert study assistant.

Read the following study notes and generate 15 educational flashcards.

Return ONLY valid JSON.

Format:

[
    {{
        "question": "...",
        "hint": "...",
        "answer": "..."
    }}
]

Study Notes:

{text}
"""

    try:

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You generate educational flashcards."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2500
        )

        content = response.choices[0].message.content.strip()

        

        # Remove markdown fences
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        # Try direct JSON parsing
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Extract JSON array if Groq added extra text
        start = content.find("[")
        end = content.rfind("]")

        if start != -1 and end != -1:
            json_text = content[start:end + 1]
            return json.loads(json_text)

        raise ValueError("No valid JSON found.")

    except Exception as e:

        print("Flashcard Generation Error:", e)

        return []