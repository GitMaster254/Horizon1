from indexer import Indexer
from search import Searcher
from crawler import Crawler
import os

def main():
    index_dir = "index"
    
    # Create the index
    indexer = Indexer(index_dir)

    # Crawl the local directory for files to index
    directory = r"C:\Users\Hedmon\OneDrive\Documents\ReadMe"
    crawler = Crawler()
    file_paths = crawler.crawl_directory(directory)

    # Index the files found
    for file_path in file_paths:
        text = Crawler.read_file(file_path)  # Read content from the file
        if text:  # Ensure the text is not None
            print(f"Indexing {file_path}...")
            document = {
                "title": os.path.basename(file_path),
                "content": text,
                "path": file_path,
                "author": "Author Name", 
            }
            indexer.add_document(file_path, text)

    searcher = Searcher(index_dir)

    query = input("Enter your search query: ")
    results = searcher.search_index(query)
    
    if results:
        for path,excerpt in results:
            print(f"Found in: {path}")
            print(f"Excerpt: {highlight(excerpt)}\n")  # Use highlights for better readability
    else:
        print("No results found.")

def highlight(excerpt):
    # Highlight the query term in the text
    return excerpt.replace("<b>", "\033[1m").replace("</b>", "\033[0m")

if __name__ == "__main__":
    main()
