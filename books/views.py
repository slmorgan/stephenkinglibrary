from django.shortcuts import render
from .services import get_author_books

# Create your views here.

def book_list(request):
    books = get_author_books()
    print(f"Books data in view: {books}")
    return render(request, 'books/book_list.html', {'books': books})
