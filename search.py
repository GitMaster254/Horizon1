from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_index(index_dir, query_str):
    """Search the Whoosh index for a given query string."""
    # Open the existing index
    ix = open_dir(index_dir)

    # Use the searcher to search the index
    with ix.searcher() as searcher:
        # Define a query parser for the 'content' field
        query_parser = QueryParser("content", ix.schema)

        # Parse the query string
        query = query_parser.parse(query_str)

        # Perform the search
        results = searcher.search(query)

        # Collect and return the results
        return [
            (
                result['url'],  # Assuming 'path' is the field that holds the URL or file path
                result.highlights("content")  # Highlights the matching terms in the content
            )
            for result in results
        ]
