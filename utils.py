import os
import random

import toml
from PIL import Image

def resize_image(image, max_width, max_height):
    original_width, original_height = image.size
    ratio = min(max_width / original_width, max_height / original_height)
    if ratio < 1:  # Only resize if the image is larger than the maximum allowed size
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return image.resize((new_width, new_height))
    return image

def load_images_from_folder(folder):
    images = {}
    max_width = 400
    max_height = 300
    for filename in os.listdir(folder):
        if filename.endswith((".png", ".jpg", ".jpeg", ".PNG")):  # Check for common image file extensions
            img_path = os.path.join(folder, filename)
            with Image.open(img_path) as img:
                img.load()  # Load the image data
                resized_img = resize_image(img, max_width, max_height)
                image_name = os.path.splitext(filename)[0]
                images[image_name] = resized_img.copy()  # Store the resized image object in the dictionary
    return images


def reveal_random_letters(word, random_count):
    if random_count >= len(word):
        raise ValueError("random_count must be less than the length of the word")

    # Convert the word to lowercase to standardize the output
    word = word.lower()
    # Create a list of positions to potentially reveal, excluding the first position
    positions = list(range(1, len(word)))
    # Randomly select positions to reveal, adjusting the count since the first is always shown
    revealed_positions = random.sample(positions, random_count - 1) if random_count > 1 else []

    # Create the masked word with underscores
    masked_word = ['_'] * len(word)
    # The first letter is always revealed
    masked_word[0] = word[0]
    # Replace underscores with actual letters at the chosen positions
    for pos in revealed_positions:
        masked_word[pos] = word[pos]

    # Join the list into a string and return
    return ' '.join(masked_word)

def load_toml_file(filepath):
    """Load and return data from a TOML file."""
    with open(filepath, 'r') as file:
        data = toml.load(file)
    return data

# print(reveal_random_letters("hello", 2))