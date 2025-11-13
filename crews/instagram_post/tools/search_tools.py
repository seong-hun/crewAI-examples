import json
import os

import requests
from crewai.tools import tool


@tool("Search internet")
def search_internet(query: str) -> str:
    """Useful to search the internet about a given topic and return relevant
    results."""
    return search(query)


@tool("Search instagram")
def search_instagram(query: str) -> str:
    """Useful to search for instagram post about a given topic and return relevant
    results."""
    query = f"site:instagram.com {query}"
    return search(query)


def search(query: str, n_results: int = 5):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": os.environ["SERPER_API_KEY"],
        "content-type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()["organic"]
    stirng = []
    for result in results[:n_results]:
        try:
            stirng.append(
                "\n".join(
                    [
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-----------------",
                    ]
                )
            )
        except KeyError as e:
            raise e

    content = "\n".join(stirng)
    return f"\nSearch result: {content}\n"
