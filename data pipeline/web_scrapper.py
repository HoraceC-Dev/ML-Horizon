from apify_client import ApifyClient
import requests
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    # Initialize the ApifyClient with your API token
    API_KEY = os.getenv("AMIFY_API_TOKEN_KEY")

    client = ApifyClient(API_KEY)

    # Prepare the Actor input
    run_input = {
    "aggressivePrune": False,
    "clickElementsCssSelector": "[aria-expanded=\"false\"]",
    "clientSideMinChangePercentage": 15,
    "crawlerType": "playwright:adaptive",
    "debugLog": False,
    "debugMode": False,
    "expandIframes": True,
    "ignoreCanonicalUrl": False,
    "keepUrlFragments": False,
    "proxyConfiguration": {
        "useApifyProxy": True
    },
    "readableTextCharThreshold": 100,
    "removeCookieWarnings": True,
    "removeElementsCssSelector": "nav, footer, script, style, noscript, svg, [role=\"alert\"], [role=\"banner\"], [role=\"dialog\"], [role=\"alertdialog\"], [role=\"region\"][aria-label*=\"skip\" i], [aria-modal=\"true\"]",
    "renderingTypeDetectionPercentage": 10,
    "saveFiles": False,
    "saveHtml": False,
    "saveHtmlAsFile": False,
    "saveMarkdown": True,
    "saveScreenshots": False,
    "startUrls": [
        {
        "url": "https://www.engineering.utoronto.ca/"
        }
    ],
    "useSitemaps": False,
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "maxCrawlDepth": 1,
    "maxCrawlPages": 1,
    "initialConcurrency": 1,
    "maxConcurrency": 10,
    "initialCookies": [],
    "maxSessionRotations": 10,
    "maxRequestRetries": 2,
    "requestTimeoutSecs": 30,
    "minFileDownloadSpeedKBps": 128,
    "dynamicContentWaitSecs": 10,
    "waitForSelector": "",
    "maxScrollHeightPixels": 5000,
    "htmlTransformer": "readableText",
    "maxResults": 9999999
    }

    # Run the Actor and wait for it to finish
    run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)


    item = client.dataset(run["defaultDatasetId"]).iterate_items()
    title = item.get('metadata', {}).get('title')
    description = item.get('metadata', {}).get('description')
    author = item.get('metadata', {}).get('author')
    keywords = item.get('metadata', {}).get('keywords')
    url = item.get('url')
    
    return {"title": title,
            "description": description,
            "author": author,
            "keywords": keywords,
            "url": url}

if __name__ == "__main__":
    main()

