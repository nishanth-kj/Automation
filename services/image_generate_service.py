import torch
from diffusers import StableDiffusionPipeline

class ImageGenerateService:
    def __init__(self, model_path="models/z_image_turbo_bf16"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.pipe = StableDiffusionPipeline.from_single_file(
            f"{model_path}/z_image_turbo_bf16.safetensors",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )

        self.pipe = self.pipe.to(self.device)

        # memory optimization (IMPORTANT for your GPU)
        self.pipe.enable_attention_slicing()

    def generate(self, prompt: str, output_path="output.png"):
        image = self.pipe(
            prompt,
            num_inference_steps=25,
            guidance_scale=7.5
        ).images[0]

        image.save(output_path)
        return output_path