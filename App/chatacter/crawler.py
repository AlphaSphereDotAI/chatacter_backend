from typing import Any, List
from langchain_core.documents.base import Document
from pydantic import StrictStr
from chatacter.search import get_search_results
from langchain_community.document_loaders import RecursiveUrlLoader


def crawl(query: str) -> List[StrictStr]:
    # get links from search results
    links_search_engine: List[StrictStr] = get_search_results(query=query)
    links_crawler: List[StrictStr] = []
    # load the documents
    for link in links_search_engine:
        try:
            html_loader = RecursiveUrlLoader(url=link, max_depth=1, timeout=5)
            docs: List[Document] = html_loader.load()
            links_crawler.extend([doc.metadata["source"] for doc in docs])
        except Exception as e:
            print(f"Error: {e}")
    return list(set(links_crawler + links_search_engine))


if __name__ == "__main__":
    print(crawl("What is the capital of France"))
