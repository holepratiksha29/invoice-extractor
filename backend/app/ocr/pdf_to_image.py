from pdf2image import convert_from_path   # Library used to convert PDF pages into images
import os                                 # Used for file and directory operations
from pathlib import Path                  # Helps manage file paths in a clean way

# Folder where converted images will be stored
IMAGES_DIR = "app/data/images"

# Create the directory if it does not already exist   
os.makedirs(IMAGES_DIR, exist_ok=True)

# Get the base directory of the project
# __file__ = current file location
# parents[2] moves two folders up in the directory structure
BASE_DIR = Path(__file__).resolve().parents[2]

# Define path to Poppler binaries (required by pdf2image on Windows)
POPPLER_PATH = BASE_DIR / "app" / "tools" / "poppler" / "Library" / "bin"


# Function to convert PDF into images
def pdf_to_images(pdf_path):

    # Print log message showing which PDF is being processed
    print(f"Converting PDF to images: {pdf_path}")

    # List to store paths of generated images
    paths = []

    # Convert PDF pages into images
    images = convert_from_path(
        pdf_path,                 # Input PDF file path
        dpi=300,                  # High DPI for better OCR accuracy
        poppler_path=str(POPPLER_PATH)   # Path to Poppler tool
    )

    # Loop through each page image
    for i, img in enumerate(images):

        # Extract filename without ".pdf"
        filename = os.path.basename(pdf_path).replace(".pdf", "")

        # Create output image path with page number
        out = os.path.join(IMAGES_DIR, f"{filename}_{i}.png")

        # Save the image as PNG format
        img.save(out, "PNG")

        # Print confirmation message
        print(f"Saved image: {out}")

        # Add image path to list
        paths.append(out)

    # Return list of generated image paths
    return paths