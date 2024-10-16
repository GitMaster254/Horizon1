import os

# Function to crawl a local directory and collect file paths
def crawl_directory(directory):
    file_paths = []
    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Filter for specific file types (add more extensions as needed)
            if file.endswith(('.txt', '.docx', '.doc', 'pdf')):
                file_paths.append(os.path.join(root, file))
    return file_paths

# Function to read content from a file
def read_file(file_path):
    try:
     if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
     return None
