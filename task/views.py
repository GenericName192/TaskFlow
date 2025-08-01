from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib import messages
from authuser.models import User
from .models import Task
from utility import utils
from django.core.exceptions import PermissionDenied
from utility.constants import (
    LOGIN_URL_NAME, PROFILE_URL_NAME, TASK_LIST_URL_NAME,
    BULK_TASK_CREATION_URL_NAME, TASK_LIST_TEMPLATE,
    BULK_TASK_TEMPLATE, TASK_DETAILS_TEMPLATE, TASK_UPDATE_TEMPLATE
)


@login_required(login_url=LOGIN_URL_NAME)
def task_list(request, user_id: int):
    """Render the task list page."""
    task_owner = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.assigned_to = task_owner
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect(TASK_LIST_URL_NAME, user_id=task_owner.id)
        else:
            data = get_task_list_data(task_owner, request.user)
            data["form"] = form
            messages.error(request, "Error creating task. " +
                           "Please check for errors and try again.")
            return render(request, TASK_LIST_TEMPLATE, data)
    else:
        data = get_task_list_data(task_owner, request.user)
        data["form"] = TaskForm()
        return render(request, TASK_LIST_TEMPLATE, data)


def get_task_list_data(task_owner, user):
    data = {}
    data["ongoing_tasks"] = (task_owner.tasks
                             .filter(completed=False)
                             .select_related("created_by", "assigned_to"))
    data["completed_tasks"] = (task_owner.tasks
                               .filter(completed=True)
                               .select_related("created_by", "assigned_to"))
    data["can_assign"] = utils.Can_assign_task(task_owner, user)
    data["task_owner"] = task_owner
    return data


@login_required(login_url=LOGIN_URL_NAME)
def bulk_task_creation(request, scope="all"):
    """Handle creation of tasks for all subordinates"""
    if scope == "all":
        subordinates = request.user.get_all_subordinates()
    elif scope == "direct":
        subordinates = request.user.get_direct_subordinates()
    else:
        # Handle invalid scope values
        subordinates = request.user.get_all_subordinates()
        scope = "all"

    if request.method == "POST":
        form = TaskForm(request.POST)
        status, message = utils.mass_create_tasks(
            subordinates, form, request.user)
        if status:
            messages.success(request, f"Task made for: {message}")
            return redirect(PROFILE_URL_NAME, user_id=request.user.id)
        else:
            messages.error(request, f"Something went wrong: {message}")
            return redirect(BULK_TASK_CREATION_URL_NAME, scope=scope)
    else:
        form = TaskForm
        return render(request, BULK_TASK_TEMPLATE, {
            "subordinates": subordinates,
            "form": form,
            "task_type": scope
        })


@login_required(login_url=LOGIN_URL_NAME)
def toggle_complete(request, task_id: int):
    """Toggles the task to either true or false, allowing
    the user to mark a task as ongoing or completed."""
    task = get_object_or_404(Task.objects.select_related("assigned_to"),
                             id=task_id)
    if request.user.id == task.assigned_to.id:
        task.completed = not task.completed
        task.save()
        return redirect(TASK_LIST_URL_NAME, task.assigned_to.id)
    else:
        return redirect(TASK_LIST_URL_NAME, task.assigned_to.id)


@login_required(login_url=LOGIN_URL_NAME)
def task_details(request, task_id: int):
    """View all details on a task"""
    task = (get_object_or_404(Task, id=task_id)
            .select_related("assigned_to", "created_by"))
    return render(request, TASK_DETAILS_TEMPLATE, {
        "task": task
    })


@login_required(login_url=LOGIN_URL_NAME)
def update_task(request, task_id: int):
    """Renders a form that allows the user to update a task
    but only if they are either the creator or the task is assinged
    to them."""
    task = (get_object_or_404(Task, id=task_id)
            .select_related("assigned_to", "created_by"))
    if (request.user.id == task.created_by.id or
            request.user.id == task.assigned_to.id):
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            return redirect(TASK_LIST_URL_NAME, task.assigned_to.id)
        return render(request, TASK_UPDATE_TEMPLATE, {
            "form": form,
            "task": task,
        })
    else:
        raise PermissionDenied("You do not have permission to edit this task")


@login_required(login_url=LOGIN_URL_NAME)
def delete_task(request, task_id: int):
    """Deletes the task with the task_id passed to it, but only if
    the user is the user who created the task."""
    task = (get_object_or_404(Task, id=task_id)
            .select_related("assigned_to", "created_by"))
    if task.created_by == request.user:
        assigned_to_id = task.assigned_to.id
        task_title = task.title
        task.delete()
        messages.success(request,
                         f"Task '{task_title}' has been deleted successfully.")
        return redirect(TASK_LIST_URL_NAME, user_id=assigned_to_id)
    else:
        raise PermissionDenied("You do not have permission to " +
                               "delete this task")
