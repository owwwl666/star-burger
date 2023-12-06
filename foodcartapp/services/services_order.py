from foodcartapp.models import ProductOrder
from foodcartapp.models import Order


def create_order_in_db(firstname, lastname, phonenumber, address):
    order = Order.objects.create(
        firstname=firstname,
        lastname=lastname,
        phonenumber=phonenumber,
        address=address,
    )
    return order


def add_product_to_order(order, **product):
    ordered_product = ProductOrder.objects.create(
        order=order,
        **product
    )

    ordered_product.order_price = ordered_product.quantity * ordered_product.product.price
    ordered_product.save()
