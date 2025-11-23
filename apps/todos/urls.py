from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_todos, name='list_todos'),
    path('search/', views.search_todos, name='search_todos'),
    path('<int:pk>/', views.retrieve_todo, name='retrieve_todo'),
    path('create/', views.create_todo, name='create_todo'),
    path('<int:pk>/update/', views.update_todo, name='update_todo'),
    path('<int:pk>/delete/', views.delete_todo, name='delete_todo'),
    path('delete/', views.delete_todos, name='delete_todos'),
]
