import pytesseract
from PIL import Image

# Function to extract text from an image
def extract_text(image_path):

    # Open image using PIL
    img = Image.open(image_path)

    # Extract text using pytesseract
    text = pytesseract.image_to_string(img)

    # Convert text into list (same format as before)
    text_list = text.split("\n")

    # Remove empty lines
    text_list = [line for line in text_list if line.strip() != ""]

    return text_list
