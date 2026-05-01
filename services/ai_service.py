from transformers import AutoProcessor, AutoModelForCausalLM
import torch

class AiService:
    def __init__(self, model_id="models/gemma-4-E2B-it"):

        self.model_id = model_id

        # Load once
        self.processor = AutoProcessor.from_pretrained(self.model_id)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )


    def generate(self, prompt: str) -> str:
        inputs = self.processor(prompt, return_tensors="pt")

        # Move to correct device
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=50
        )

        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result