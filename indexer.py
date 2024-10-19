# indexer.py
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.writing import AsyncWriter
import os

class Indexer:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            path=ID(stored=True,unique=True),
            author=TEXT(stored=True),  # Optional field with default
        )
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
            create_in(self.index_dir, self.schema)

    def add_document(self, document):

        index = open_dir(self.index_dir)
        writer = AsyncWriter(index)

        # Handle missing fields gracefully
        writer.add_document(
            title=document.get("title", "Untitled"),
            content=document.get("content", ""),
            path=document.get("path", ""),
            author=document.get("author", "Unknown Author")  # Default value if missing
            )
        
        writer.commit()

    # Add other indexing methods as needed
