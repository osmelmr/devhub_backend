from django.urls import path
from .views import (
    get_cart, add_to_cart,
    increase_quantity, decrease_quantity,
    remove_from_cart
)

urlpatterns = [
    path('', get_cart),
    path('add/', add_to_cart),
    path('increase/', increase_quantity),
    path('decrease/', decrease_quantity),
    path('remove/', remove_from_cart),
]
