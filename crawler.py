import os

class Crawler:

    def crawl_directory(self,directory):
        file_paths = []
        # Traverse the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Filter for specific file types (add more extensions as needed)
                if file.endswith(('.txt', '.docx', '.doc', '.pdf')):
                    file_paths.append(os.path.join(root, file))
        return file_paths


    def read_file(self,file_path):
        """Reads the content from a given file based on its extension."""
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            # Handle other file types here (e.g., .docx, .pdf)
            elif file_path.endswith('.docx'):
                import docx  # Ensure you have the python-docx library installed
                doc = docx.Document(file_path)
                return '\n'.join([para.text for para in doc.paragraphs])
            elif file_path.endswith('.doc'):
                import textract
                return textract.process(file_path).decode('utf-8')
            elif file_path.endswith('.pdf'):
                from PyPDF2 import PdfReader  # Ensure you have PyPDF2 installed
                pdf_reader = PdfReader(file_path)
                return '\n'.join([page.extract_text() for page in pdf_reader.pages])
            # You can add more file types as needed
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
