import requests
from dotenv import load_dotenv
import os
import requests
# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

def brave_search(query, api_key, num_results=15, safesearch="moderate", freshness="2020-10-09to2024-10-09",summary=False):
    endpoint = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "x-subscription-token": api_key,
        "accept": "application/json",
        "Accept-Encoding": "gzip"
    }
    params = {
        "q": query,
        "count": num_results,
        "safesearch": safesearch,
        "freshness": freshness,
        "summary": summary,
    }
    
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()
        # print(results)
        return results.get('web', {}).get('results', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Example usage
if __name__ == "__main__":
    query = "What is the ranking of uoft in canada?"
    search_results = brave_search(query, API_KEY,num_results=3)


    for index, result in enumerate(search_results):
        # url = result['url']
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')

        # # Example to get all text from the page
        # all_text = soup.get_text()
        # print(all_text)
        print(f"{index + 1}. Title: {result['title']}")

        print(f"   URL: {result['url']}")
        print(f"   Description: {result['description']}\n")