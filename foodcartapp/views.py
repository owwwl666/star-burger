from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

import phonenumbers

from .models import Product
from .models import ProductOrder
from .serializer import OrderSerializer
from .services import add_product_to_order
from .services import create_order_in_db


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    validate_order = OrderSerializer(data=request.data)
    validate_order.is_valid(raise_exception=True)

    products = validate_order.validated_data.get('products')
    firstname = validate_order.validated_data.get('firstname')
    lastname = validate_order.validated_data.get('lastname')
    phonenumber = validate_order.validated_data.get('phonenumber')
    address = validate_order.validated_data.get('address')

    print(validate_order.validated_data)

    order = create_order_in_db(
        firstname=firstname,
        lastname=lastname,
        phonenumber=phonenumber,
        address=address
    )

    for product in products:
        add_product_to_order(
            order=order,
            **product
        )

    return Response(request.data)
