from rest_framework import serializers
from garage_api.models import Manufacturer, Car


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    # model = serializers.CharField(min_length=2)
    # year = serializers.IntegerField(min_value=1900)
    class Meta:
        model = Car
        fields = "__all__"

