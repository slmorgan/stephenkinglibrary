from django.contrib import admin
from django.urls import path
from books.views import book_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_list, name='book_list'),
] 