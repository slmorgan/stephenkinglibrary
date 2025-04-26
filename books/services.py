import requests
import xml.etree.ElementTree as ET
from books.settings import SAS_API_KEY, SAS_API_URL

def get_author_books():
    headers = {
        'Accept': 'application/xml'
    }
    
    try:
        print(f"Making request to: {SAS_API_URL}")
        response = requests.get(SAS_API_URL, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content[:500]}")  # Print first 500 chars of response
        
        # Parse XML response
        root = ET.fromstring(response.content)
        books = []
        
        # Extract book information from XML
        for work in root.findall('.//work'):
            # Get the thumbnail URL from the work element
            thumbnail = work.findtext('thumbnail', '')
            if not thumbnail:
                # If no thumbnail in work, try to get it from the book element
                book = work.find('.//book')
                if book is not None:
                    thumbnail = book.findtext('thumbnail', '')
            
            # Get format from work or book element
            format_text = work.findtext('item_format', '')
            if not format_text:
                book = work.find('.//book')
                if book is not None:
                    format_text = book.findtext('item_format', '')
            
            # Get price from work or book element
            price = work.findtext('price', '')
            if not price:
                book = work.find('.//book')
                if book is not None:
                    price = book.findtext('price', '')
            
            # Get product detail URL
            product_url = work.findtext('product_detail_url', '')
            if not product_url:
                book = work.find('.//book')
                if book is not None:
                    product_url = book.findtext('product_detail_url', '')
            
            # Get title and other fields
            title = work.findtext('title', 'Unknown Title')
            publication_date = work.findtext('publication_date', '')
            isbn = work.findtext('isbn', '')
            description = work.findtext('description', '')
            
            book_data = {
                'title': title,
                'publication_date': publication_date,
                'isbn': isbn,
                'description': description,
                'thumbnail': thumbnail,
                'format': format_text,
                'price': price,
                'product_url': product_url
            }
            
            # Only add books with titles
            if book_data['title'] != 'Unknown Title':
                books.append(book_data)
        
        # If no books found in works, try to find them in books
        if not books:
            for book in root.findall('.//book'):
                book_data = {
                    'title': book.findtext('title', 'Unknown Title'),
                    'publication_date': book.findtext('publication_date', ''),
                    'isbn': book.findtext('isbn', ''),
                    'description': book.findtext('description', ''),
                    'thumbnail': book.findtext('thumbnail', ''),
                    'format': book.findtext('item_format', ''),
                    'price': book.findtext('price', ''),
                    'product_url': book.findtext('product_detail_url', '')
                }
                # Only add books with titles
                if book_data['title'] != 'Unknown Title':
                    books.append(book_data)
        
        print(f"Found {len(books)} books")  # Debug print
        return books
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        return None 