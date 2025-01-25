import requests # allows http request, get post
from bs4 import BeautifulSoup # scraps webpage's html 
import urllib.parse # components of url

def googleSearch(query, numResults=10):
    baseURL = "https://www.google.com/search"
    headers = { # dictionary
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    param = {
        "q": query,
        "num": numResults
    }
    response = requests.get(baseURL, headers=headers, params=param)

    if response.status_code != 200:
        print("Failed to retrieve results. HTTP status Code: {response.status_code}.")
        print("Check your internet connection")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select('.tF2Cxc'): # css class that typically wraps individual search result items on google (heading, description, url)
        title = result.select_one('h3')
        link = result.select_one('a')
        desc = result.select_one('.VwiC3b')

        if title and link and desc:
            results.append({
                "title":title.get_text(),
                "link":link['href'],
                "desc":desc.get_text()
            })
    
    if not results:
        print("No results found")

    return results


query=input("Enter Query: ")
results = googleSearch(query, numResults=10)

for index, result in enumerate(results, start=1):
    print(f"{index}. {result['title']}")
    print(f"    link: {result['link']}")
    print(f"    description: {result['desc']}\n")