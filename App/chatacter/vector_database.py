import nltk
from qdrant_client import QdrantClient
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import (
    clean_extra_whitespace,
    replace_unicode_quotes,
    bytes_string_to_string,
    clean_non_ascii_chars,
)
from unstructured.partition.auto import partition

from chatacter.settings import get_settings

settings = get_settings()

client = QdrantClient(host="localhost", port=6333)

downloader = nltk.downloader.Downloader()
downloader._update_index()
downloader.download("popular")
downloader.download("punkt")
downloader.download("averaged_perceptron_tagger")


def get_chunks(url):
    elements = partition(url=url)
    for i in range(len(elements)):
        elements[i].text = clean_non_ascii_chars(elements[i].text)
        elements[i].text = replace_unicode_quotes(elements[i].text)
        elements[i].text = clean_extra_whitespace(elements[i].text)
        elements[i].text = bytes_string_to_string(elements[i].text)
    return chunk_by_title(elements)


def add_data(chunks):
    docs = [chunks[i].text for i in range(len(chunks))]
    metadata = [chunks[i].metadata.to_dict() for i in range(len(chunks))]
    ids = [ID for ID in range(1, len(chunks) + 1)]
    client.add(
        collection_name=settings.vector_database_name,
        documents=docs,
        metadata=metadata,
        ids=ids
    )


def query_db(query):
    return client.query(collection_name=settings.vector_database_name, query_text=query, )


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Napoleon"
    chunks = get_chunks(url)
    add_data(chunks)
    r = query_db("Napoleon Bonaparte")
    print(len(r))
    print(r)
