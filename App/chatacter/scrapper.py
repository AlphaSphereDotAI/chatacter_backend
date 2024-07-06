from requests import get
from langchain_community.document_loaders import RecursiveUrlLoader
from vector_database import add_to_db
from search import get_search_results
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import replace_unicode_quotes
from unstructured.cleaners.core import bytes_string_to_string


def crawl(query: str):
    # get links from search results
    links_search_engine = get_search_results(query)
    links_crawler = []
    # load the documents
    for link in links_search_engine:
        try:
            html_loader = RecursiveUrlLoader(url=link, max_depth=1, timeout=5)
            docs = html_loader.load()
            links_crawler.extend([doc.metadata["source"] for doc in docs])
        except Exception as e:
            print(f"Error: {e}")
    return list(set(links_crawler + links_search_engine))


def scrap(query: str):
    # get links from search results
    links_search_engine = get_search_results(query)
    for link in links_search_engine:
        try:
            elements = partition_html(
                url=link,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
                },
                timeout=5,
                content_type="text/html",
            )
            for element in elements:
                element.apply(replace_unicode_quotes)
                element.apply(bytes_string_to_string)

            chunks = chunk_by_title(elements)
            add_to_db(chunks, [range(len(chunks))])
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print(scrap("What is the capital of France"))
