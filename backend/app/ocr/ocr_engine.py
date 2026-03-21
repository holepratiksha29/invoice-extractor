import pytesseract
from PIL import Image

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    text_list = text.split("\n")
    text_list = [line for line in text_list if line.strip() != ""]

    return text_list
