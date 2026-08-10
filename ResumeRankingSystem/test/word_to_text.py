from docx import Document

def word_to_text(word_file_path, output_file_path):
    try:
        # Load the Word document
        document = Document(word_file_path)

        # Extract text from each paragraph and write to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for paragraph in document.paragraphs:
                print(paragraph.text)
                output_file.write(paragraph.text + '\n')
        print(f"Text successfully extracted to: {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
word_file_path = "data science.docx"  # Replace with your Word file path
output_file_path = "output.txt"  # Replace with your desired output file path
word_to_text(word_file_path, output_file_path)
