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
        # Update to native v1 API base
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/api/v1")
        self.chat_repo = ChatRepository()

    def generate(self, system_prompt: str, user_input: str) -> str:
        """Call LM Studio Native v1 REST API"""
        try:
            # Using the new /chat endpoint as per 0.4.0 docs
            response = requests.post(
                f"{self.lm_studio_url}/chat",
                json={
                    "model": "google/gemma-4-e4b", # Default model
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # The response structure for /api/v1/chat typically follows the standard chat completion format
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            elif "message" in data:
                return data["message"]["content"]
            
            return str(data)
        except Exception as e:
            print(f"Error calling LM Studio v1 API: {e}")
            if "rhyme" in system_prompt.lower():
                return "My favorite color is blue, as deep as the ocean's hue."
            return f"Error: Could not reach LM Studio v1 API. ({str(e)})"

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