import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

class TextService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model_id = "google/gemma-4-E2B-it"
        self.local_path = "models/gemma-4-E2B-it"

        # Download + save locally
        self.processor = AutoProcessor.from_pretrained(
            self.model_id,
            cache_dir=self.local_path
        )

        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_id,
            cache_dir=self.local_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def generate(self, prompt):
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True
        ).to(self.model.device)

        input_len = inputs["input_ids"].shape[-1]

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=80
        )

        return self.processor.decode(
            outputs[0][input_len:], skip_special_tokens=True
        )