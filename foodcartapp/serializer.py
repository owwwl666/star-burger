from rest_framework.serializers import ModelSerializer

from .models import Order
from .models import ProductOrder


class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = ProductOrderSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ["firstname", "lastname", "phonenumber", "address", "products"]
