from indexer import Indexer
from search import Searcher
from crawler import Crawler
import sys
import re
import os
import json

def highlight(result, query):
    plain_text = re.sub(r'<.*?>', '', result)
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted_text = pattern.sub(lambda m: f'**{m.group(0)}**', plain_text)
    return highlighted_text

def get_title(content):
    lines = content.strip().splitlines()
    return lines[0] if lines else "Untitled"

def main(directory):
    if not os.path.exists(directory):
        print(f"[Error] Directory '{directory}' does not exist.")
        return

    index_dir = "index"
    indexer = Indexer(index_dir)
    crawler = Crawler()
    
    print(f"[Info] Crawling and indexing files in '{directory}'...\n")
    file_paths = crawler.crawl_directory(directory)
    
    if not file_paths:
        print("[Info] No files found to index.")
        return

    indexed_count = 0
    for file_path in file_paths:
        content = crawler.read_file(file_path)
        if content:
            title = get_title(content)
            indexer.add_document(
                file_path=file_path,
                content=content,   
                title=title, 
                author="Unknown Author",
                metadata={}
            )

        print(f"[Indexed] {file_path}")
        indexed_count += 1

    print(f"\n[Success] Indexed {indexed_count} file(s). You can now search!\n")

    searcher = Searcher(index_dir)
    while True:
        query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break
        if not query:
            print("[Warning] Please enter a valid query.\n")
            continue

        results = searcher.search_index(query,limit=10)
        if results:
            print(f"\n[Results for '{query}']\n")
            for result in results:
                path = result["path"]
                title = result["title"]
                author = result["author"]
                excerpt = result["snippet"]
                metadata = result["metadata"]
                score = result["score"]

                print(f"Title: {title}")
                print(f"Path: {path}")
                print(f"Author: {author}")
                print(f"Score: {score:.2f}")
                print(f"Excerpt: {highlight(excerpt, query)}")
                
                if metadata:
                    print(f"Metadata: {json.dumps(metadata, indent=2)}")

        else:
            print(f"[No results found for '{query}']\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = r"C:\Users\okoth\Desktop\Horizon\read"  # Set your preferred default
    main(directory)
