from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from books.views import book_list

def health_check(request):
    return HttpResponse('OK')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_list, name='book_list'),
    path('health/', health_check, name='health_check'),
] 