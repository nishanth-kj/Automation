import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TextService:
    def __init__(self):
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

    def generate(self, prompt: str) -> str:
        """Call LM Studio for general text generation"""
        try:
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "model": "google/gemma-4-e4b",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"TextService Error: {e}")
            return f"Error: Could not reach LM Studio. ({str(e)})"