from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Min, Max
from rest_framework import status
from rest_framework.generics import get_object_or_404, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from garage_api.models import Manufacturer, Car, Part
from garage_api.serializers import CarSerializer, PartSerializer, ManufacturerNestedReadSerializer, \
    ManufacturerSerializer, CarNestedReadSerializer, PartWriteSerializer


# Create your views here.
#TODO:move to utils
class ReadWriteSerializerMixin:
    SAFE_METHODS = ['GET']

    read_serializer = None
    write_serializer = None

    def get_serializer_class(self):
        if self.request.method in self.SAFE_METHODS:
            return self.read_serializer
        return self.write_serializer


class ListCreateCarApiView(ReadWriteSerializerMixin, ListCreateAPIView):
    queryset = Car.objects.select_related('manufacturer').prefetch_related('parts').all()
    read_serializer = CarNestedReadSerializer
    write_serializer = CarSerializer
    filterset_fields = ['verified', 'year']
    ordering_fields = ['year']


class RetrieveUpdateDestroyCarApiView(ReadWriteSerializerMixin, RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.select_related('manufacturer').prefetch_related('parts').all()
    read_serializer = CarNestedReadSerializer
    write_serializer = CarSerializer


class ListCreateManufacturerApiView(ReadWriteSerializerMixin, ListCreateAPIView):
    queryset = Manufacturer.objects.prefetch_related('cars', 'parts').all()
    read_serializer = ManufacturerNestedReadSerializer
    write_serializer = ManufacturerSerializer


class PartModelViewSet(ReadWriteSerializerMixin, ModelViewSet):
    queryset = Part.objects.all()
    read_serializer = PartSerializer
    write_serializer = PartWriteSerializer


class CarStatsView(APIView):
    def get(self, request: Request) -> Response:
        stats = Car.objects.aggregate(
            total_cars=Count('id'),
            oldest_year=Min('year'),
            newest_year=Max('year'),
        )
        return Response(data=stats, status=status.HTTP_200_OK)


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        User = get_user_model()
        data = {
            'users_count': User.objects.count(),
            'manufacturers_count': Manufacturer.objects.count(),
            'cars_count': Car.objects.count(),
            'parts_count': Part.objects.count(),
            'requested_by': request.user.username
        }
        return Response(data=data, status=status.HTTP_200_OK)


# class ListManufacturerApiView(APIView):
#     def get(self, request: Request) -> Response:
#         manufacturers = Manufacturer.objects.all()
#         serializer = ManufacturerSerializer(manufacturers, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = ManufacturerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True) # If there is exception 400 Bad request will be returned
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class CarDetailApiView(APIView):
#     def get(self, request: Request, pk: int) -> Response:
#         car = get_object_or_404(Car, pk=pk)
#         serializer = CarSerializer(car)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request: Request, pk: int) -> Response:
#         car = get_object_or_404(Car, pk=pk)
#         serializer = CarSerializer(car, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def patch(self, request: Request, pk: int) -> Response:
#         car = get_object_or_404(Car, pk=pk)
#         serializer = CarSerializer(car, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request: Request, pk: int) -> Response:
#         car = get_object_or_404(Car, pk=pk)
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def head(self, request: Request, pk: int) -> Response:
#         try:
#             car = Car.objects.get(pk=pk)
#             return Response(status=status.HTTP_200_OK)
#         except Car.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#
# class CarListApiView(APIView):
#     QUERY_LOOKUP_FIELDS = {
#         'year': lambda x: Q(year=x),
#         'manufacturer_id': lambda x: Q(manufacturer_id=x),
#         'model_name': lambda x: Q(model=x),
#     }
#
#     QUERY_ORDER_BY_FIELDS = [
#         'year',
#         '-year',
#     ]
#
#     def get(self, request: Request) -> Response:
#         cars = Car.objects.all()
#
#         for param in request.query_params:
#             query_lookup = self.QUERY_LOOKUP_FIELDS.get(param)
#
#             if query_lookup:
#                 cars = cars.filter(query_lookup(request.query_params.get[param]))
#
#         ordering = request.query_params.get('order_by')
#         if ordering and ordering in self.QUERY_ORDER_BY_FIELDS:
#             cars = cars.order_by(ordering)
#
#         serializer = CarSerializer(cars, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = CarSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True) # If there is exception 400 Bad request will be returned
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)