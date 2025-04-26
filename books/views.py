from django.shortcuts import render
from books.services import get_author_books

# Create your views here.

def book_list(request):
    data = get_author_books()
    print(f"Books data in view: {data}")
    
    context = {
        'author': None,
        'books': []
    }
    
    if data and isinstance(data, dict):
        context['author'] = data.get('author')
        books = data.get('books', [])
        print(f"Number of books found: {len(books)}")
        for book in books:
            print(f"Book title: {book.get('title')}")
            print(f"Book thumbnail: {book.get('thumbnail')}")
        context['books'] = books
    
    return render(request, 'books/book_list.html', context)
