from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
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
    serialize_order = request.data

    products = serialize_order.get('products')
    firstname = serialize_order.get('firstname')
    lastname = serialize_order.get('lastname')
    phonenumber = serialize_order.get('phonenumber')
    address = serialize_order.get('address')

    match products:
        case list() if products != []:
            order = create_order_in_db(
                firstname=firstname,
                lastname=lastname,
                phonenumber=phonenumber,
                address=address
            )

            for product in products:
                product_id = product.get('product')
                product_quantity = product.get('quantity')

                add_product_to_order(
                    order=order,
                    product_id=product_id,
                    product_quantity=product_quantity
                )

            return Response(serialize_order)
        case None:
            content = {
                'error': 'products: Required field.'
            }
            return Response(content)
        case []:
            content = {
                'error': 'products: This list cannot be empty.'
            }
            return Response(content)
        case str():
            content = {
                'error': 'products: Expected list with values, but received "str".'
            }
            return Response(content)
