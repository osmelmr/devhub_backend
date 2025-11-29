from django.urls import path
from .views import auth, profile, admin

urlpatterns = [
    path('', admin.list_users, name='list_users'),
    path('<uuid:pk>/', admin.retrieve_user, name='retrieve_user'),
    path('create/', admin.create_user, name='create_user'),
    path('update/<uuid:pk>/', admin.update_user, name='update_user'),
    path('delete/<uuid:pk>/', admin.delete_user, name='delete_user'),
    path('delete/', admin.delete_users, name='delete_users'),

    path("auth/me/", auth.me, name="me"),
    path("auth/register/", auth.register_user, name="register-user"),
    path("auth/social-login/", auth.social_login, name="social-login"),

    path("profile/me/", profile.me, name="profile-me"),
    path("profile/update/<int:pk>/", profile.update_user, name="profile-update"),
    path("profile/delete-avatar/", profile.delete_avatar, name="profile-delete-avatar"),
    path("profile/delete-account/", profile.delete_my_account, name="profile-delete-account"),

]
