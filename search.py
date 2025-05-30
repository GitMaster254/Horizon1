from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import json

class Searcher:
    def __init__(self, index_dir):
        self.index_dir = index_dir

    def search_index(self, query_str, limit=10):
        ix = open_dir(self.index_dir)
        with ix.searcher() as searcher:
            # Search across title, content, and author
            query_parser = MultifieldParser(["title", "content", "author"], ix.schema)
            query = query_parser.parse(query_str)

            results = searcher.search(query)

            return [
                {
                    "path": result["path"],
                    "title": result["title"],
                    "author": result["author"],
                    "snippet": result.highlights("content"),
                    "metadata": json.loads(result.get("metadata", "{}")),  # Optional metadata
                    "score": result.score
                }
                for result in results
            ]
