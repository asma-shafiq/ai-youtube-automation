#!/usr/bin/env python3
"""
Generate YouTube thumbnails automatically
"""

import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

class ThumbnailGenerator:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.output_dir = os.getenv('THUMBNAIL_OUTPUT_DIR', './content/thumbnails')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def create_thumbnail(
        self,
        text: str,
        background_color: tuple = (20, 30, 48),
        text_color: tuple = (255, 255, 255),
        accent_color: tuple = (0, 150, 255)
    ) -> str:
        """
        Create a YouTube thumbnail with text
        """
        print(f"[INFO] Creating thumbnail with text: {text}")
        
        # Create image
        image = Image.new('RGB', (self.width, self.height), background_color)
        draw = ImageDraw.Draw(image)
        
        # Add accent bar
        bar_height = 80
        draw.rectangle(
            [(0, self.height - bar_height), (self.width, self.height)],
            fill=accent_color
        )
        
        # Add main text
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (centered)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 - 100
        
        # Draw text with outline for better visibility
        outline_range = 2
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=(0, 0, 0))
        
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Add branding at bottom
        brand_text = "AI Daily Insights"
        draw.text((50, self.height - 50), brand_text, font=font, fill=text_color)
        
        # Save thumbnail
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.output_dir}/thumbnail_{timestamp}.png"
        
        image.save(output_path, 'PNG')
        print(f"[SUCCESS] Thumbnail created: {output_path}")
        
        return output_path


if __name__ == "__main__":
    generator = ThumbnailGenerator()
    try:
        thumbnail = generator.create_thumbnail("GPT-4\nFEATURES")
        print(f"[SUCCESS] Thumbnail: {thumbnail}")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
