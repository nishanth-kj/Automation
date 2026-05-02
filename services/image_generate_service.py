import requests
import os
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

class ImageGenerateService:
    def __init__(self):
        self.comfyui_url = os.getenv("COMFYUI_URL", "http://localhost:8188")

    def generate(self, prompt: str, output_path="output.png"):
        """Call ComfyUI API to generate an image"""
        # Simple ComfyUI API Prompt structure
        # This is a basic example; real ComfyUI workflows can be more complex
        workflow = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 8,
                    "denoise": 1,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0],
                    "positive": ["6", 0],
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "seed": 8566257,
                    "steps": 20
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.ckpt"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": 512,
                    "width": 512
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": prompt
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": ["4", 1],
                    "text": "low quality, bad anatomy, text, watermark"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "GemmaChat",
                    "images": ["8", 0]
                }
            }
        }

        try:
            client_id = str(uuid.uuid4())
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow, "client_id": client_id},
                timeout=10
            )
            response.raise_for_status()
            print(f"ComfyUI prompt sent: {response.json()}")
            
            # Note: In a real scenario, we'd wait for the image to be generated
            # and fetch it via websocket or history API.
            # For now, we'll return a placeholder or success message.
            return f"Prompt sent to ComfyUI at {self.comfyui_url}"
            
        except Exception as e:
            print(f"Error calling ComfyUI: {e}")
            return f"Error: Could not reach ComfyUI. ({str(e)})"