from whoosh.index import open_dir
from whoosh.qparser import QueryParser

class Searcher:
    def __init__(self, index_dir):
        self.index_dir = index_dir

    def search_index(self, query_str):
        ix = open_dir(self.index_dir)
        with ix.searcher() as searcher:
            query_parser = QueryParser("content", ix.schema)
            query = query_parser.parse(query_str)
            results = searcher.search(query)
            return [(result['path'], result.highlights("content"), result['title'], result['author']) for result in results]
