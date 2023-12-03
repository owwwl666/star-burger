import requests
from django import forms
from django.shortcuts import redirect, render, HttpResponse

from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order
from star_burger.settings import YANDEX_APIKEY
from operator import itemgetter


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects. \
        calculate_final_price(). \
        exclude(status='delivered')

    restaurants = Restaurant.objects.all()

    products_in_restaurant = {restaurant: set(restaurant.menu_items.values_list('product', flat=True)) for
                              restaurant in
                              restaurants}

    order_details = []

    for order in orders:
        perfomers = {}
        products_in_order = set(order.ordered_products.values_list('product', flat=True))

        for restaurant, products in products_in_restaurant.items():
            if products_in_order.issubset(products):
                try:
                    spacing = distance.distance(
                        fetch_coordinates(YANDEX_APIKEY, restaurant.address),
                        fetch_coordinates(YANDEX_APIKEY, order.address)
                    ).km
                except requests.exceptions.HTTPError:
                    perfomers[restaurant] = 'Ошибка определения координат'
                else:
                    perfomers[restaurant] = spacing

        order_details.append(
            {
                'pk': order.pk,
                'final_price': order.final_price,
                'firstname': order.firstname,
                'lastname': order.lastname,
                'phonenumber': order.phonenumber,
                'address': order.address,
                'status': order.get_status_display(),
                'payment': order.get_payment_display(),
                'restaurants': sorted(perfomers.items(), key=itemgetter(1)),
                'restaurant': order.restaurant
            }

        )

    return render(
        request,
        template_name='order_items.html',
        context={
            'order_items': order_details,
            'url': request.path
        }
    )
