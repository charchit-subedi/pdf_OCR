import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os

def extract_text_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path).replace('.pdf', '')

    output_text = ""  # To store extracted text

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)

        # Extract selectable text if available
        text = page.get_text()
        if text.strip():
            output_text += text + "\n"
        else:
            # Perform OCR on image-based PDFs
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(image, lang='jpn')
            output_text += ocr_text + "\n"

    # Save text to a separate file
    output_file = os.path.join(output_folder, f"{pdf_name}_text.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"Processed '{pdf_path}'. Output saved to '{output_file}'.")

def process_single_pdf(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_text_from_pdf(pdf_path, output_folder)

if __name__ == "__main__":
    # Ask user for the PDF file name and output folder path
    pdf_file_name = input("Enter the PDF file name (with extension, e.g., 'example.pdf'): ")
    input_folder = "./"  # Assuming the script runs in the current directory
    output_folder = "./output_texts"  # Replace with your desired output folder path

    pdf_path = os.path.join(input_folder, pdf_file_name)

    # Check if the provided PDF file exists
    if os.path.exists(pdf_path) and pdf_file_name.lower().endswith('.pdf'):
        process_single_pdf(pdf_path, output_folder)
    else:
        print(f"Error: '{pdf_file_name}' does not exist or is not a valid PDF.")
