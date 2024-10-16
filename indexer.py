#creating an index(db of keywords) and adding documents to it
from whoosh.index import create_in #library for indexing
from whoosh.fields import Schema, TEXT, ID 
import os

def create_index(index_dir):
    schema = Schema(
    title=TEXT(stored=True, optional=True),  # Store the title
    url=ID(stored=True),
    content=TEXT(stored=True), # Store the text content
    author=TEXT(stored=True, optional=True),  # Optional field
    )

    # Create the index directory if it doesn't exist
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    #create the index
    ix = create_in(index_dir, schema)
    return ix

def add_document_to_index(ix, title, url, content, author):
    writer = ix.writer()
    writer.add_document(
        title=title,
        url=url, 
        content=content,
        author=author
        )
    writer.commit()