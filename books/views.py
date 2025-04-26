from django.shortcuts import render
from books.services import get_author_books

# Create your views here.

def book_list(request):
    books_data = get_author_books()
    print(f"Books data in view: {books_data}")  # Debug print
    
    # Handle different possible response structures
    if books_data:
        if isinstance(books_data, list):
            books = books_data
        elif isinstance(books_data, dict):
            books = books_data.get('books', []) or books_data.get('works', [])
        else:
            books = []
    else:
        books = []
    
    context = {
        'books': books
    }
    return render(request, 'books/book_list.html', context)
