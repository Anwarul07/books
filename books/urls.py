from django.urls import path
from . import views

urlpatterns = [
    # API Overview
    path('', views.api_overview, name='api_overview'),
    
    # Books
    path('books/', views.BookListCreateView.as_view(), name='book_list_create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    
    # Authors
    path('authors/', views.AuthorListCreateView.as_view(), name='author_list_create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Statistics
    path('stats/', views.library_stats, name='library_stats'),
]