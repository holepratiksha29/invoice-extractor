import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path):
    images = []

    pdf = fitz.open(pdf_path)

    for i, page in enumerate(pdf):
        pix = page.get_pixmap()
        img_path = f"uploads/page_{i}.png"
        pix.save(img_path)
        images.append(img_path)

    return images
