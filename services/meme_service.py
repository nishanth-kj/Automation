import os
from PIL import Image, ImageDraw, ImageFont

class MemeService:
    def __init__(self, font_path="assets/fonts/arial.ttf", font_size=40):
        self.font_path = font_path
        self.font_size = font_size

    def _draw_centered(self, draw, text, y, img_width, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img_width - text_width) // 2

        draw.text(
            (x, y),
            text.upper(),
            font=font,
            fill="white",
            stroke_width=2,
            stroke_fill="black"
        )

    def create_meme(self, image_path, top_text, bottom_text, output_path="meme.png"):
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # Priority: Local assets -> System fonts -> Default
        target_font = self.font_path
        
        if not os.path.exists(target_font):
            if os.path.exists(system_font):
                target_font = system_font
        
        try:
            if os.path.exists(target_font):
                font = ImageFont.truetype(target_font, self.font_size)
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        # Top text
        self._draw_centered(draw, top_text, 20, img.width, font)

        # Bottom text
        self._draw_centered(draw, bottom_text, img.height - 80, img.width, font)

        img.save(output_path)
        return output_path