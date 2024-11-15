from PIL import Image, ImageDraw, ImageFont
import os

def create_tree_image(tree_str, output_file='tree_structure'):
    # Parse the tree string
    lines = tree_str.strip().split('\n')
    
    # Calculate image dimensions
    line_height = 20
    padding = 10
    max_width = max(len(line) for line in lines) * 10
    height = len(lines) * line_height + 2 * padding
    width = max_width + 2 * padding

    # Create a new image
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    # Draw the tree
    y = padding
    for line in lines:
        indent = len(line) - len(line.lstrip())
        draw.text((padding + indent * 10, y), line.strip(), fill='black', font=font)
        y += line_height

    # Save the image
    image.save(f"{output_file}.png")
    print(f"Tree image saved as {output_file}.png")