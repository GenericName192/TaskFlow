from django.urls import path
from .views import index, profile

urlpatterns = [
    path("", index, name="index"),
    path("profile/<int:user_id>/", profile, name="profile"),
]
