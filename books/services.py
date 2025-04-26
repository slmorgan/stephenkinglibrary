import requests
import xml.etree.ElementTree as ET
import html
from django.conf import settings

def get_author_books():
    try:
        url = "https://www.simonandschuster.com/ws/authors/1666839"
        headers = {
            'Accept': 'application/xml'
        }
        
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Parse XML response
                root = ET.fromstring(response.text)
                
                # Extract author information
                author_data = {
                    'first_name': root.find('first_name').text if root.find('first_name') is not None else '',
                    'last_name': root.find('last_name').text if root.find('last_name') is not None else '',
                    'image': root.find('image').text if root.find('image') is not None else '',
                    'thumbnail': root.find('thumbnail').text if root.find('thumbnail') is not None else '',
                    'bio': html.unescape(root.find('bio').text) if root.find('bio') is not None else '',
                }
                
                # Extract books information
                books = []
                works = root.findall('.//work')
                
                print(f"Found {len(works)} works")
                
                # Add debug print for XML structure
                print(f"XML Structure sample: {ET.tostring(root, encoding='unicode')[:500]}")
                
                for work in works:
                    # Print the entire work element for debugging
                    print(f"Processing work: {ET.tostring(work, encoding='unicode')[:500]}")
                    
                    # Try to get image from work element first
                    image = work.find('.//image')
                    if image is not None and image.text:
                        print(f"Found image in work: {image.text}")
                        image_url = image.text
                    else:
                        # If not found in work, try to get it from the book element
                        book = work.find('book')
                        if book is not None:
                            image = book.find('.//image')
                            if image is not None and image.text:
                                print(f"Found image in book: {image.text}")
                                image_url = image.text
                            else:
                                image_url = None
                        else:
                            image_url = None
                    
                    # Make sure the URL is complete
                    if image_url and not image_url.startswith('http'):
                        if image_url.startswith('/'):
                            image_url = f"https://www.simonandschuster.com{image_url}"
                        else:
                            image_url = f"https://www.simonandschuster.com/{image_url}"
                    
                    # Get the book element for additional details
                    book = work.find('book')
                    if book is not None:
                        # Print the book element for debugging
                        print(f"Book element: {ET.tostring(book, encoding='unicode')[:500]}")
                        
                        # Extract publication date with better error handling
                        pub_date = book.find('pub_date')
                        if pub_date is not None and pub_date.text:
                            publication_date = pub_date.text.strip()
                            print(f"Found publication date in book: {publication_date}")
                        else:
                            # Try to find publication date in other possible locations
                            pub_date = work.find('pub_date')
                            if pub_date is not None and pub_date.text:
                                publication_date = pub_date.text.strip()
                                print(f"Found publication date in work: {publication_date}")
                            else:
                                # Try to find publication date in other possible elements
                                pub_date = work.find('.//pub_date')
                                if pub_date is not None and pub_date.text:
                                    publication_date = pub_date.text.strip()
                                    print(f"Found publication date in nested element: {publication_date}")
                                else:
                                    # Try to find release date
                                    pub_date = work.find('release_date')
                                    if pub_date is not None and pub_date.text:
                                        publication_date = pub_date.text.strip()
                                        print(f"Found release date: {publication_date}")
                                    else:
                                        publication_date = 'No date'
                                        print("No publication date found in any location")
                        
                        # Extract format
                        format_elem = book.find('format')
                        if format_elem is not None:
                            format = format_elem.text
                            print(f"Found format: {format}")
                        else:
                            format = 'No format'
                        
                        # Extract ISBN-13
                        isbn13_elem = book.find('isbn13')
                        if isbn13_elem is not None:
                            isbn13 = isbn13_elem.text
                            print(f"Found ISBN-13: {isbn13}")
                        else:
                            isbn13 = 'No ISBN'
                    else:
                        publication_date = 'No date'
                        format = 'No format'
                        isbn13 = 'No ISBN'
                    
                    book_data = {
                        'title': work.find('title').text if work.find('title') is not None else 'No title',
                        'publication_date': publication_date,
                        'description': html.unescape(work.find('description').text) if work.find('description') is not None else 'No description',
                        'isbn': isbn13,
                        'isbn13': isbn13,
                        'format': format,
                        'thumbnail': image_url
                    }
                    books.append(book_data)
                
                return {
                    'author': author_data,
                    'books': books
                }
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
                print(f"Response content: {response.text[:500]}")  # Print first 500 chars for debugging
                return None
        else:
            print(f"Error fetching data from API: {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None 