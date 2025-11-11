from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.list_todos, name='list_todos'),
    path('todos/search/', views.search_todos, name='search_todos'),
    path('todos/<int:pk>/', views.retrieve_todo, name='retrieve_todo'),
    path('todos/create/', views.create_todo, name='create_todo'),
    path('todos/<int:pk>/update/', views.update_todo, name='update_todo'),
    path('todos/<int:pk>/delete/', views.delete_todo, name='delete_todo'),
    path('todos/bulk-delete/', views.bulk_delete_todos, name='bulk_delete_todos'),
]
