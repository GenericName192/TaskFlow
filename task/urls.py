from django.urls import path
from .views import task_list, toggle_complete

urlpatterns = [
    path('<int:user_id>/', task_list, name='task_list'),
    path("toggle_complete<int:task_id>/", toggle_complete,
         name="toggle_complete"),
]
