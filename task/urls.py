from django.urls import path
from .views import task_list, toggle_complete, update_task, task_details
from .views import bulk_task_creation, delete_task

urlpatterns = [
    path('<int:user_id>/', task_list, name='task_list'),
    path("toggle_complete<int:task_id>/", toggle_complete,
         name="toggle_complete"),
    path("task_details<int:task_id>", task_details, name="task_details"),
    path("update_task<int:task_id>", update_task, name="update_task"),
    path("delete_task<int:task_id>/", delete_task, name="delete_task"),
    path("bulk_task_creation<str:scope>/", bulk_task_creation,
         name="bulk_task_creation"),
]
