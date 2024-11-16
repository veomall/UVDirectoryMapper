from PIL import Image, ImageDraw, ImageFont
import os
import requests
import io

def get_font(font_size):
    # URL to Noto Sans Mono font (regular weight)
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansmono/NotoSansMono%5Bwdth%2Cwght%5D.ttf"

    try:
        # Download the font file
        response = requests.get(font_url)
        font_data = io.BytesIO(response.content)

        # Create a font object
        font = ImageFont.truetype(font_data, font_size)
    except Exception as e:
        print(f"Failed to load Noto Sans Mono font: {str(e)}")
        print("Falling back to default font.")
        font = ImageFont.load_default()

    return font
def create_tree_image(tree_str, output_file='tree_structure'):
    # Parse the tree string
    lines = tree_str.strip().split('\n')

    # Calculate image dimensions
    font_size = 14
    line_height = font_size + 4
    padding = 20
    char_width = 9  # Approximate width for monospace font
    max_width = max(len(line) for line in lines) * char_width
    height = len(lines) * line_height + 2 * padding
    width = max_width + 2 * padding

    # Create a new image
    background_color = (40, 42, 54)  # Dracula theme background
    text_color = (248, 248, 242)  # Dracula theme foreground
    image = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Load the font
    font = get_font(font_size)

    # Draw the tree
    y = padding
    for line in lines:
        indent = len(line) - len(line.lstrip())
        draw.text((padding + indent * char_width, y), line.strip(), fill=text_color, font=font)
        y += line_height

    # Save the image
    image.save(f"{output_file}.png")
    print(f"Tree image saved as {output_file}.png")

