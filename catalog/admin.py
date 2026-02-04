from django.contrib import admin

from promocode.models import Promocode, MainModel, TestModel
from .models import Author, Genre, Book, BookInstance

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
