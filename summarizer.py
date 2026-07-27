from ai.groq_client import client, MODEL

def summarize(text):

    prompt = f"""
    Summarize this PDF.

    Use headings.

    Use bullet points.

    Keep it concise.

    TEXT:

    {text[:12000]}
    """

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0.3,

        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ]

    )

    return response.choices[0].message.content