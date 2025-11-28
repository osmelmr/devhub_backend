from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list_users'),
    path('<uuid:pk>/', views.retrieve_user, name='retrieve_user'),
    path('create/', views.create_user, name='create_user'),
    path('update/<uuid:pk>/', views.update_user, name='update_user'),
    path('delete/<uuid:pk>/', views.delete_user, name='delete_user'),
    path('delete/', views.delete_users, name='delete_users'),
    path('me/', views.me, name="me"),
    path('register/', views.register_user, name='create_user'),
    path('delete/avatar/', views.delete_avatar, name='delete_avatar'),
]
