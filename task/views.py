from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib import messages
from authuser.models import User
from .models import Task


@login_required(login_url='login_view')
def task_list(request, user_id):
    """Render the task list page."""
    task_owner = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if task_creation(request, task_owner):
            messages.success(request, 'Task created successfully!')
            return redirect('task_list', user_id=task_owner.id)
    else:
        form = TaskForm()
        ongoing_tasks = task_owner.tasks.filter(completed=False)
        completed_tasks = task_owner.tasks.filter(completed=True)
        can_assign = Can_assign_task(user_id)
        return render(request, 'task/task_list.html',
                      {'task_owner': task_owner,
                       'ongoing_tasks': ongoing_tasks,
                       'completed_tasks': completed_tasks,
                       'form': form,
                       "can_assign": can_assign})


@login_required(login_url='login_view')
def task_creation(request, user):
    """Handle task creation."""
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.assigned_to = user
        task.save()
        return True
    else:
        messages.error(request, 'Error creating task. Please try again.')
        return False


@login_required(login_url='login_view')
def mass_task_creation(request, users):
    """Handle creation of multiple tasks."""
    errors = []
    successes = []
    for user in users:
        if task_creation(request, user):
            successes.append(user.first_name + ' ' + user.last_name)
        else:
            errors.append({user.first_name + ' ' + user.last_name})

    if successes:
        messages.success(request,
                         f"""Successfully created tasks for {len(successes)}\
                         users.""" + ' '.join(successes))
    if errors:
        messages.error(request,
                       f"""Failed to create tasks for {len(errors)} users.
                       """ + ' '.join(errors))


@login_required(login_url='login_view')
def toggle_complete(request, task_id):
    """Mark a task as completed."""
    task = get_object_or_404(Task, id=task_id)
    if task.completed is True:
        task.completed = False
    elif task.completed is False:
        task.completed = True
    task.save()
    return redirect("task_list", task.assigned_to.id)


@login_required(login_url="login_view")
def task_details(request, task_id):
    """View all details on a task"""
    task = get_object_or_404(Task, id=task_id)
    return render(request, "task/task_details.html", {
        "task": task
    })


@login_required(login_url="login_view")
def update_task(request, task_id):
    """Updates the task"""
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect("task_list", task.assigned_to.id)
    return render(request, "task/task_update.html", {
        "form": form,
        "task": task,
    })


def Can_assign_task(user_id):
    """Returns a list of everyone who can assign the user a task"""
    user = get_object_or_404(User, id=user_id)
    bosses = [user.id]
    boss = user.boss
    # creates loops that collects the boss until the value is null
    while boss:
        # if the user is already in bosses then its stuck in a loop
        if boss in bosses:
            break
        else:
            bosses.append(boss.id)
            boss = boss.boss
    return bosses
