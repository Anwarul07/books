# from  django.core import serializers
from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    totalbook = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "birth_date",
            "nationality",
            "totalbook",
            "created_at",
            "updated_at",
        ]

    def get_totalbook(self, val):
        return val.books_author.count()


class CategorySerializer(serializers.ModelSerializer):
    total_book = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "total_book",
            "created_at",
        ]

    def get_total_book(self, value):
        return value.books_ctry.count()


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    category_name = (
        serializers.SerializerMethodField()
    )  # both method works and almost same

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "author_name",
            "category",
            "category_name",
            "isbn",
            "publication_date",
            "pages",
            "rating",
            "description",
            "availability",
            "created_at",
            "updated_at",
        ]

    def get_category_name(self, val):
        if val.category:
            return val.category.name
        return None

    def validate_isbn(self, value):
        """Custom validation for ISBN"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long.")
        return value


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Separate serializer for create/update operations"""

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "isbn",
            "publication_date",
            "pages",
            "rating",
            "description",
            "availability",
        ]

    def validate_rating(self, value):
        if value is not None and (value < 0 or value > 5):
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value
