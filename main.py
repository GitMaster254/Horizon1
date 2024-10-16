from indexer import Indexer
from search import Searcher
from crawler import Crawler

def main():
    index_dir = "index"
    
    # Create the index
    indexer = indexer(index_dir)

    # Crawl the local directory for files to index
    directory = r"C:\Users\Hedmon\OneDrive\Documents\ReadMe"  # Specify your local directory
    file_paths = Crawler.crawl_directory(directory)

    # Index the files found
    for file_path in file_paths:
        text = Crawler.read_file(file_path)  # Read content from the file
        if text:  # Ensure the text is not None
            print(f"Indexing {file_path}...")
            indexer.add_document_to_index(file_path, text)

    query = input("Enter your search query: ")
    results = Searcher.search_index(query)
    
    if results:
        for url,excerpt in results:
            print(f"Found in: {url}")
            print(f"Excerpt: {excerpt}\n")  # Use highlights for better readability
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
