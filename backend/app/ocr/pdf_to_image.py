import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path, output_folder="temp_images"):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        img_path = f"{output_folder}/page_{i}.png"
        pix.save(img_path)
        image_paths.append(img_path)

    return image_paths
