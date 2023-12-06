import requests
from django.db.models import OuterRef, Subquery

from geocoder.models import Location
from star_burger.settings import YANDEX_APIKEY
from geopy import distance


def fetch_coordinates(address, apikey=YANDEX_APIKEY):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None, None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_or_create_location(address):
    longitude, latitude = fetch_coordinates(address)
    location, _ = Location.objects.get_or_create(
        address=address,
        defaults={
            'longitude': longitude,
            'latitude': latitude
        }

    )
    return location


def annotate_coordinates(Order, Restaurant):
    location = Location.objects.filter(address=OuterRef('address'))

    orders = Order.objects. \
        calculate_final_price(). \
        exclude(status='delivered'). \
        prefetch_related('restaurant'). \
        annotate(
            longitude=Subquery(location.values('longitude')),
            latitude=Subquery(location.values('latitude'))
        )

    restaurants = Restaurant.objects.annotate(
        longitude=Subquery(location.values('longitude')),
        latitude=Subquery(location.values('latitude'))
    )

    return orders, restaurants


def calculate_distance(order, restaurant):
    spacing = distance.distance(
        (order.latitude, order.longitude),
        (restaurant.latitude, restaurant.longitude)
    ).km if None not in (order.latitude, order.longitude) \
        else 'Ошибка определения координат'
    return spacing
