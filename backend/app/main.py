import os
import shutil
from fastapi import FastAPI, UploadFile, File

from app.ocr.pdf_to_image import pdf_to_images
from app.ocr.ocr_engine import extract_text
from app.parser.invoice_parser import parse_invoice

app = FastAPI()

# ✅ ADD THIS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Invoice API Running"}


@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):

    try:

        file_location = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"PDF Saved: {file_location}")

        # PDF → Images
        images = pdf_to_images(file_location)

        all_text = []

        # OCR
        for img_path in images:
            text = extract_text(img_path)
            all_text.extend(text)

        print("OCR TEXT:", all_text)

        # Parse invoice
        invoice_data = parse_invoice(all_text)

        return invoice_data

    except Exception as e:
        return {"error": str(e)}


# @app.post("/upload-invoice")
# async def upload_invoice(file: UploadFile = File(...)):

#     try:

#         # Save uploaded PDF
#         file_location = os.path.join(UPLOAD_FOLDER, file.filename)

#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         print("PDF Saved:", file_location)

#         # Convert PDF → Images
#         images = pdf_to_images(file_location)

#         all_text = []

#         # OCR on images
#         for img in images:
#             text = extract_text(img)
#             print("OCR TEXT:", text)
#             # print("OCR:", text)
#             all_text.extend(text)

#         # Parse invoice fields
#         invoice_data = parse_invoice(all_text)

#         print("PARSED:", invoice_data)

#         return invoice_data

#     except Exception as e:
#         print("ERROR:", e)
#         return {"error": str(e)}















# import os
# from fastapi import FastAPI, UploadFile, File
# import shutil

# app = FastAPI()

# UPLOAD_FOLDER = "uploads"

# # create uploads folder automatically
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.post("/upload-invoice")
# async def upload_invoice(file: UploadFile = File(...)):

#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {"message": "File uploaded successfully"}




# from fastapi import FastAPI
# from app.email.email_reader import EmailReader
# from app.ocr.pdf_to_image import pdf_to_images
# from app.ocr.ocr_engine import extract_text
# from app.parser.invoice_parser import parse_invoice
# from app.storage.json_writer import save_json

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"status": "Invoice Reader API Running"}


# @app.get("/run")
# def run():
#     client = EmailReader()
#     files = client.fetch_latest_invoice_attachments(max_messages=2)

#     results = []

#     for file in files:
#         images = []

#         if file.endswith(".pdf"):
#             images = pdf_to_images(file)
#         else:
#             images = [file]

#         all_text = []
#         for img in images:
#             all_text.extend(extract_text(img))

#         invoice = parse_invoice(all_text)
#         save_json(invoice)
#         results.append(invoice)

#     return {
#         "total_attachments": len(files),
#         "processed_invoices": results
#     }


# import os
# from fastapi import FastAPI
# from app.email.email_reader import EmailReader
# from app.ocr.pdf_to_image import pdf_to_images
# from app.ocr.ocr_engine import extract_text
# from app.parser.invoice_parser import parse_invoice
# from app.storage.json_writer import save_json

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"status": "Invoice Reader API Running"}


# @app.get("/run")
# def run():
#     client = EmailReader()
#     files = client.fetch_latest_invoice_attachments(max_messages=10)
#     # files = client.fetch_latest_invoice_attachments(max_messages=2)
#     print("Files found:", files)

#     results = []

#     for file in files:
#         images = []

#         if file.endswith(".pdf"):
#             images = pdf_to_images(file)
#         else:
#             images = [file]

#         all_text = []
#         for img in images:
#             all_text.extend(extract_text(img))

#         invoice = parse_invoice(all_text)
#         save_json(invoice)
#         results.append(invoice)

#     return {
#         "total_attachments": len(files),
#         "processed_invoices": results
#     }
