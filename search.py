#implements the search functionality
from whoosh.index import open_dir #library for searching
from whoosh.query import Term, And, Or
from whoosh.qparser import QueryParser  # Import for parsing queries


def search_index(index_dir, query_str):
    #open the existing index
    ix = open_dir(index_dir)

    #use the searcher to search the index
    with ix.searcher() as searcher:
        # Define a query parser for the 'content' field
        query_parser = QueryParser("content", ix.schema)
        
        # Parse the query string
        query = query_parser.parse(query_str)
        
        # Perform the search
        results = searcher.search(query)
        
        # Collect and return the results
        return [(
            result['url'], 
            result.highlights("content")
             )for result in results]