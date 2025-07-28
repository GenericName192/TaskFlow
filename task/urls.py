from django.urls import path
from .views import task_list

urlpatterns = [
    path('tasks/<int:user_id>/', task_list, name='task_list'),
]
