from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

import phonenumbers

from .models import Product
from .services import add_product_to_order
from .services import checks_product_availability
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

    order_information = [products, firstname, lastname, phonenumber, address]

    match order_information:
        case [list(products), str(firstname), str(lastname), str(phonenumber),
              str(address)] if products != [] and '' not in order_information:

            phonenumber_valid = phonenumbers.is_valid_number(phonenumbers.parse(phonenumber, "RU"))

            if phonenumber_valid:
                order = create_order_in_db(
                    firstname=firstname,
                    lastname=lastname,
                    phonenumber=phonenumber,
                    address=address
                )
            else:
                content = {
                    'error': 'phonenumber: The entered telephone number is incorrect.'
                }
                return Response(content)

            for product in products:
                product_id = product.get('product')
                product_quantity = product.get('quantity')

                try:
                    checks_product_availability(product_id=product_id)
                except Product.DoesNotExist:
                    content = {
                        'error': 'products: Invalid primary key.'
                    }
                    return Response(content)
                add_product_to_order(
                    order=order,
                    product_id=product_id,
                    product_quantity=product_quantity
                )

            return Response(serialize_order)
        case [None as products, *_]:
            content = {
                'error': 'products: Required field.'
            }
            return Response(content)
        case [_, None as firstname, None as lastname, None as phonenumber, None as address]:
            content = {
                'error': 'firstname, lastname, phonenumber, address: Required field.'
            }
            return Response(content)
        case [[] as products, *_]:
            content = {
                'error': 'products: This list cannot be empty.'
            }
            return Response(content)
        case [str() as products, *_]:
            content = {
                'error': 'products: Expected list with values, but received "str".'
            }
            return Response(content)
        case [_, '' as firstname, *_]:
            content = {
                'error': 'firstname: This field cannot be empty.'
            }
            return Response(content)
        case [_, '' as firstname, "" as lastname, "" as phonenumber, "" as address]:
            content = {
                'error': 'firstname, lastname, phonenumber, address: This field cannot be empty.'
            }
            return Response(content)
        case [*_, '' as phonenumber, _]:
            content = {
                'error': 'phonenumber: This field cannot be empty.'
            }
            return Response(content)
        case [_, [] as firstname, *_]:
            content = {
                'error': 'firstname: Not a valid string.'
            }
            return Response(content)
