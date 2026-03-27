from django.urls import path, include
from rest_framework.routers import DefaultRouter

from garage_api import views

router = DefaultRouter()
router.register('parts', views.PartModelViewSet, basename='parts')

urlpatterns = [

    path('cars/', include([
        path('', views.ListCreateCarApiView.as_view(), name='car-list'),
        path('<int:pk>/', views.RetrieveUpdateDestroyCarApiView.as_view(), name='car-detail'),
        path('stats/', views.CarStatsView.as_view(), name='car-stats'),
        ])),
    path('manufacturers/', include([
        path('', views.ListCreateManufacturerApiView.as_view(), name='manufacturer-list'),
        ])),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard')
] + router.urls