import re
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

# ==========================================
# Groq Client
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)

# ==========================================
# Generate Quiz
# ==========================================

def generate_quiz(text):

    prompt = f"""
You are an expert exam paper creator.

Create EXACTLY 10 multiple-choice questions from the study material.

Rules:

1. Return EXACTLY 10 questions.
2. Each question must have FOUR options.
3. Only ONE option should be correct.
4. Make questions clear and factual.
5. Do NOT repeat questions.
6. Keep explanations between 20-40 words.
7. Do NOT use Markdown.
8. Follow the format EXACTLY.

Q1. Question

A. Option
B. Option
C. Option
D. Option

Answer: B

Explanation:
Short explanation here.

Repeat for all 10 questions.

Study Material:

{text[:12000]}
"""

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        temperature=0.4,

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    quiz_text = response.choices[0].message.content

    return parse_quiz(quiz_text)


# ==========================================
# Parse Quiz
# ==========================================

def parse_quiz(text):

    pattern = re.compile(

        r"Q\d+\.\s*(.*?)\s*"
        r"A\.\s*(.*?)\s*"
        r"B\.\s*(.*?)\s*"
        r"C\.\s*(.*?)\s*"
        r"D\.\s*(.*?)\s*"
        r"Answer:\s*([ABCD])\s*"
        r"Explanation:\s*(.*?)(?=Q\d+\.|$)",

        re.S

    )

    answer_map = {

        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3

    }

    quiz = []

    matches = pattern.findall(text)

    for m in matches:

        quiz.append({

            "question": m[0].strip(),

            "options": [

                m[1].strip(),
                m[2].strip(),
                m[3].strip(),
                m[4].strip()

            ],

            "answer": answer_map[m[5]],

            "explanation": m[6].strip()

        })

    # -----------------------------------------
    # Fallback if parsing fails
    # -----------------------------------------

    if len(quiz) == 0:

        quiz.append({

            "question": "Unable to generate quiz.",

            "options": [

                "Retry",
                "Retry",
                "Retry",
                "Retry"

            ],

            "answer": 0,

            "explanation": "Groq did not return the expected format."

        })

    return quiz