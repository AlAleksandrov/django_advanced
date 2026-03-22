from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(
        max_length=20,
    )
    pages = models.IntegerField(
        default=0,
    )
    description = models.TextField(
        max_length=100,
        default="",
    )
    authors = models.ManyToManyField(
        'Author',
        related_name='books',
    )

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(
        max_length=100,
    )


    def __str__(self) -> str:
        return self.name


class Publisher(models.Model):
    name = models.CharField(
        max_length=100,
    )
    established_year = models.PositiveIntegerField()
    location = models.CharField(
        max_length=100,
    )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    description = models.TextField(
        max_length=200,
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"Review for {self.book.title} by {self.book.author}"