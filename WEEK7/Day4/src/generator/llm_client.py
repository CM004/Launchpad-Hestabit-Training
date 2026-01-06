from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def generate_answer(prompt):
    response = client.models.generate_content(
        model='models/gemini-flash-latest',
        contents=prompt
    )
    return response.text
