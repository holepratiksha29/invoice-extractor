from paddleocr import PaddleOCR   # Import PaddleOCR for text detection and recognition
import cv2                        # Import OpenCV for image processing

# Initialize the PaddleOCR engine
# use_angle_cls=True helps detect rotated text
# lang="en" sets OCR language to English
# use_gpu=False runs OCR on CPU instead of GPU
# enable_mkldnn=False disables MKL acceleration (sometimes avoids compatibility issues)

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    use_gpu=False,
    enable_mkldnn=False
)

# Function to extract text from an image
def extract_text(image_path):

    # Read the image from the given path using OpenCV
    img = cv2.imread(image_path)

    # Run OCR on the image
    # It detects text regions and recognizes text inside them
    result = ocr.ocr(img)

    # Create an empty list to store detected text
    text_list = []

    # Check if OCR returned any result
    if result:

        # Loop through each detected text box
        for line in result[0]:

            # line structure:
            # line[0] → bounding box coordinates
            # line[1][0] → recognized text
            # line[1][1] → confidence score

            text = line[1][0]   # Extract recognized text

            # Add the detected text into the list
            text_list.append(text)

    # Return the list of detected text lines
    return text_list