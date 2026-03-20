import streamlit as st   # Import Streamlit library to create web UI
import requests          # Import requests library to call FastAPI backend

# Configure the Streamlit page
st.set_page_config(page_title="Invoice Extractor", layout="centered")

# Display page title
st.title("📄 Invoice Data Extractor")          

# Short description for the user
st.write("Upload your invoice PDF and extract details.")

# -------- File Upload Section --------

# File uploader to upload PDF invoices
uploaded_file = st.file_uploader("Upload Invoice PDF", type=["pdf"])

# Check if user uploaded a file
if uploaded_file is not None:

    # Show success message after upload
    st.success("PDF Uploaded Successfully")

    # Button to trigger data extraction
    if st.button("Extract Data"):

        # Prepare file to send to FastAPI backend
        # Format: {"file": (filename, fileobject, mimetype)}
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

        try:
            # Send POST request to FastAPI API endpoint
            response = requests.post(
                "https://invoice-extractor-5bnj.onrender.com/upload-invoice",
                files=files
            )

            # Check if API request was successful
            if response.status_code == 200:

                # Convert response JSON into Python dictionary
                data = response.json()

                # Display section header
                st.subheader("📊 Extracted Invoice Data")

                # Show extracted fields from API response
                st.write("**Invoice Number:**", data.get("invoice_number"))
                st.write("**Invoice Date:**", data.get("invoice_date"))
                st.write("**Customer Name:**", data.get("customer_name"))
                st.write("**Email:**", data.get("email"))
                st.write("**Phone Number:**", data.get("phone_number"))
                st.write("**Total Amount:**", data.get("total_amount"))

            else:
                # Show error if API response failed
                st.error("API Error")

        except Exception as e:
            # Handle backend connection errors
            st.error(f"Error connecting to backend: {e}")
