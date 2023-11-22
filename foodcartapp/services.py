from .models import ProductOrder
from .models import Product
from .models import Order


def create_order_in_db(firstname, lastname, phonenumber, address):
    order = Order.objects.create(
        firstname=firstname,
        lastname=lastname,
        phonenumber=phonenumber,
        address=address,
    )

    return order


def add_product_to_order(order, **product):
    ProductOrder.objects.create(
        order=order,
        **product
    )
