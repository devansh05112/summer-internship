from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY

)

MODEL = "llama-3.3-70b-versatile"