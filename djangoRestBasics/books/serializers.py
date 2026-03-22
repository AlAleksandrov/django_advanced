from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    pages = serializers.IntegerField(default=0)
    description = serializers.CharField(max_length=100, default="")
    author = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.pages = validated_data.get('pages', instance.pages)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance