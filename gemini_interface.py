# gemini_interface.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Choose the Gemini Flash model (for speed)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def ask_gemini(satellite_name, field_name, raw_snippet, url=None, extra_context = None):
    print(f"\nGemini prompt for {satellite_name} - {field_name}:")
    print(raw_snippet)

    use_gemini_knowledge = False

    # Check if snippet is missing or low quality
    if not raw_snippet or len(raw_snippet.strip()) < 30:
        use_gemini_knowledge = True
        raw_snippet = "No reliable snippet was found online. Please use your own knowledge base to answer."
    context_clause = f"\n\n{extra_context}" if extra_context else ""
    prompt = f"""
You are a concise satellite analyst. Your job is to extract a short, precise answer (max 2 lines) for a satellite property from raw text.

Satellite: {satellite_name}
Field to answer: {field_name}
Raw web result: {raw_snippet} 
Context clause : {context_clause}
If context is provided, try your best to satisfy the requirements of the context.

If the result is not found or unclear, just say "Data not available".
If a number or label is expected, return only that.
Don't return any explanations.

Respond concisely and clearly for that field only.
    """.strip()

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        if use_gemini_knowledge and response.lower() != "data not available":
            answer += "\n\n⚠️This answer is based on Gemini's internal knowledge, not live internet search."

        return answer
    except Exception as e:
        print("Gemini Error:", e)
        return "Data not available"
