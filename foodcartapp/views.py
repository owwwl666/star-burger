from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializer import OrderSerializer
from .services.services_order import add_product_to_order
from .services.services_order import create_order_in_db
from .services.services_location import get_or_create_location


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse(
        [
            {
                "title": "Burger",
                "src": static("burger.jpg"),
                "text": "Tasty Burger at your door step",
            },
            {
                "title": "Spices",
                "src": static("food.jpg"),
                "text": "All Cuisines",
            },
            {
                "title": "New York",
                "src": static("tasty.jpg"),
                "text": "Food is incomplete without a tasty dessert",
            },
        ],
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


def product_list_api(request):
    products = Product.objects.select_related("category").available()

    dumped_products = []
    for product in products:
        dumped_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "special_status": product.special_status,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
            }
            if product.category
            else None,
            "image": product.image.url,
            "restaurant": {
                "id": product.id,
                "name": product.name,
            },
        }
        dumped_products.append(dumped_product)
    return JsonResponse(
        dumped_products,
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


@api_view(["POST"])
def register_order(request):
    valid_order = OrderSerializer(data=request.data)
    valid_order.is_valid(raise_exception=True)

    products = valid_order.validated_data.get("products")
    firstname = valid_order.validated_data.get("firstname")
    lastname = valid_order.validated_data.get("lastname")
    phonenumber = valid_order.validated_data.get("phonenumber")
    address = valid_order.validated_data.get("address")
    with transaction.atomic():
        order = create_order_in_db(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            address=address,
        )

        get_or_create_location(order.address)

        serialize_order = OrderSerializer(order)

        for product in products:
            add_product_to_order(order=order, **product)

        return Response(serialize_order.data)
