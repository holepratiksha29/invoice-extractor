# Invoice_PDF_Upload
# Invoice PDF Upload & Data Extraction

## 📌 Project Overview

This project extracts important information from **invoice PDFs ** using OCR and displays the results through a simple web interface.

The system allows users to upload invoice files and automatically extract details such as invoice number, date, vendor name, and amount.

## 🚀 Features

* Upload invoice **PDF or image**
* **OCR-based text extraction**
* Extract important invoice fields
* Backend API for processing
* Simple **Streamlit frontend UI**

## 🛠️ Technologies Used

* Python
* FastAPI
* Streamlit
* OCR (PaddleOCR / OpenCV)
* PDF Processing
* REST API


## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/holepratiksha29/invoice-extractor.git
```

Go to project folder:

```
cd invoice-extractor
```

Create virtual environment:

```
python -m venv venv
```

Activate environment:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## ▶️ Run the Backend

```
uvicorn main:app --reload
```

## ▶️ Run Streamlit UI

```
streamlit run frontend_streamlit.py
```

## 📷 Example Workflow

1. Upload invoice PDF
2. OCR extracts text
3. Important fields are detected
4. Results displayed on UI

## 🎯 Use Cases

* Invoice automation
* Accounting data entry
* Document digitization
* Finance workflow automation

## 👩‍💻 Author

Pratiksha Hole


