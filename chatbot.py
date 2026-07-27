from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def ask_notes(notes, question):

    prompt = f"""
You are Cerebra AI.

Answer ONLY using the study material below.

If the answer cannot be found in the notes,
reply exactly:

"The uploaded notes do not contain this information."

------------------------
Study Material
------------------------

{notes[:15000]}

------------------------
Question
------------------------

{question}

------------------------
Answer
------------------------
"""

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[

            {
                "role": "system",
                "content": "You answer only from study notes."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2,

        max_tokens=500

    )

    return response.choices[0].message.content.strip()