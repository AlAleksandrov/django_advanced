from django.urls import path
from books import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
