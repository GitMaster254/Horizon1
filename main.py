from indexer import Indexer
from search import Searcher
from crawler import Crawler
import sys,re

def highlight(result,query):
    plain_text=re.sub(r'<.*?>', '', result)
    highlighted_text=re.sub(query, f'**{query}**', plain_text, flags=re.IGNORECASE)
    return highlighted_text

def get_title(content):
    lines = content.splitlines()
    return lines[0] if lines else "Untitled"

def main():
    index_dir = "index"
    
    # Create the index
    indexer = Indexer(index_dir)

    # Crawl the local directory for files to index
    
    crawler = Crawler()
    file_paths = crawler.crawl_directory(directory)

    # Index the files found
    for file_path in file_paths:
        content = crawler.read_file(file_path)  # Read content from the file
        if content:  # Ensure the text is not None
            print(f"Indexing {file_path}...")
            title= get_title(content)
            document = {
                "title": title,
                "content": content,
                "path": file_path,
                "author": "Unknown Author"
            }
            indexer.add_document(document)

    searcher = Searcher(index_dir)

    query = input("Enter your search query: ")
    results = searcher.search_index(query)
    
    if results:
        for path,excerpt,author,title in results:
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"Found in: {path}")
            print(f"Excerpt: {highlight(excerpt,query)}\n")  # Use highlights for better readability
    else:
        print("No results found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = r"C:\Users\Hedmon\OneDrive\Documents\ReadMe"  # Default directory if not passed
    
    main(directory)
