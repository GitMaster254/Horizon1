import tkinter as tk
from tkinter import scrolledtext, messagebox
import indexer
import search
import crawler

class SearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Search Application")

        self.label = tk.Label(master, text="Enter search term:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_text = scrolledtext.ScrolledText(master, width=80, height=20)
        self.results_text.pack()

    def perform_search(self):
        query = self.entry.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        index_dir = "index"  # Adjust as needed
        results = search.search_index(index_dir, query)

        self.results_text.delete(1.0, tk.END)  # Clear previous results
        if results:
            for url, excerpt in results:
                # Use the appropriate field for the URL or file path
                self.results_text.insert(tk.END, f"Found in: {url}\n")
                self.results_text.insert(tk.END, f"Excerpt: {excerpt}\n\n")
        else:
            self.results_text.insert(tk.END, "No results found.\n")

def main():
    # Create the index if it doesn't exist
    index_dir = "index"
    ix = indexer.create_index(index_dir)

    # Crawl the local directory for files to index
    directory = r"C:\Users\Hedmon\OneDrive\Documents\ReadMe"  # Adjust your local directory
    file_paths = crawler.crawl_directory(directory)

    # Index the files found
    for file_path in file_paths:
        text = crawler.read_file(file_path)  # Read content from the file
        if text:
            print(f"Indexing {file_path}...")
            indexer.add_document_to_index(ix, file_path, text)

    # Start the UI
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
