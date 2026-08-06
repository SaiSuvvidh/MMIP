import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

class AIHelper:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    def explain(self, object_name):
        prompt = f"Explain what a {object_name} is in 1-2 simple sentences."
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Couldn't fetch info: {e}"
