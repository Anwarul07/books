from django.contrib import admin
from .models import Book, Author, Category

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'created_at']
    list_filter = ['nationality', 'created_at']
    search_fields = ['name', 'nationality']
    ordering = ['name']
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'availability', 'rating', 'created_at']
    list_filter = ['availability', 'category', 'author', 'created_at']
    search_fields = ['title', 'isbn', 'author__name']
    ordering = ['-created_at']
    list_editable = ['availability', 'rating']