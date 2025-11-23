from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_projects, name='list_projects'),
    path('<uuid:pk>/', views.retrieve_project, name='retrieve_project'),
    path('create/', views.create_project, name='create_project'),
    path('update/<uuid:pk>/', views.update_project, name='update_project'),
    path('delete/<uuid:pk>/', views.delete_project, name='delete_project'),
    path('delete/', views.delete_projects, name='delete_projects'),
]
