from rest_framework import generics, status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Book, Author, Category
from .serializers import (
    BookSerializer,
    BookCreateUpdateSerializer,
    AuthorSerializer,
    CategorySerializer,
)
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAdminUser


# Book Views
class BookListCreateView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookCreateUpdateSerializer
        return BookSerializer

    def get_queryset(self):
        queryset = Book.objects.select_related("author", "category").all()

        # Search functionality
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(author__name__icontains=search)
                | Q(isbn__icontains=search)
            )

        # Filter by category
        category = self.request.query_params.get("category", None)
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        # Filter by availability
        availability = self.request.query_params.get("availability", None)
        if availability:
            queryset = queryset.filter(availability=availability)

        # Filter by author
        author = self.request.query_params.get("author", None)
        if author:
            queryset = queryset.filter(author__name__icontains=author)

        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related("author", "category").all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BookCreateUpdateSerializer
        return BookSerializer


# Author Views
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Additional API endpoints
@api_view(["GET"])
def api_overview(request, format=None):
    """API overview with available endpoints"""
    api_urls = {
        "API Overview": "/api/",
        "Books": {
            "total_Books": Book.objects.count(),
            "books": reverse("book_list_create", request=request, format=format),
            "Book Detail": "api/books/id/",
            "Search Books": "/api/books/?search=<query>",
            "Filter by Category": "/api/books/?category=<category_name>",
            "Filter by Availability": "/api/books/?availability=<status>",
            "Filter by Author": "/api/books/?author=<author_name>",
        },
        "Authors": {
            "List/Create Authors": reverse(
                "author_list_create", request=request, format=format
            ),
            "Author Detail": "/api/authors/<int:id>/",
            "total_authors": Author.objects.count(),
        },
        "Categories": {
            "List/Create Categories": reverse(
                "category_list_create", request=request, format=format
            ),
            "Category Detail": "/api/categories/<int:id>/",
            "total_Catogry": Category.objects.count(),
        },
        "Statistics": reverse("library_stats", request=request, format=format),
    }
    return Response(api_urls)


@api_view(["GET"])
def library_stats(request):
    """Get library statistics"""
    stats = {
        "total_books": Book.objects.count(),
        "available_books": Book.objects.filter(availability="available").count(),
        "borrowed_books": Book.objects.filter(availability="borrowed").count(),
        "total_authors": Author.objects.count(),
        "total_categories": Category.objects.count(),
        "books_by_category": {},
        "books_by_availability": {},
    }

    # Books by category
    for category in Category.objects.all():
        stats["books_by_category"][category.name] = category.books_ctry.count()

    # Books by availability
    for choice in Book.AVAILABILITY_CHOICES:
        status_key = choice[0]
        status_label = choice[1]
        count = Book.objects.filter(availability=status_key).count()
        stats["books_by_availability"][status_label] = count

    return Response(stats)
