from django.urls import path
from .views import task_list, toggle_complete, update_task, task_details
from .views import mass_task_creation, direct_task_creation

urlpatterns = [
    path('<int:user_id>/', task_list, name='task_list'),
    path("toggle_complete<int:task_id>/", toggle_complete,
         name="toggle_complete"),
    path("task_details<int:task_id>", task_details, name="task_details"),
    path("update_task<int:task_id>", update_task, name="update_task"),
    path("all_subordinates", mass_task_creation, name="mass_task_creation"),
    path("direct_task_creation", direct_task_creation,
         name="direct_task_creation")
]
