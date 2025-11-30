from django.urls import path
from .views import (
    get_cart, add_to_cart,
    increase_quantity, decrease_quantity,
    remove_from_cart
)

urlpatterns = [
    path('cart/', get_cart),
    path('cart/add/', add_to_cart),
    path('cart/increase/', increase_quantity),
    path('cart/decrease/', decrease_quantity),
    path('cart/remove/', remove_from_cart),
]
