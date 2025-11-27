from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_categories),
    path("create/", views.create_category),
    path("<int:pk>/", views.retrieve_category),
    path("<int:pk>/update/", views.update_category),
    path("<int:pk>/delete/", views.delete_category),
    path("delete/bulk/", views.delete_categories),
]
