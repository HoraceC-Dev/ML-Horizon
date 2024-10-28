import requests
from dotenv import load_dotenv
import os
import requests
import httpx
# Load environment variables from .env file

def brave_search(query, num_results=15, safesearch="moderate", freshness="2020-10-09to2024-10-09",summary=False):
    load_dotenv()

# Get the API key from environment variables
    API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
    endpoint = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "x-subscription-token": API_KEY,
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
        search_results = results.get('web', {}).get('results', []) 
        processed_result= []
        for index, result in enumerate(search_results):
            temp = {"Title": result['title'],
                    "URL": result['url'],
                    "Description": result['description']}
            processed_result.append(temp)
        return processed_result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
    

