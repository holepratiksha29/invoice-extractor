from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path):
    
    poppler_path = os.path.join(os.getcwd(), "app", "tools", "poppler", "bin")

    images = convert_from_path(
        pdf_path,
        poppler_path=poppler_path
    )

    image_paths = []

    for i, img in enumerate(images):
        path = f"uploads/page_{i}.png"
        img.save(path, "PNG")
        image_paths.append(path)

    return image_paths
