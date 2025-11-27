from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_products),
    path("create/", views.create_product),
    path("<uuid:pk>/", views.retrieve_productct),
    path("<uuid:pk>/update/", views.update_product),
    path("<uuid:pk>/delete/", views.delete_product),
    path("delete/bulk/", views.delete_products),
]
