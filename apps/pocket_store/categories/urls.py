from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_categories),
    path("create/", views.create_category),
    path("<uuid:pk>/", views.retrieve_category),
    path("<uuid:pk>/update/", views.update_category),
    path("<uuid:pk>/delete/", views.delete_category),
    path("delete/bulk/", views.delete_categories),
]
