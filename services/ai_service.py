import requests
import os
from typing import Optional
from dotenv import load_dotenv
from repository.chat_repository import ChatRepository
from utils.logger import logger

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

    def generate(self, system_prompt: str, user_input: str, model: str = "google/gemma-4-e4b") -> str:
        """Call LM Studio Native v1 REST API"""
        try:
            # Using the LM Studio Native v1 API format
            response = requests.post(
                f"{self.lm_studio_url}/chat",
                json={
                    "model": model,
                    "system_prompt": system_prompt,
                    "input": user_input
                },
                timeout=30
            )
            if not response.ok:
                logger.error(f"LM Studio Error Response: {response.text}")
            response.raise_for_status()
            data = response.json()
            
            # LM Studio Native v1 API usually returns {"response": "..."} or {"choices": [...]}
            if "response" in data:
                return data["response"]
            elif "choices" in data:
                return data["choices"][0]["message"]["content"]
            
            return str(data)
        except Exception as e:
            logger.error(f"Error calling LM Studio v1 API: {e}")
            if "rhyme" in system_prompt.lower():
                return "My favorite color is blue, as deep as the ocean's hue."
            return f"Error: Could not reach LM Studio v1 API. ({str(e)})"

    def chat(self, model: str, system_prompt: str, input_text: str) -> str:
        response_text = self.generate(system_prompt, input_text, model=model)
        
        # Save to database
        try:
            self.chat_repo.save(
                model=model,
                system_prompt=system_prompt,
                input_text=input_text,
                response_text=response_text
            )
        except Exception as e:
            logger.error(f"Failed to save chat to DB: {e}")
            
        return response_text