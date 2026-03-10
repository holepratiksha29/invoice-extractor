import re   # Import regex library for pattern matching

# Function to parse invoice information from OCR extracted text lines
def parse_invoice(text_lines):

    # Join all lines into a single string for easier regex searching
    text = " ".join(text_lines)

    # -------- Invoice Number --------
   
    # Initialize invoice_number as None
    invoice_number = None

    # 1️⃣ Strong regex patterns to detect invoice number in different formats
    patterns = [
        r'Invoice\s*no\.?\s*[:\-]?\s*(\d+)',      # Matches: Invoice No: 12345
        r'Invoice\s*number\s*[:\-]?\s*(\d+)',     # Matches: Invoice Number: 12345
        r'Bill\s*No\s*[:\-]?\s*(\d+)'             # Matches: Bill No: 12345
    ]

    # Loop through all patterns to find a match
    for pattern in patterns:

        # Search the pattern in the text (case insensitive)
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            # Extract the captured invoice number
            invoice_number = match.group(1)

            # Stop checking once a match is found
            break


    # 2️⃣ Fallback logic if invoice number was not found using regex
    if not invoice_number:

        # Loop through each line of the text
        for i, line in enumerate(text_lines):

            # Check if the current line contains "invoice no"
            if "invoice no" in line.lower():

                # Check the next few lines for a possible number
                for j in range(i+1, min(i+4, len(text_lines))):

                    # Remove extra spaces
                    possible = text_lines[j].strip()

                    # Search for any number with 4 or more digits
                    num_match = re.search(r'\d{4,}', possible)

                    if num_match:
                        # Assign the detected number as invoice number
                        invoice_number = num_match.group()

                        break

            # Stop outer loop if invoice number is found
            if invoice_number:
                break


    # -------- Invoice Date --------

    # Search for invoice date in formats like:
    # Invoice Date: 15.11.2025
    # Date: 3/4/2026
    invoice_date_match = re.search(

        r'(?:Invoice\s*Date|Date)[\s:\-]*([0-9]{1,2}[\/\.\-][0-9]{1,2}[\/\.\-][0-9]{2,4})',

        text,

        re.IGNORECASE
    )


    # -------- Customer Name --------

    # Initialize customer_name
    customer_name = None

    # Patterns to detect customer name in different invoice formats
    customer_patterns = [

        # Example: Customer Name: ABC Pvt Ltd
        r'Customer\s*Name\s*[:\-]?\s*([A-Za-z\s\.&]+?)(?=\sBill|\sInvoice|\sDate|$)',

        # Example: Bill To: ABC Pvt Ltd
        r'Bill\s*To\s*[:\-]?\s*([A-Za-z\s\.&]+)'
    ]

    # Debug message for customer name detection
    print("----- CUSTOMER NAME DEBUG -----")

    # Try each pattern
    for pattern in customer_patterns:

        print("Trying pattern:", pattern)

        # Search pattern in text
        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            # Extract possible customer name
            possible_name = match.group(1).strip()

            print("Matched value:", possible_name)

            # Reject if the extracted value contains unwanted keywords
            if not re.search(r'invoice|date|total|amount|number', possible_name.lower()):

                # Accept valid customer name
                customer_name = possible_name

                print("Accepted customer:", customer_name)

                break
            else:
                print("Rejected value:", possible_name)


    # -------- Fallback detection for customer name --------

    # If regex patterns failed, use line scanning
    if not customer_name:

        # Loop through text lines
        for i, line in enumerate(text_lines):

            # Look for "Bill To"
            if "bill to" in line.lower():

                # Check next few lines
                for j in range(i+1, min(i+5, len(text_lines))):

                    possible_name = text_lines[j].strip()

                    # Skip unwanted labels
                    if possible_name.lower() in ["bill to", "invoice number", "date"]:
                        continue

                    # Skip if the line contains long numbers
                    if re.search(r'\d{4,}', possible_name):
                        continue

                    # Skip if it contains invoice related words
                    if re.search(r'invoice|date|total|amount|number', possible_name.lower()):
                        continue

                    # Assign valid customer name
                    customer_name = possible_name

                    break

            # Stop loop if customer name found
            if customer_name:
                break


    # Debug final detected customer name
    print("FINAL CUSTOMER NAME:", customer_name)
    print("--------------------------------")


    # -------- Email Detection --------

    # Search for email pattern in the text
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )


    # -------- Phone Detection --------

    # Search for Indian phone number format (10 digits starting from 6–9)
    phone_match = re.search(
        r'\b[6-9]\d{9}\b',
        text
    )


    # -------- Total Amount Detection --------

    # Detect total amount from keywords like Total, Grand Total, Amount Due
    total_amount_match = re.search(

        r'(Total|Grand\s*Total|Amount\s*Due)\s*(Rs\.?|INR|\$)?\s*([\d,]+(\.\d{1,2})?)',

        text,

        re.IGNORECASE
    )


    # -------- Return Final Extracted Data --------

    return {

        # Extracted invoice number
        "invoice_number": invoice_number,

        # Extracted invoice date
        "invoice_date": invoice_date_match.group(1) if invoice_date_match else None,

        # Extracted customer name
        "customer_name": customer_name,

        # Extracted email
        "email": email_match.group(0) if email_match else None,

        # Extracted phone number
        "phone_number": phone_match.group(0) if phone_match else None,

        # Extracted total amount
        "total_amount": total_amount_match.group(3) if total_amount_match else None
    }