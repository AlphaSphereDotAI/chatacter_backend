import os

from langchain_community.utilities import SearxSearchWrapper

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

search = SearxSearchWrapper(searx_host="http://localhost:8080")
search.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


def get_search_results(query: str, num_results: int = 10):
    results = search.results(query, num_results=num_results)
    links = []
    for result in results:
        if result["link"] is not None:
            print(result["link"])
            links.append(result["link"])
    return links


if __name__ == "__main__":
    print(get_search_results("What is the capital of France"))
