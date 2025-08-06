from django.urls import path
from .views import chat_bot_view


urlpatterns = [
    path("", chat_bot_view, name="chat_bot_view"),
]
