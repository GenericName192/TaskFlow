from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib import messages
from authuser.models import User
from .models import Task
from utility import utils
from django.core.exceptions import PermissionDenied


@login_required(login_url='login_view')
def task_list(request, user_id: int):
    """Render the task list page."""
    task_owner = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if task_creation(request, task_owner):
            messages.success(request, "Task created successfully!")
            return redirect('task_list', user_id=task_owner.id)
    else:
        form = TaskForm()
        ongoing_tasks = task_owner.tasks.filter(completed=False)
        completed_tasks = task_owner.tasks.filter(completed=True)
        can_assign = utils.Can_assign_task(task_owner, request.user)
        return render(request, 'task/task_list.html',
                      {'task_owner': task_owner,
                       'ongoing_tasks': ongoing_tasks,
                       'completed_tasks': completed_tasks,
                       'form': form,
                       "can_assign": can_assign})


@login_required(login_url='login_view')
def task_creation(request, user: User):
    """Handle task creation."""
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.assigned_to = user
        task.save()
        return True
    else:
        messages.error(request, "Error creating task. " +
                       "Please check for errors and try again.")
        return False


@login_required(login_url='login_view')
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
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, f"Something went wrong: {message}")
            return redirect('bulk_task_creation', scope=scope)
    else:
        form = TaskForm
        return render(request, "task/bulk_task_creation.html", {
            "subordinates": subordinates,
            "form": form,
            "task_type": scope
        })


@login_required(login_url='login_view')
def toggle_complete(request, task_id: int):
    """Toggles the task to either true or false, allowing
    the user to mark a task as ongoing or completed."""
    task = get_object_or_404(Task, id=task_id)
    if request.user.id == task.assigned_to.id:
        task.completed = not task.completed
        task.save()
        return redirect("task_list", task.assigned_to.id)
    else:
        return redirect("task_list", task.assigned_to.id)


@login_required(login_url="login_view")
def task_details(request, task_id: int):
    """View all details on a task"""
    task = get_object_or_404(Task, id=task_id)
    return render(request, "task/task_details.html", {
        "task": task
    })


@login_required(login_url="login_view")
def update_task(request, task_id: int):
    """Renders a form that allows the user to update a task
    but only if they are either the creator or the task is assinged
    to them."""
    task = get_object_or_404(Task, id=task_id)
    if (request.user.id == task.created_by.id or
            request.user.id == task.assigned_to.id):
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list", task.assigned_to.id)
        return render(request, "task/task_update.html", {
            "form": form,
            "task": task,
        })
    else:
        raise PermissionDenied("You do not have permission to edit this task")


@login_required(login_url="login_view")
def delete_task(request, task_id: int):
    """Deletes the task with the task_id passed to it, but only if
    the user is the user who created the task."""
    task = get_object_or_404(Task, id=task_id)
    if task.created_by == request.user:
        assigned_to_id = task.assigned_to.id
        task_title = task.title
        task.delete()
        messages.success(request,
                         f'Task "{task_title}" has been deleted successfully.')
        return redirect("task_list", user_id=assigned_to_id)
    else:
        raise PermissionDenied("You do not have permission to " +
                               "delete this task")
