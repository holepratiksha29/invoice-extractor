import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.ocr.pdf_to_image import pdf_to_images
from app.ocr.ocr_engine import extract_text
from app.parser.invoice_parser import parse_invoice

app = FastAPI()

# ✅ CORS (for frontend connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder create
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Home route (for test)
@app.get("/")
def home():
    return {"message": "Invoice API Running"}


# Main API
@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):

    try:
        # Save uploaded file
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"PDF Saved: {file_location}")

        # PDF → Images
        images = pdf_to_images(file_location)

        # OCR text store
        all_text = []

        for img_path in images:
            text_list = extract_text(img_path)
            if text_list:
                all_text.extend(text_list)

        print("OCR TEXT:", all_text)

        # Parse invoice data
        invoice_data = parse_invoice(all_text)

        return invoice_data

    except Exception as e:
        return {"error": str(e)}
