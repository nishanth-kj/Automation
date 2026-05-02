import requests
import os
from typing import Optional
from dotenv import load_dotenv
from repository.chat_repository import ChatRepository

load_dotenv()

class AiService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AiService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
        self.chat_repo = ChatRepository()

    def generate(self, system_prompt: str, user_input: str) -> str:
        """Call LM Studio (OpenAI compatible API)"""
        try:
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "model": "google/gemma-4-e4b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7,
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling LM Studio: {e}")
            # Fallback/Mock logic if LM Studio is not running
            if "rhyme" in system_prompt.lower():
                return "My favorite color is blue, as deep as the ocean's hue."
            return f"Error: Could not reach LM Studio. ({str(e)})"

    def chat(self, model: str, system_prompt: str, input_text: str) -> str:
        response_text = self.generate(system_prompt, input_text)
        
        # Save to database
        try:
            self.chat_repo.save(
                model=model,
                system_prompt=system_prompt,
                input_text=input_text,
                response_text=response_text
            )
        except Exception as e:
            print(f"Failed to save chat to DB: {e}")
            
        return response_text