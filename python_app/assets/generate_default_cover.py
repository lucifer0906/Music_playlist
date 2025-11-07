"""
Generate a default cover image for the music player.
Run this script to create default.jpg if it doesn't exist.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_default_cover():
    """Generate a default album cover image."""
    # Create a 400x400 image with dark background
    img = Image.new('RGB', (400, 400), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    # Draw a circle in the center
    center = (200, 200)
    radius = 150
    draw.ellipse(
        [center[0] - radius, center[1] - radius, 
         center[0] + radius, center[1] + radius],
        fill='#1DB954',
        outline='#1DB954',
        width=3
    )
    
    # Draw a musical note symbol (simplified)
    # Draw a circle for note head
    note_center = (200, 180)
    note_radius = 20
    draw.ellipse(
        [note_center[0] - note_radius, note_center[1] - note_radius,
         note_center[0] + note_radius, note_center[1] + note_radius],
        fill='#0d0d0d',
        outline='#0d0d0d'
    )
    
    # Draw note stem
    draw.rectangle(
        [note_center[0] + note_radius - 5, note_center[1] - note_radius,
         note_center[0] + note_radius + 5, note_center[1] + 80],
        fill='#0d0d0d'
    )
    
    # Try to add text
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Add text
    text = "MUSIC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (400 - text_width) // 2
    text_y = 320
    draw.text((text_x, text_y), text, fill='#ffffff', font=font)
    
    # Save the image
    output_path = os.path.join(os.path.dirname(__file__), "default.jpg")
    img.save(output_path, "JPEG", quality=95)
    print(f"Default cover image generated: {output_path}")

if __name__ == "__main__":
    generate_default_cover()

