from django.contrib.auth import get_user_model
from rest_framework import serializers
from books.models import Book, Publisher, Author, Review





class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer()

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        book = Book.objects.create(**book_data)

        review = Review.objects.create(book=book, **validated_data)
        return review

    def update(self, instance, validated_data):
        book_data = validated_data.pop('book', None)
        instance.description = validated_data.get('description', instance.description)

        if book_data:
            for attr, value in book_data.items():
                setattr(instance.book, attr, value)
            instance.book.save()

        instance.save()
        return instance









# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=20)
#     pages = serializers.IntegerField(default=0)
#     description = serializers.CharField(max_length=100, default="")
#     author = serializers.CharField(max_length=20)
#
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.pages = validated_data.get('pages', instance.pages)
#         instance.description = validated_data.get('description', instance.description)
#         instance.author = validated_data.get('author', instance.author)
#         instance.save()
#         return instance