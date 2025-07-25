from django.urls import path
from .views import index, profile, edit_profile, change_password, register
from .views import logout_view, login_view

urlpatterns = [
    path("", index, name="index"),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("profile/<int:user_id>/edit/", edit_profile, name="edit_profile"),
    path("profile/<int:user_id>/change_password/", change_password,
         name="change_password"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout_view"),
    path("login/", login_view, name="login_view"),
]
