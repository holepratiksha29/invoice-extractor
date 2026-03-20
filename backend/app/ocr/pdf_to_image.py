import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path):

    doc = fitz.open(pdf_path)
    image_paths = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        path = f"uploads/page_{i}.png"
        pix.save(path)
        image_paths.append(path)

    return image_paths

