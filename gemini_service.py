import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_document(text):
    prompt = f"""
    Extract:
    - Patient Name
    - Diagnosis
    - Total Bill Amount
    - Dates
    Return JSON only.
    Document:
    {text}
    """

    response = model.generate_content(prompt)
    return response.text