from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer

from .models import Order
from .models import ProductOrder
from .services.services_location import get_or_create_location


class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = ProductOrderSerializer(many=True, allow_empty=False, write_only=True)
    phonenumber = PhoneNumberField(region="RU")

    class Meta:
        model = Order
        fields = ["firstname", "lastname", "phonenumber", "address", "products"]

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data.get("firstname"),
            lastname=validated_data.get("lastname"),
            phonenumber=validated_data.get("phonenumber"),
            address=validated_data.get("address"),
        )

        get_or_create_location(order.address)

        for product in validated_data.get("products"):
            quantity = product.get("quantity")
            product_price = product.get("product").price

            ordered_product = ProductOrder.objects.create(
                order=order, **product, order_price=quantity * product_price
            )

            ordered_product.save()

        return order
