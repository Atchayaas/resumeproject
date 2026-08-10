import PyPDF2

def pdf_to_text(pdf_file_path, output_file_path):
    try:
        # Open the PDF file in binary mode
        with open(pdf_file_path, 'rb') as pdf_file:
            # Initialize a PDF reader
            reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from each page and write to the output file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for page in reader.pages:
                    text = page.extract_text()
                    print(text)
                    output_file.write(text + '\n')
        print(f"Text successfully extracted to: {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
pdf_file_path = "Jeevankumar O M – Latest Resume.pdf"  # Replace with your PDF file path
output_file_path = "output.txt"  # Replace with your desired output file path
pdf_to_text(pdf_file_path, output_file_path)
