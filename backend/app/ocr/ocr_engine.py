from paddleocr import PaddleOCR

# Initialize OCR (only once)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Function to extract text from an image
def extract_text(image_path):

    result = ocr.ocr(image_path)

    text_list = []

    for line in result:
        for word in line:
            text_list.append(word[1][0])

    return text_list
