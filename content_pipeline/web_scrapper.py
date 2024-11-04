from dotenv import load_dotenv
import os
from scrapingbee import ScrapingBeeClient
import urllib.parse
from bs4 import BeautifulSoup
from io import StringIO

def web_scrapper(url):
    load_dotenv()
    API_KEY = os.getenv("SCRAPING_BEE_API_KEY")
    client = ScrapingBeeClient(api_key=API_KEY)
    
    
    encoded_url = urllib.parse.quote(url)

    response = client.get(url,
        params = { 
            'render_js': 'False',
        }
    )
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    header_tags = []
    content = []
    current_header = ''
    current_text = ''
    
    # Find all tags in the document
    all_tags = soup.find_all(True)
    
    # Identify header tags dynamically
    for tag in all_tags:
        # Detect standard header tags (e.g., h1, h2, ..., h6)
        if tag.name.startswith('h') and tag.name[1:].isdigit():
            if tag.name not in header_tags:
                header_tags.append(tag.name)
    
    # If no standard headers are found, you can add additional logic to detect headers
    # For example, tags with bold text could be considered headers
    if not header_tags:
        for tag in all_tags:
            if tag.name in ['strong', 'b']:
                if tag.name not in header_tags:
                    header_tags.append(tag.name)
    
    # Sort header tags to maintain hierarchy (optional)
    header_tags = sorted(header_tags, key=lambda x: (len(x), x))
    
    # StringIO object to build the output string
    output = StringIO()
    
    # Find all headers and paragraphs in order
    for elem in soup.find_all(header_tags + ['p']):
        if elem.name in header_tags:
            # If there's existing header and text, store them before moving to the next header
            if current_header or current_text:
                content.append((current_header, current_text.strip()))
                current_text = ''
            current_header = elem.get_text(strip=True)
        elif elem.name == 'p':
            current_text += elem.get_text(separator=' ', strip=True) + '\n'
    
    # Add the last header and text after the loop ends
    if current_header or current_text:
        content.append((current_header, current_text.strip()))
    
    # Count the number of headers
    num_headers = len(content)
    # Create a list of headers
    header_list = [header for header, _ in content]
    output.write("List of headers:\n")
    for header in header_list:
        output.write(f"{header}\n")
    
    # Output the headers and their corresponding text
    output.write("\nHeaders and their corresponding texts:\n")
    for header, text in content:
        output.write(f"Header: {header}\n")
        output.write(f"Text: {text}\n")
        output.write('-' * 80 + '\n')
    
    # Get the full output string
    result = output.getvalue()
    output.close()
    return result
