from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from books.models import Book, Review
from books.permissions import IsOwner
from books.serializers import BookSerializer, ReviewSerializer
from djangoRestBasics.exceptions import ServiceUnavailable


# Create your views here.
class HomeView(APIView):
    def get(self, request):
        return Response({"text": "Hello, World!"}, status=status.HTTP_200_OK)


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.select_related('book').all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.select_related('book').all()
    serializer_class = ReviewSerializer


class BookListCreateView(APIView):
    def get(self, request: Request) -> Response:
        # raise ServiceUnavailable()
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Book.objects.all()
    serializer_class = BookSerializer




# class BookDetailView(APIView):
#     def get_object(self, pk: int) -> Book:
#         return get_object_or_404(Book, pk=pk)
#
#     def get(self, request: Request, pk: int) -> Response:
#         book = self.get_object(pk=pk)
#         serializer = BookSerializer(book)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request: Request, pk: int) -> Response:
#         book = self.get_object(pk=pk)
#         serializer = BookSerializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#     def patch(self, request: Request, pk: int) -> Response:
#         book = self.get_object(pk=pk)
#         serializer = BookSerializer(book, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request: Request, pk: int) -> Response:
#         book = self.get_object(pk=pk)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)