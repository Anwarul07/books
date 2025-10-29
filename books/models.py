from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Book(models.Model):
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("maintenance", "Under Maintenance"),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books_author"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="books_ctry"
    )
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    pages = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    availability = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ["-created_at"]
