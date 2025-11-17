# backend/utils/pdf_reader.py

from PyPDF2 import PdfReader
from fastapi import HTTPException, UploadFile
from io import BytesIO

def extract_text_pypdf2(pdf_path):
    """Extract text from PDF using PyPDF2"""
    reader = PdfReader(pdf_path)
    text = ""
    
    # Extract text from each page
    for page in reader.pages:
        text += page.extract_text().strip() + "\n"
    
    return text

def extract_text_from_upload(file: UploadFile):
    """Extract text from uploaded PDF file"""
    try:
        # Read the uploaded file content
        pdf_content = file.file.read()
        
        # Create a BytesIO object from the content
        pdf_file = BytesIO(pdf_content)
        
        # Use PyPDF2 to read the PDF
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text, num_pages
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    
    finally:
        # Reset file pointer for potential reuse
        file.file.seek(0)

'''# Usage
if __name__ == "__main__":
    pdf_file = "IDS_COURSE_CONTENT.pdf"
    
    try:
        extracted_text = extract_text_pypdf2(pdf_file)
        print(extracted_text)
        
        # Optionally save to a text file
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
    except Exception as e:
        print(f"Error: {e}")'''
