from langchain_community.document_loaders import UnstructuredFileLoader, UnstructuredURLLoader, AsyncHtmlLoader, RecursiveUrlLoader
from langchain_community.utilities import SearxSearchWrapper

search = SearxSearchWrapper(searx_host="https://localhost:8080")


def get_search_results(query: str, num_results: int = 10):
    return search.results(query, num_results=num_results)


if __name__ == "__main__":
    print(get_search_results("What is the capital of France"))
