import requests
import xml.etree.ElementTree as ET
from django.conf import settings

def get_author_books():
    try:
        url = "https://www.simonandschuster.com/ws/authors/1666839"
        headers = {
            "Authorization": f"Bearer {settings.SIMON_SCHUSTER_API_KEY}"
        }
        
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                books = []
                
                for work in root.findall('.//work'):
                    book_data = {
                        'title': work.find('title').text if work.find('title') is not None else 'No title',
                        'publication_date': work.find('publication_date').text if work.find('publication_date') is not None else 'No date',
                        'description': work.find('description').text if work.find('description') is not None else 'No description',
                        'isbn': work.find('isbn').text if work.find('isbn') is not None else 'No ISBN',
                        'thumbnail': work.find('thumbnail').text if work.find('thumbnail') is not None else None
                    }
                    books.append(book_data)
                
                return books
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
                return None
        else:
            print(f"Error fetching data from API: {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None 