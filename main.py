import indexer
import search
import crawler

def main():
    index_dir = "index"
    
    # Create the index
    ix = indexer.create_index(index_dir)

    # Crawl the local directory for files to index
    directory = r"C:\Users\Hedmon\OneDrive\Documents\ReadMe"  # Specify your local directory
    file_paths = crawler.crawl_directory(directory)

    # Index the files found
    for file_path in file_paths:
        text = crawler.read_file(file_path)  # Read content from the file
        if text:  # Ensure the text is not None
            print(f"Indexing {file_path}...")
            indexer.add_document_to_index(ix, file_path, text)

    # Perform a search query 
    query = input("Enter your search query: ")
    results = search.search_index(index_dir, query)
    
    # Display search results
    if results:
        for url,excerpt in results:
            print(f"Found in: {url}")
            print(f"Excerpt: {excerpt}\n")  # Use highlights for better readability
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
