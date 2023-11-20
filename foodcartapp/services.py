from .models import ProductOrder
from .models import Product
from .models import Order


def create_order_in_db(firstname, lastname, phonenumber, address):
    order, _ = Order.objects.get_or_create(
        firstname=firstname,
        lastname=lastname,
        phonenumber=phonenumber,
        address=address,
    )

    return order


def add_product_to_order(order, product_id, product_quantity):
    product = Product.objects.select_related('category').get(pk=product_id)
    order_product, _ = ProductOrder.objects.get_or_create(
        order=order,
        product=product,
        quantity=product_quantity
    )

    return order_product
