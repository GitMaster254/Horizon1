# indexer.py
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir, exists_in
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser
import os
import json

class Indexer:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            path=ID(stored=True, unique=True),
            author=TEXT(stored=True),
            metadata=STORED,
        )
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
            create_in(self.index_dir, self.schema)
        if not exists_in(self.index_dir):
            create_in(self.index_dir, self.schema)

    def add_document(self, file_path, content,title, author="Unknown Author", metadata=None):

        index = open_dir(self.index_dir)
        writer = AsyncWriter(index)

        writer.add_document(
            title=title,
            content=content,
            path=file_path,
            author=author,
            metadata=json.dumps(metadata or {})
        )
        writer.commit()
    def remove_document(self, file_path):
        index = open_dir(self.index_dir)
        writer = AsyncWriter(index)

        writer.delete_by_term('path', file_path)
        writer.commit()